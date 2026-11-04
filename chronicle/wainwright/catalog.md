# Wainwright asset catalog

Folder: `wain/`. Source files in `drive/` (untouched). Contact sheets in `chk/`.
Helper: `tools/sheet.py` (contact sheet + grid).

- `chk/sheet.jpg`: all 11 photos.
- `chk/clip_sheet.jpg`: first / middle / last frame of every video segment (labels = time + frame no.).
- `chk/sign.jpg`: video 0.0 to 9.4 s every 0.2 s (6 frames), full 1920x1080 frame with 200 px grid (yellow = 400 px multiples).

All photos are colorized, and the `_2K_` file names mean an AI upscaler (2K) was run on them. Expect smoothed skin, invented texture on fabric and ribbons, and colors that are guesses. No photo has a watermark or channel logo. No photo shows a Japanese rising-sun flag.

---

## Photos

Boxes are x0,y0,x1,y1 in original pixels of the drive file.

### w01.jpg: 2400x1792 (orig. "645657875_...n.jpg", from Facebook)
- **Shows:** two US officers in khaki standing on a wooden platform in the field, with a tree on the right and hills behind. This looks like the well-known Fort Stotsenburg, Philippines photo of 10 Oct 1941.
- **Wainwright:** YES, on the left. He wears a campaign hat with the chin strap in his mouth, a Sam Browne belt and a holster. Face (950,180,1110,340).
- **Others:** MacArthur on the right (braided peaked cap, hands in pockets). Face (1480,170,1630,340).
- **Setting/year:** pre-war Philippines, 1941.
- **Doubts:** heavy colorization and upscale. The source is a Facebook repost, so the caption is not verified. The identities match the famous photo.
- **Text surfaces:**
  1. Sky, upper left: (0,0,820,700). Flat, no perspective. Best.
  2. Sky band above the hills between the two men and the tree: (1900,0,2050,950). Narrow.
  3. Front face of the wooden crate: (410,1360,1400,1540). Mild perspective, partly covered by leaves.

### w02.jpg: 2400x1792 ("71hr6flKkpL._AC_UF894,1000_QL80_.jpg", from an Amazon print listing)
- **Shows:** President Truman pins the Medal of Honor on Wainwright outdoors at the White House, with smiling officials behind.
- **Wainwright:** YES, on the right in a 4-star tunic, with the medal ribbon at his neck. Face (1395,190,1810,580).
- **Others:** Truman, face (240,360,820,890). Three or four unidentified men in suits and uniforms behind (left edge and center). No MacArthur.
- **Setting/year:** Medal of Honor ceremony, White House, 10 Sept 1945.
- **Doubts:** the source is a retail print (Amazon), colorized and upscaled. The event itself is genuine.
- **Text surfaces:**
  1. Dark foliage above Truman's head: (700,0,1300,330). Flat. Light text needed.
  2. White building wall, top left: (0,0,670,310). Small, slight perspective.
  3. Foliage right of Wainwright's head: (1850,0,2400,600). Flat.

### w03.jpg: 2400x1792 ("images.jpeg")
- **Shows:** Wainwright seated at a wicker table, reading into a radio microphone with a "KZRH" plate. A Japanese officer or interpreter in a dark uniform sits on the left. Studio curtains and furniture behind.
- **Wainwright:** YES, in the center, wearing glasses. Face (1230,290,1470,675).
- **Others:** Japanese officer/interpreter, face (265,385,530,750).
- **Setting/year:** captivity. This is the forced surrender broadcast on station KZRH in Manila, 7 May 1942.
- **Burned-in text:** the "KZRH" microphone plate (1145,1035,1340,1300). It is a real object, not a watermark.
- **Doubts:** colorized and upscaled from a low-res "images.jpeg" thumbnail, so detail is likely hallucinated. Faces look plausible.
- **Text surfaces:**
  1. Curtain band at the top: (0,0,2400,265). Flat.
  2. Wooden cabinet on the right: (1830,430,2360,1350). Perspective (receding to the left).
  3. Papers on the table: (720,1140,1000,1215). Small, in perspective.

