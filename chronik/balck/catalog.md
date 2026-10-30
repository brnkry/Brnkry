# Balck asset catalog

All boxes are `x0,y0,x1,y1` in ORIGINAL pixels of the file (for the video: 3840x2160 source pixels unless marked "@1920", which are coordinates in the extracted `clip/` frames; multiply by 2 for source).

Folders: `drive/` untouched originals. `clip/f0001.jpg..f0939.jpg` = every video frame at 1920x1080 (frame n starts at t=(n-1)/30 s). `g/bNN.jpg` = full photo with labelled 200 px grid. `z/` = zoom verification crops (`z/V_*` have the final tight swastika box drawn in red). `chk/sheet.jpg` = all photos, `chk/clip_sheet.jpg` = first/mid/last frame of every video segment, `chk/clip_every10_a/b.jpg` = every 10th frame, `chk/clip_cut_candidates.jpg` = frames around each cut, `chk/clip_framediff.txt` = per-frame difference scores.

## General warnings

* **Every photo is a re-processed file**: the Drive names all end in `_2K_20261022HHMMSS`, i.e. they were all pushed through an AI upscaler/colorizer on 22 Oct 2026. Colours are invented, fine detail (faces, insignia) may have been redrawn by the model. Treat insignia shapes as "probably what the original shows", not as evidence.
* **No Hitler found in any photo or in the video. Nothing needs EXCLUDE for Hitler.**
* The video contains **Joseph Goebbels** (party uniform with swastika armband) in segment S12. Not Hitler, but a top Nazi; decide editorially.
* **Duplicate:** `b25.jpg` and `b26.jpg` are byte identical (md5 `725e00cc430cb449bbd9cc97bc884e0f`). Use only one.
* Not a duplicate, but same man and same style: b16 / b24 / b27 (general portraits), and b07 / b09 / b21 right man (gaunt field look).

## Photo table (summary)

