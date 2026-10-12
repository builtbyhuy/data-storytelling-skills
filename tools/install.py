"""Install this bounded suite without deleting existing skill resources.

Dry-run by default. Replacement requires --replace and a backup directory.
No network requests, config edits, dependency installation or servers.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import shutil
import zipfile
from validate import ROOT, NAMES, validate

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path.home() / '.codex' / 'skills')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    args = parser.parse_args()
    errors = validate()
    if errors:
        parser.error('; '.join(errors))
    destination = args.dest.expanduser().resolve()
    if destination == ROOT or destination.is_relative_to(ROOT / 'skills'):
        parser.error('Destination must be outside the source skills.')
    existing = []
    for name in sorted(NAMES):
        target = destination / name
        if target.is_symlink():
            parser.error(f'Refusing symbolic-link target: {name}')
        if target.exists():
            if not target.is_dir():
                parser.error(f'Skill target is not a directory: {name}')
            entry = target / 'SKILL.md'
            if not entry.exists() or f'name: {name}\n' not in entry.read_text(encoding='utf-8').replace('\r\n', '\n'):
                parser.error(f'Existing folder is not the matching skill: {name}')
            existing.append(name)
    if args.apply and existing and (not args.replace or not args.backup_dir):
        parser.error('Existing skills require --replace and --backup-dir before applying.')
    receipt = {'state': 'dry_run', 'skills': sorted(NAMES), 'replacing': existing,
               'preserves_unlisted_resources': True}
    if args.apply:
        backup = args.backup_dir.expanduser().resolve() if args.backup_dir else None
        if backup and backup.is_relative_to(destination):
            parser.error('Backup directory must be outside destination skills.')
        if backup:
            backup.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            archive = backup / f'skills-before-{stamp}.zip'
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
                for name in existing:
                    for file in sorted((destination / name).rglob('*')):
                        if file.is_symlink():
                            parser.error(f'Symbolic link found inside {name}; installation stopped before copying.')
                        if file.is_file():
                            z.write(file, file.relative_to(destination).as_posix())
            receipt['backup'] = str(archive)
        destination.mkdir(parents=True, exist_ok=True)
        for name in sorted(NAMES):
            shutil.copytree(ROOT / 'skills' / name, destination / name, dirs_exist_ok=True)
        receipt['state'] = 'installed'
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
