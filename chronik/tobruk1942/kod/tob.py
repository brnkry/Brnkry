# "Tobruk 1942" CDM Short (9:16), map story modelled on the reference: date/clock tag top left, VS card,
# portraits on the map, the fortress ring, hour-by-hour assault, archive film cards; channel type and safe areas.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
ALLY, SAND = (60, 90, 170), (226, 204, 160)
def basemap2(t):
    p = P(t); im = Image.new('RGB', (W, H), WATER); d = ImageDraw.Draw(im)
    yy = np.linspace(0, 1, H)[:, None]; sea = np.stack([22 + 20 * yy, 56 + 30 * yy, 110 + 30 * yy], -1) * np.ones((1, W, 1))
    im = Image.fromarray(sea.astype(np.uint8)); d = ImageDraw.Draw(im)
    for name, pts in GEO['countries']: d.polygon([p(*q) for q in pts], fill=LAND)
    for name, pts in GEO['countries']: d.line([p(*q) for q in pts] + [p(*pts[0])], fill=SAND, width=max(3, int(p.k / 300)))
    a = np.asarray(im, np.float32) + NOISE[..., None] * 0.8
    xx = np.linspace(-1, 1, W)[None, :]; y2 = np.linspace(-1, 1, H)[:, None]; v = np.clip(1.12 - 0.36 * (xx ** 2 + y2 ** 2), 0.5, 1)
    return Image.fromarray((a * v[..., None]).clip(0, 255).astype(np.uint8)).convert('RGBA')
def tag(im, t, t0, s, red=None):
    """date / clock tag top left (in the safe area)"""
    if t < t0: return
    k = eout((t - t0) / 0.2); d = ImageDraw.Draw(im); f = font('Anton', 58); b = d.textbbox((60, 300), s, font=f)
    d.rectangle((b[0] - 16, b[1] - 10, b[2] + 16, b[3] + 12), fill=(14, 14, 16, int(235 * k))); d.text((60, 300 + 10 * (1 - k)), s, font=f, fill=WHITE + (int(255 * k),))
    if red:
        f2 = font('Oswald', 30); b2 = d.textbbox((b[2] + 34, 312), red, font=f2); d.rectangle((b2[0] - 10, b2[1] - 6, b2[2] + 10, b2[3] + 8), fill=RED + (int(255 * k),)); d.text((b[2] + 34, 312), red, font=f2, fill=WHITE + (int(255 * k),))
def glowring(im, t, t0, c, r):
    if t < t0: return
    k = eout((t - t0) / 0.5); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); rr = r * (1.4 - 0.4 * k)
    d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=YEL + (int(255 * k),), width=14)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(lay)
def perimeter(im, t, t0, p, dur=1.2, col=(232, 232, 228), wd=7, broken=0.0):
    if t < t0: return
    u = eio((t - t0) / dur); c = (23.96, 32.075); pts = []
    for i in range(0, 181):
        a = math.radians(180 + i); pts.append(p(c[0] + 0.19 * math.cos(a), c[1] + 0.12 * math.sin(a) - 0.0 * i))
    n = int(len(pts) * u); d = ImageDraw.Draw(im)
    for i in range(0, max(0, n - 1), 3):
        d.line((pts[i], pts[min(i + 2, n - 1)]), fill=col + (255,), width=wd)
def plane(im, xy, ang=0.4, s=1.0, col=(30, 30, 32)):
    x, y = xy; R = lambda dx, dy: (x + (dx * math.cos(ang) - dy * math.sin(ang)) * s, y + (dx * math.sin(ang) + dy * math.cos(ang)) * s)
    d = ImageDraw.Draw(im); d.polygon([R(-30, -4), R(30, -4), R(36, 0), R(30, 4), R(-30, 4)], fill=col + (255,)); d.polygon([R(-4, -40), R(6, -40), R(8, 40), R(-4, 40)], fill=col + (255,)); d.polygon([R(-30, -12), R(-24, -12), R(-24, 12), R(-30, 12)], fill=col + (255,))
