# Teil 3: Der Krieg im Westen — uzun video planı (dergi düzeni)

Biçim Teil 2 ile aynı: `teil02_kod/teil2b.py` motoru (dergi, sayfa çevirme, çerçevede arşiv filmi, `lmap`/`drawings2` haritaları). Seslendirme Teil 2 ile aynı ses ve ayarlarla, `[quickly reads]` YOK, hız kesilmez; sadece uzun duraklamalar kısaltılır. Sayfa geçişi: anlatım bitince yaklaşık 0,5 s, sonra sayfa döner.

Senaryo: `teil03_script_de.txt` (1340 kelime, Teil 2 ile aynı uzunluk, tahminen 10–11 dk). 22 paragraf.

## Kaynak kısaltmaları (indirme: scratchpad `t3/dl/`, fotoğraflar `t3/ba/`)
- **dac**: Why We Fight 3, "Divide and Conquer" (Frank Capra, US Army 1943, kamu malı, 56 dk). Norveç, Hollanda, Rotterdam, Belçika, Maginot, Dunkerque, Paris, Compiègne. Animasyonlu haritalar (Disney) da var.
- **u492 / u497**: UfA-Tonwoche 492 (7.2.1940) ve 497 (13.3.1940): Sitzkrieg dönemi, Westwall tatbikatı, İngiliz esirler.
- **u504**: UfA-Tonwoche 504 (3.5.1940): Norveç cephesi, **Oscarsborg kalesinde Alman askerleri**, Westwall.
- **u507**: UfA-Tonwoche 507 (22.5.1940): paraşütçüler, Rotterdam, Hollanda'nın teslimi, Liège kaleleri.
- **u508**: UfA-Tonwoche 508 (29.5.1940): Narvik (0:00–3:44), Stuka ve hava saldırıları (3:45), Anvers (8:37), Leuven (13:55) …
- **u509**: UfA-Tonwoche 509 (5.6.1940): Dunkerque dönemi.
- **w511**: Deutsche Wochenschau 511 (20.6.1940): Paris'e giriş.
- **w512**: Deutsche Wochenschau 512 (26.6.1940, 44 dk): Maginot hattının yarılması, Verdun, tank savaşları, Hitler ve generaller, Paris geçidi, **Compiègne imzası**.
- **castle**: Castle Films "Battle for France" (ABD, 1940): Dunkerque gemileri ve kıyı (1:23–2:49), Paris bombardımanı, mülteciler (6:21–7:04).
- **fb56**: US War Dept Film Bulletin 56 (ele geçirilmiş Alman filmi): Eben-Emael alev silahı ve patlayıcı, Maas geçişi, Kanal'a varış, Dunkerque enkazı, İngiliz esirler, Paris.
- **compiegne**: "La France se rend, 22 juin 1940" (4 dk).
- **paris**: Hitler'in Paris turu (1,5 dk).
- **ba**: Bundesarchiv fotoğrafları (aşağıda imzalarla). **cm**: Wikimedia Commons (Churchill, Reynaud, de Gaulle, Haakon VII, Wilhelmina, Dunkerque IWM fotoğrafları, Bletchley Park, Enigma).

Gamalı haç ve bayraklar: küçük ve tam yerinde bulanık (Compiègne'deki Reichskriegsflagge, Paris'teki bayrak, uçak kuyrukları). Hitler görünebilir.

