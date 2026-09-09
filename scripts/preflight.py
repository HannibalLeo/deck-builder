#!/usr/bin/env python3
"""Read-only local inventory; does not install packages or select a renderer."""
import json
import os
from pathlib import Path
import shutil
import subprocess


def existing(paths):
    seen = set()
    result = []
    for value in paths:
        if not value:
            continue
        p = Path(value).expanduser()
        if p.is_file() and os.access(p, os.X_OK):
            key = str(p.resolve())
            if key not in seen:
                result.append(str(p))
                seen.add(key)
    return result


def main():
    home = Path.home()
    bundle = home / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
    modules = bundle / 'node/node_modules'
    nodes = existing([os.environ.get('DECK_NODE'), shutil.which('node'),
                      bundle / 'node/bin/node'])
    probe = """const roots=JSON.parse(process.argv[1]);
const found={};
for(const name of ['pptxgenjs','@oai/artifact-tool','sharp']) {
try { found[name]=require.resolve(name,{paths:roots}); }
catch { found[name]=null; }
}
console.log(JSON.stringify(found));"""
    candidates = []
    for node in nodes:
        try:
            run = subprocess.run([node, '-e', probe,
                                  json.dumps([str(Path.cwd()), str(modules)])],
                                 capture_output=True, text=True, timeout=10)
            resolved = json.loads(run.stdout) if run.returncode == 0 else None
            candidates.append({'node': node, 'packages': resolved,
                               'probe_ok': resolved is not None})
        except (OSError, subprocess.TimeoutExpired, ValueError):
            candidates.append({'node': node, 'packages': None, 'probe_ok': False})
    result = {
        'scope': 'inventory only; no library execution, generation or application QA',
        'node_candidates': candidates,
        'python_candidates': existing([shutil.which('python3'), bundle / 'python/bin/python3']),
        'renderers': {
            'bundled_soffice': existing([bundle / 'bin/override/soffice']),
            'other_soffice': existing([shutil.which('soffice')]),
            'pdftoppm': existing([bundle / 'bin/override/pdftoppm', shutil.which('pdftoppm')]),
        },
        'font_directories': [str(p) for p in [home / 'Library/Fonts',
                                             Path('/System/Library/Fonts'),
                                             Path('/usr/share/fonts')]
                             if p.is_dir()],
        'policy': 'Use the active host presentation skill; path discovery does not override its rules.',
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