### w04.jpg: 1792x2400 ("images_(2).jpeg")
- **Shows:** formal seated portrait of a general in an OD service coat and braided peaked cap, with 4 stars on the shoulders, gold overseas stripes on the sleeve and hands folded. Patterned wallpaper and a framed picture behind.
- **Wainwright:** POSSIBLY, but doubtful. The face is fuller and rounder than in his other photos. Face (710,630,1075,1010).
- **Setting/year:** studio portrait, 1945 or later if it is him (4 stars).
- **Doubts:** **identity unverified.** It may be another general. Colorized and upscaled from a thumbnail. Do not use it as a "Wainwright" face shot without checking.
- **Text surfaces:**
  1. Wallpaper, right: (1265,0,1775,1150). Flat, patterned.
  2. Wall below the picture frame, left: (0,800,380,1250). Flat.

### w05.jpg: 1792x2400 ("images_(3).jpeg")
- **Shows:** a gaunt Wainwright seated in an armchair in an OD coat with **3 stars** (Lt. Gen.), smiling slightly and holding a cigarette. Room interior.
- **Wainwright:** YES. Face (695,240,1190,900).
- **Setting/year:** right after liberation, Aug/Sep 1945, before his 4th star. He looks emaciated.
- **Doubts:** colorized and upscaled from a thumbnail. The cigarette and hand look slightly AI-smoothed.
- **Text surfaces:**
  1. Olive wall, upper left: (0,0,670,860). Flat. Best.
  2. Wall and dark picture frame, upper right: (1330,0,1792,850). Flat.

### w06.jpg: 2752x1536 ("images_(4).jpeg")
- **Shows:** a general in a tan greatcoat and braided cap waving his right arm high, standing in an open car or on a stand. A civilian with glasses is on the right, and spectators, cars and mountains are behind.
- **Wainwright:** very likely, waving. Face (1185,330,1530,650).
- **Others:** civilian with glasses, face (2150,500,2400,830). Crowd heads at the lower left.
- **Setting/year:** homecoming welcome or parade, 1945. The mountains suggest the US West Coast, but the location is **unverified**.
- **Doubts:** colorized and upscaled. Date and place unknown.
- **Text surfaces:**
  1. Sky to the right of his head: (1650,0,2752,480). Flat. Best.
  2. Sky, upper left inside the raised arm: (330,0,1130,700). Flat. The arm crosses the left part.
  3. Mountain band: (0,750,1100,1250). Flat, but busy.

### w07.jpg: 1792x2400 ("images_(5).jpeg")
- **Shows:** Wainwright in profile, drinking from a white cup, in a khaki 4-star tunic. Office with a framed map behind.
- **Wainwright:** YES, profile. Head and face (460,140,1100,1000), face only (460,320,985,1000).
- **Setting/year:** late 1945 or later (4 stars).
- **Burned-in text:** the framed map has the printed word "SAM ..." at (285,270,510,365), plus small map labels across (0,0,1100,520). These are real props, not a watermark.
- **Doubts:** colorized and upscaled.
- **Text surfaces:**
  1. Plain wall right of his head: (1175,0,1792,800). Flat. Best.
  2. Map frame, upper left: (0,0,1100,520). Flat, but busy.

### w08.jpg: 1792x2400 ("Jonathan_M._Wainwright_(cropped).jpg", from Wikimedia)
- **Shows:** official portrait. Wainwright in an OD coat with 4 stars, a braided cap and ribbons, looking left. US and other flags behind.
- **Wainwright:** YES. Face (550,630,1265,1235).
- **Setting/year:** official 4-star portrait, about late 1945 or 1946.
- **Flags:** the US flag (stars and stripes) on the left (190,0,700,1500). There are no Japanese flags.
- **Doubts:** none on identity (Wikimedia source). Colorized and upscaled.
- **Text surfaces:**
  1. Beige wall between the flag and the staff, right: (1270,0,1600,1350). Flat, narrow.
  2. Flag drape, left: (0,0,600,1400). Folded, not suitable for clean text.
  3. Tunic chest, left: (150,1700,700,2100). Fabric. Avoid.

