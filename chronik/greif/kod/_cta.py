def cta(can, t, t0):
    """small comment card in the lower left: the bubble rocks, the question mark bounces, both lines wipe in"""
    if t < t0: return
    k = eout((t - t0) / 0.45); A = int(255 * k); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0 = 70 - (1 - k) * 60, 1330; f1, f2 = oswald(46, 600), oswald(38, 500)
    s1, s2 = 'Kanntet ihr diese Geschichte', 'Schreibt es in die Kommentare!'; w1_ = f1.getlength(s1); wq = f1.getlength('?')
    wd = max(w1_ + wq, f2.getlength(s2)) + 150
    d.rounded_rectangle((x0, y0, x0 + wd, y0 + 140), 22, fill=(10, 11, 14, int(185 * k)), outline=YEL + (int(220 * k),), width=3); can.alpha_composite(L)
    B_ = Image.new('RGBA', (90, 90), (0, 0, 0, 0)); db = ImageDraw.Draw(B_)
    db.rounded_rectangle((12, 14, 78, 64), 12, fill=YEL + (A,)); db.polygon([(26, 62), (42, 62), (22, 80)], fill=YEL + (A,))
    for i in range(3): db.ellipse((27 + i * 15, 35, 35 + i * 15, 43), fill=DARK + (A,))
    B_ = B_.rotate(9 * math.sin((t - t0) * 4.2), resample=Image.BICUBIC); can.alpha_composite(B_, (int(x0 + 18), int(y0 + 22)))
    def wipe(s_, f, col, xy, ts_, dur=0.7):
        if t < ts_: return
        bb = f.getbbox(s_); T_ = Image.new('RGBA', (bb[2] + 20, bb[3] + 20), (0, 0, 0, 0)); ImageDraw.Draw(T_).text((0, 0), s_, font=f, fill=col + (255,))
        u = eio((t - ts_) / dur); m = np.clip((u * (T_.width + 40) - np.arange(T_.width)) / 40, 0, 1)
        T_.putalpha(Image.fromarray((np.asarray(T_.getchannel('A'), np.float32) * m[None, :] * k).astype(np.uint8))); can.alpha_composite(T_, (int(xy[0]), int(xy[1])))
    tx = x0 + 125; wipe(s1, f1, WHITE, (tx, y0 + 20), t0 + 0.25); wipe(s2, f2, YEL, (tx, y0 + 82), t0 + 0.9)
    tq = t0 + 0.9
    if t > tq:
        bo = -abs(math.sin((t - tq) * 5.0)) * 10 * min(1, (t - tq) / 0.3); Q = Image.new('RGBA', (60, 80), (0, 0, 0, 0)); ImageDraw.Draw(Q).text((4, 0), '?', font=f1, fill=YEL + (A,))
        Q = Q.rotate(12 * math.sin((t - tq) * 3.0), resample=Image.BICUBIC); can.alpha_composite(Q, (int(tx + w1_ + 2), int(y0 + 20 + bo)))
