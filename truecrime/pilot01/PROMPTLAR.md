# Pilot 01 (v3): 20 saniyelik test, animasyonu Claude yapıyor

Format: 16:9, 1920×1080, 30 fps, 20 saniye, İngilizce. Anlatıcı yok; diyalog, ortam sesi ve ekran yazıları var.

## Yöntem
Sen Gemini'de görselleri üretiyorsun, ben onları kod ile canlandırıyorum (2.5D / cutout animasyon):
- **Katmanlar:** Gökyüzü, deniz, duvar ve karakterler ayrı görseller. Bunlarla derinlik (parallax), kamera kaydırma ve zoom yapıyorum.
- **Yeşil zemin:** Karakterler düz yeşil (#00B140) zeminde. Zemini ben temizleyip sahneye yerleştiriyorum.
- **Düzenleme varyantları:** Göz kırpma, ağız açma, el hareketi gibi şeyler için Gemini'de **aynı görseli düzenleyip** sadece bir şeyi değiştiriyorsun ("Edit" prompt'ları). Görseller birebir üst üste oturduğu için aralarında geçiş yapınca hareket ediyormuş gibi görünüyor. Dudak senkronunu ağız varyantlarını ses dosyasına göre değiştirerek yapıyorum.
- **Benim eklediklerim:** Dalga ve su parıltısı, rüzgarda sallanan otlar, kum tozu, nefes alma ve vücut sallanması, ışık, film grain, yazılar, ses miksi.

**Düzenleme varyantları nasıl yapılır:** Gemini'de bir önceki görseli sohbete yükle (veya aynı sohbette üretilen görselin üzerinde devam et), "Edit" prompt'unu yapıştır. Sonuç kaymışsa veya başka bir yeri de değişmişse tekrar üret. Küçük kaymaları ben düzeltebilirim.

**Ses (ElevenLabs):** Diyalogları ve efektleri sen üretiyorsun, listesi en altta.

Not: Sahne bir dramatizasyondur. Diyaloglar uydurmadır; dedektif ve memur temsili karakterlerdir. Ceketten çıkan kullanılmamış tren bileti kayıtlara dayanır. Hava: 1 Aralık 1948 sabahı için yağmur kaydı bilmiyorum, açık bir yaz sabahı kullanıyoruz (uzun videodan önce doğrulanacak).

## Dosya listesi (toplam 21 görsel)
| Grup | Dosyalar |
|---|---|
| Referans | DET_01_sheet, CON_01_sheet, VIC_01_ref |
| Sahne 1 | S1_bg, S1_fg, S1_vic, S1_con_a, S1_con_b, S1_det_a, S1_det_b, S1_det_c, S1_det_d |
| Sahne 2 | S2_k1, S2_k1_blink, S2_k2, S2_k3, S2_k3_talk |
| Sahne 3 | S3_k1, S3_k1_blink, S3_k1_talk, S3_k2, S3_k2_talk |
| Eşya | PR_ticket |

Sıra: önce referanslar. Sonra her sahnenin "ana" görseli. Varyantlar en son, ana görseli düzenleyerek.

---

# REFERANSLAR

## DET_01_sheet
```
Character reference sheet of ONE character only, on a plain flat light grey background, 16:9 landscape, no scenery, no text, no labels, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look. Clean confident ink linework, realistic adult human proportions (about 7.5 heads tall), cel-shaded flat color areas with soft two-tone shadows, subtle painterly texture, subtle film grain. Muted 1940s palette. Not photorealistic, not 3D, not anime, not cartoonish.

Character DET_01: an Australian police detective in 1948, man in his mid forties, lean build, tall. Long narrow face, strong square jaw, deep-set tired grey eyes, heavy straight dark eyebrows, a short neat dark brown mustache, light stubble, a small vertical crease between the brows. Short dark brown hair with grey at the temples, mostly hidden under a hat. Mid-grey felt fedora (#6B6A66) with a black band and a slightly forward-tilted brim. Charcoal grey single-breasted wool suit (#3A3A3E), jacket buttoned, white shirt, dark navy tie (#1E2533) with a small tie clip, black leather shoes. Signature prop: a small black leather notebook held in his left hand.

Layout: top row, four full-body views at exactly the same scale standing on one thin ground line: front, three-quarter, side profile facing right, back. Bottom row, six head-and-shoulders expressions of the same man with the fedora on: neutral, suspicious (narrowed eyes, one brow lowered), worried, shocked, angry, quietly determined. Right side: one large close-up portrait of the face with the fedora.

Keep face, proportions, costume, colors and line weight identical in every panel. No other characters, no alternate outfits, no extra fingers, no extra limbs.
```

