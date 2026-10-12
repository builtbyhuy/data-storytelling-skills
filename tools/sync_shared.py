"""Copy canonical shared references into independently installable skills."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def sync():
    count = 0
    for entry in sorted((ROOT / 'skills').glob('*/SKILL.md')):
        destination = entry.parent / 'references'
        destination.mkdir(exist_ok=True)
        for source in sorted((ROOT / 'shared').glob('*.md')):
            shutil.copyfile(source, destination / source.name)
            count += 1
        for name in ('LICENSE', 'NOTICE.md'):
            shutil.copyfile(ROOT / name, entry.parent / name)
    return count

if __name__ == '__main__':
    print(f'Synchronized {sync()} shared reference copies.')
