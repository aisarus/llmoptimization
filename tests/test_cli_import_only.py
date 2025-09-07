import importlib
import types

def test_package_importable():
    pkg = importlib.import_module("efmcalc")
    if not isinstance(pkg, types.ModuleType):
        raise TypeError()