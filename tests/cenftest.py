import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "mha-finance" / "src"
sys.path.insert(0, str(SRC))