## CON_01_sheet
```
Character reference sheet of ONE character only, on a plain flat light grey background, 16:9 landscape, no scenery, no text, no labels, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look. Clean confident ink linework, realistic adult human proportions (about 7.5 heads tall), cel-shaded flat color areas with soft two-tone shadows, subtle painterly texture, subtle film grain. Muted 1940s palette. Not photorealistic, not 3D, not anime, not cartoonish.

Character CON_01: a young South Australian police constable in 1948, man in his early twenties, slim, average height. Round open face, clean shaven, slightly sunburnt cheeks, wide alert brown eyes, thin arched eyebrows, a few freckles on the nose, short neat light brown hair under the cap. Dark navy police uniform (#1C2433): peaked cap with a black visor and a small silver badge at the front, buttoned tunic with a single row of silver buttons and a black leather belt, matching navy trousers, polished black boots. A whistle chain across the chest.

Layout: top row, four full-body views at exactly the same scale standing on one thin ground line: front, three-quarter, side profile facing right, back. Bottom row, six head-and-shoulders expressions of the same man with the cap on: neutral, eager, worried, shocked, nervous, determined. Right side: one large close-up portrait of the face with the cap.

Keep face, proportions, costume, colors and line weight identical in every panel. No other characters, no alternate outfits, no extra fingers, no extra limbs.
```

## VIC_01_ref
```
Single full-body character reference of ONE man standing, front view, on a plain flat light grey background, 3:4 portrait, no scenery, no text, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look. Clean confident ink linework, realistic adult proportions (about 7.5 heads tall), cel-shaded flat color areas with soft two-tone shadows, subtle painterly texture, subtle film grain. Not photorealistic, not 3D, not cartoonish.

Character VIC_01: a well-dressed man in 1948, in his forties, tall, athletic build, broad shoulders. Calm face with a strong jaw, short neatly combed light brown hair, clean shaven, no hat. Grey-brown double-breasted jacket (#6B5E50), brown knitted pullover (#7A5536) underneath, white shirt, a tie with thin red, white and blue diagonal stripes, brown trousers (#5C4430), polished brown lace-up shoes. Neutral calm expression, arms at his sides.
```

---

# SAHNE 1 (0 - 6.5 sn): Sahil, memur ve dedektif
Ben ne yapacağım: kamera soldan sağa yavaş kayar, deniz ve gökyüzü daha yavaş kayar (derinlik). Dedektif sağdan yürüyerek girer (S1_det_a ile S1_det_b dönüşümlü), durur (S1_det_c). Memur konuşur (S1_con_a ile S1_con_b ağız), dedektif cevap verir (S1_det_c ile S1_det_d ağız).

## S1_bg (en arka katman)
```
Background layer only, 21:9 ultra-wide landscape, no people, no animals, no text, no signs, no watermark.

Art style: semi-realistic 2D animated feature film background, hand-painted noir graphic novel look, clean ink linework, cel-shaded flat color areas, soft painterly texture, subtle film grain. Not photorealistic, not 3D.

Somerton Beach near Adelaide, South Australia, early morning of 1 December 1948, early summer, clear calm morning. Show ONLY the far distance: a pale blue morning sky with a few thin high clouds, low warm sunlight coming from the right, and a calm blue-grey sea filling the lower half of the image with small gentle waves and soft sun glints, a faint far horizon line in the middle. On the far left, a low distant headland. No sea wall, no sand, no buildings in the foreground. The whole image is only sky and sea.
```

