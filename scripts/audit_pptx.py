#!/usr/bin/env python3
"""Read-only PPTX structural checks. This is not visual acceptance or a renderer.

Exit codes: 0 = supported checks clear, 1 = error, 2 = partial/unknown (or CLI misuse).
Font distributions count Unicode characters at declared run/default sizes in points.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import posixpath
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
EXEMPT = ('caption-', 'footer-', 'page-')
LIMITATIONS = [
    'Structural checks only; no visual acceptance, overlap, clipping, OCR or rendering checks.',
    'Only slide-local native text and pictures are inspected; master/layout artwork is not scanned.',
    'Font sizes come from native run or local default rPr; theme/layout/master inheritance and font availability are not resolved.',
    'Font distribution is declared size, weighted by Unicode characters including spaces, excluding paragraph breaks.',
    'Grouped, alternate-content, tiled, 3D and other complex image objects are unknown; no false distortion verdict is inferred.',
    'PNG/JPEG dimensions use stdlib header inspection, assuming square pixels; this does not validate full image decoding.',
    'Image aspect compares cropped source with fillRect in local coordinates; rotation/flips alone preserve aspect.',
]


def relationships(archive, part):
    path = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')
    if path not in archive.namelist():
        return {}
    return {node.get('Id'): node.attrib for node in ET.fromstring(archive.read(path))}


def target_part(part, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), target)) if not target.startswith('/') else target.lstrip('/')


def image_dimensions(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 33 and data[12:16] == b'IHDR':
        width, height = struct.unpack('>II', data[16:24])
        if width and height:
            return width, height
    if data.startswith(b'\xff\xd8'):
        offset, size = 2, None
        while offset < len(data):
            if data[offset] != 0xff:
                break
            while offset < len(data) and data[offset] == 0xff:
                offset += 1
            if offset >= len(data):
                break
            marker = data[offset]
            offset += 1
            if marker in (0xd9, 0xda):
                break
            if marker == 0x01 or 0xd0 <= marker <= 0xd8:
                continue
            if offset + 2 > len(data):
                break
            length = int.from_bytes(data[offset:offset + 2], 'big')
            if length < 2 or offset + length > len(data):
                break
            payload = data[offset + 2:offset + length]
            if marker == 0xe1 and payload.startswith(b'Exif\0\0'):
                raise ValueError('JPEG EXIF orientation is not resolved')
            if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf) and len(payload) >= 5:
                height, width = struct.unpack('>HH', payload[1:5])
                if width and height:
                    size = (width, height)
            offset += length
        if size:
            return size
    raise ValueError('Unsupported or unreadable image dimensions (PNG/JPEG headers only)')


def rectangle_scale(node):
    def value(edge):
        raw = node.get(edge, '0') if node is not None else '0'
        return float(raw[:-1]) / 100 if raw.endswith('%') else float(raw) / 100000
    width, height = 1 - value('l') - value('r'), 1 - value('t') - value('b')
    if not all(math.isfinite(v) and v > 0 for v in (width, height)):
        raise ValueError('Invalid source/fill rectangle')
    return width, height


def audit_picture(archive, part, rels, shape, grouped, name, threshold):
    result = {'shape': name, 'status': 'unknown', 'distortion': None}
    try:
        if grouped:
            raise ValueError('Group transforms are not supported')
        if shape.find('.//a:scene3d', NS) is not None or shape.find('.//a:sp3d', NS) is not None:
            raise ValueError('3D picture transforms are not supported')
        fill = shape.find('p:blipFill', NS)
        if fill is None or fill.find('a:stretch', NS) is None:
            raise ValueError('Only explicit picture stretch fills are supported')
        if fill.find('a:tile', NS) is not None:
            raise ValueError('Tiled images are not supported')
        blip = fill.find('a:blip', NS)
        rel = rels.get(blip.get('{' + NS['r'] + '}embed') if blip is not None else None)
        if not rel or rel.get('TargetMode') == 'External':
            raise ValueError('Missing or external image relationship')
        media = target_part(part, rel['Target'])
        width, height = image_dimensions(archive.read(media))
        result.update(source=media, source_pixels=[width, height])
        xfrm = shape.find('p:spPr/a:xfrm', NS)
        ext = xfrm.find('a:ext', NS) if xfrm is not None else None
        if ext is None:
            raise ValueError('Missing local picture extents')
        cx, cy = float(ext.get('cx')), float(ext.get('cy'))
        if not all(math.isfinite(v) and v > 0 for v in (cx, cy)):
            raise ValueError('Invalid picture extents')
        crop_x, crop_y = rectangle_scale(fill.find('a:srcRect', NS))
        fill_x, fill_y = rectangle_scale(fill.find('a:stretch/a:fillRect', NS))
        source_ratio = width * crop_x / (height * crop_y)
        display_ratio = cx * fill_x / (cy * fill_y)
        ratio = display_ratio / source_ratio
        distortion = max(ratio, 1 / ratio) - 1
        rotation = float(xfrm.get('rot', '0')) / 60000
        if not math.isfinite(rotation):
            raise ValueError('Invalid picture rotation')
        result.update(status='error' if distortion > threshold + 1e-9 else 'ok',
                      source_aspect_after_crop=source_ratio, display_aspect=display_ratio,
                      distortion=distortion, stretch_factor=max(ratio, 1 / ratio),
                      rotation_degrees=rotation)
    except (ValueError, TypeError, KeyError, struct.error) as exc:
        result.update(status='unknown', reason=str(exc))
    return result


def declared_size(run, paragraph, body):
    level = paragraph.find('a:pPr', NS)
    level_index = int(level.get('lvl', '0')) + 1 if level is not None else 1
    candidates = [run.find('a:rPr', NS), paragraph.find('a:pPr/a:defRPr', NS),
                  body.find(f'a:lstStyle/a:lvl{level_index}pPr/a:defRPr', NS),
                  body.find('a:lstStyle/a:defPPr/a:defRPr', NS)]
    for node in candidates:
        if node is not None and node.get('sz') is not None:
            size = float(node.get('sz')) / 100
            if not math.isfinite(size) or size <= 0:
                raise ValueError('Invalid font size')
            return size
    return None


def audit_pptx(path, min_font_pt=None, max_slide_chars=None, max_image_distortion=0.03):
    report = {'scope': 'PPTX structural checks; not visual acceptance', 'source': str(Path(path).resolve()),
              'thresholds': {'min_font_pt': min_font_pt, 'max_slide_chars': max_slide_chars,
                             'max_image_distortion': max_image_distortion},
              'status': 'ok', 'limitations': LIMITATIONS, 'slides': [], 'findings': []}

    def finding(slide, code, message, severity='unknown', **details):
        report['findings'].append(dict(slide=slide, code=code, severity=severity, message=message, **details))

    try:
        with zipfile.ZipFile(path) as archive:
            presentation = ET.fromstring(archive.read('ppt/presentation.xml'))
            rels = relationships(archive, 'ppt/presentation.xml')
            ids = presentation.findall('p:sldIdLst/p:sldId', NS)
            if not ids:
                raise ValueError('No slides found in the presentation slide list')
            for index, slide_id in enumerate(ids, 1):
                rel = rels[slide_id.get('{' + NS['r'] + '}id')]
                part = target_part('ppt/presentation.xml', rel['Target'])
                root = ET.fromstring(archive.read(part))
                slide_rels = relationships(archive, part)
                stats = {'slide': index, 'part': part, 'native_text_chars': 0, 'font_sizes_pt': {},
                         'unknown_font_chars': 0, 'exempt_text_chars': 0, 'images': []}
                font_sizes = Counter()
                report['slides'].append(stats)

                def inspect_shape(shape, grouped=False):
                    tag = shape.tag.rsplit('}', 1)[-1]
                    if tag == 'grpSp':
                        for child in shape:
                            inspect_shape(child, True)
                        return
                    if tag == 'AlternateContent':
                        finding(index, 'complex_object', 'Alternate-content branches are not resolved')
                        return
                    if tag not in ('sp', 'pic', 'graphicFrame', 'cxnSp', 'contentPart'):
                        return
                    nonvisual = shape.find('.//p:cNvPr', NS)
                    name = nonvisual.get('name', '') if nonvisual is not None else ''
                    name = name or '(unnamed)'
                    if tag == 'pic':
                        info = audit_picture(archive, part, slide_rels, shape, grouped, name, max_image_distortion)
                        stats['images'].append(info)
                        if info['status'] == 'unknown':
                            finding(index, 'image_unknown', info['reason'], shape=name)
                        elif info['status'] == 'error':
                            finding(index, 'image_distortion', 'Picture is stretched non-proportionally', 'error',
                                    shape=name, distortion=info['distortion'], stretch_factor=info['stretch_factor'])
                    elif shape.find('.//a:blipFill', NS) is not None:
                        finding(index, 'image_unknown', 'Image fills outside native pictures are not supported', shape=name)
                    if tag == 'contentPart' or (tag == 'graphicFrame' and shape.find('.//a:tbl', NS) is None):
                        finding(index, 'complex_object', 'Chart, diagram or embedded object is not inspected', shape=name)
                    for body in shape.iter():
                        if body.tag.rsplit('}', 1)[-1] != 'txBody':
                            continue
                        chars = sum(len(node.text or '') for node in body.findall('.//a:t', NS))
                        stats['native_text_chars'] += chars
                        exempt = name.startswith(EXEMPT)
                        if exempt:
                            stats['exempt_text_chars'] += chars
                        unknown, small, counted = 0, Counter(), 0
                        auto = body.find('a:bodyPr/a:normAutofit', NS)
                        for para in body.findall('a:p', NS):
                            for run in para:
                                text = run.find('a:t', NS)
                                if text is None or not text.text:
                                    continue
                                count = len(text.text)
                                counted += count
                                try:
                                    size = declared_size(run, para, body)
                                except (ValueError, TypeError):
                                    size = None
                                if size is None:
                                    unknown += count
                                    continue
                                font_sizes[f'{size:g}'] += count
                                if auto is not None:
                                    unknown += count
                                if min_font_pt is not None and size < min_font_pt and not exempt:
                                    small[size] += count
                        unknown += max(0, chars - counted)
                        stats['unknown_font_chars'] += unknown
                        if unknown:
                            finding(index, 'font_unknown', 'Font size inheritance, autofit or text properties are unresolved',
                                    shape=name, chars=unknown)
                        for size, count in sorted(small.items()):
                            finding(index, 'font_too_small', 'Declared native text size is below the configured font threshold', 'error',
                                    shape=name, font_pt=size, chars=count, min_font_pt=min_font_pt)

                tree = root.find('p:cSld/p:spTree', NS)
                if tree is None:
                    raise ValueError(f'Missing shape tree in slide {index}')
                for shape in tree:
                    inspect_shape(shape)
                if root.find('p:cSld/p:bg//a:blipFill', NS) is not None:
                    finding(index, 'image_unknown', 'Background image fills are not inspected')
                stats['font_sizes_pt'] = dict(sorted(font_sizes.items(), key=lambda item: float(item[0])))
                if max_slide_chars is not None and stats['native_text_chars'] > max_slide_chars:
                    finding(index, 'slide_text_limit', 'Native text exceeds the configured character limit', 'error',
                            chars=stats['native_text_chars'], max_slide_chars=max_slide_chars)
    except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError, ValueError) as exc:
        finding(None, 'package_error', str(exc), 'error')
    counts = Counter(item['severity'] for item in report['findings'])
    report['summary'] = {'slides': len(report['slides']), 'errors': counts['error'], 'unknowns': counts['unknown']}
    report['status'] = 'error' if counts['error'] else 'partial' if counts['unknown'] else 'ok'
    return report


def nonnegative_float(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError('must be finite and nonnegative')
    return number


def nonnegative_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError('must be nonnegative')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', type=Path)
    parser.add_argument('--min-font-pt', type=nonnegative_float, help='Optional native font threshold in points')
    parser.add_argument('--max-slide-chars', type=nonnegative_int, help='Optional native text limit per slide')
    parser.add_argument('--max-image-distortion', type=nonnegative_float, default=0.03,
                        help='max(display/source, source/display) - 1; default 0.03 (3%%)')
    parser.add_argument('--report', type=Path, help='Also write JSON to this path')
    args = parser.parse_args()
    report = audit_pptx(args.pptx, args.min_font_pt, args.max_slide_chars, args.max_image_distortion)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        if args.report.resolve() == args.pptx.resolve():
            parser.error('--report must not overwrite the source PPTX')
        try:
            args.report.write_text(output + '\n', encoding='utf-8')
        except OSError as exc:
            print(f'Cannot write report: {exc}', file=sys.stderr)
            return 1
    print(output)
    return {'ok': 0, 'error': 1, 'partial': 2}[report['status']]


if __name__ == '__main__':
    sys.exit(main())