## Sayfa sayfa plan
| # | Senaryo bölümü | Sayfa düzeni | Görüntü |
|---|---|---|---|
| 0 | Giriş: Fransa'nın daha çok tankı vardı… aynı vagon | Kapak: "DER KRIEG IM WESTEN", "Teil 3". Sağda büyük çerçeve. Altta iki sütun: "Frankreich 3.384 Panzer" / "Wehrmacht 2.445 Panzer" | w512 Compiègne vagonu, ba 183-L05360 (vagon), dac Fransız tankları |
| 1 | drôle de guerre / Phoney War / Sitzkrieg | Üç dilde aynı kavram, üç etiket yan yana. Maginot kesit çizimi (drawings2) | ba 121-0485/-0486, 183-B17024 (kubbe), 183-S53854 (Westwall), u492/u497, dac Maginot |
| 2 | Flugblätter yerine bomba yok, BEF Fransa'da, "zaman bizden yana" | Sol: uçuşan broşürler (kod animasyonu), sağ: BEF | cm BEF 1939, cm Phoney War, ba 183-L15658 |
| 3 | Hitler Ekim 1939'da saldırı ister, erteleme, 1914 benzeri plan | Harita: Schlieffen benzeri ok Belçika üzerinden (gri) | lmap Batı Avrupa, ba 101I-123-0177-20A |
| 4 | Mechelen olayı 10.1.1940, Reinberger | Gazete kesiği gibi kutu: "10. Januar 1940, Maasmechelen". Yanmış kâğıt efekti | cm Mechelen incident (uçak enkazı), kod: yanan kâğıt |
| 5 | Manstein planı, Ardennen, 17.2.1940 | Harita: ikinci ok Ardenler üzerinden (kırmızı), "Manstein" portresi | cm Manstein, ba 101I-382-0248-32A (ormanda Panzer) |
| 6 | Kuzey: İsveç demiri, mayın planı, 9.4.1940 Weserübung, Danimarka | Harita: Narvik demir yolu, oklar Oslo–Bergen–Trondheim–Narvik; Danimarka | ba 101I-754-0051N-28, 146-1980-078-06A (Kopenhag), 101II-MN-1007-37, 183-L21356 (filo) |
| 7 | Blücher, Oscarsborg, Kral Haakon ve altın, Narvik 10 muhrip | Sol: Oscarsborg (u504 + ba 134-D062/-D067), sağ: Blücher (134-B4218); Narvik krokisi 134-C2115 | u508 0:00–3:44 Narvik, ba 134-C2593, 101II-MW-5618-16 (batık gemiler), cm Haakon VII |
| 8 | 10 Mayıs: Hollanda, Belçika, Lüksemburg; Chamberlain çekilir, Churchill | Tarih büyük: "10. MAI 1940". İki portre: Chamberlain → Churchill | ba 183-L11297, 146-1975-020-20A (Lüksemburg sınırı), 183-H12959 (Chamberlain), cm Churchill |
| 9 | Paraşütçüler, Eben-Emael, 780 Belçikalı teslim | Çizim: kale kesiti + planörler üstte | ba 183-S61243, 183-S61241, 183-L05069, 146-1974-113-59; fb56 Eben-Emael; u507 Ju 52 |
| 10 | Müttefikler Belçika'ya ilerler: tuzak | Harita: mavi oklar kuzeye, kırmızı ok Ardenler'de bekliyor | dac haritası, ba 146-1984-093-23 (Maastricht) |
| 11 | Rotterdam 14 Mayıs, 850 ölü, 80.000 evsiz, teslim | Siyah sayfa, tek büyük fotoğraf; rakamlar tek tek | ba 146-1984-021-14, 146-2005-0003, 116-483-032, 146-1984-021-17 (teslim); dac Rotterdam |
| 12 | Ardenler'de trafik, keşif, Sedan 13 Mayıs, Maas | Harita yakın: Sedan; sağda ponton köprü | ba 101I-382-0248-33A, RH 82 Bild-00165/-00164 (13.5.1940), 146-1978-062-24 (Floing ponton), 146-1971-088-63; fb56 Maas geçişi; u508 Stuka |
| 13 | Pervitin, 35 milyon tablet | Küçük kutu sayfa: tablet tüpü çizimi + "35.000.000" | cm Pervitin tüpü |
| 14 | Kanal'a dönüş, Rommel, Gespensterdivision, Abbeville 20 Mayıs, Reynaud "Wir sind geschlagen" | Harita: kırmızı ok Kanal'a, "Sichelschnitt" etiketi kullanılmıyor (dönemin resmi adı değil, sonradan yaygınlaştı) | ba 146-1998-043-20A, 146-1972-045-02 (Rommel), 101I-126-0329-05 (Abbeville), cm Reynaud |
| 15 | Dunkerque'ye çekilme, 24 Mayıs Haltbefehl, Rundstedt | Harita: cep küçülüyor; "HALT" damgası | ba 101I-769-0229-10A (Guderian), cm Rundstedt |
| 16 | Operation Dynamo, 338.226, Belçika teslim, Churchill sözü | Büyük rakam sayacı 0 → 338.226 | castle 1:23–2:49, dac Dunkerque, cm IWM Dunkerque; ba 116-483-081, -084, 101II-MW-1160-18/-38 |
| 17 | Askerler kurtuldu; Bletchley Park, Enigma (Teil 2'ye bağ) | Sayfa: Enigma makinesi fotoğrafı + Teil 2'deki Polonyalı matematikçilere geri dönüş | cm Bletchley Park, cm Enigma |
| 18 | 5 Haziran ikinci faz, İtalya, mülteciler, Paris 14 Haziran | Mülteci kolonları; Paris haritası | ba 101I-749-0016-11, 101I-127-0371-09A, castle 6:21–7:04 (mülteciler), ba 183-L11769, 101I-126-0346-34A; w511 |
| 19 | Reynaud istifa, Pétain, de Gaulle BBC | İki portre karşılıklı: Pétain / de Gaulle; mikrofon | cm Pétain 1940, cm de Gaulle BBC; ba 183-L06528 (Berlin'de haber) |
| 20 | Compiègne: vagon, Foch'un yeri, 22 Haziran, Fransa ikiye bölünür, esirler, 27.000 ölü | Harita: işgal/Vichy bölgeleri; vagon fotoğrafı | w512 son bölüm, compiegne, ba 183-L05360, B 145 Bild-P50284/-P50287, 183-1982-0809-503, 146-1982-089-18, 183-M1112-500; esirler 121-0623, 183-B15308 |
| 21 | 23 Haziran Hitler Paris'te, çanlar | Tek büyük fotoğraf: Eyfel Kulesi | ba 183-H28708, paris filmi |
| 22 | Kapanış: altı hafta / dört yıl, İngiltere yalnız, Luftwaffe | Son sayfa: "FORTSETZUNG FOLGT · TEIL 4" | dac Kanal, kıyı; Teil 4 başlığı (önerim: "Die Luftschlacht um England") |

## Teil 2'den bilinen kurallar
- Bayrak ve gamalı haçlar her karede tek tek kontrol edilip bulanıklaştırılacak.
- Haritalar Almanca yer adlarıyla, tarihler sayfa köşesinde.
- Teil 2'deki gibi bölümlü açıklama (kapitel süreleri render sonrası).