## S1_fg (ön katman: duvar ve kum)
```
Foreground layer only, 21:9 ultra-wide landscape, on a perfectly flat solid chroma green background (#00B140) above the drawn elements, no people, no text, no watermark.

Art style: semi-realistic 2D animated feature film background, hand-painted noir graphic novel look, clean ink linework, cel-shaded flat color areas, soft painterly texture, subtle film grain. Not photorealistic, not 3D.

Somerton Beach, South Australia, 1948, early morning, low warm sunlight from the right. The lower 45 percent of the image: wide flat pale sand (#D8C9A3) with footprints and a few small tufts of dry grass, and on top of the sand an old low concrete and stone sea wall running horizontally across the entire width, about waist height for an adult, with a flat top edge, weathered stones, soft shadow on its left faces, and a short flight of concrete steps at the far right. Behind and above the wall: modest 1940s seaside houses with tiled roofs and two tall Norfolk pines standing on the land above the wall, in muted slate blue and warm grey tones. Everything above the rooftops and the pines is plain flat chroma green (#00B140) so it can be removed. The sand area in front of the left half of the wall is completely empty.
```

## S1_vic (yatan adam)
```
Single character on a perfectly flat solid chroma green background (#00B140), no shadow, no ground, no scenery, the whole body fully visible with margin, 16:9 landscape, no text, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic adult proportions, cel-shaded flat colors with soft two-tone shadows, subtle film grain. Not photorealistic, not 3D, not cartoonish. Use the attached VIC_01 reference for face and clothing.

VIC_01: a well-dressed man in 1948, in his forties, tall, athletic build, short neatly combed light brown hair, clean shaven, no hat, grey-brown double-breasted jacket (#6B5E50), brown knitted pullover (#7A5536), white shirt, tie with thin red, white and blue diagonal stripes, brown trousers (#5C4430), polished brown lace-up shoes.

Pose, seen exactly from his left side at eye level: he lies on his back, head and shoulders slightly raised as if resting against a low wall at the left edge, legs stretched straight toward the right with the ankles crossed, arms relaxed along his sides. Eyes closed, peaceful face, as if asleep. Warm low light from the right. No injuries, no blood, nothing graphic.
```

## S1_con_a (diz çökmüş memur)
```
Single character on a perfectly flat solid chroma green background (#00B140), no shadow, no ground, no scenery, the whole body fully visible with margin, 1:1 square, no text, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic adult proportions, cel-shaded flat colors with soft two-tone shadows, subtle film grain. Not photorealistic, not 3D, not cartoonish. Use the attached CON_01 reference sheet: same face, same uniform, same colors.

CON_01: a young South Australian police constable in 1948, early twenties, slim, round open face, clean shaven, slightly sunburnt cheeks, wide brown eyes, thin arched eyebrows, freckles on the nose, dark navy uniform (#1C2433) with peaked cap, black visor, small silver cap badge, single row of silver buttons, black leather belt, whistle chain, navy trousers, black boots.

Pose: side view facing right, kneeling on his left knee with his right foot flat on the ground, upper body upright, right hand resting on his right knee, head turned up and to the right as if looking at someone tall arriving. Nervous expression, eyebrows slightly raised, mouth closed. Warm low light from the right.
```

## S1_con_b (Edit: S1_con_a üzerinde)
```
Edit the attached image. Change ONLY the mouth: the constable is speaking, mouth half open as if saying "sir". Keep everything else exactly identical: same pose, same size, same position in the frame, same face, same eyes, same uniform, same colors, same lighting, same green background.
```

## S1_det_a (yürüyen dedektif, adım A)
```
Single character on a perfectly flat solid chroma green background (#00B140), no shadow, no ground, no scenery, the whole body fully visible with margin, 3:4 portrait, no text, no watermark.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic adult proportions, cel-shaded flat colors with soft two-tone shadows, subtle film grain. Not photorealistic, not 3D, not cartoonish. Use the attached DET_01 reference sheet: same face, same hat, same suit, same colors.

DET_01: an Australian police detective in 1948, mid forties, lean and tall, long narrow face, strong square jaw, deep-set grey eyes, heavy dark eyebrows, short neat dark brown mustache, light stubble, mid-grey fedora (#6B6A66) with black band, charcoal grey single-breasted suit (#3A3A3E), white shirt, dark navy tie (#1E2533), black leather shoes, small black notebook in his left hand.

Pose: full body, exact side profile facing LEFT, walking mid-stride: right leg forward, left leg back, left arm with the closed notebook swinging slightly forward, right arm back. Serious focused expression, eyes looking ahead and slightly down, mouth closed. Warm low light from the right, so his back is lit.
```

