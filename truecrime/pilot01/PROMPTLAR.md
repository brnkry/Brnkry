# Pilot 01: 20 saniyelik test videosu (Somerton Man açılışı)

Amaç: stili, karakter tutarlılığını ve Claude'un görsellerden animasyon üretme hattını test etmek.
Format: 16:9, 1920×1080, 30 fps, 20 saniye, İngilizce.

## Nasıl çalışıyoruz
1. Önce iki karakter sayfasını üret (DET_01, CON_01). Beğendiğin sayfa artık kilitli referanstır.
2. Poz görsellerini üretirken ilgili karakter sayfasını **referans olarak ekle**.
3. Poz ve eşya görselleri **düz yeşil zeminde** (#00B140) olacak. Zemini ben temizleyip karakterleri hareket ettireceğim (cutout animasyon).
4. Yüz hareketlerini (göz kırpma, kaş, ağız) ben çizeceğim. Bu yüzden ifadesiz "boş yüz" bir kafa görseli de istiyoruz.
5. Görselleri dosya adlarıyla gönder. ElevenLabs sesini de gönderirsen ona göre kurgularım. Göndermezsen geçici zamanlamayla yaparım.

Dosya adları: `DET_01_sheet`, `CON_01_sheet`, `VIC_01_pose`, `P1a`, `P1b`, `P2`, `P3`, `H1`, `L1`, `L2`, `PR1`, `PR2`, `PR3`

Not: Sahne bir dramatizasyondur. Cesedi ilk bulan sivillerdi, olay yerine önce bir polis memuru geldi. Dedektif karakteri temsilidir.

---

## STYLE BLOCK (her prompt'un içinde aynen yer alır)
```
Locked style: clean flat 2D stickman animation style. Perfectly round bone-white heads (#F2EEE6) with a uniform thick black outline, solid black dot eyes, small expressive black eyebrows, no nose, no ears, a simple thin black mouth line. Thin black stick arms and legs of uniform thickness, small round hands, simple rounded shoes. Clothing is drawn as simple flat shapes over the stick body with the same thick black outline. Flat colors only: no gradients, no 3D, no photorealism, no detailed anatomy, no heavy texture. Scenery lines are thinner and lighter than character outlines. Muted 1940s noir palette: ink black #1A1A1A, bone white #F2EEE6, aged paper #E8E0CF, slate blue #3E4C5E, fog grey #9AA0A6, sand #CDBB94, with evidence red #B3262E used only as a tiny accent. No text, no letters, no numbers, no logos, no watermark.
```

---

## KARAKTERLER

### DET_01: Detective (temsili karakter)
Palet: fötr #5A4A3A, şerit #1A1A1A, trençkot #8C7A5B, yaka #6E5F45, kravat #2B2B2B, pantolon #3A3A40
Değişmez: fötr şapka, bıyık, trençkot rengi ve düğmeleri, defter. Değişebilir: ifade, poz, defterin açık/kapalı olması.

**Identity paragraph**
```
DET_01 is a 1940s police detective, an adult man in his forties. Round bone-white head, total height of 6 head units, thin black stick limbs, slightly forward-leaning posture. Solid black dot eyes set fairly close together, thick straight black eyebrows, a short neat black rectangular mustache directly above the thin mouth line. Grey-brown fedora (#5A4A3A) with a black band (#1A1A1A), a pinched crown and a brim tilted slightly forward. Belted beige trench coat (#8C7A5B) reaching the knees, double row of four dark buttons, flat darker lapels (#6E5F45), belt tied at the waist. White shirt collar and a dark charcoal tie (#2B2B2B) visible at the neck. Dark grey trousers (#3A3A40), black rounded shoes. Signature prop: a small black notebook in his left hand and a short yellow pencil in his right hand.
```

**CHARACTER REFERENCE SHEET PROMPT**
```
Create a clean character reference sheet of ONE character only, on a plain flat light off-white background (#F4F1EA), 16:9 landscape, no scenery.

[Locked style] Clean flat 2D stickman animation style. Perfectly round bone-white heads (#F2EEE6) with a uniform thick black outline, solid black dot eyes, small expressive black eyebrows, no nose, no ears, a simple thin black mouth line. Thin black stick arms and legs of uniform thickness, small round hands, simple rounded shoes. Clothing drawn as simple flat shapes over the stick body with the same thick black outline. Flat colors only, no gradients, no 3D, no photorealism.

[Character] DET_01 is a 1940s police detective, an adult man in his forties. Round bone-white head, total height of 6 head units, thin black stick limbs, slightly forward-leaning posture. Solid black dot eyes set fairly close together, thick straight black eyebrows, a short neat black rectangular mustache directly above the thin mouth line. Grey-brown fedora (#5A4A3A) with a black band (#1A1A1A), a pinched crown and a brim tilted slightly forward. Belted beige trench coat (#8C7A5B) reaching the knees, double row of four dark buttons, flat darker lapels (#6E5F45), belt tied at the waist. White shirt collar and a dark charcoal tie (#2B2B2B) visible at the neck. Dark grey trousers (#3A3A40), black rounded shoes. Signature prop: a small black notebook in his left hand and a short yellow pencil in his right hand.

[Layout] Top row: four full-body views at exactly the same scale, standing on one thin grey ground line, evenly spaced: front view, three-quarter view, side view facing right, back view. Bottom row: six head-and-shoulders expression studies of the same character with the fedora on: neutral, suspicious (one eyebrow lowered, eyes narrowed), worried, shocked (eyebrows high, small round mouth), angry, determined. At the right side: one large close-up of the head with the fedora, and the black notebook with pencil drawn alone.

Keep anatomy, outline thickness, costume, proportions and colors identical in every panel. Do not show any other character, alternate costumes, realistic shading, extra limbs, extra fingers or redesigned faces. No text, no labels, no letters, no watermark.
```

### CON_01: Constable (temsili karakter)
Palet: üniforma #1F2A3A, düğme ve rozet #B8963E, siper #1A1A1A, pantolon #1F2A3A, fener başı #B8963E
Değişmez: kasket, pirinç düğmeler, fener. Değişebilir: ifade, poz, fenerin açık/kapalı olması.

**Identity paragraph**
```
CON_01 is a young 1940s police constable in his early twenties. Round bone-white head, total height of 5.5 head units, thin black stick limbs, upright eager posture. Solid black dot eyes set slightly wide apart, thin curved black eyebrows, clean shaven, no mustache. Dark navy peaked police cap (#1F2A3A) with a black visor (#1A1A1A) and a small round brass badge (#B8963E) at the front. Dark navy buttoned tunic (#1F2A3A) with a single row of four small brass buttons (#B8963E) and a thin black belt, matching dark navy trousers, black rounded boots. Signature prop: a long black hand torch with a brass head (#B8963E), always held in his right hand.
```

**CHARACTER REFERENCE SHEET PROMPT**
```
Create a clean character reference sheet of ONE character only, on a plain flat light off-white background (#F4F1EA), 16:9 landscape, no scenery.

[Locked style] Clean flat 2D stickman animation style. Perfectly round bone-white heads (#F2EEE6) with a uniform thick black outline, solid black dot eyes, small expressive black eyebrows, no nose, no ears, a simple thin black mouth line. Thin black stick arms and legs of uniform thickness, small round hands, simple rounded shoes. Clothing drawn as simple flat shapes over the stick body with the same thick black outline. Flat colors only, no gradients, no 3D, no photorealism.

[Character] CON_01 is a young 1940s police constable in his early twenties. Round bone-white head, total height of 5.5 head units, thin black stick limbs, upright eager posture. Solid black dot eyes set slightly wide apart, thin curved black eyebrows, clean shaven, no mustache. Dark navy peaked police cap (#1F2A3A) with a black visor (#1A1A1A) and a small round brass badge (#B8963E) at the front. Dark navy buttoned tunic (#1F2A3A) with a single row of four small brass buttons (#B8963E) and a thin black belt, matching dark navy trousers, black rounded boots. Signature prop: a long black hand torch with a brass head (#B8963E), always held in his right hand.

[Layout] Top row: four full-body views at exactly the same scale, standing on one thin grey ground line, evenly spaced: front view, three-quarter view, side view facing right, back view. Bottom row: six head-and-shoulders expression studies of the same character with the cap on: neutral, happy, worried, shocked (eyebrows high, small round mouth), nervous (eyebrows tilted up in the middle), determined. At the right side: one large close-up of the head with the cap, and the hand torch drawn alone.

Keep anatomy, outline thickness, costume, proportions and colors identical in every panel. Do not show any other character, alternate costumes, realistic shading, extra limbs, extra fingers or redesigned faces. No text, no labels, no letters, no watermark.
```

### VIC_01: The Unknown Man (tek poz, saygılı)
Kıyafetler kayıtlara göre: gri-kahve kruvaze ceket, kahve örgü kazak, beyaz gömlek, kırmızı-beyaz-mavi çizgili kravat, kahve pantolon, parlak kahve ayakkabı, şapkasız. Yaralanma veya kan yok.

**VIC_01_pose**
```
[Locked style] Clean flat 2D stickman animation style. Perfectly round bone-white head (#F2EEE6) with a uniform thick black outline, no nose, no ears, thin black stick limbs of uniform thickness, small round hands, simple rounded shoes. Clothing drawn as simple flat shapes over the stick body with the same thick black outline. Flat colors only, no gradients, no 3D, no photorealism, no text, no watermark.

Single character on a perfectly flat solid chroma green background (#00B140), no shadow, no ground, no scenery, the whole body fully visible with generous margin, 16:9 landscape.

VIC_01 is a well-dressed man from 1948, in his forties, tall and athletic, total height of 6.5 head units. Neatly combed short hair drawn as a smooth dark brown cap shape (#2A211B) on top of the head, no hat. Grey-brown double-breasted jacket (#6B5E50), brown knitted pullover (#7A5536) under it, white shirt collar, a tie with thin red, white and blue diagonal stripes (#8A2F35, #F2EEE6, #2F4A6B), brown trousers (#5C4430), polished brown shoes (#4A3324).

Pose, seen from the side: he lies peacefully on his back, head and shoulders slightly raised as if resting against a low wall at the left edge of the frame, legs stretched out straight toward the right with the ankles crossed, arms relaxed at his sides. Eyes closed, drawn as two short gentle curved lines, calm neutral face, thin relaxed mouth line. No injuries, no blood, nothing disturbing. Do not add any other character or object.
```

---

## POZLAR (yeşil zemin, ilgili karakter sayfası referans olarak eklenecek)

Her poz prompt'unun başına şunu koy:
```
Use the attached character reference sheet. Same character, same proportions, same colors, same outline thickness. Single character on a perfectly flat solid chroma green background (#00B140), no shadow, no ground line, no scenery, the whole body fully visible with generous margin, 1:1 square. Flat 2D stickman style, flat colors, no gradients, no text, no watermark.
```

**P1a: DET_01 walking, step A**
```
[başlık bloğu] + [DET_01 identity paragraph]
Pose: full body, pure side view facing right, mid-stride walking: left leg forward, right leg back, right arm swinging forward, left arm back holding the closed black notebook. Calm focused expression, eyebrows slightly lowered.
```

**P1b: DET_01 walking, step B**
```
[başlık bloğu] + [DET_01 identity paragraph]
Pose: full body, pure side view facing right, the opposite walking step: right leg forward, left leg back, left arm with the closed notebook swinging forward, right arm back. Same calm focused expression, eyebrows slightly lowered. Exactly the same size and head height as a standing pose.
```

**P2: DET_01 crouching**
```
[başlık bloğu] + [DET_01 identity paragraph]
Pose: full body, side view facing left, crouching low on the right knee with the left foot flat, upper body leaning forward. The notebook is open in the left hand, the pencil in the right hand resting on the page. Head tilted down toward the ground at the left, suspicious expression with one eyebrow lowered.
```

**P3: CON_01 pointing the torch**
```
[başlık bloğu] + [CON_01 identity paragraph]
Pose: full body, side view facing right, standing, right arm extended straight forward and slightly downward holding the switched-on torch. A soft pale yellow cone of light (#F3E3A0, semi-transparent) extends from the torch toward the right edge. Left arm relaxed. Nervous expression, eyebrows tilted up in the middle, small mouth.
```

**H1: DET_01 boş yüz kafa (yüz animasyonunu ben çizeceğim)**
```
Use the attached character reference sheet. Head and shoulders close-up of DET_01, front view, centered, on a perfectly flat solid chroma green background (#00B140), 1:1 square, no shadow.
DET_01 identity: round bone-white head (#F2EEE6) with a thick black outline, grey-brown fedora (#5A4A3A) with a black band and a slightly forward brim, short neat black rectangular mustache, beige trench coat collar (#8C7A5B) with darker lapels (#6E5F45), white shirt collar, dark charcoal tie (#2B2B2B).
IMPORTANT: the face is completely blank. NO eyes, NO eyebrows, NO mouth. Only the mustache stays on the face. Flat 2D style, flat colors, no gradients, no text, no watermark.
```

---

## MEKANLAR (karakter yok)

**L1: Geniş sahil**
```
[Locked style] Flat 2D stickman animation style background, scenery lines thin and light, flat colors, no gradients, no photorealism, no text, no signs, no watermark. 16:9 landscape.

Empty location plate, no people, no characters, no animals. Somerton Beach, near Adelaide, South Australia, early morning of 1 December 1948, soft pale dawn light. Wide shot from eye level. Background: calm grey-blue sea (#6F8496) and a pale peach and fog grey dawn sky (#E9D6C0, #9AA0A6), a few flat simple clouds. Middle ground: a low old stone sea wall (#A79F8F) running horizontally across the whole frame, about knee to waist height, with a few simple 1940s seaside houses and pine trees behind it in muted slate blue (#3E4C5E). Foreground: wide flat sand (#CDBB94) with a few faint footprints and small tufts of dry grass. Keep the sand area in the left and center of the frame clear and empty so characters can be added later. Period correct, nothing modern.
```

**L2: Duvar dibi yakın plan**
```
[Locked style] Flat 2D stickman animation style background, scenery lines thin and light, flat colors, no gradients, no photorealism, no text, no watermark. 16:9 landscape.

Empty location plate, no people. A closer low-angle view of the same old stone sea wall (#A79F8F) at Somerton Beach, 1948, early morning. The wall fills the left third of the frame, its stones drawn as simple flat rounded rectangles with thin lines. Flat sand (#CDBB94) covers the lower half of the frame, a strip of grey-blue sea (#6F8496) and pale dawn sky (#E9D6C0) visible at the top right. A few small shells and a scrap of dry seaweed on the sand. Leave the sand directly next to the wall and the center of the frame clear for characters.
```

---

## EŞYALAR (yeşil zemin, tek tek)

Her eşya prompt'unun başına:
```
Single object only, centered, on a perfectly flat solid chroma green background (#00B140), no shadow, 1:1 square. Flat 2D stickman animation prop style, uniform thick black outline, flat colors, no gradients, no photorealism. No text, no letters, no numbers, no logos, no watermark.
```

**PR1: Etiketi kesilmiş yaka**
```
[başlık bloğu]
The inside back collar of a 1940s white shirt (#F2EEE6), seen flat from the front, with a small rectangular spot where a clothing label has been cut away: a few short loose thread ends and a slightly darker rectangle outline. A thin evidence red circle (#B3262E) drawn around the cut spot.
```

**PR2: Kullanılmamış tren bileti**
```
[başlık bloğu]
A small unused 1940s railway ticket made of thick card, pale green-grey (#B9C4B0), rectangular with rounded corners, slightly tilted. Its surface is completely blank, only a few thin decorative border lines. No printed words or numbers.
```

**PR3: Sigara paketi ve kibrit**
```
[başlık bloğu]
A simple 1940s soft cigarette packet in muted cream and dark red (#E8E0CF, #7A2A2E) with no brand name, lying next to a small box of safety matches (#C9A86A) slightly open with a few matches visible. Both objects drawn together as one small evidence group.
```

---

## SENARYO (ElevenLabs, düz metin)
```
On the morning of December first, 1948, a man was found lying on Somerton Beach in South Australia. He was neatly dressed. He had no papers and no ID. And someone had cut the labels from his clothes. So who was he?
```
Not: Ayrıntılar (etiketler, kıyafetler) uzun video senaryosu öncesinde kaynaklarla tek tek doğrulanacak.

## STORYBOARD (20 sn)
| Zaman | Sahne | Görseller | Claude'un ekleyeceği |
|---|---|---|---|
| 0-5 | Geniş sahil, yavaş yaklaşma | L1 | Dalga ve bulut hareketi, tarih/yer damgası "SOMERTON BEACH · 1 DEC 1948" |
| 5-9 | Polis feneri duvara tutuyor, dedektif soldan yürüyerek giriyor | L1, P3, P1a/P1b | Yürüme döngüsü, fener ışığı titremesi |
| 9-13 | Duvar dibi: adam yatıyor, dedektif çömeliyor ve not alıyor | L2, VIC_01_pose, P2 | Defterde yazı animasyonu, hafif kamera kayması |
| 13-17 | Dedektifin yakın planı, ardından delil kartları | H1, PR1, PR2, PR3 | Göz kırpma, kaş kalkışı, polaroid delil kartları, kırmızı daire |
| 17-20 | Dosya kapanışı | Hepsi | "UNIDENTIFIED" damgası, "WHO WAS HE?" yazısı |
