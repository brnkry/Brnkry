# Wainwright 9:16 cover for Chronicle of Power: the gaunt general after captivity (w05), name as the biggest line; no heroic framing
from lib9 import *
from thumb_m import T, grad, photo, OUT
def mark(can, y):
    """channel wordmark: CHRONICLE in white, OF POWER on a yellow plate, red rule"""
    d = ImageDraw.Draw(can); f = anton(58); a, b = 'CHRONICLE ', 'OF POWER'; wa, wb = f.getlength(a), f.getlength(b); x = CX - (wa + wb + 24) / 2
    d.text((x, y), a, font=f, fill=WHITE, anchor='lm'); bb = d.textbbox((x + wa + 12, y), b, font=f, anchor='lm')
    d.rectangle((bb[0] - 12, bb[1] - 8, bb[2] + 12, bb[3] + 6), fill=YEL); d.text((x + wa + 12, y), b, font=f, fill=DARK, anchor='lm')
    d.rectangle((bb[0] - 12, bb[3] + 12, bb[0] + 60, bb[3] + 17), fill=RED)
def cover():
    can = Image.new('RGBA', (W, H), DARK + (255,))
    photo(can, 'w05', 120, 60, 1560, 400)
    grad(can, [(520, 400, 255, 0, 640), (960, 1210, 235, 0, H)])
    mark(can, 375)
    d = ImageDraw.Draw(can); f = bebas(70); s_ = 'SURRENDERED IN 1942'; b = d.textbbox((CX, 530), s_, font=f, anchor='mm')
    d.rectangle((b[0] - 20, b[1] - 10, b[2] + 20, b[3] + 10), fill=RED); d.text((CX, 530), s_, font=f, fill=WHITE, anchor='mm')
    T(can, (CX, 1120), 'JONATHAN', 124, WHITE)
    T(can, (CX, 1265), 'WAINWRIGHT', 200, YEL)
    T(can, (CX, 1405), 'THEN WATCHED JAPAN SURRENDER', 76, WHITE, bold=1)
    can.convert('RGB').save(OUT + 'EN_Wainwright_Surrendered.jpg', quality=93)
if __name__ == '__main__': cover(); print('ok')
