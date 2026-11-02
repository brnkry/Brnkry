# shim so the shared tools (covers4.py) work for the Egon Mayer project: fonts/colours from the Laconia kit, photos from egon/drive with the blurs of eg.py
import importlib.util, os, sys
_sp = importlib.util.spec_from_file_location('lib9_lac', os.path.dirname(os.path.abspath(__file__)) + '/../../lac/code/lib9.py')
_L = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_L)
for _k in dir(_L):
    if not _k.startswith('__'): globals()[_k] = getattr(_L, _k)
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eg as _eg
def src(n): return _eg.src(n)
