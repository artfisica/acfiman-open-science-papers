from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
for path in (root / 'papers').glob('*/build'):
    shutil.rmtree(path)
