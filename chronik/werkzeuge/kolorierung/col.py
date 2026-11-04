# hand-built colourisation of the Kammhuber portrait: luminance from the upscaled photo, colour from region masks (Lab a/b),
# historically fitting colours: Luftwaffe blue-grey cloth, General's white collar tabs with gold, gold/silver shoulder boards, gold buttons
import numpy as np, cv2
S = 4; up = cv2.imread('up4.png', 0); H, W = up.shape
def P(*pts): return np.array([(x * S, y * S) for x, y in pts], np.int32)
def mask(polys, feather=6):
    m = np.zeros((H, W), np.uint8)
    for p in polys: cv2.fillPoly(m, [P(*p)], 255)
    return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), feather * S / 2)
def disc(pts, r, feather=1.5):
    m = np.zeros((H, W), np.uint8)
    for x, y in pts: cv2.circle(m, (x * S, y * S), r * S, 255, -1)
    return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), feather * S)
L = up.astype(np.float32) / 255 * 100
a = np.zeros((H, W), np.float32); b = np.zeros((H, W), np.float32)
def paint(m, ca, cb, lmod=None):
    global a, b
    k = m if lmod is None else m * lmod
    a = a * (1 - m) + ca * k + a * 0; b = b * (1 - m) + cb * k
Ln = L / 100
hp = L - cv2.GaussianBlur(L, (0, 0), 6 * S)   # local detail
# ---- background: dark = foliage green, bright = pale summer sky/gravel (warm grey)
person = mask([[(225, 80), (262, 70), (312, 72), (352, 86), (380, 110), (392, 150), (396, 192), (404, 196), (407, 232), (396, 262), (381, 292), (372, 322), (395, 345),
               (430, 368), (470, 380), (500, 393), (526, 420), (542, 452), (556, 485), (567, 520), (567, 800), (38, 800), (42, 700), (47, 600), (55, 480), (72, 428),
               (98, 386), (140, 368), (186, 358), (206, 332), (204, 300), (195, 255), (191, 200), (195, 150), (206, 112)]], 2)
src = cv2.imread('src.jpg'); pm = (cv2.resize(person, (src.shape[1], src.shape[0])) > 0.5).astype(np.uint8)
gc = np.where(cv2.erode(pm, np.ones((25, 25), np.uint8)) > 0, cv2.GC_FGD, np.where(pm > 0, cv2.GC_PR_FGD, np.where(cv2.dilate(pm, np.ones((15, 15), np.uint8)) > 0, cv2.GC_PR_BGD, cv2.GC_BGD))).astype(np.uint8)
bgm, fgm = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
cv2.grabCut(src, gc, None, bgm, fgm, 6, cv2.GC_INIT_WITH_MASK)
pm2 = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 1, 0).astype(np.float32)
person = cv2.GaussianBlur(cv2.resize(pm2, (W, H), interpolation=cv2.INTER_LINEAR), (0, 0), 3)
cut = np.zeros((H, W), np.uint8); cv2.fillPoly(cut, [P((375, 300), (398, 266), (430, 262), (440, 372), (398, 346))], 255)
person = person * (1 - cv2.GaussianBlur(cut.astype(np.float32) / 255, (0, 0), 6))
cv2.imwrite('mask_person.png', (person * 255).astype(np.uint8))
g = np.clip((70 - L) / 40, 0, 1)            # how "foliage-dark" a pixel is
a_bg = -16 * g + 1.5 * (1 - g); b_bg = 24 * g + 5 * (1 - g)
a = a_bg * (1 - person); b = b_bg * (1 - person)
# ---- uniform: Luftwaffe blue-grey (Tuch), a touch less colour in deep folds and highlights
uni = person.copy(); lm = np.clip(1 - np.abs(Ln - 0.5) * 1.2, 0.35, 1)
a += uni * (-1.5 * lm); b += uni * (-8 * lm)
def over(m, ca, cb, sat=None):
    global a, b
    s = 1 if sat is None else sat
    a = a * (1 - m) + ca * s * m; b = b * (1 - m) + cb * s * m
# ---- skin (face, ears, neck), cheeks and lips warmer
skin = mask([[(186, 150), (210, 104), (252, 94), (302, 96), (342, 112), (368, 142), (384, 180), (404, 192), (412, 230), (396, 266), (380, 300), (372, 326), (344, 340),
              (300, 346), (262, 342), (230, 334), (208, 304), (194, 262), (184, 205)]], 2) * person