### w09.jpg: 1792x2400 ("Jonathan_M._Wainwright_as_a_Brigadier_General.jpg", from Wikimedia)
- **Shows:** a frontal studio portrait with a braided cap, white shirt and collar insignia. Plain grey background.
- **Wainwright:** YES. Face (585,690,1350,1265).
- **Setting/year:** pre-war portrait as Brigadier General, about 1938 to 1940.
- **Doubts:** none on identity. Colorized and upscaled.
- **Text surfaces:**
  1. Grey background, left: (0,0,380,1300). Flat, narrow.
  2. Grey background, right: (1530,0,1792,1300). Flat, narrow.
  3. Dark tunic, lower part: (150,1900,800,2400). Fabric, flat-ish.

### w10.jpg: 2048x2048 ("MacArthur_and_Wainright_1945_HD-SN-99-02411_cropped.jpg", from Wikimedia/NARA)
- **Shows:** MacArthur and Wainwright embrace, face to face, at their reunion.
- **Wainwright:** YES, on the right. He is thin, with 3 stars on his collar. Face (950,120,1470,745).
- **Others:** MacArthur on the left, in profile. Face (110,335,715,875).
- **Setting/year:** 1945 liberation reunion, New Grand Hotel, Yokohama, 31 Aug 1945.
- **Doubts:** genuine NARA photo. Colorized and upscaled.
- **Text surfaces:**
  1. Dark ceiling, upper left: (0,0,930,315). Perspective (the ceiling slopes down to the right).
  2. Wall and door frame, right edge: (1790,0,2048,1300). Flat, narrow.

### w11.jpg: 1792x2400 ("pr10492.jpg")
- **Shows:** Wainwright in a tan service cap with a gold eagle and a glossy black raincoat, sitting in an open car in a parade, looking up and left. A man in a straw hat behind, red/white/blue pennant bunting, and a cloudy sky.
- **Wainwright:** YES (heavier face because of the angle). Face (960,915,1365,1345).
- **Others:** spectator in a straw boater, face (205,725,420,995). Crowd in the background.
- **Setting/year:** homecoming parade, Sept 1945. The city is unverified. The bunting is US/patriotic, not Japanese.
- **Doubts:** colorized and upscaled. The source ID "pr10492" is unknown.
- **Text surfaces:**
  1. Cloudy sky, top: (270,0,1792,620). Flat. Best, but pennants cross it at (1000,150,1792,300).
  2. Raincoat area, lower left: (0,1500,700,2400). Glossy and busy. Avoid.

---

## Video: drive/wainwright.mov

- **Format:** 3840x2160 H.264, **30 fps** (1168 frames), **38.93 s**.
- **Audio:** AAC stereo 44.1 kHz. It has sound at 0 to 9.5 s and 34.77 to 38.93 s, and is silent (below -45 dB) from 9.51 to 34.77 s. The content is probably source film sound or music; it was not listened to.
- `drive/wainwright.mp3` (66.5 s) is also present, probably the voiceover.
- **Extracted frames:** `clip/fNNNN.jpg`, every frame, 1920x1080. Frame N = N/30 s.

**ALL VIDEO BOXES BELOW ARE IN 1920x1080 CLIP COORDINATES. Multiply by 2 for the original 3840x2160.**

### Segments
Cuts were found by frame differencing and each one checked by eye in `clip_sheet.jpg`.