def fire(im, xy, t, s=1.0):
    x, y = xy; lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); f = 1 + 0.12 * math.sin(t * 13 + x)
    for r, c in ((34, (255, 120, 20, 200)), (22, (255, 200, 60, 230)), (10, (255, 250, 200, 255))):
        rr = r * s * f; d.ellipse((x - rr, y - rr * 1.3, x + rr, y + rr * 0.7), fill=c)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))
def vscard(im, t, t0, t1):
    if t < t0 or t > t1 + 0.25: return
    k = eout((t - t0) / 0.3) * (1 - eout((t - t1) / 0.25)); x0, y0, w, h = 70, 700, 820, 760; a = int(245 * k)
    L = Image.new('RGBA', (w, h), (16, 16, 18, a)); d = ImageDraw.Draw(L)
    d.text((40, 30), 'DIE FESTUNG TOBRUK', font=font('Anton', 74), fill=WHITE + (int(255 * k),)); d.text((42, 128), '20.-21. JUNI 1942', font=font('Oswald', 36), fill=YEL + (int(255 * k),))
    d.rectangle((40, 200, 390, 560), fill=ALLY + (a,)); d.rectangle((430, 200, 780, 560), fill=(150, 120, 70, a))
    d.ellipse((370, 330, 450, 410), fill=(16, 16, 18, a)); d.text((410, 370), 'VS', font=font('Anton', 40), fill=WHITE + (int(255 * k),), anchor='mm')
    for i, s_ in enumerate(('SÜDAFRIKANER', 'BRITEN', 'INDER')):
        if t >= K(['gegen Südafrikaner,', 'Briten und', 'und Inder.'][i], 1 if i == 0 else (0 if i == 1 else 1)): d.text((215, 260 + i * 80), s_, font=font('Anton', 52), fill=WHITE + (int(255 * k),), anchor='mt')
    if t >= K('Rommels Afrikakorps'): d.text((605, 300), 'ROMMELS', font=font('Anton', 52), fill=WHITE + (int(255 * k),), anchor='mt'); d.text((605, 370), 'AFRIKAKORPS', font=font('Anton', 52), fill=WHITE + (int(255 * k),), anchor='mt')
    d.text((215, 600), 'ALLIIERTE', font=font('Oswald', 40), fill=(170, 190, 255, int(255 * k)), anchor='mt'); d.text((605, 600), 'DEUTSCHE / ITALIENER', font=font('Oswald', 36), fill=(230, 200, 140, int(255 * k)), anchor='mt')
    sh = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 40, w + 40, h + 40), fill=(0, 0, 0, int(160 * k))); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), (x0 - 30, y0 - 20 + int(50 * (1 - k))))
    im.alpha_composite(L, (x0, y0 + int(50 * (1 - k))))
