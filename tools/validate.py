"""Structural package checks; these do not establish behavioral quality."""
from pathlib import Path
import re
import sys
import hashlib
import json
import zipfile

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

def validate_original_archive(failures):
    """Check the declared original example archive without rewriting its recipe."""
    folder = ROOT / 'examples/07-bike-sharing'
    archive = folder / 'untouched-practical.zip'
    receipt = folder / 'PUBLICATION.json'
    if not archive.exists() and not receipt.exists():
        return
    try:
        metadata = json.loads(receipt.read_text(encoding='utf-8'))
        if hashlib.sha256(archive.read_bytes()).hexdigest() != metadata['archive_sha256']:
            raise ValueError('archive hash differs from publication receipt')
        expected = metadata['original_files_sha256']
        with zipfile.ZipFile(archive) as bundle:
            if len(bundle.namelist()) != len(set(bundle.namelist())) or set(bundle.namelist()) != set(expected):
                raise ValueError('archive file set differs from original manifest')
            for name, digest in expected.items():
                if name.startswith(('/', '\\')) or '..' in Path(name).parts:
                    raise ValueError('unsafe archive entry')
                data = bundle.read(name)
                if hashlib.sha256(data).hexdigest() != digest:
                    raise ValueError(f'original bytes changed: {name}')
                if Path(name).suffix.lower() not in {'.md','.py','.csv','.json','.svg','.ps1','.html','.txt'}:
                    raise ValueError(f'unexpected original file type: {name}')
                # Preserve these two sealed environment-specific recipe receipts.
                # PACKAGE.md must disclose that they are not portable commands.
                if name not in {'README.md', 'Rebuild.ps1'} and re.search(r'[A-Za-z]:[/\\]+Users[/\\]+', data.decode('utf-8-sig'), re.I):
                    raise ValueError(f'undisclosed personal path: {name}')
        note = (folder / 'PACKAGE.md').read_text(encoding='utf-8')
        if 'environment-specific' not in note or '3.4.0' not in note:
            raise ValueError('original version/runtime qualification missing')
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        failures.append(f'Original Bike Sharing archive: {error}')

def validate_visual_complements(failures):
    """Preserve the frozen optional methods and their original license boundary."""
    folder = ROOT / 'optional-complements'
    archive = folder / 'visual-complements-v3.5.zip'
    receipt = folder / 'PUBLICATION.json'
    if not archive.exists() and not receipt.exists():
        return
    try:
        metadata = json.loads(receipt.read_text(encoding='utf-8'))
        if hashlib.sha256(archive.read_bytes()).hexdigest() != metadata['archive_sha256']:
            raise ValueError('archive hash differs from publication receipt')
        expected = metadata['original_files_sha256']
        allowed_local_receipts = {'frontend-design/SKILL.md',
                                  'frontend-design/references/local-browser-checks.md'}
        if set(metadata['environment_specific_original_receipts']) != allowed_local_receipts:
            raise ValueError('environment-specific receipt set changed')
        if len(expected) != 10 or 'frontend-design/LICENSE.txt' not in expected:
            raise ValueError('original ten-file snapshot or upstream license missing')
        with zipfile.ZipFile(archive) as bundle:
            if len(bundle.namelist()) != len(set(bundle.namelist())) or set(bundle.namelist()) != set(expected):
                raise ValueError('archive file set differs from original manifest')
            for name, digest in expected.items():
                if name.startswith(('/', '\\')) or '..' in Path(name).parts:
                    raise ValueError('unsafe archive entry')
                data = bundle.read(name)
                if hashlib.sha256(data).hexdigest() != digest:
                    raise ValueError(f'original bytes changed: {name}')
                if Path(name).suffix.lower() not in {'.md', '.txt', '.json', '.yaml'}:
                    raise ValueError(f'unexpected original file type: {name}')
                if name not in allowed_local_receipts and re.search(r'[A-Za-z]:[/\\]+Users[/\\]+', data.decode('utf-8-sig'), re.I):
                    raise ValueError(f'undisclosed personal path: {name}')
            if b'Apache License' not in bundle.read('frontend-design/LICENSE.txt'):
                raise ValueError('upstream Apache license missing')
        note = (folder / 'README.md').read_text(encoding='utf-8')
        if 'Environment-specific' not in note or 'composite' not in note or 'Apache-2.0' not in note:
            raise ValueError('license, activation or environment qualification missing')
        outer = folder / metadata['distribution_archive']
        if outer.parent != folder or hashlib.sha256(outer.read_bytes()).hexdigest() != metadata['distribution_archive_sha256']:
            raise ValueError('licensed outer distribution identity differs')
        expected_outer = metadata['distribution_files_sha256']
        if set(expected_outer) != {'LICENSE', 'README.md', archive.name}:
            raise ValueError('outer distribution needs notice, instructions and unchanged snapshot')
        with zipfile.ZipFile(outer) as bundle:
            if len(bundle.namelist()) != 3 or set(bundle.namelist()) != set(expected_outer):
                raise ValueError('outer distribution file set differs')
            if any(hashlib.sha256(bundle.read(n)).hexdigest() != h for n, h in expected_outer.items()):
                raise ValueError('outer distribution bytes differ')
            if bundle.read('LICENSE') != (ROOT / 'LICENSE').read_bytes() or bundle.read(archive.name) != archive.read_bytes():
                raise ValueError('outer notice/snapshot differs')
            if bundle.read('README.md') != (folder / 'DISTRIBUTION-README.md').read_bytes():
                raise ValueError('outer instructions differ')
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        failures.append(f'Optional visual complements: {error}')

