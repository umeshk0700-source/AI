import os, sys, pathlib
_root = pathlib.Path(__file__).parent
sys.path.insert(0, str(_root / os.getenv("LAB_SRC", "src")))
sys.path.insert(0, str(_root / "tests"))
sys.path.insert(0, str(_root / "fixtures"))
sys.path.insert(0, str(_root))
