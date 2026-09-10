#!/usr/bin/env python3
"""Behavior checks using small OOXML packages; no presentation library required."""
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib

SCRIPT = Path(__file__).with_name('audit_pptx.py')
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def png(width=200, height=100):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress((b'\0' + b'\0' * width * 3) * height)) + chunk(b'IEND', b''))


def picture(cx=200, cy=100, crop='', extra='', fill=''):
    return f'''<p:pic><p:nvPicPr><p:cNvPr id="2" name="photo"/></p:nvPicPr>
    <p:blipFill><a:blip r:embed="img"/>{crop}<a:stretch><a:fillRect {fill}/></a:stretch></p:blipFill>
    <p:spPr><a:xfrm {extra}><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"/></p:spPr></p:pic>'''


def text_shape(text='正文文字', size='770', name='body', default=False):
    props = '' if size is None else f'<a:rPr sz="{size}"/>'
    para = f'<a:pPr><a:defRPr sz="{size}"/></a:pPr>' if default else ''
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="3" name="{name}"/></p:nvSpPr>
    <p:txBody><a:bodyPr/><a:lstStyle/><a:p>{para}<a:r>{'' if default else props}<a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>'''


def package(path, shapes, data=None):
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('ppt/presentation.xml', f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst><p:sldId id="256" r:id="s1"/></p:sldIdLst></p:presentation>')
        archive.writestr('ppt/_rels/presentation.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="s1" Target="slides/slide1.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"/></Relationships>')
        archive.writestr('ppt/slides/slide1.xml', f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree>{shapes}</p:spTree></p:cSld></p:sld>')
        archive.writestr('ppt/slides/_rels/slide1.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="img" Target="../media/image.png" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"/></Relationships>')
        archive.writestr('ppt/media/image.png', png() if data is None else data)


class AuditTests(unittest.TestCase):
    def run_audit(self, shapes='', *args, data=None):
        with tempfile.TemporaryDirectory() as temp:
            deck = Path(temp) / 'fixture.pptx'
            output = Path(temp) / 'report.json'
            package(deck, shapes, data)
            result = subprocess.run([sys.executable, str(SCRIPT), str(deck), '--report', str(output), *args], capture_output=True, text=True)
            self.assertTrue(output.exists(), f'Audit did not produce a report: {result.stderr}')
            return result, json.loads(output.read_text())

    def test_twofold_stretch_is_error_and_nonzero_exit(self):
        result, report = self.run_audit(picture(400, 100))
        self.assertEqual(result.returncode, 1)
        self.assertIn('image_distortion', [f['code'] for f in report['findings']])
        self.assertAlmostEqual(report['slides'][0]['images'][0]['distortion'], 1.0)

    def test_equal_scale_rotation_and_crop_do_not_trigger_distortion(self):
        for shapes in [picture(400, 200), picture(extra='rot="5400000"'), picture(100, 100, '<a:srcRect l="25000" r="25000"/>'), picture(200, 200, fill='b="50000"')]:
            with self.subTest(shapes=shapes):
                result, report = self.run_audit(shapes)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(report['slides'][0]['images'][0]['status'], 'ok')

    def test_distortion_tolerance_is_configurable_and_symmetric(self):
        result, _ = self.run_audit(picture(200, 200), '--max-image-distortion', '1.01')
        self.assertEqual(result.returncode, 0)
        result, report = self.run_audit(picture(200, 200))
        self.assertEqual(result.returncode, 1)
        self.assertAlmostEqual(report['slides'][0]['images'][0]['distortion'], 1.0)

    def test_body_small_font_and_default_properties_are_checked(self):
        for default in (True, False):
            with self.subTest(default=default):
                result, report = self.run_audit(text_shape(default=default), '--min-font-pt', '14')
                self.assertEqual(result.returncode, 1)
                self.assertIn('font_too_small', [f['code'] for f in report['findings']])
                self.assertEqual(report['slides'][0]['font_sizes_pt']['7.7'], 4)

    def test_small_font_exemptions_still_count_characters(self):
        for name in ['caption-source', 'footer-note', 'page-number']:
            result, report = self.run_audit(text_shape(name=name), '--min-font-pt', '14')
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report['slides'][0]['native_text_chars'], 4)
            self.assertEqual(report['slides'][0]['exempt_text_chars'], 4)

    def test_font_threshold_is_inclusive_and_opt_in(self):
        result, _ = self.run_audit(text_shape())
        self.assertEqual(result.returncode, 0)
        result, _ = self.run_audit(text_shape(size='1400'), '--min-font-pt', '14')
        self.assertEqual(result.returncode, 0)

    def test_character_limit_is_opt_in_and_counts_unicode(self):
        result, report = self.run_audit(text_shape('中文AB'), '--max-slide-chars', '3')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['slides'][0]['native_text_chars'], 4)
        self.assertIn('slide_text_limit', [f['code'] for f in report['findings']])
        result, _ = self.run_audit(text_shape('中文AB'), '--max-slide-chars', '4')
        self.assertEqual(result.returncode, 0)

    def test_inherited_font_and_unreadable_image_are_unknown(self):
        _, report = self.run_audit(text_shape(size=None) + picture(), data=b'not an image')
        self.assertEqual(report['status'], 'partial')
        self.assertEqual(report['slides'][0]['unknown_font_chars'], 4)
        self.assertEqual(report['slides'][0]['images'][0]['status'], 'unknown')

    def test_group_transform_is_unknown_instead_of_false_error(self):
        group = '<p:grpSp><p:grpSpPr><a:xfrm><a:ext cx="100" cy="100"/><a:chExt cx="400" cy="100"/></a:xfrm></p:grpSpPr>' + picture(400, 100) + '</p:grpSp>'
        _, report = self.run_audit(group)
        self.assertEqual(report['status'], 'partial')
        self.assertEqual(report['slides'][0]['images'][0]['status'], 'unknown')
        self.assertNotIn('image_distortion', [f['code'] for f in report['findings']])

    def test_jpeg_dimensions_are_supported_without_pillow(self):
        # Minimal SOF0 stream for header inspection, with 200 x 100 dimensions.
        jpeg = b'\xff\xd8\xff\xc0\x00\x11\x08\x00\x64\x00\xc8\x03' + b'\x01\x11\x00\x02\x11\x00\x03\x11\x00' + b'\xff\xd9'
        result, report = self.run_audit(picture(400, 100), data=jpeg)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['slides'][0]['images'][0]['source_pixels'], [200, 100])

    def test_autofit_does_not_hide_known_small_declared_size(self):
        shapes = text_shape().replace('<a:bodyPr/>', '<a:bodyPr><a:normAutofit/></a:bodyPr>')
        result, report = self.run_audit(shapes, '--min-font-pt', '14')
        self.assertEqual(result.returncode, 1)
        self.assertIn('font_too_small', [f['code'] for f in report['findings']])
        self.assertIn('font_unknown', [f['code'] for f in report['findings']])

    def test_local_list_default_font_is_resolved(self):
        shapes = text_shape(size=None).replace('<a:lstStyle/>', '<a:lstStyle><a:lvl1pPr><a:defRPr sz="770"/></a:lvl1pPr></a:lstStyle>')
        result, report = self.run_audit(shapes, '--min-font-pt', '14')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['slides'][0]['unknown_font_chars'], 0)

    def test_unknown_only_has_distinct_nonzero_exit(self):
        result, report = self.run_audit(text_shape(size=None))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report['status'], 'partial')

    def test_invalid_archive_returns_structured_error(self):
        with tempfile.TemporaryDirectory() as temp:
            deck = Path(temp) / 'broken.pptx'
            deck.write_bytes(b'broken')
            result = subprocess.run([sys.executable, str(SCRIPT), str(deck)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)['status'], 'error')


if __name__ == '__main__':
    unittest.main()
