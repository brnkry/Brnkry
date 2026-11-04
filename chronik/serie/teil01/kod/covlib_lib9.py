# shim so covers4.py can build the Teil 1 cover: fonts and colours from the Udet project, the image from teil1/cov
import importlib.util, os
_S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_sp = importlib.util.spec_from_file_location('lib9_ju87', _S + '/ju87/code/lib9.py'); _L = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_L)
oswald, YEL, RED, WHITE, DARK = _L.oswald, _L.YEL, _L.RED, _L.WHITE, _L.DARK
from PIL import Image
def src(n): return Image.open(_S + '/teil1/cov/' + n + '.jpg').convert('RGB')
