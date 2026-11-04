CLIP = {}
def clipping(can, t, t0, n, box, xy, wd, rot):
    """a newspaper cutting dropped onto the pile"""
    if t < t0: return
    if n not in CLIP: CLIP[n] = src(n).crop(box).convert('RGBA')
    k = eout((t - t0) / 0.32); P_ = CLIP[n]; P_ = P_.resize((int(wd), int(wd * P_.height / P_.width)), Image.LANCZOS).rotate(rot + (1 - k) * 7, expand=True, resample=Image.BICUBIC)
    sc = lerp(1.3, 1.0, k); P_ = P_.resize((int(P_.width * sc), int(P_.height * sc)), Image.BICUBIC)
    if k < 1: P_.putalpha(P_.getchannel('A').point(lambda v: int(v * min(1, k * 1.6))))
    sh = Image.new('RGBA', P_.size, (0, 0, 0, 0)); sh.putalpha(P_.getchannel('A').point(lambda v: int(v * 0.7)))
    x, y = int(xy[0] - P_.width / 2), int(xy[1] - P_.height / 2); can.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (x + 10, y + 20)); can.alpha_composite(P_, (x, y))
