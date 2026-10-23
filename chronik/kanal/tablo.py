# channel inventory from the YouTube Studio screenshots (18.10.2026): every video with topic, nation, branch, views
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from collections import defaultdict
# (date, title/person, format, nation, branch, topic, views or None if hidden in the screenshot, comments)
V = [
 ('2026-10-18','Eino Luukkanen','Short','Finnland','Luftwaffe (Jagd)','Jagdflieger',439,1),
 ('2026-10-17','Adalbert Schnee','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',30656,18),
 ('2026-10-17','Franz Stigler und Charlie Brown','Short','Deutschland / USA','Luftwaffe (Jagd)','Jagdflieger / Bomber',4715,7),
 ('2026-10-16','Josef Kammhuber','Short','Deutschland','Luftwaffe (Nachtjagd)','Kommandeur / Technik',18399,11),
 ('2026-10-12','Erich Hartmann (lang)','Lang','Deutschland','Luftwaffe (Jagd)','Jagdflieger',2763,3),
 ('2026-10-06','Heinz Bär','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',67181,68),
 ('2026-09-29','Sabiha Gökçen','Short','Türkei','Luftwaffe (Kampf)','Pilotin',14704,18),
 ('2026-09-28','Hans Philipp','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',49535,47),
 ('2026-09-27','Adriano Visconti','Short','Italien','Luftwaffe (Jagd)','Jagdflieger',39228,44),
 ('2026-09-25','Frederic John Walker','Short','Großbritannien','Marine (Überwasser)','U-Jagd',11933,9),
 ('2026-09-21','Schlachtschiff Scharnhorst','Short','Deutschland','Marine (Überwasser)','Schiff',8039,4),
 ('2026-09-19','Isoroku Yamamoto','Short','Japan','Marine (Überwasser)','Admiral / Stratege',53917,39),
 ('2026-09-19','Ernst Lindemann (Bismarck)','Short','Deutschland','Marine (Überwasser)','Schiffskommandant',178748,76),
 ('2026-09-10','Heinrich Lehmann-Willenbrock (lang)','Lang','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',11526,3),
 ('2026-09-09','Erich Rudorffer','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',35271,61),
 ('2026-09-0?','Loyce Edward Deen','Short','USA','Marine (Flieger)','Pilot / Seebestattung',None,10),
 ('2026-09-03','Reinhard Hardegen','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',179802,133),
 ('2026-08-30','Günther Rall','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',58510,None),
 ('2026-08-18','William Hart Pitsenbarger','Short','USA','Luftwaffe (Rettung)','Vietnamkrieg / Sanitäter',14798,19),
 ('2026-08-12','Messerschmitt Me 262','Short','Deutschland','Luftwaffe (Technik)','Flugzeug',293641,276),
 ('2026-08-05','Hans-Ulrich Rudel','Short','Deutschland','Luftwaffe (Sturzkampf)','Stuka-Pilot',121240,175),
 ('2026-08-04','George Beurling','Short','Kanada','Luftwaffe (Jagd)','Jagdflieger',9452,8),
 ('2026-08-02','Junkers Ju 87 Stuka','Short','Deutschland','Luftwaffe (Technik)','Flugzeug',923173,961),
 ('2026-07-2?','Josef Priller','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',None,144),
 ('2026-07-28','Carlo Fecia di Cossato','Short','Italien','Marine (U-Boot)','U-Boot-Kommandant',49773,48),
 ('2026-07-23','Max Wünsche','Short','Deutschland','Heer (Panzer)','Panzerkommandeur',352809,None),
 ('2026-07-23','Herbert Schultze','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',185269,88),
 ('2026-07-21','Walter Nowotny','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',137253,97),
 ('2026-07-18','Günther Lützow','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',135520,114),
 ('2026-07-14','Heinrich Lehmann-Willenbrock','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',471912,224),
 ('2026-07-12','Werner Mölders','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',200072,136),
 ('2026-07-1?','Gerhard Barkhorn','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',None,80),
 ('2026-07-08','Joachim Schepke','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',106298,64),
 ('2026-07-06','Adolf Galland','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',251947,None),
 ('2026-07-05','Johannes Steinhoff','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger / NATO',468170,553),
 ('2026-07-04','Albrecht Brandi','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',None,None),
 ('2026-07-03','Franz Bäke','Short','Deutschland','Heer (Panzer)','Panzerkommandeur',None,None),
 ('2026-07-02','Erich Topp','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',131655,56),
 ('2026-07-01','Douglas Bader','Short','Großbritannien','Luftwaffe (Jagd)','Jagdflieger',49204,49),
 ('2026-06-29','Hermann Graf','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',88582,60),
 ('2026-06-28','Hans Wind','Short','Finnland','Luftwaffe (Jagd)','Jagdflieger',31617,26),
 ('2026-06-26','Hans-Joachim Marseille ("Stern von Afrika")','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',53691,None),
 ('2026-06-2?','Erich Hartmann','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',None,None),
 ('2026-06-20','Wolfgang Lüth','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',181705,102),
 ('2026-06-19','Lauri Törni','Short','Finnland / Deutschland / USA','Heer (Infanterie)','Soldat / Spezialeinheit',None,None),
 ('2026-06-18','Franz von Werra','Short','Deutschland','Luftwaffe (Jagd)','Flucht / Gefangenschaft',281567,293),
 ('2026-06-17','Simo Häyhä','Short','Finnland','Heer (Infanterie)','Scharfschütze',36534,28),
 ('2026-06-16','Kurt Bühligen','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',302037,96),
 ('2026-06-16','Michael Wittmann (Winniza)','Short','Deutschland','Heer (Panzer)','Panzerkommandant',428355,257),
 ('2026-06-15','Hermann von Oppeln-Bronikowski','Short','Deutschland','Heer (Panzer)','Panzerkommandeur / Olympia',102187,97),
 ('2026-06-14','Ilmari Juutilainen','Short','Finnland','Luftwaffe (Jagd)','Jagdflieger',204160,55),
 ('2026-06-11','Helmut Lent','Short','Deutschland','Luftwaffe (Nachtjagd)','Nachtjäger',61945,55),
 ('2026-06-0?','Michael Wittmann','Short','Deutschland','Heer (Panzer)','Panzerkommandant',None,131),
 ('2026-06-07','Otto Carius','Short','Deutschland','Heer (Panzer)','Panzerkommandant',277020,162),
 ('2026-06-05','Hans Dammers','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',110552,25),
 ('2026-06-04','Theodor Weissenberger','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',149038,69),
 ('2026-06-03','Joachim Peiper','Short','Deutschland','Heer (Panzer)','Panzerkommandeur',134713,141),
 ('2026-06-02','Heinrich Ehrler','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',184104,176),
 ('2026-05-31','Otto Kittel','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',78069,46),
 ('2026-05-30','Johannes Bölter','Short','Deutschland','Heer (Panzer)','Panzerkommandant',60720,37),
 ('2026-05-2?','Helmut Wick','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',None,52),
 ('2026-05-24','Heinz-Wolfgang Schnaufer','Short','Deutschland','Luftwaffe (Nachtjagd)','Nachtjäger',60019,48),
 ('2026-05-21','Günther Prien','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',107870,185),
 ('2026-05-14','Egon Mayer','Short','Deutschland','Luftwaffe (Jagd)','Jagdflieger',371103,276),
 ('2026-05-11','Otto Kretschmer','Short','Deutschland','Marine (U-Boot)','U-Boot-Kommandant',142137,55),
 ('2026-05-10','Erwin Rommel','Short','Deutschland','Heer (Führung)','General',7769,13),
 ('2026-05-09','Kurt Knispel','Short','Deutschland','Heer (Panzer)','Panzerkommandant',205618,None),
]
def grp(i): return V[i]
H = ['Datum', 'Person / Thema', 'Format', 'Land', 'Waffengattung', 'Rolle', 'Aufrufe', 'Kommentare']
wb = Workbook(); ws = wb.active; ws.title = 'Alle Videos'
hdr = PatternFill('solid', fgColor='0E0F12'); yel = PatternFill('solid', fgColor='F4C70F')
ws.append(H)
for c in ws[1]: c.font = Font(bold=True, color='F4C70F'); c.fill = hdr
for v in V: ws.append(list(v))
for i, w in enumerate([12, 42, 8, 26, 24, 26, 12, 12], 1): ws.column_dimensions[get_column_letter(i)].width = w
for r in ws.iter_rows(min_row=2, min_col=7, max_col=7):
    for c in r: c.number_format = '#,##0'
ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions
def summary(name, key):
    s = wb.create_sheet(name); s.append([name, 'Videos', 'Aufrufe (bekannt)', 'Ø Aufrufe']); [setattr(c, 'font', Font(bold=True, color='F4C70F')) or setattr(c, 'fill', hdr) for c in s[1]]
    agg = defaultdict(lambda: [0, 0, 0])
    for v in V:
        k = key(v); agg[k][0] += 1
        if v[6]: agg[k][1] += v[6]; agg[k][2] += 1
    for k, (n, tot, known) in sorted(agg.items(), key=lambda x: -x[1][1]):
        s.append([k, n, tot, round(tot / known) if known else None])
    s.column_dimensions['A'].width = 30
    for col in 'BCD': s.column_dimensions[col].width = 18
    for r in s.iter_rows(min_row=2, min_col=3, max_col=4):
        for c in r: c.number_format = '#,##0'