| # | frames | time (s) | content | active picture (pillarbox) |
|---|---|---|---|---|
| 1 | 0 to 285 | 0.00 to 9.53 | **USS Missouri, 2 Sept 1945, colorized.** MacArthur seated at the surrender table signing. Wainwright standing at the left edge, with rows of US officers behind. Signing, then **pen handed to Wainwright**, then signing again. | x 219 to 1700 (black bars on both sides) |
| 2 | 286 to 527 | 9.53 to 17.57 | B&W: PT boat speeding at the camera, US flag on the mast. Fits MacArthur's PT boat escape from Corregidor (Mar 1942); generic footage. | x 280 to 1639 |
| 3 | 528 to 552 | 17.60 to 18.40 | B&W: landing craft (LCI) burning offshore. **Overlays: play icon + mouse cursor.** | full frame |
| 4 | 553 to 623 | 18.43 to 20.77 | B&W: LCVP "476" with a large US flag heading to shore, other craft, volcano/island. Play icon continues until f563. | full |
| 5 | 624 to 688 | 20.80 to 22.93 | B&W: island under bombardment (smoke), seen from a landing craft ramp. | full |
| 6 | 689 to 725 | 22.97 to 24.17 | B&W: line of warships/landing craft firing, splashes/birds over the cliffs. | full |
| 7 | 726 to 880 | 24.20 to 29.33 | B&W: landing craft beaching, US flag, posts in the foreground. | full |
| 8 | 881 to 986 | 29.37 to 32.87 | B&W: helmeted US troops moving up a beach. | full |
| 9 | 987 to 1042 | 32.90 to 34.73 | B&W: troops running past a sand mound. | full |
| 10 | 1043 to 1078 | 34.77 to 35.93 | B&W: officers descend the stairs of a USAAF transport (star insignia), with a crowd and press below. The camera zooms in about f1050. Likely Wainwright's 1945 arrival, unverified. | x 165 to 1757, y 20 to 1077 |
| 11 | 1079 to 1167 | 35.97 to 38.93 | B&W close-up: a general in a peaked cap salutes by the aircraft, with an officer behind on the left. Likely Wainwright (gaunt, long face), **unverified**. | x 231 to 1757 |

No Corregidor siege footage, no Japanese delegation, no captivity footage and no Medal of Honor footage is in this clip. Segments 3 to 9 are generic Pacific amphibious landings: they may be the 1945 return to Corregidor/Leyte, but this is not verifiable.

**Japanese rising-sun flags:** none seen in any segment. All visible flags are US (segments 2, 4 and 7).

### Burned-in overlays (must be cropped or avoided)
- **Play-button icon** (grey disc with a white triangle), screen-recording residue. Frames **538 to 563** (17.93 to 18.80 s): it fades in at f538 to 541, is solid at f542 to 562 and gone at f564. It crosses the cut into segment 4. Box **(856,231,1043,418)**.
- **Mouse cursor** (arrow): frames **528 to 554** (17.60 to 18.47 s). Box **(1320,995,1380,1050)**; at f553 it is at (1360,1020,1380,1050).
- So use segment 3 not at all (or crop below y 420 and above y 990, which leaves almost nothing). Start segment 4 at **f564 (18.80 s)** or later.
- No channel name, watermark or logo elsewhere. The black pillarbox bars must be cropped (see table).

### (1) MacArthur signing (segment 1)
Camera locked off. There is a very slight reframe around f60 to 75 while he sits up.

- **Pen on paper at the clip start:** f0 (0.00 s), so the pen is already writing on the front (nearest) document. He writes continuously through about **f101 (3.37 s)**. Pen tip about (1340,921) at f30.
- **Pen lift / finish of the first signature:** f101 to 103 (3.37 to 3.43 s). f105 to 110: a quick touch higher, on the middle document. f112 to 121 (3.73 to 4.03 s): his arm swings up off the table (finish flourish).
- **Second signature** (with a new pen after the handoff): he picks up a pen at the left of the papers at f204 to 222, and the **pen touches the paper at about f226 to 228 (7.53 to 7.60 s)**. Pen tip about (1340,882) at f240. He is still writing at the cut f285 (9.50 s), so **the finish is not in the shot**.
- **Documents on the table** (three open folders in a diagonal row, front one signed). They are stable throughout the segment:
  - Front (being signed): **(1120,885,1572,1010)**, partly covered by his right hand and arm.
  - Middle: (1018,700,1483,882).
  - Back/top: (1000,620,1400,700); partly hidden behind his head and shoulder.
  - Whole paper group: **(1000,620,1575,1012)**. It is in perspective, receding up and left.
