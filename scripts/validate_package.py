#!/usr/bin/env python3
"""Validate Amigo skill structure, naming, assets, local links and helper scripts."""
from __future__ import annotations
from pathlib import Path
import ast, re, sys, zipfile

root = Path(__file__).resolve().parents[1]
errors: list[str] = []
warnings: list[str] = []

# Exactly one active manifest, located at the bundle root.
skills = [p for p in root.rglob('*') if p.is_file() and p.name.lower() == 'skill.md']
if skills != [root / 'SKILL.md']:
    errors.append(f"Expected only root SKILL.md; found: {[str(p.relative_to(root)) for p in skills]}")

text_suffixes = {'.md','.html','.svg','.txt','.yaml','.yml','.xml','.json','.css','.js','.py','.sh','.sql','.toml'}
text_files: list[tuple[Path,str]] = []
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in text_suffixes:
        try: text_files.append((p, p.read_text(encoding='utf-8', errors='replace')))
        except Exception as e: errors.append(f"Cannot read text file {p.relative_to(root)}: {e}")

# Construct legacy names from fragments so this validator does not match itself.
legacy_terms = ('sar' + 'wam', 'sar' + 'vam', 'सर्व' + 'म', 'सर्व' + 'म्')
legacy_re = re.compile('|'.join(re.escape(x) for x in legacy_terms), re.I)
for p in root.rglob('*'):
    if legacy_re.search(p.name): errors.append(f"Previous brand spelling in path: {p.relative_to(root)}")
for p, content in text_files:
    if legacy_re.search(content): errors.append(f"Previous brand spelling remains in {p.relative_to(root)}")

brand = root/'references'/'modules'/'brand-for-pptx'
required = [
 'assets/logo/Amigo Wordmark Black.svg','assets/logo/Amigo Wordmark Black.png',
 'assets/logo/Amigo Wordmark White.svg','assets/logo/Amigo Wordmark White.png',
 'assets/logo/Amigo Monogram Black.svg','assets/logo/Amigo Monogram Black.png',
 'assets/logo/Amigo Monogram Black-1.svg','assets/logo/Amigo Monogram Black-1.png',
 'assets/gradients/main-gradient.png',
]
required += [f'assets/shapes/Assets {i:02d}.{ext}' for i in range(1,23) for ext in ('svg','png')]
for rel in required:
    if not (brand/rel).is_file(): errors.append(f"Missing required visual asset: {rel}")

manifest = root/'SKILL.md'
if not manifest.is_file() or not manifest.read_text(encoding='utf-8').startswith('---\nname: amigo\n'):
    errors.append('Root SKILL.md frontmatter is missing or malformed')

# Check local Markdown links (relative paths from each Markdown file).
for p, content in text_files:
    if p.suffix.lower() != '.md': continue
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', content):
        target = target.strip().split()[0].strip('<>') if target.strip() else ''
        if not target or target.startswith(('http://','https://','mailto:','#','data:')): continue
        target = target.split('#',1)[0]
        if not target: continue
        dest = (p.parent / target).resolve()
        try: dest.relative_to(root.resolve())
        except ValueError: continue
        if not dest.exists(): warnings.append(f"Unresolved local Markdown link: {p.relative_to(root)} -> {target}")

# Syntax-check Python source without executing it.
for p in root.rglob('*.py'):
    try: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    except SyntaxError as e: errors.append(f"Python syntax error in {p.relative_to(root)}: {e}")

if errors:
    print('FAIL')
    for item in errors: print(' -', item)
    for item in warnings: print(' WARN:', item)
    sys.exit(1)
print('PASS: one manifest, legacy-name scan, Amigo assets, metadata and Python syntax')
if warnings:
    print(f"WARNINGS: {len(warnings)} unresolved local links (may be schematic examples)")
    for item in warnings[:30]: print(' -', item)