| file | size | Balck? | Balck face box | others | period | flags |
|---|---|---|---|---|---|---|
| b01 | 1792x2400 | probably NO | (KC officer face 450,640,640,920) | KC officer with goggles, NCO in shirt, soldier at right | WW2 summer, field, motorcycle | **AI-generated suspect** (Drive name `a_photo_grouping_of_1` looks like a generator prompt); unverifiable |
| b02 | 2752x1536 | YES | 1040,450,1440,860 | crowd of young soldiers | WW2 (late war, general rank) | upscaled |
| b03 | 2048x2048 | YES (old man, right) | 560,770,830,1310 | younger man in suit with lapel pin, left (filename says Mellenthin, but man looks ~50, Mellenthin b.1904 would be 70+) | post-war (1970s-80s) | identity of left man **unverifiable** |
| b04 | 2048x2048 | YES (very old) | 1100,450,1700,1600 | none | post-war (filename: "few days before [death]", c.1982) | upscaled |
| b05 | 2400x1792 | YES (left, KC) | 400,490,720,830 | 3 officers; filename: Horst von Mellenthin (brother of F.W.) | WW2 winter (Eastern Front) | chalk graffiti "ZOSKE" on wall |
| b06 | 2400x1792 | YES (right, side cap) | 1430,455,2100,1030 | back of a man in brown cap, civilian women | WW2 (inspection, filename) | |
| b07 | 1792x2400 | YES (filename "Balck02") | 480,270,1170,1120 | none | WW2, general rank (gold oak collar), KC + EK1 | |
| b08 | 1792x2400 | YES (filename) | 470,980,1540,1820 (cap to 330) | none | WW2, General der Panzertruppe era (Oak Leaves + Swords) | very clean, **heavily AI-retouched face** |
| b09 | 1792x2400 | YES (filename "Balck07") | 370,455,1270,1240 | none | WW2 (Oberst rank litzen, c.1941-42) | |
| b10 | 2400x1792 | NO | - | German soldiers/officer surrendering, hands up | 1945 Budapest | file is "BalckinBuda" article image, no Balck |
| b11 | 2400x1792 | NO | - | knocked-out Sherman (Soviet lend-lease), bodies, house | 1945 Hungary | |
| b12 | 2752x1536 | NO | - | Waffen-SS crew (camo smocks) at Pak 40, ruins | 1945 Hungary | |
| b13 | 2400x1792 | NO | - | Soviet soldiers with Maxim MG, T-34 with tank riders | 1945 (Soviet side) | no German insignia |
| b14 | 2400x1792 | YES (profile) | 760,350,1620,1210 | blurred heads in foreground left/right | WW2 general (Oak Leaves + Swords) | |
| b15 | 2400x1792 | UNCERTAIN | general 3rd from left: 1440,450,1720,740 | filename "F.W. von Mellenthin, Bobby Woll": man in black SS uniform = Woll (SS runes), general = Mellenthin per filename (looks a lot like Balck); 2 Heer men | WW2 1944, table with drinks | identity **unverifiable** |
| b16 | 1536x2752 | YES | 400,240,1470,1420 | none | WW2 general | **AI-look** (very smooth skin, intense eyes) |
| b17 | 2400x1792 | POSSIBLY (right general) | 1878,300,2118,566 | filename: Graf Strachwitz, Sepp Dietrich, Oldwig von Natzmer; left smiling KC officer face 343,223,635,515; centre man seen from behind in light coat; young Oberleutnant with papers 1240,60,1440,330 | WW2 summer field | Balck not named in file; unverifiable |
| b18 | 1792x2400 | YES (close-up, peaked cap) | 310,880,1420,1740 | none | WW2 (Oberst era, KC) | |
| b19 | 2400x1792 | YES (left, smiling) | 830,640,1110,900 | Heinz Guderian (right, fur collar, profile) 1700,560,1900,840; soldiers at building | WW2 winter, Eastern Front (Cyrillic sign) | |
| b20 | 1792x2400 | YES (general, centre-left) | 386,772,635,1012 | Major Walter (black Panzer uniform, pointing) 943,720,1166,960; 3 officers behind | WW2 summer | |
| b21 | 2400x1792 | PROBABLY (right man with KC, head bowed) | 1520,330,1800,720 | middle officer reading map 617,430,960,823; soldier left | WW2 winter (Generalmajor, 1942-43) | which man is Balck is **uncertain** |
| b22 | 2400x1792 | UNCERTAIN (smiling man in black Panzer jacket?) | 800,0,1000,180 | soldier in helmet left, officer bending, crew on 2nd tank | WW2 summer, Panzer III column | filename only; unverifiable |
| b23 | 2400x1792 | YES (centre, smiling in open staff car) | 945,620,1090,735 | 2 officers behind, driver | WW2 summer, pine forest, camo car, plate "WH-..." | small face |
| b24 | 2400x1792 | YES (seated at map table) | 800,170,1230,660 | none | WW2 general, office | |
| b25 | 2752x1536 | NO | - | Panther tanks under foliage, crew, French villagers | 1944 France/Lorraine | = b26 |
| b26 | 2752x1536 | NO | - | identical to b25 | | **DUPLICATE of b25** |
| b27 | 1792x2400 | YES (close-up face) | 220,400,1430,1720 | none | WW2 general (Oak Leaves + Swords + Diamonds style KC) | |

## Swastikas in photos

Boxes are tight on the swastika (verified in `z/`). "Readable" = a viewer can recognise it as a swastika at full image size; "tiny" = sub-20 px, blurred or hidden, but technically there (still blur if strict).

### Clearly readable
| file | where | box | crop |
|---|---|---|---|
| b07 | breast eagle wreath | 708,1483,750,1525 | z/V_b07_breast.jpg |
| b08 | peaked cap eagle | 810,343,866,398 | z/V_b08_cap.jpg |
| b09 | breast eagle | 298,1836,338,1884 | z/V_b09_breast.jpg |
| b15 | general's gold breast eagle | 1511,859,1529,880 | z/V_b15_geneagle.jpg |
| b18 | peaked cap eagle | 822,310,882,368 | z/V_b18_cap.jpg |
| b20 | Major Walter, German Cross in Gold (right breast) | 1001,1278,1033,1308 | z/V_b20_germancross.jpg |
| b24 | breast eagle | 846,1006,876,1036 | z/V_b24_breast.jpg |
| b24 | Knight's Cross centre | 1031,887,1063,916 | z/V_b24_kc.jpg |
| b27 | Knight's Cross centre (bottom edge) | 862,2270,935,2342 | z/V_b27_kc.jpg |