summary('Waffengattung', lambda v: v[4].split(' (')[0])
summary('Bereich', lambda v: v[4])
summary('Land', lambda v: v[3])
top = wb.create_sheet('Top 15'); top.append(['Platz'] + H); [setattr(c, 'font', Font(bold=True, color='F4C70F')) or setattr(c, 'fill', hdr) for c in top[1]]
for i, v in enumerate(sorted([v for v in V if v[6]], key=lambda v: -v[6])[:15], 1): top.append([i] + list(v))
top.column_dimensions['C'].width = 42
for r in top.iter_rows(min_row=2, min_col=8, max_col=8):
    for c in r: c.number_format = '#,##0'
wb.save('Kanal_Inhalte.xlsx')
# console summary for the chat
print(len(V), 'videos')
for name, key in (('Gattung', lambda v: v[4].split(' (')[0]), ('Bereich', lambda v: v[4]), ('Land', lambda v: v[3])):
    agg = defaultdict(lambda: [0, 0, 0])
    for v in V:
        k = key(v); agg[k][0] += 1
        if v[6]: agg[k][1] += v[6]; agg[k][2] += 1
    print('--', name)
    for k, (n, tot, kn) in sorted(agg.items(), key=lambda x: -x[1][1]): print(f'{k:32s} {n:3d} {tot:>10,} avg {round(tot/kn) if kn else 0:>9,}')
