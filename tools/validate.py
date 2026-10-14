"""Structural package checks; these do not establish behavioral quality."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'data-storytelling', 'business-insight-diagnosis', 'evidence-to-narrative',
         'business-chart-communication', 'data-story-redteam', 'analytics-adoption'}
AUTHORED_EXAMPLE_PDFS = {
    f'examples/{case}/brief.pdf'
    for case in ('01-profit-decision', '02-fair-comparison', '03-join-audit')
}
AUTHORED_EXAMPLE_PDFS.add('examples/04-attendance-pilot/thu-nghiem-chuyen-can.pdf')
AUTHORED_EXAMPLE_PDFS.add('examples/05-asean-electricity/energy-editorial.vi.pdf')
AUTHORED_EXAMPLE_PDFS.add('examples/06-bank-marketing/report.pdf')

def validate():
    failures = []
    entries = list((ROOT / 'skills').glob('*/SKILL.md'))
    if {p.parent.name for p in entries} != NAMES:
        failures.append('Six expected skill entries must be present.')
    for entry in entries:
        body = entry.read_text(encoding='utf-8')
        match = re.match(r'^---\n(.*?)\n---\n', body, re.S)
        if not match:
            failures.append(f'{entry.relative_to(ROOT)}: frontmatter missing')
            continue
        header = match.group(1)
        if not re.search(r'^name: ' + re.escape(entry.parent.name) + r'$', header, re.M):
            failures.append(f'{entry.parent.name}: name mismatch')
        if not re.search(r'^description: .+', header, re.M):
            failures.append(f'{entry.parent.name}: description missing')
        if re.search(r'\bTODO\b|\bTBD\b|\[INSERT', body):
            failures.append(f'{entry.parent.name}: unfinished scaffold')
        metadata = entry.parent / 'agents' / 'openai.yaml'
        if not metadata.exists() or 'allow_implicit_invocation: true' not in metadata.read_text(encoding='utf-8'):
            failures.append(f'{entry.parent.name}: implicit invocation must be enabled')
        for name in ('LICENSE', 'NOTICE.md'):
            copy = entry.parent / name
            if not copy.exists() or copy.read_bytes() != (ROOT / name).read_bytes():
                failures.append(f'{entry.parent.name}: missing/drifted distribution notice: {name}')
        for shared in (ROOT / 'shared').glob('*.md'):
            copy = entry.parent / 'references' / shared.name
            if not copy.exists() or copy.read_bytes() != shared.read_bytes():
                failures.append(f'{entry.parent.name}: shared reference drift: {shared.name}')
        for document in entry.parent.rglob('*.md'):
            text = document.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#')[0]
                if target and not (document.parent / target).resolve().exists():
                    failures.append(f'{document.relative_to(ROOT)}: broken link {target}')
    for file in ROOT.rglob('*'):
        if not file.is_file() or '.git' in file.parts:
            continue
        if file.suffix.lower() == '.pdf':
            relative = file.relative_to(ROOT).as_posix()
            if relative not in AUTHORED_EXAMPLE_PDFS:
                failures.append(f'Only explicitly allowlisted authored example handoffs may be PDFs: {relative}')
            elif not file.read_bytes().startswith(b'%PDF-'):
                failures.append(f'Authored example is not a PDF: {relative}')
        if file.suffix.lower() in {'.md', '.json', '.yaml', '.py', '.csv', '.mjs', '.cjs', '.js', '.ps1', '.html', '.svg', '.css'}:
            text = file.read_text(encoding='utf-8')
            if re.search(r'[A-Za-z]:[/\\]+Users[/\\]+', text, re.I):
                failures.append(f'Personal absolute path in public file: {file.relative_to(ROOT)}')
    if not (ROOT / 'LICENSE').exists() or not (ROOT / 'NOTICE.md').exists():
        failures.append('License and attribution notice required.')
    return failures

if __name__ == '__main__':
    errors = validate()
    print('\n'.join(errors) if errors else 'Package structural checks passed (6 skills).')
    sys.exit(bool(errors))