### Tiny / unreadable (present or implied)
| file | where | box |
|---|---|---|
| b01 | KC officer breast eagle | 430,1055,470,1085 |
| b02 | Balck cap eagle | 1165,180,1190,205 |
| b05 | Balck breast eagle | 282,1025,300,1048 |
| b05 | Balck cap eagle | 500,305,520,325 |
| b05 | right officer cap eagle | 1925,305,1945,330 |
| b08 | breast eagle, swastika cut by bottom edge | 400,2370,445,2400 |
| b09 | side-cap eagle (hidden in fold) | 470,100,520,150 |
| b10 | officer cap eagle | 770,375,790,395 |
| b15 | left man breast eagle | 220,1290,250,1335 |
| b15 | right man breast eagle | 2075,760,2100,795 |
| b15 | SS belt buckle (Woll) | 990,1300,1060,1360 |
| b16 | breast eagle wreath | 220,2220,310,2320 |
| b17 | left officer breast eagle | 230,710,270,745 |
| b17 | right general breast eagle | 1855,860,1885,890 |
| b17 | right general cap eagle | 1870,85,1900,112 |
| b20 | Balck breast eagle | 460,1148,483,1168 |
| b20 | Balck cap eagle | 590,650,612,672 |
| b20 | left soldier German Cross | 95,978,123,1003 |
| b20 | middle soldier breast eagle | 715,950,745,975 |
| b21 | middle officer cap eagle | 915,240,935,270 |
| b23 | Balck cap eagle | 1000,590,1015,605 |
| b23 | officer behind, cap eagle | 785,600,800,612 |

### No swastika visible
b03, b04, b06 (cap eagle in profile, KC centre covered by oak leaves), b11, b12, b13, b14 (breast eagle cut at the frame, KC centre plain), b19 (cap eagles too small/blurred, none visible), b22, b25/b26. Knight's Cross centres in b01, b05, b07, b08, b09, b17, b18, b21 show no readable swastika.

## Text surfaces in photos

(F = flat/frontal, P = in perspective)

| file | surfaces |
|---|---|
| b01 | sky 0,0,1792,540 F (best) ; gravel ground 200,1950,1700,2400 P |
| b02 | blurred dark hair mass lower-left 50,1000,1000,1500 F (soft) ; train/sky strip top-right 1700,0,2752,120 F (thin) |
| b03 | black background top 0,0,2048,480 F ; black right side 1700,500,2048,1300 F |
| b04 | dark background top 0,0,2048,380 F ; blurred right 1650,300,2048,1100 F |
| b05 | wooden wall 600,80,1700,480 F (chalk "ZOSKE" at 900,190,1500,300 already there) |
| b06 | dark coat of man at left 0,900,900,1792 F (blurred) ; trees top 200,0,1400,250 F (busy) |
| b07 | sky left 0,0,430,900 F ; sky right 1300,0,1792,650 F |
| b08 | grey wall left 0,0,450,1700 F ; right 1450,0,1792,1600 F |
| b09 | dark foliage top-right 1250,0,1792,700 F (busy) ; uniform chest 0,2000,1792,2400 F |
| b10 | white wall/shutter top-left 0,0,550,800 F ; bright top-right 1950,0,2400,300 F |
| b11 | sky 0,0,1600,500 F ; snow ground 0,800,1100,1300 P |
| b12 | ground planks 0,1300,1300,1536 P ; ruined wall 600,40,1500,250 F (busy) |
| b13 | smoky sky 0,0,2400,450 F (best) |
| b14 | blurred background right 1850,0,2400,1792 F ; left 0,0,500,900 F |
| b15 | wall 0,0,2400,450 F ; tablecloth 1400,1250,2400,1792 P |
| b16 | top background 0,0,1536,200 F ; curtain left 0,0,400,1500 F |
| b17 | sky 0,0,2400,450 between heads F ; field right 1700,600,2400,900 P |
| b18 | sky left 0,0,330,1700 F ; bokeh right 1450,0,1792,1900 F |
| b19 | white building wall 0,0,2400,200 F (sign at 1580,60,1960,220) ; car roof 300,350,1000,700 P |
| b20 | sky top 0,0,1792,250 F (busy leaves) ; grass bottom 0,2000,800,2400 P |
| b21 | map paper 700,1200,1500,1792 P (curved) ; sky 0,0,2400,200 F |
| b22 | Panzer III front plate 1000,900,2000,1150 P ; turret side 950,1000,2000,1300 P |
| b23 | car side door 400,850,1100,1250 slight P (camo) ; trees top 0,0,2400,500 F (busy) |
| b24 | map on table 600,1300,2400,1792 P (strong) ; wall top-left 0,0,700,500 F |
| b25/26 | sky 700,0,1800,400 F ; right building wall 2100,0,2752,600 P |
| b27 | dark background top 0,0,1792,200 F ; sides 0,0,250,1500 and 1450,0,1792,1700 F |

## Video balck.mov

