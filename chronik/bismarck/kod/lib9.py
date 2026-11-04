# shim so the shared tools (covers4.py) work for the Bismarck project: fonts/colours from the Laconia kit, photos from bism/img
import importlib.util, os
from PIL import Image
_sp = importlib.util.spec_from_file_location('lib9_lac', os.path.dirname(os.path.abspath(__file__)) + '/../../lac/code/lib9.py')
_L = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_L)
for _k in dir(_L):
    if not _k.startswith('__'): globals()[_k] = getattr(_L, _k)
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
def src(n): return Image.open(B + 'img/' + n + '.jpg').convert('RGB')