## S1_det_b (Edit: S1_det_a üzerinde)
```
Edit the attached image. Change ONLY the legs and arms to the opposite walking step: left leg forward, right leg back, right arm swinging slightly forward, left arm with the notebook slightly back. Keep everything else exactly identical: same head position and height, same face, same hat, same suit, same colors, same size, same green background.
```

## S1_det_c (Edit: S1_det_a üzerinde)
```
Edit the attached image. Change ONLY the pose: he has stopped walking and stands still with both feet together, the notebook held at his side in his left hand, his head tilted down and to the left as if looking at something on the ground in front of him. Mouth closed. Keep everything else exactly identical: same face, same hat, same suit, same colors, same size and head height, same green background.
```

## S1_det_d (Edit: S1_det_c üzerinde)
```
Edit the attached image. Change ONLY the mouth: he is speaking quietly, mouth slightly open. Keep everything else exactly identical: same pose, same head angle, same eyes, same face, same hat, same suit, same colors, same size, same green background.
```

---

# SAHNE 2 (6.5 - 13 sn): Ceketin cebinden bilet
Ben ne yapacağım: yavaş zoom; k1, k2, k3 arasında kısa geçişlerle el hareketi; göz kırpma; dedektif konuşurken ağız değişimi; arkada su parıltısı ve kum tozu.

## S2_k1 (ana kare)
```
A single cinematic still frame, 16:9 landscape, no text, no watermark. Use the attached DET_01 and VIC_01 references: same faces, same clothes, same colors.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic human proportions, cel-shaded flat colors with soft two-tone shadows, painterly background, subtle film grain. Not photorealistic, not 3D, not cartoonish.

Scene: beside an old low stone sea wall at Somerton Beach, South Australia, early morning of 1 December 1948, clear summer morning, warm low sunlight from the right.

Composition: medium close shot, slightly low angle, camera on the sand. Right half: the detective DET_01 (mid forties, lean, long narrow face, deep-set grey eyes, heavy dark eyebrows, short neat dark brown mustache, light stubble, mid-grey fedora with black band, charcoal grey suit, white shirt, dark navy tie) crouches on his right knee facing left, leaning in, his right hand reaching toward and just touching the edge of the jacket of the lying man. Focused expression, eyes narrowed, mouth closed. Lower left: only the torso of VIC_01 lying on his back against the wall (grey-brown double-breasted jacket, brown knitted pullover, white shirt, red white and blue striped tie), his face out of frame above the left edge. Background: weathered stone wall on the left, sand, and a strip of blue-grey sea and pale sky at the top right.
```

## S2_k1_blink (Edit: S2_k1 üzerinde)
```
Edit the attached image. Change ONLY the detective's eyes: fully closed, as in the middle of a blink. Keep everything else exactly identical: framing, pose, hand, face shape, hat, clothes, the lying man, background, colors, lighting.
```

## S2_k2 (Edit: S2_k1 üzerinde)
```
Edit the attached image. Change ONLY the detective's right hand and forearm: he has lifted the edge of the man's jacket and his hand is now slipped inside the inner jacket pocket, the jacket edge slightly folded back. Keep everything else exactly identical: framing, the detective's face and expression, hat, clothes, the lying man, background, colors, lighting.
```

## S2_k3 (Edit: S2_k1 üzerinde)
```
Edit the attached image. Change ONLY the detective's right arm, hand and expression: he has drawn his hand back toward himself and holds a small pale green 1940s railway ticket made of thick card between thumb and finger at chest height, looking at it with a frown. The ticket's printed text is tiny and unreadable. Mouth closed. Keep everything else exactly identical: framing, face shape, hat, clothes, the lying man, background, colors, lighting.
```

## S2_k3_talk (Edit: S2_k3 üzerinde)
```
Edit the attached image. Change ONLY the detective's mouth: slightly open, speaking quietly. Keep everything else exactly identical, including the ticket in his hand, his eyes, the framing and the background.
```

---

# SAHNE 3 (13 - 18 sn): Yakın plan
Ben ne yapacağım: çok yavaş zoom, göz kırpma, bilete bakarken (k1) konuşur, sonra gözleri sola kayar (k2) ve son cümleyi söyler. Kenarlarda hafif karartma.