- MacArthur body while signing: about (760,480,1350,1080). Head/cap about (950,490,1090,600) at f0 to 54, moving to about (880,480,1000,600) at f72 to 110.

### (2) Pen handed to Wainwright (segment 1)
Only one handoff is in the clip. **Percival does not receive a pen on screen.** A dark British-style cap is just visible behind Wainwright at (260,50,350,150) at the top left; it may be Percival, whose face is hidden.

- **Start:** f121 to 124 (4.03 to 4.13 s). MacArthur lifts the pen off the table and turns his head and torso left.
- f133 to 145 (4.43 to 4.83 s): Wainwright raises his right hand to his face; MacArthur's right arm extends left with the pen.
- **Hand contact / pen passes:** **f151 to 169 (5.03 to 5.63 s)**. The hands meet at about **(310,590,430,650)**.
- f166 to 180 (5.53 to 6.00 s): Wainwright bends forward to take the pen, and MacArthur's hand withdraws.
- **End:** about f184 to 187 (6.13 to 6.23 s), when MacArthur faces the table again. At f190 to 222 he reaches for the next pen.
- **Direction:** MacArthur is at center-right and Wainwright at the far left, so **the pen moves from right to left** in the 16:9 frame.
- **Boxes through the motion:**

| frame | t (s) | MacArthur head/cap | MacArthur body + arm | Wainwright face | Wainwright body |
|---|---|---|---|---|---|
| 118 | 3.93 | (720,500,810,590) | (650,480,1100,1080), arm up | (250,160,345,290) | (219,100,540,1080) |
| 145 | 4.83 | (720,510,820,600) | (430,500,1000,1080), arm out to x 430 | (260,150,360,290), hand at face | (219,100,540,1080) |
| 160 | 5.33 | (720,510,810,600) | (330,500,1000,1080), hand at (310 to 430, 590 to 650) | (330,170,450,310), leaning in | (219,100,560,1080) |
| 172 | 5.73 | (700,500,800,600) | (380,500,1000,1080) | (430,270,530,390), bowed | (219,140,600,1080) |
| 200 | 6.67 | (700,560,860,650), facing the table | (640,520,1100,1080) | (350,160,450,280) | (219,100,560,1080) |

The microphone stand in front of Wainwright is at about (300,430,390,560) on the stand line at x 330. The cane runs down to the bottom at x about 300 to 330.

### (3) Every shot with Wainwright visible
- **Segment 1 (0.00 to 9.53 s): visible throughout**, standing at the far left. His body is partly cut by the left pillarbox edge (x 219).
  - Face boxes: f0 (250,170,340,290); f90 (250,160,345,290); f140 (260,150,360,290); f160 (330,170,450,310); f172 (430,270,530,390); f200 (350,160,450,280); f285 (250,160,345,290).
  - Practical vertical-crop (9:16) window to hold both men during the handoff: x about **219 to 827** (608 px wide is 9:16 of 1080), covering f120 to 190. The signing hand and papers then fall out of the crop; for the signing use x about 1000 to 1608.
- **Segment 10 (34.77 to 35.93 s): possibly Wainwright** (unverified) as the first officer down the stairs. Head about (750,270,820,350) at f1045, and about (740,280,820,360) at f1070 after the zoom.
- **Segment 11 (35.97 to 38.93 s): possibly Wainwright** (unverified) saluting in close-up. Cap (520,240,1100,540); face (700,500,1120,920), with the saluting hand across (640,480,860,980). Almost static.
- No other segment shows him.