def validate_wine_originals(failures):
    """Check complete original handoffs and the copied candidate, not quality."""
    folder = ROOT / 'evals/practical-v3.5'
    receipt = folder / 'PUBLICATION.json'
    if not receipt.exists():
        return
    try:
        metadata = json.loads(receipt.read_text(encoding='utf-8'))
        expected_codes = {'N17', 'N42', 'N68', 'N91', 'N35'}
        if set(metadata['archives']) != expected_codes:
            raise ValueError('five complete handoff receipts required')
        source_payloads = {}
        for code, item in metadata['archives'].items():
            archive = folder / item['archive']
            if archive.parent != folder or hashlib.sha256(archive.read_bytes()).hexdigest() != item['archive_sha256']:
                raise ValueError(f'{code}: archive identity differs')
            expected = item['original_files_sha256']
            allowed = {'inspect-detail.mjs', 'verify-render.mjs'} if code == 'N35' else set()
            if set(item['environment_specific_optional_qa_files']) != allowed:
                raise ValueError(f'{code}: environment-specific exceptions differ')
            with zipfile.ZipFile(archive) as bundle:
                if len(bundle.namelist()) != len(set(bundle.namelist())) or set(bundle.namelist()) != set(expected):
                    raise ValueError(f'{code}: original file set differs')
                for name, digest in expected.items():
                    if name.startswith(('/', '\\')) or '..' in Path(name).parts:
                        raise ValueError(f'{code}: unsafe entry')
                    data = bundle.read(name)
                    if hashlib.sha256(data).hexdigest() != digest:
                        raise ValueError(f'{code}: original bytes changed: {name}')
                    suffix = Path(name).suffix.lower()
                    if suffix not in {'.md','.py','.csv','.json','.svg','.mjs','.html','.txt','.css','.js','.png','.zip','.names'}:
                        raise ValueError(f'{code}: unexpected original file type: {name}')
                    if suffix not in {'.png', '.zip'} and name not in allowed:
                        if re.search(r'[A-Za-z]:[/\\]+Users[/\\]+', data.decode('utf-8-sig'), re.I):
                            raise ValueError(f'{code}: undisclosed personal path: {name}')
                    if code == 'N91':
                        source_payloads[name] = digest
        note = (folder / 'README.md').read_text(encoding='utf-8')
        if 'Environment-specific optional QA' not in note or 'CC BY 4.0' not in note:
            raise ValueError('original runtime/license qualification missing')
        example = ROOT / 'examples/08-wine-quality'
        published = json.loads((example / 'PUBLICATION.json').read_text(encoding='utf-8'))
        if published['original_files_sha256'] != source_payloads or len(source_payloads) != 16:
            raise ValueError('candidate original-file manifest differs')
        for name, digest in source_payloads.items():
            if hashlib.sha256((example / name).read_bytes()).hexdigest() != digest:
                raise ValueError(f'candidate original bytes changed: {name}')
        for name, item in published['previews'].items():
            if hashlib.sha256((example / name).read_bytes()).hexdigest() != item['sha256']:
                raise ValueError(f'candidate native preview changed: {name}')
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        failures.append(f'Wine original packages: {error}')

def validate_review_receipts(failures):
    folder = ROOT / 'evals/forward-v3.5'
    try:
        publication = folder / 'PUBLICATION.json'
        if publication.exists():
            metadata = json.loads(publication.read_text(encoding='utf-8'))
            for name, digest in metadata['unchanged_evaluation_receipts_sha256'].items():
                if Path(name).name != name or hashlib.sha256((folder / name).read_bytes()).hexdigest() != digest:
                    raise ValueError(f'original evaluation receipt changed: {name}')
        receipt = folder / 'REVIEWS-PUBLICATION.json'
        if not receipt.exists():
            return
        metadata = json.loads(receipt.read_text(encoding='utf-8'))
        if metadata['reader_contexts'] != 10 or metadata['visual_contexts'] != 8 or metadata['owner_answer_edits'] != 0:
            raise ValueError('original review scope changed')
        archive = folder / metadata['archive']
        if archive.parent != folder or hashlib.sha256(archive.read_bytes()).hexdigest() != metadata['archive_sha256']:
            raise ValueError('review archive identity differs')
        expected = metadata['original_files_sha256']
        with zipfile.ZipFile(archive) as bundle:
            if len(bundle.namelist()) != len(set(bundle.namelist())) or set(bundle.namelist()) != set(expected):
                raise ValueError('original review file set differs')
            for name, digest in expected.items():
                if name.startswith(('/', '\\')) or '..' in Path(name).parts:
                    raise ValueError('unsafe review entry')
                if Path(name).suffix.lower() not in {'.json','.csv','.md','.txt','.py','.mjs','.ps1','.png'}:
                    raise ValueError(f'unexpected original review type: {name}')
                if hashlib.sha256(bundle.read(name)).hexdigest() != digest:
                    raise ValueError(f'original review bytes changed: {name}')
            # Original environment paths are receipts, never executable setup advice.
            if 'environment-specific' not in metadata['note']:
                raise ValueError('original review environment qualification missing')
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        failures.append(f'Original review receipts: {error}')

def validate():
    failures = []
    validate_original_archive(failures)
    validate_visual_complements(failures)
    validate_wine_originals(failures)
    validate_review_receipts(failures)
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