CH = Image.open(B + 'ch/churchill.png').convert('RGBA'); CH = CH.crop(CH.getchannel('A').getbbox())
CH = Image.merge('RGBA', [*ImageEnhance.Color(CH.convert('RGB')).enhance(0.75).split(), CH.getchannel('A')])
def portrait(im, t, t0, t1, img, name, x=60, h=560):
    if t < t0 or t > t1 + 0.25: return
    k = eout((t - t0) / 0.3) * (1 - eout((t - t1) / 0.25)); g = img.resize((int(img.width * h / img.height), h), Image.LANCZOS)
    g = ImageEnhance.Contrast(ImageOps.grayscale(g.convert('RGB'))).enhance(1.2).convert('RGBA') if False else g
    a = g.getchannel('A').point(lambda v: int(v * k)); g.putalpha(a); y = 1560 - h + int(60 * (1 - k))
    sh = Image.new('RGBA', g.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.6))); im.alpha_composite(sh, (x + 10, y + 14)); im.alpha_composite(g, (x, y))
    label(im, t, t0 + 0.15, name, (x + g.width // 2, 1545), 38, WHITE, box=(14, 14, 16))
from PIL import ImageOps
TOB = (23.96, 32.08); GAZ_N = (23.3, 32.17); BIRH = (23.48, 31.6); ELADEM = (23.92, 31.85); ALAM = (28.95, 30.83); BREACH = (24.08, 31.97); KX = (23.98, 32.03)
T0H = K('Ein Jahr zuvor') - 0.25
def tc(t, k, lon=23.98, up=400): return (t, lon, 32.08 - up / (1.18 * k), k)
CAM[:] = [(T0H, 25.0, 32.2, 120), tc(K('dieselbe Festung'), 260, 24.0), tc(K('Juni 1942:'), 260, 24.0), (K('Bei Gazala'), 23.7, 31.75, 520), (K('Churchill befahl') - 0.7, 23.7, 31.75, 520), tc(K('Churchill befahl'), 1500, 23.95),
          tc(K('Am 20. Juni'), 2100, 24.0), tc(K('Am Abend brannte'), 2600), tc(K('Am nächsten Morgen'), 2600, up=230), tc(K('Hitler ernannte'), 2600, up=230), tc(K('Mit dem erbeuteten'), 1100), (K('Mit dem erbeuteten') + 1.8, 26.5, 31.4, 120), (K('Heute liegen'), 26.5, 31.4, 120), tc(K('Ehrenmal bei Tobruk,'), 900, 23.96, 180), tc(T_END, 950, 23.96, 180)]
def frame(t):
    if t < T0H:
        im = fullfilm('pows', t, 0)
        say(im, t, [[(K('Warum ergaben'), 'WARUM', 'y'), (K('ergaben sich'), 'ERGABEN SICH', 'w')]], y0=330, size=96)
        counter(im, t, K('fast 33.000'), 33000, lambda v: de(v), (W / 2, nx(330, 96)), 230, YEL, 0.7)
        say(im, t, [[(K('alliierte Soldaten'), 'ALLIIERTE SOLDATEN', 'w')]], y0=nx(nx(330, 96), 230), size=96)
        say(im, t, [[(K('nach nur'), 'NACH NUR', 'w'), (K('einem Tag'), '1 TAG', 'r')], [(K('Kampf?'), 'KAMPF?', 'w')]], y0=nx(nx(nx(330, 96), 230), 96), size=96)
        return im.convert('RGB')
    if K('Hitler ernannte') <= t < K('Mit dem erbeuteten'):
        im = fullfilm('rommel', t, K('Hitler ernannte'), 1.05, 1.15)
        say(im, t, [[(K('Hitler ernannte'), 'HITLER ERNENNT', 'w')], [(K('Rommel zum'), 'ROMMEL', 'y')], [(K('zum Generalfeldmarschall.', 1), 'GENERALFELDMARSCHALL', 'r')]], y0=330, size=110)
        return im.convert('RGB')
    im = basemap2(t); p = P(t); pt = p(*TOB)
    if not (K('Für Südafrika') <= t < K('Hitler ernannte')): label(im, t, T0H + 0.2, 'TOBRUK', (pt[0], pt[1] - 60), 46, WHITE, box=(14, 14, 16)); pin(im, t, T0H, pt, WHITE, 12)
    if t < K('Juni 1942:'):
        tag(im, t, T0H, '1941'); glowring(im, t, K('dieselbe Festung'), pt, 110)
        label(im, t, T0H + 0.2, 'LIBYEN', p(21.5, 30.6), 54, (90, 70, 40)); label(im, t, T0H + 0.2, 'ÄGYPTEN', p(28.5, 30.0), 54, (90, 70, 40)); label(im, t, T0H + 0.2, 'MITTELMEER', p(24.5, 33.6), 46, (150, 180, 230))
        say(im, t, [[(K('Ein Jahr zuvor'), 'EIN JAHR ZUVOR:', 'w')], [(K('fast acht Monate'), '8 MONATE', 'y'), (K('lang standgehalten.'), 'GEHALTEN', 'w')]], y0=430, size=100)
        card(im, t, K('Rommel fast'), K('Juni 1942:') - 0.25, 'rommel', box=(70, 1130, 840, 430))
    elif t < K('Bei Gazala'):
        tag(im, t, K('Juni 1942:'), 'JUNI 1942'); vscard(im, t, K('Juni 1942:'), K('Bei Gazala') - 0.25)
    elif t < K('Churchill befahl'):
        tag(im, t, K('Bei Gazala'), '26. MAI 1942', 'GAZALA')
        d = ImageDraw.Draw(im); q = [p(*GAZ_N), p(23.38, 31.9), p(*BIRH)]; d.line(q, fill=ALLY + (255,), width=12)
        label(im, t, K('Bei Gazala'), 'GAZALA-LINIE', (p(*GAZ_N)[0] - 10, p(*GAZ_N)[1] - 50), 40, WHITE, box=ALLY)
        arrow(im, t, K('britische Linie'), 1.4, p, [(22.6, 31.7), (22.9, 31.3), (23.6, 31.35), (23.9, 31.6), ELADEM], (24, 24, 26), 30)
        label(im, t, K('Linie im Süden'), 'ROMMEL', (p(22.9, 31.3)[0], p(22.9, 31.3)[1] + 70), 42, WHITE, box=(24, 24, 26))
        if t >= K('Von rund 850'):
            v = 850 if t < K('noch etwa 70') else max(70, 850 - (850 - 70) * eout((t - K('noch etwa 70')) / 0.9))
            counter(im, t, K('rund 850'), v, lambda x: '%d' % round(x), (W / 2, 430), 220, YEL, 0.01)
            say(im, t, [[(K('britischen Panzern'), 'BRITISCHE PANZER', 'w')]], y0=nx(430, 220), size=80)
            if t >= K('noch etwa 70'):
                for i in range(6): fire(im, (220 + i * 120, 1300 + (i % 2) * 70), t, 1.0)
                say(im, t, [[(K('einsatzbereit.'), 'EINSATZBEREIT', 'r')]], y0=nx(nx(430, 220), 80), size=80)
        else:
            say(im, t, [[(K('Bei Gazala'), 'GAZALA:', 'w'), (K('im Süden umgangen.'), 'UMGANGEN', 'y')]], y0=430, size=100)
    elif t < K('Am 20. Juni'):
        tag(im, t, K('Churchill befahl'), '14. JUNI 1942', 'TOBRUK HALTEN')
        perimeter(im, t, K('rund 50 Kilometer'), p)
        if t < K('Doch der rund'):
            portrait(im, t, K('Churchill befahl'), K('Doch der rund') - 0.2, CH, 'WINSTON CHURCHILL', 40, 640)
            say(im, t, [[(K('Churchill befahl'), 'CHURCHILL:', 'w')], [(K('Tobruk zu halten.'), '„HALTEN!“', 'r')]], y0=430, size=100)
        elif t < K('und der neue'):
            say(im, t, [[(K('rund 50 Kilometer'), '50 KM', 'y'), (K('lange Verteidigungsring'), 'RING', 'w')], [(K('war verfallen,', 1), 'VERFALLEN', 'r')]], y0=430, size=100)
            label(im, t, K('rund 50 Kilometer'), '50 KM', p(23.96, 31.94), 50, YEL)
        else:
            card(im, t, K('General Klopper,'), K('Am 20. Juni') - 0.25, 'klopper', box=(70, 1130, 840, 430))
            say(im, t, [[(K('General Klopper,'), 'GENERAL', 'w'), (K('General Klopper,', 1), 'KLOPPER', 'y')], [(K('erst seit'), 'ERST SEIT', 'w'), (K('einem Monat.', 1), '1 MONAT', 'r')]], y0=430, size=100)
    elif t < K('Am nächsten Morgen'):
        perimeter(im, t, K('Am 20. Juni') - 5, p)
        if t < K('Pioniere überbrückten'):
            tag(im, t, K('um 5:20'), '05:20', 'DER ANGRIFF'); say(im, t, [[(K('Am 20. Juni'), '20. JUNI', 'y')]], y0=430, size=100, until=K('bombardierten Stukas'))
            for i in range(5):
                u = clamp((t - K('bombardierten Stukas') - i * 0.15) / 1.4); s = (lerp(-120 + i * 40, p(*BREACH)[0] - 230 + i * 40, u), lerp(380 + i * 110, p(*BREACH)[1] - 140 + i * 50, u)); plane(im, s, 0.55, 1.3)
            if t > K('eine Ecke'): fire(im, p(*BREACH), t, 1.6)
            card(im, t, K('bombardierten Stukas'), K('Pioniere überbrückten') - 0.2, 'stukas', box=(70, 1150, 840, 410))
            say(im, t, [[(K('bombardierten Stukas'), 'STUKAS', 'r')], [(K('eine Ecke des Rings.'), 'AUF EINE ECKE', 'w')]], y0=430, size=100)
        elif t < K('Um 13 Uhr'):
            tag(im, t, K('Pioniere überbrückten'), '07:45', 'DURCHBRUCH')
            label(im, t, K('Pioniere überbrückten'), 'PANZERGRABEN', (p(*BREACH)[0] - 170, p(*BREACH)[1] + 70), 40, WHITE, box=(14, 14, 16))
            arrow(im, t, K('waren die deutschen'), 1.0, p, [(24.11, 31.88), BREACH, (24.03, 32.0)], (24, 24, 26), 34)
            card(im, t, K('waren die deutschen'), K('Um 13 Uhr') - 0.2, 'tanks', box=(70, 1230, 660, 330))
            say(im, t, [[(K('Pioniere überbrückten'), 'PIONIERE', 'w'), (K('den Panzergraben,'), 'ÜBER DEN GRABEN', 'y')], [(K('Panzer durch.'), 'PANZER DURCH', 'r')]], y0=430, size=100)
        elif t < K('Am Abend brannte'):
            tag(im, t, K('Um 13 Uhr'), '13:00'); arrow(im, t, K('Um 13 Uhr') - 3, 0.01, p, [(24.11, 31.88), BREACH, KX], (24, 24, 26), 34)
            pin(im, t, K('die Höhen'), p(*KX), YEL, 16); label(im, t, K('die Höhen'), 'KING\'S CROSS', (p(*KX)[0], p(*KX)[1] + 80), 42, WHITE, box=(14, 14, 16))
            say(im, t, [[(K('Um 13 Uhr'), 'DIE HÖHEN', 'y')], [(K('über der Stadt.'), 'ÜBER DER STADT', 'w')]], y0=430, size=100)
        else:
            tag(im, t, K('Am Abend brannte'), '18:00'); arrow(im, t, 0, 0.01, p, [(24.11, 31.88), BREACH, KX, (23.97, 32.07)], (24, 24, 26), 34)
            for i in range(4): fire(im, (pt[0] - 90 + i * 60, pt[1] + 10 + (i % 2) * 30), t, 1.3)
            card(im, t, K('brannte der Hafen.'), K('Am nächsten Morgen') - 0.2, 'harbour', box=(70, 1150, 840, 410))
            say(im, t, [[(K('Am Abend'), 'AM ABEND:', 'w')], [(K('brannte der Hafen.'), 'DER HAFEN BRENNT', 'r')]], y0=430, size=100)
    elif t < K('Hitler ernannte'):
        tag(im, t, K('Am nächsten Morgen'), '21. JUNI 09:40', 'KAPITULATION')
        stamp(im, t, K('kapitulierte Klopper.'), 'KAPITULATION', (W / 2, 520), 110)
        card(im, t, K('kapitulierte Klopper.'), K('Hitler ernannte') - 0.2, 'pows2', box=(70, 1000, 840, 540))
        if t >= K('Für Südafrika'): say(im, t, [[(K('die schwerste'), 'SCHWERSTE NIEDERLAGE', 'r')], [(K('seiner Geschichte.'), 'SÜDAFRIKAS', 'w')]], y0=680, size=90)
    elif t < K('Heute liegen'):
        tag(im, t, K('Mit dem erbeuteten'), 'JULI 1942')
        arrow(im, t, K('fuhr Rommel'), 1.5, p, [(24.2, 32.0), (25.2, 31.7), (27.2, 31.3), (28.85, 30.85)], (24, 24, 26), 30)
        pa = p(*ALAM); label(im, t, K('bei El Alamein'), 'EL ALAMEIN', (pa[0], pa[1] - 70), 46, WHITE, box=(14, 14, 16))
        stamp(im, t, K('gestoppt wurde.'), 'GESTOPPT', (pa[0] - 40, pa[1] + 90), 70)
        label(im, t, K('Mit dem erbeuteten'), 'ÄGYPTEN', p(27.4, 29.2), 54, (90, 70, 40))
        say(im, t, [[(K('Mit dem erbeuteten'), 'ERBEUTETER', 'w'), (K('Treibstoff fuhr'), 'TREIBSTOFF', 'y')], [(K('nach Ägypten,'), 'NACH ÄGYPTEN', 'w')]], y0=430, size=100)
        card(im, t, K('Mit dem erbeuteten'), K('nach Ägypten,') + 0.6, 'fuel', box=(70, 1050, 840, 480))
    else:
        tag(im, t, K('Heute liegen'), 'HEUTE')
        counter(im, t, K('über 6.000'), 6000, lambda v: 'ÜBER ' + de(v), (W / 2, 430), 160, YEL)
        say(im, t, [[(K('deutsche Gefallene'), 'DEUTSCHE GEFALLENE', 'w')], [(K('in einem Ehrenmal'), 'IN EINEM EHRENMAL', 'w')], [(K('wie eine Festung'), 'WIE EINE FESTUNG', 'y')]], y0=nx(430, 160), size=72)
        if t >= K('Ehrenmal bei Tobruk,'):
            d = ImageDraw.Draw(im); c = p(23.93, 31.86); s = 60
            d.rectangle((c[0] - s, c[1] - s, c[0] + s, c[1] + s), fill=(120, 100, 70, 255), outline=WHITE + (255,), width=4)
            for dx in (-s, s):
                for dy in (-s, s): d.rectangle((c[0] + dx - 16, c[1] + dy - 16, c[0] + dx + 16, c[1] + dy + 16), fill=(120, 100, 70, 255), outline=WHITE + (255,), width=3)
            label(im, t, K('Ehrenmal bei Tobruk,'), 'DEUTSCHES EHRENMAL', (c[0], c[1] + 120), 42, WHITE, box=(14, 14, 16))
    return im.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'T': print(round(T_END, 3)); sys.exit()
    if sys.argv[1] == 'p':
        ts = [float(x) for x in sys.argv[3:]]; Pc = Image.new('RGB', (270 * len(ts), 480))
        for i, tt in enumerate(ts):
            im = frame(tt); ImageDraw.Draw(im).text((20, 20), '%.2f' % tt, font=font('Anton', 60), fill=(255, 0, 255)); Pc.paste(im.resize((270, 480)), (i * 270, 0))
        Pc.save(B + 'sh/' + sys.argv[2], quality=85); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
    for n in range(int(round(a * FPS)), int(round(b * FPS))): pr.stdin.write(np.asarray(frame(n / FPS)).tobytes())
    pr.stdin.close(); pr.wait(); print('rc', pr.returncode)