## S3_k1 (ana kare)
```
A single cinematic still frame, 16:9 landscape, no text, no watermark. Use the attached DET_01 reference sheet: same face, same hat, same suit, same colors.

Art style: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident ink linework, realistic human proportions, cel-shaded flat colors with soft two-tone shadows, painterly background, subtle film grain. Not photorealistic, not 3D, not cartoonish.

Scene: Somerton Beach, South Australia, early morning of 1 December 1948, warm low sunlight from the right.

Composition: close-up of the detective DET_01 from the chest up, crouching, three-quarter view facing left, positioned in the right half of the frame. Mid forties, lean, long narrow face, strong square jaw, deep-set tired grey eyes, heavy dark eyebrows, short neat dark brown mustache, light stubble, mid-grey fedora with black band, charcoal grey suit, white shirt, dark navy tie. In his right hand, at chin height, he holds a small pale green 1940s railway ticket of thick card between thumb and finger and looks down at it. The ticket's printed text is tiny and unreadable. Mouth closed. Warm sunlight on the right side of his face, soft shadow under the hat brim. Background in the left half: softly out-of-focus blue-grey sea and pale sand.
```

## S3_k1_blink (Edit: S3_k1 üzerinde)
```
Edit the attached image. Change ONLY the eyes: fully closed, as in the middle of a blink. Keep everything else exactly identical: framing, face, hat, hand, ticket, clothes, background, colors, lighting.
```

## S3_k1_talk (Edit: S3_k1 üzerinde)
```
Edit the attached image. Change ONLY the mouth: slightly open, speaking quietly. Keep everything else exactly identical: framing, eyes, face, hat, hand, ticket, clothes, background, colors, lighting.
```

## S3_k2 (Edit: S3_k1 üzerinde)
```
Edit the attached image. Change ONLY the eyes and eyebrows: his eyes have moved to look toward the far left edge of the frame, off screen, and his eyebrows are drawn slightly together in a grim, thoughtful look. Mouth closed. Keep everything else exactly identical: head angle, framing, face shape, hat, hand, ticket, clothes, background, colors, lighting.
```

## S3_k2_talk (Edit: S3_k2 üzerinde)
```
Edit the attached image. Change ONLY the mouth: slightly open, speaking almost in a whisper. Keep everything else exactly identical, including the eyes looking to the left.
```

---

# EŞYA

## PR_ticket (kapanıştaki delil kartı için)
```
Single object only, centered, on a perfectly flat solid chroma green background (#00B140), no shadow, 1:1 square, no watermark.

Art style: semi-realistic 2D animated film prop illustration, clean ink linework, cel-shaded flat colors, subtle paper texture. Not photorealistic, not 3D.

A small unused 1940s Australian railway ticket made of thick pale green card (#B9C4A6), rectangular with slightly worn rounded corners, slightly tilted, seen from above. Thin decorative printed border lines. Any printed lettering is tiny, faded and unreadable. No hole punch, because it was never used.
```

---

# SES (ElevenLabs)

## Diyaloglar (her satır ayrı mp3)
Memur sesi: genç Avustralyalı erkek, gergin. Dedektif sesi: 40'larında Avustralyalı erkek, alçak, sakin, hafif boğuk.

| Dosya | Karakter | Metin |
|---|---|---|
| D1 | Memur | Found him like this, sir. Couple of blokes on the beach saw him. |
| D2 | Dedektif | Anyone know who he is? |
| D3 | Dedektif | No papers. Nothing with a name on it. But a train ticket. |
| D4 | Dedektif | Bought a ticket and never used it. |
| D5 | Dedektif | So who are you, mate? |

## Efektler (ElevenLabs Sound Effects)
| Dosya | Prompt |
|---|---|
| SFX_waves | calm ocean waves gently rolling onto a sandy beach, early morning, no wind gusts, 20 seconds |
| SFX_gull | single distant seagull call over the sea |
| SFX_steps | slow footsteps of leather shoes walking on soft dry sand |
| SFX_cloth | soft fabric rustle of a wool jacket being moved |
| SFX_crowd | faint distant murmur of a few people talking on a beach, far away |
| SFX_stamp | old typewriter keys followed by a heavy rubber stamp hitting paper |