ls = np.clip((Ln - 0.2) / 0.5, 0.65, 1.1)
over(skin, 11 * ls, 16 * ls)
cheek = disc([(228, 248), (330, 245)], 20, 8); over(cheek * 0.35, 18, 16)
lips = mask([[(236, 270), (258, 267), (284, 269), (298, 274), (284, 282), (258, 283)]], 2); over(lips * 0.45, 19, 12)
nose = disc([(258, 236)], 14, 5); over(nose * 0.4, 18, 15)
# hair: short, ash-blond going grey; brows a bit darker
hair = mask([[(212, 102), (250, 74), (316, 74), (362, 92), (386, 128), (394, 172), (384, 182), (370, 150), (348, 120), (310, 103), (262, 99), (228, 108)]], 3)
over(hair * person, 2, 11)
eyes = disc([(213, 196), (290, 196)], 5, 1); over(eyes * 0.8, -3, -9)
# ---- shirt collar white, tie dark blue-grey
shirt = mask([[(226, 330), (258, 343), (262, 380), (244, 398), (226, 372)], [(300, 342), (334, 330), (356, 336), (346, 370), (312, 386), (296, 366)]], 1.5)
over(shirt, -0.5, -2.5)
tie = mask([[(256, 352), (292, 350), (292, 388), (286, 470), (270, 500), (252, 470), (252, 390)]], 1.5); over(tie, -1, -7)
# Knight's Cross ribbon (black-white-red: the visible band is mostly red), cross itself neutral black/silver
rib = mask([[(258, 362), (288, 360), (288, 384), (258, 386)]], 1); over(rib, 50 * np.clip((Ln - 0.12) / 0.4, 0, 1), 32 * np.clip((Ln - 0.12) / 0.4, 0, 1))
cross = mask([[(238, 385), (290, 385), (292, 438), (238, 440)]], 0.8); over(cross, 0, 0)
# ---- General's insignia: white collar tabs with gold embroidery, gold collar piping, gold/silver shoulder boards
tabs = mask([[(150, 365), (196, 352), (206, 390), (178, 440), (148, 430)], [(352, 384), (392, 378), (404, 412), (402, 462), (360, 452)]], 1)
emb = np.clip((-hp - 2) / 6, 0, 1)                        # darker strokes inside the white tab = gold thread
over(tabs, 6 * emb, 40 * emb)
boards = mask([[(98, 388), (118, 372), (180, 360), (190, 372), (130, 392), (102, 402)], [(428, 384), (460, 380), (500, 392), (526, 418), (520, 430), (480, 410), (432, 398)]], 1)
over(boards * np.clip((Ln - 0.55) / 0.15, 0, 1), 5, 30)
# ---- gold: breast eagle and buttons; silver: clasp, badges stay neutral
eagle = mask([[(96, 495), (170, 488), (168, 530), (100, 532)]], 1); over(eagle * np.clip((hp - 2.5) / 5, 0, 1), 5, 32)
btn = disc([(110, 562), (220, 580), (210, 650), (196, 720), (182, 792), (370, 595)], 11, 1); over(btn, 6, 38)
silver = mask([[(188, 585), (240, 585), (228, 640), (185, 650)], [(335, 625), (390, 625), (392, 735), (335, 735)], [(265, 745), (335, 735), (345, 800), (262, 800)]], 0.8)
over(silver, 0, 0)
pilot = mask([[(268, 770), (300, 752), (330, 760), (340, 800), (270, 800)]], 1); over(pilot * np.clip((hp - 1) / 6, 0, 1), 4, 26)
# ---- signature ink stays black
ink = (L < 22).astype(np.float32) * (1 - skin); ink = cv2.GaussianBlur(ink, (0, 0), 2); over(ink, 0, 0)
# small blur over the swastika details (channel rule), done on luminance before colour
for (x, y, r) in [(264, 412, 9), (361, 700, 9), (119, 514, 8), (360, 652, 7), (302, 774, 8)]:
    x, y, r = x * S, y * S, r * S; box = L[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r]
    bl = cv2.GaussianBlur(cv2.resize(cv2.resize(box, (box.shape[1] // 8, box.shape[0] // 8)), box.shape[::-1]), (0, 0), r * 0.25)
    mm = np.zeros(box.shape, np.float32); cv2.circle(mm, (2 * r, 2 * r), r, 1, -1); mm = cv2.GaussianBlur(mm, (0, 0), r * 0.3)
    L[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r] = box * (1 - mm) + bl * mm
a = cv2.GaussianBlur(a, (0, 0), 1.2); b = cv2.GaussianBlur(b, (0, 0), 1.2)
rgb = cv2.cvtColor(np.dstack([L, a, b]).astype(np.float32), cv2.COLOR_LAB2RGB)
rgb = np.clip(rgb, 0, 1)
# final grade: very slight warmth, gentle contrast, fine film grain so the upscale does not look plastic
rgb = np.clip((rgb - 0.5) * 1.04 + 0.5, 0, 1); rgb[..., 0] *= 1.01; rgb[..., 2] *= 0.985
out = (rgb * 255).astype(np.float32) + np.random.default_rng(1).normal(0, 2.2, (H, W, 1))
out = np.clip(out, 0, 255).astype(np.uint8)
fh = cv2.resize(out, (1360, 1920), interpolation=cv2.INTER_AREA)
cv2.imwrite('Kammhuber_koloriert_FullHD.jpg', cv2.cvtColor(fh, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite('prev.jpg', cv2.cvtColor(cv2.resize(out, (680, 960), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2BGR))
