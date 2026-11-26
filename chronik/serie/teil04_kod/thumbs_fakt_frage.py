import sys; sys.argv = ['x']
src = open('th_serie.py').read().split('J = [')[0]
src = (src.replace("font=font('Anton', 520), fill=255, anchor='mm')", "font=font('Anton', 400), fill=255, anchor='mm')")
          .replace("ImageDraw.Draw(M).text((TW / 2, 395), year", "ImageDraw.Draw(M).text((TW / 2, 405), year")
          .replace("text(can, (TW / 2, 30), title, fit_font('Anton', title, 890, 96)", "text(can, (TW / 2, 100), title, fit_font('Anton', title, 1160, 128)"))
exec(src)
exec(open('/home/user/Brnkry/chronik/serie/teil04_kod/thumbs_stil_serie_personen.py').read().split('P = {')[0].split("exec(open('th_serie.py')")[1].split('\n', 1)[1])
def plate(c, s):
    f = fit_font('Anton', s, 1060, 108); d = ImageDraw.Draw(c); y = 622; b = d.textbbox((TW / 2, y), s, font=f, anchor='mm'); px, py = 28, 12
    d.rectangle((b[0] - px, b[1] - py, b[2] + px, b[3] + py), fill=(244, 196, 22)); d.text((TW / 2, y), s, font=f, fill=(14, 14, 16), anchor='mm')
    d.rectangle((b[0] - px, b[3] + py + 6, b[0] - px + 170, b[3] + py + 14), fill=(200, 22, 26))
SS = '/home/user/Brnkry/chronik/serie/'
J = [(1, '1933', 'OHNE PANZER, OHNE GELD', 't1_brand.jpg', [('rede_c', 520, 470), ('chamberlain', 505, 870)], 'WIE KAM ES ZUM KRIEG?', SS + 'lang/thumbnails/Teil1_D_Ohne_Panzer_ohne_Geld.jpg'),
     (2, '1939', 'VON ZWEI SEITEN ÜBERFALLEN', 't2_brand.jpg', [('t2_panzer', 620, 650)], 'WIE FIEL POLEN IN 5 WOCHEN?', SS + 'teil02/thumbnails/Teil2_D_Zwei_Seiten_Fuenf_Wochen.jpg'),
     (3, '1940', 'IN SECHS WOCHEN BESIEGT', 't3_duenk.jpg', [('manstein', 520, 470), ('degaulle_c', 510, 880)], 'WIE FIEL FRANKREICH SO SCHNELL?', SS + 'teil03/thumbnails/Teil3_D_Sechs_Wochen_besiegt.jpg'),
     (4, '1940', '57 NÄCHTE BOMBEN AUF LONDON', 'london_fire.jpg', [('dowding', 460, 340), ('galland', 470, 960), ('churchill_c', 490, 650)], 'WARUM FIEL ENGLAND NICHT?', SS + 'teil04/thumbnails/Teil4_D_57_Naechte.jpg')]
for n, y, title, bg, fg, q, out in J:
    c = C(n, y, title, bg, 0.5, 0.4)
    for nm, h, cx in fg: put(c, nm, h, cx)
    vign(c); text(c, (TW / 2, 100), title, fit_font('Anton', title, 1160, 128), (240, 240, 240), 'mt', shadow=5); plate(c, q); logo(c); badge(c, 36, 28, 'TEIL %d' % n); c.convert('RGB').save(out, quality=95); print(n, flush=True)
