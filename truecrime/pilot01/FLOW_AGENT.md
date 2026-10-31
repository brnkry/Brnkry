# Pilot 01: Google Flow kurulumu (agent talimatları + Sahne 1)

## 0. Hazırlık (Gemini, 2 görsel)

### L1_beach: yeşil gökyüzünü gerçek gökyüzüyle değiştir
Gemini'ye `S1_fg` ve `S1_bg` görsellerini birlikte yükle:
```
Edit the first image. Replace ALL of the flat green area with the pale early morning summer sky from the second image: soft blue sky, a few thin high clouds, warm golden glow low on the right. Keep the sea wall, steps, sand, houses and Norfolk pines exactly as they are, same style, same colors, same composition. 16:9 landscape. No people, no text, no watermark.
```

### Karakter kırpımları
Karakter sayfalarından tek bir tam boy görünüm kes (telefonda kırpma yeterli):
- `DET_01_ref`: DET_01_sheet içinden **3/4 görünüm** (soldan ikinci tam boy figür)
- `CON_01_ref`: CON_01_sheet içinden **3/4 görünüm**
- `VIC_01_ref`: olduğu gibi kullan

Flow'a çok panelli sayfa verince bazen aynı kişiyi sahnede iki kez çiziyor. Tek figür daha güvenli.

---

## 1. AGENT TALİMATLARI

### Talimat 1: STYLE AND WORLD
Görsel ekleyebiliyorsan: `L1_beach`
```
You are the visual style and world supervisor for an animated true crime series. Every image and video must use this exact look: semi-realistic 2D animated feature film style with a noir graphic novel look, clean confident black ink linework, realistic adult human proportions, cel-shaded flat colors with soft two-tone shadows, hand-painted backgrounds, subtle film grain, muted 1940s palette. Never photorealistic, never 3D, never anime, never cartoonish, never chibi.

Episode 1 setting: Somerton Beach near Adelaide, South Australia, early morning of 1 December 1948, early summer. Clear calm morning, low warm sunlight from the right, long soft shadows, light sea breeze, gentle waves. An old waist-high concrete and stone sea wall runs along the beach with a short flight of steps at one end. Behind the wall: modest 1940s seaside houses with tiled roofs and tall Norfolk pines. Pale sand with footprints and small tufts of dry grass.

Everything must be period correct for 1948 Australia: no modern clothing, cars, signs, plastic, phones or buildings. Never put text, captions, subtitles, logos or watermarks in the picture. Never show blood, wounds or anything graphic; death is shown calmly and respectfully. Keep the camera cinematic and calm: one main action and at most one camera move per shot, no shaky cam, no sudden cuts inside a clip. Keep the same light direction and time of day in every clip of this location.
```

### Talimat 2: CHARACTERS
Görsel ekleyebiliyorsan: `DET_01_ref`, `CON_01_ref`, `VIC_01_ref`
```
You are the character continuity supervisor. Use these fixed designs in every shot and never change them. Never swap features or clothes between characters. Never add extra people unless the shot asks for them, never duplicate a character, no extra fingers or limbs.

DET_01, the detective: Australian police detective in 1948, man in his mid forties, lean and tall. Long narrow face, strong square jaw, deep-set tired grey eyes, heavy straight dark eyebrows, short neat dark brown mustache, light stubble. Short dark brown hair with grey at the temples. Mid-grey felt fedora with a black band and a slightly forward brim. Charcoal grey single-breasted wool suit, jacket buttoned, white shirt, dark navy tie with a small tie clip, black leather shoes. Carries a small black leather notebook in his left hand. Calm, observant, serious. Voice: low, calm, slightly husky Australian man in his forties, speaks quietly.

CON_01, the constable: young South Australian police constable in 1948, early twenties, slim, average height. Round open face, clean shaven, slightly sunburnt cheeks, wide brown eyes, thin arched eyebrows, a few freckles on the nose, short light brown hair. Dark navy police uniform: peaked cap with black visor and small silver badge, buttoned tunic with a single row of silver buttons, black leather belt, whistle chain, navy trousers, polished black boots. Eager but nervous. Voice: young Australian man in his twenties, a little tense and breathless.

VIC_01, the unknown man: well-dressed man in his forties, tall, athletic build, short neatly combed light brown hair, clean shaven, no hat. Grey-brown double-breasted jacket, brown knitted pullover, white shirt, tie with thin red, white and blue diagonal stripes, brown trousers, polished brown lace-up shoes. He lies on his back on the sand with his head and shoulders resting against the base of the sea wall, legs stretched out with the ankles crossed, arms relaxed at his sides, eyes closed, peaceful as if asleep. He NEVER moves, never opens his eyes, never speaks. Never show injuries. Avoid close-ups of his face.
```

