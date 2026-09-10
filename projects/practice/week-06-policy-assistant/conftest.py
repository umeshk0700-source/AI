import os, sys, pathlib
# LAB_SRC=solution  ->  run the tests against the reference implementation
_root = pathlib.Path(__file__).parent
sys.path.insert(0, str(_root / os.getenv("LAB_SRC", "src")))
sys.path.insert(0, str(_root / "tests"))
