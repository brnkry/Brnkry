# Balck 9:16 cover in the CDM style: the profile portrait (b14), name as the biggest line; no heroic framing
from lib9 import *
from thumb_m import badge, T, grad, tag, photo, OUT
def cover():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    photo(can, 'b14', 600, 120, 1180, 400)
    grad(can, [(520, 400, 255, 0, 640), (960, 1210, 235, 0, H)])
    d = ImageDraw.Draw(can); badge(can, W / 2 - 75, 330, 92)
    tag(d, 290, 520, 'PENTAGON 1980', YEL)
    T(can, (CX, 1120), 'HERMANN', 124, WHITE)
    T(can, (CX, 1265), 'BALCK', 230, YEL)
    f = anton(88); s_ = 'LEHRER ODER TÄTER?'; T(can, (CX, 1405), s_, 88, WHITE, bold=1)
    x0 = CX - f.getlength(s_) / 2 + f.getlength('LEHRER ODER '); x1 = x0 + f.getlength('TÄTER')
    ImageDraw.Draw(can).rectangle((x0, 1452, x1, 1460), fill=RED)
    can.convert('RGB').save(OUT + 'DE_Balck_Lehrer_oder_Taeter.jpg', quality=93)
if __name__ == '__main__': cover(); print('ok')