### Talimat 3: DIRECTION, SOUND AND CONTINUITY
Görsel gerekmez.
```
You are the director and sound supervisor. There is NO narrator. The story is told only through what the characters say and natural sound.

Dialogue: English with Australian accents. Only characters visible in the shot speak. Lines are short and natural, spoken exactly as written in the prompt, no extra words, no singing. Lip movement must match the speaking character only.

Sound: realistic ambient sound only: gentle waves, light wind, occasional distant seagulls, footsteps on soft sand, fabric rustle, faint distant murmur of a few onlookers. No music. No sound effects that do not belong to 1948.

Continuity for this location: the sea wall runs across the frame; the unknown man lies against the wall on the LEFT side of the frame, head to the left, feet to the right. The constable stays near the man's feet. The detective arrives from the RIGHT and faces left toward the man. Keep this screen direction in every clip. Each clip ends on a clear, held final pose so the next clip can continue from it. Never add on-screen text or subtitles.
```

---

## 2. SAHNE 1 (ilk 8-10 saniye)

### Yol A (önerilen): başlangıç karesi + Frames to Video
Sahnede 3 kişi + mekan var. Ingredients modunda genelde en fazla 3 referans kabul ediliyor, kurban dışarıda kalıyor. Bu yüzden önce Gemini'de başlangıç karesini üretmek daha güvenilir.

**Gemini, F1** (ekle: `DET_01_ref`, `CON_01_ref`, `VIC_01_ref`, `L1_beach`)
```
Use the attached images: the beach image is the location, the three people are the characters. Keep every face, costume, color and proportion exactly as in the references, and keep the location exactly as in the beach image.

A single cinematic still frame, 16:9 landscape, semi-realistic 2D animated feature film style with a noir graphic novel look, clean ink linework, cel-shaded flat colors, soft two-tone shadows, painterly background, subtle film grain. Not photorealistic, not 3D, not cartoonish. No text, no watermark.

Somerton Beach, early morning, 1 December 1948, low warm sun from the right. Medium wide shot at eye level. Left third: the well-dressed man in the grey-brown double-breasted jacket lies on his back on the sand, head and shoulders resting against the base of the sea wall, legs stretched toward the right, ankles crossed, eyes closed, peaceful, partly in the wall's shadow. Nothing graphic. Center: the young constable kneels on one knee beside the man's feet, looking up and to the right, nervous. Right edge: the detective in the grey fedora and charcoal suit is just entering the frame, walking left across the sand toward them, notebook closed in his left hand. Only these three people.
```

**Flow:** Frames to Video, ilk kare `F1`, 16:9, mümkün olan en uzun süre (8 sn ise 8). Prompt:
```
Continue from the provided first frame. Same art style, same characters, same location, same light.

0 to 2 seconds: the detective keeps walking left across the sand toward the wall with slow, steady steps; the constable watches him approach.
2 to 5 seconds: the constable stands up quickly, brushes sand off his knee and speaks.
5 to 8 seconds: the detective stops beside him, looks down at the still man by the wall, pauses, then answers quietly.
8 to 10 seconds: hold. The detective keeps looking at the man, the constable looks at the detective. Final pose held.

The man lying against the wall does not move at all.
Camera: static medium wide shot with a very slow push in.

Dialogue:
Constable (young, nervous, Australian): "Found him like this, sir. Couple of blokes on the beach saw him."
Detective (low, calm, Australian): "Anyone know who he is?"

Sound: gentle waves, light wind, a distant seagull, footsteps on sand. No music, no narrator.
Avoid: extra people, character redesign, style change, modern objects, subtitles, text, blood.
```

### Yol B: Ingredients to Video (başlangıç karesi olmadan)
Referanslar: `DET_01_ref`, `CON_01_ref`, `L1_beach`. Kurban metinle tarif edilir (Talimat 2'de zaten var). Prompt yukarıdakiyle aynı, ilk satırı şununla değiştir:
```
Use the references: the beach image is the location, the detective and the constable are the characters. The unknown man (described in the character instructions) lies against the base of the sea wall on the left side of the frame. Opening: medium wide shot, the constable kneels beside the man's feet, the detective enters from the right edge walking left.
```

### Klip 8 saniyeyse
Flow 10 saniye vermiyorsa: 8 saniyelik klibi üret, "Extend" ile 2-4 saniye uzat. Extend prompt'u:
```
The detective and the constable stand still beside the man by the wall. The detective slowly opens his notebook and looks down at the man. The constable glances at the sea. Gentle waves, light wind. No dialogue. Hold the final pose.
```

## 3. Kontrol listesi
- Dedektif şapkası, bıyığı ve takımı referansla aynı mı?
- Memur kasketi ve lacivert üniforması doğru mu?
- Kurban hiç kıpırdamadı mı, gözleri kapalı mı?
- Konuşan kişinin ağzı mı oynuyor?
- Arkada müzik veya anlatıcı sesi çıktı mı (çıkmamalı)?
- Ekranda yazı var mı (olmamalı)?
