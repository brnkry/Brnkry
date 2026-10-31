# Pilot 01 (v2): 20 saniyelik test, gerçekçi animasyon, anlatıcısız

Format: 16:9, 20 saniye, İngilizce. Anlatıcı yok. Hikaye sahnedeki diyaloglar, ortam sesleri ve ekran yazılarıyla anlatılıyor.
Yapı: 3 Flow klibi (her biri 8 sn üretilir, kurguda yaklaşık 6.5 sn'ye kırpılır) + Claude'un eklediği yazılar, ses katmanları ve kapanış kartı.

## Hava durumu
1 Aralık 1948, Adelaide'de yaz başı. Ceset sabah saat 06:30 civarında bulundu, yani güneş doğmuştu (fenere gerek yok). Bir önceki akşam sahilde insanlar vardı, bu da havanın ılık olduğunu gösteriyor. O sabah yağmur yağdığına dair bir kayıt bilmiyorum. Bu yüzden sakin, açık, hafif rüzgarlı bir yaz sabahı kullanıyoruz. Uzun videodan önce meteoroloji kaydına bakıp doğrulayacağım.

## İş akışı
1. **Gemini:** 3 karakter görseli (DET_01, CON_01, VIC_01) ve 1 mekan görseli (L1) üret. Bunlar referanslardır.
2. **Gemini:** 3 başlangıç karesi (F1, F2, F3) üret. Her birinde ilgili karakter görsellerini ve L1'i referans olarak **ekle**, sonra prompt'u yapıştır.
3. **Flow:** Her başlangıç karesini "Frames to Video" ile ilk kare olarak yükle, ilgili video prompt'unu (V1, V2, V3) yapıştır. 16:9, 8 saniye. Test için hızlı model, beğenince kaliteli model. Her prompt'tan 2 sonuç al, en iyisini seç.
4. **Bana gönder:** V1, V2, V3 mp4 dosyaları. Kırpma, ses katmanları (dalga, martı, rüzgar, uzak kalabalık), ses eşitleme, renk, tarih damgası, delil kartı ve kapanış kartını ben yaparım.

Ayrı poz görseli (çömelme vb.) yok. Çömelme gibi hareketleri Flow, videonun içinde yapıyor. Gemini'de sadece klibin **ilk anı** üretiliyor.

Not: Sahne bir dramatizasyondur. Diyaloglar uydurmadır. Dedektif ve memur temsili karakterlerdir. Ceplerde bulunan eşyalar (kullanılmamış tren bileti dahil) kayıtlara dayanır.

---

## 1. REFERANS GÖRSELLER (Gemini)

### DET_01: Detective
```
Character reference sheet of ONE character only, on a plain flat light grey background, 16:9 landscape, no scenery, no text, no labels, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look. Clean confident ink linework, realistic adult human proportions (about 7.5 heads tall), cel-shaded flat color areas with soft two-tone shadows, subtle painterly texture, subtle film grain. Muted 1940s palette. Not photorealistic, not 3D, not anime, not cartoonish, not chibi.

Character DET_01: an Australian police detective in 1948, man in his mid forties, lean build, tall. Long narrow face, strong square jaw, deep-set tired grey eyes, heavy straight dark eyebrows, a short neat dark brown mustache, light stubble, a small vertical crease between the brows. Short dark brown hair with grey at the temples, mostly hidden under a hat. Mid-grey felt fedora (#6B6A66) with a black band and a slightly forward-tilted brim. Charcoal grey single-breasted wool suit (#3A3A3E), jacket buttoned, white shirt, dark navy tie (#1E2533) with a small tie clip, black leather shoes. Signature prop: a small black leather notebook held in his left hand and a short pencil in his right hand. Calm, observant, serious presence.

Layout: top row, four full-body views at exactly the same scale standing on one thin ground line: front, three-quarter, side profile facing right, back. Bottom row, six head-and-shoulders expressions of the same man with the fedora on: neutral, suspicious (narrowed eyes, one brow lowered), worried, shocked, angry, quietly determined. Right side: one large close-up portrait of the face with the fedora, and the notebook with pencil drawn alone.

Keep face, proportions, costume, colors and line weight identical in every panel. No other characters, no alternate outfits, no extra fingers, no extra limbs.
```

### CON_01: Constable
```
Character reference sheet of ONE character only, on a plain flat light grey background, 16:9 landscape, no scenery, no text, no labels, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look. Clean confident ink linework, realistic adult human proportions (about 7.5 heads tall), cel-shaded flat color areas with soft two-tone shadows, subtle painterly texture, subtle film grain. Muted 1940s palette. Not photorealistic, not 3D, not anime, not cartoonish, not chibi.

Character CON_01: a young South Australian police constable in 1948, man in his early twenties, slim, average height. Round open face, clean shaven, slightly sunburnt cheeks, wide alert brown eyes, thin arched eyebrows, a few freckles on the nose, short neat light brown hair under the cap. Dark navy police uniform (#1C2433): peaked cap with a black visor and a small silver badge at the front, buttoned tunic with a single row of silver buttons and a black leather belt, matching navy trousers, polished black boots. Signature prop: a small notebook in his breast pocket and a whistle chain across the chest. Eager, slightly nervous presence.

Layout: top row, four full-body views at exactly the same scale standing on one thin ground line: front, three-quarter, side profile facing right, back. Bottom row, six head-and-shoulders expressions of the same man with the cap on: neutral, eager, worried, shocked, nervous, determined. Right side: one large close-up portrait of the face with the cap.

Keep face, proportions, costume, colors and line weight identical in every panel. No other characters, no alternate outfits, no extra fingers, no extra limbs.
```

### VIC_01: The Unknown Man (tek görsel, saygılı)
```
Single full-body reference image of ONE man, on a plain flat light grey background, 16:9 landscape, no scenery, no text, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look. Clean confident ink linework, realistic adult proportions, cel-shaded flat color areas with soft two-tone shadows, subtle painterly texture, subtle film grain. Not photorealistic, not 3D, not cartoonish.

Character VIC_01: a well-dressed man in 1948, in his forties, tall, athletic build, broad shoulders. Calm face with a strong jaw, short neatly combed light brown hair, clean shaven, no hat. Grey-brown double-breasted jacket (#6B5E50), brown knitted pullover (#7A5536) underneath, white shirt, a tie with thin red, white and blue diagonal stripes, brown trousers (#5C4430), polished brown lace-up shoes.

Pose, seen from his left side: he lies on his back on the ground, head and shoulders slightly raised as if resting against a low wall at the left edge, legs stretched out straight toward the right with the ankles crossed, arms relaxed at his sides. Eyes closed, peaceful expression, as if asleep. No injuries, no blood, nothing graphic or disturbing.
```

### L1: Mekan, Somerton Beach
```
Empty location background, 16:9 landscape, no people, no animals, no text, no signs, no watermark.

Art style: semi-realistic 2D animated feature film background, hand-painted noir graphic novel look, clean ink linework, cel-shaded flat color areas, soft painterly texture, subtle film grain. Not photorealistic, not 3D.

Somerton Beach near Adelaide, South Australia, early morning of 1 December 1948, early summer. Clear calm morning with low warm sunlight from the right, long soft shadows, a few thin high clouds, light sea breeze. Eye-level wide shot. Background: calm blue-grey sea with small gentle waves and a pale blue sky. Middle ground: a low old concrete and stone sea wall running horizontally across the frame, about waist height, with steps at the far right; behind it a row of modest 1940s seaside houses, a couple of tall Norfolk pines and a large old institutional brick building in the distance. Foreground: wide flat pale sand with footprints and small tufts of dry grass. The sand area along the wall in the left half of the frame is clear and empty. Period correct, nothing modern.
```

---

## 2. BAŞLANGIÇ KARELERİ (Gemini, referansları ekleyerek)

### F1 (ekle: DET_01, CON_01, VIC_01, L1)
```
Use the attached reference images for the characters and the location. Keep every face, costume, color and proportion exactly as in the references.

A single cinematic still frame, 16:9 landscape. Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic human proportions, cel-shaded flat colors with soft two-tone shadows, painterly background, subtle film grain. Not photorealistic, not 3D, not cartoonish. No text, no watermark.

Scene: Somerton Beach, South Australia, early morning of 1 December 1948, clear calm summer morning, low warm sun from the right, long soft shadows, gentle waves.

Composition: medium wide shot from eye level. Left third: the low stone sea wall; against it the man VIC_01 (well-dressed man in his forties, grey-brown double-breasted jacket, brown knitted pullover, white shirt, red white and blue striped tie, brown trousers, polished brown shoes, no hat) lies on his back with head and shoulders resting against the wall, legs stretched toward the right, ankles crossed, eyes closed, peaceful, partly in the shadow of the wall. Nothing graphic. Center: the young constable CON_01 (early twenties, clean shaven, freckles, dark navy uniform with peaked cap, silver buttons, black belt, whistle chain) crouches on one knee beside the man's feet, looking up toward the right with a nervous expression. Right third, entering from the right edge: the detective DET_01 (mid forties, lean, long narrow face, short dark mustache, mid-grey fedora, charcoal grey suit, white shirt, dark navy tie) walking across the sand toward the wall, notebook closed in his left hand, serious expression. Background: calm sea, distant houses and Norfolk pines behind the wall.
```

### F2 (ekle: DET_01, VIC_01, L1)
```
Use the attached reference images for the characters and the location. Keep every face, costume, color and proportion exactly as in the references.

A single cinematic still frame, 16:9 landscape. Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic human proportions, cel-shaded flat colors with soft two-tone shadows, painterly background, subtle film grain. Not photorealistic, not 3D, not cartoonish. No text, no watermark.

Scene: the same spot against the stone sea wall at Somerton Beach, 1 December 1948, early morning, low warm sunlight from the right.

Composition: medium close shot, slightly low angle. The detective DET_01 (mid forties, lean, long narrow face, deep-set grey eyes, short dark mustache, light stubble, mid-grey fedora, charcoal grey suit, white shirt, dark navy tie) crouches on his right knee on the sand, facing left, leaning in. His right hand is reaching toward the left side of the jacket of VIC_01, whose torso is visible at the lower left of the frame (grey-brown double-breasted jacket, brown knitted pullover, white shirt, red white and blue striped tie); the man's face is out of frame. The detective's notebook sticks out of his own left jacket pocket. Expression: focused, eyes narrowed. Background: the stone wall on the left, sand and a strip of blue-grey sea at the top right.
```

### F3 (ekle: DET_01, L1)
```
Use the attached reference images for the character and the location. Keep the face, costume, colors and proportions exactly as in the references.

A single cinematic still frame, 16:9 landscape. Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic human proportions, cel-shaded flat colors with soft two-tone shadows, painterly background, subtle film grain. Not photorealistic, not 3D, not cartoonish. No text, no watermark.

Scene: Somerton Beach, 1 December 1948, early morning, low warm sunlight from the right.

Composition: close-up of the detective DET_01 (mid forties, lean, long narrow face, strong square jaw, deep-set tired grey eyes, heavy dark eyebrows, short neat dark mustache, light stubble, mid-grey fedora with black band, charcoal grey suit, white shirt, dark navy tie) from the chest up, crouching, three-quarter view facing left. He holds up a small unused 1940s railway ticket made of thick pale green card between the thumb and finger of his right hand, at chin height, looking at it. Its printed text is too small and blurred to read. Warm sunlight on the right side of his face, soft shadow under the hat brim. Background: softly out-of-focus sea and sand.
```

---

## 3. FLOW VİDEO PROMPT'LARI (Frames to Video, ilk kare olarak F1/F2/F3)

### V1 (ilk kare: F1)
```
The provided image is the first frame. Keep the exact art style: semi-realistic 2D animated feature film with a noir graphic novel look, clean ink linework, cel-shaded flat colors, painterly background, subtle film grain. Keep both characters' faces, costumes and colors exactly as in the first frame. Not photorealistic, not 3D.

Setting: Somerton Beach, South Australia, early morning, 1 December 1948. Clear calm summer morning, light sea breeze moving the dry grass, gentle waves rolling in.

Action: 0 to 2 seconds, the detective keeps walking across the sand toward the wall, small puffs of sand at each step; the constable looks up at him. 2 to 5 seconds, the constable stands up quickly and speaks. 5 to 8 seconds, the detective stops beside him, looks down at the still man by the wall and answers quietly. The man lying against the wall does not move at all.

Camera: static, very slight slow push in.

Dialogue, Australian accents:
Constable, young and nervous: "Found him like this, sir. Couple of blokes on the beach saw him."
Detective, low and calm: "Anyone know who he is?"

Audio: soft waves, light wind, a distant seagull, footsteps on sand. No music.
Avoid: character redesign, style change, modern objects, extra people, extra limbs, flicker, scene cuts, text, subtitles, watermark, blood or injuries.
```

### V2 (ilk kare: F2)
```
The provided image is the first frame. Keep the exact art style: semi-realistic 2D animated feature film with a noir graphic novel look, clean ink linework, cel-shaded flat colors, painterly background, subtle film grain. Keep the detective's face, hat, suit and colors exactly as in the first frame. Not photorealistic, not 3D.

Setting: beside the stone sea wall at Somerton Beach, early morning, 1 December 1948, warm low sunlight, gentle breeze.

Action: 0 to 2 seconds, the detective leans in a little closer. 2 to 5 seconds, he carefully lifts the edge of the man's jacket with two fingers and slides his hand into the inside pocket. 5 to 8 seconds, he slowly draws out a small pale green railway ticket, holds it up and frowns at it. The man lying down never moves.

Camera: static, slight drift toward the detective's hand.

Dialogue, Australian accent:
Detective, quietly to himself: "No papers. Nothing with a name on it." (pause) "But a train ticket."

Audio: soft waves, light wind, fabric rustle, faint distant voices of onlookers further along the beach. No music.
Avoid: character redesign, style change, showing the lying man's face, modern objects, extra hands, extra fingers, flicker, scene cuts, readable text on the ticket, subtitles, watermark, blood or injuries.
```

### V3 (ilk kare: F3)
```
The provided image is the first frame. Keep the exact art style: semi-realistic 2D animated feature film with a noir graphic novel look, clean ink linework, cel-shaded flat colors, painterly background, subtle film grain. Keep the detective's face, hat, suit and colors exactly as in the first frame. Not photorealistic, not 3D.

Setting: Somerton Beach, early morning, 1 December 1948, warm low sunlight, light breeze.

Action: 0 to 3 seconds, the detective turns the small ticket over in his fingers and studies it, eyes narrowing. 3 to 5 seconds, he lowers the ticket and looks slowly to the left, toward the man by the wall (off screen). 5 to 8 seconds, he holds that look, jaw tight, and speaks quietly. Hold on his face at the end.

Camera: static close-up, very slow push in on his eyes.

Dialogue, Australian accent:
Detective, almost a whisper: "Bought a ticket and never used it." (pause) "So who are you, mate?"

Audio: soft waves, light wind, a single distant seagull. No music.
Avoid: character redesign, style change, modern objects, extra fingers, flicker, scene cuts, readable text on the ticket, subtitles, watermark.
```

---

## 4. CLAUDE'UN EKLEYECEKLERİ
- 0-6.5 sn (V1): sol alttan daktilo efektiyle gelen "SOMERTON BEACH · SOUTH AUSTRALIA · 1 DECEMBER 1948" yazısı
- 6.5-13 sn (V2): bilet çıktığı anda küçük bir delil etiketi: "EVIDENCE 01 · UNUSED RAIL TICKET"
- 13-18 sn (V3): yüzde hafif kararma
- 18-20 sn: siyah ekran, kırmızı "UNIDENTIFIED" damgası, daktilo sesi
- Ses: dalga, rüzgar ve martı katmanları; klipler arasında kesintisiz ortam sesi; diyalogların seviye eşitlemesi; son saniyelerde alçak bir drone sesi
- Renk: üç klibin rengini birbirine eşitleme