* 3840x2160, H.264, 30 fps constant, 939 frames, 31.30 s, ~28.9 Mb/s.
* Audio track present (AAC, 31.28 s) but **silent** (mean and max volume -91 dB).
* Black and white archival footage with an added "old film" look: dark rounded vignette frame on all edges. Picture area @1920 x 44..1874, y 38..1042 (source 88,76,3748,2084). Corners are rounded and black; crop at least ~100 px (source) more on each side to lose the rounded corners.
* **No watermark, logo, channel name or burned-in text found** (checked by eye on all segments and by per-pixel temporal std map `chk/clip_temporal_std.jpg`: nothing static except the vignette frame).
* Cuts: found from frame differences (`chk/clip_framediff.txt`) and checked by eye on `chk/clip_cut_candidates.jpg`.

| seg | frames | time (s) | content | Balck? |
|---|---|---|---|---|
| S1 | 1-29 | 0.00-0.97 | soldiers in camo helmets seen from behind, armoured vehicle and wooden fence | no |
| S2 | 30-114 | 0.97-3.80 | two officers in light summer tunics with KC looking down, foliage | possibly the right man (face down, profile) |
| S3 | 115-214 | 3.80-7.13 | tank advancing on a street before a white building, body on road, soldiers running | no |
| S4 | 215-303 | 7.13-10.10 | infantry advancing past wooden houses in smoke | no |
| S5 | 304-370 | 10.10-12.33 | close-up of officer in side cap with Knight's Cross, foliage behind, he turns his head | **probably Balck** (2.2 s) |
| S6 | 371-372 | 12.33-12.40 | 2-frame flash: soldiers on horizon | no (cut it) |
| S7 | 373-409 | 12.40-13.63 | knocked-out Soviet tanks by a road, foreground tank with foliage | no |
| S8 | 410-468 | 13.63-15.60 | handheld: Panzer hull with Balkenkreuz and number (not a swastika), then running gear passing (possible soft cut at f453) | no |
| S9 | 469-506 | 15.60-16.87 | field gun firing, smoke | no |
| S10 | 507-598 | 16.87-19.93 | Panther drives at and past the camera; last ~1 s very dark | no |
| S11 | 599-682 | 19.93-22.73 | camouflaged vehicle with crew, gun; dark | no |
| S12 | 683-779 | 22.73-26.00 | group of officers in front of a wall; **Joseph Goebbels** (party jacket, armband) in centre; general with high decorations right | not identifiable (looks like the Goebbels Lauban visit, March 1945) |
| S13 | 780-939 | 26.00-31.30 | Panzer IV with crew and rocket launcher frame, then tank column crossing a field | no |

### Balck in the video
* S5 (10.10-12.33 s, 2.2 s), probable, not certain (no caption). Face box (source px):
  * t=10.17 (f306): 1520,660,2400,1600
  * t=11.20 (f337): 1380,800,2340,2000
  * t=12.30 (f368): 1540,860,2460,2000
* S2 (0.97-3.80 s), right man, face lowered, maybe the same man and shoot as S5 (same light tunic, KC, foliage). Face box t=1.97 (f60): 2000,240,2640,880. Unverified.
* S12: the general at right with high-grade KC (face @1920 about 1450,90,1580,230) is NOT clearly Balck; treat as unknown.

### Swastikas in the video
Readable:
* S12 Goebbels' armband, moves with him for the whole segment (22.73-26.00 s). Source px boxes:
  * t=22.73 (f683): 2500,930,2584,1034
  * t=23.63 (f710): 2620,900,2700,1010
  * t=24.63 (f740): 2640,880,2720,990
  * t=25.93 (f779): 2600,824,2670,926
  * Safe union box for the whole segment: 2460,800,2760,1080 (verified on f683, f695, f725, f755, f765, f779, crops `z/V_vid_f*_union.jpg`).

Tiny / unreadable:
* S2 left officer breast eagle (whole segment, nearly static) @1920 480,440,600,500 → source 960,880,1200,1000; his badge below is a General Assault/Wound badge type, no readable swastika.
* S2 right officer KC centre @1920 1220,440,1290,520 → source 2440,880,2580,1040.
* S5 KC centre @1920 880,880,960,960 at t=10.17 (moves down to about 900,960,980,1040 by t=12.3) → source 1760,1760,1920,1920 to 1800,1920,1960,2080.
* S12 other men's breast eagles/caps: small, blurred, not readable.
* S8: Balkenkreuz and number on the hull, no swastika.
