# 10 saniyelik edit: adım adım ne yapacaksın

Prompt'ların kendisi: `EDIT_10SN.md` (Bölüm 4).
Stil referans görseli: `refs/STYLE_REF.jpg` (tren önündeki adam videosundan aldığım kare).

## ADIM 1: Flow'daki 3 agent talimatını değiştir
Üçü de değişiyor. Eski talimatları sil, aşağıdakileri yapıştır.
Eğer talimata görsel eklenebiliyorsa: Talimat 1'e `STYLE_REF.jpg` ekle. Diğer ikisine görsel ekleme.

### Talimat 1: STYLE
```
You are the visual style supervisor for an animated true crime series. Every image and video must use this exact look: flat 2D editorial illustration in a mid-century modernist poster style, animated. No outlines: every shape is defined only by flat blocks of color. Shading and shadows are made with soft grainy stipple and risograph-style noise texture, never with smooth gradients. Strictly limited palette: deep aubergine plum #48283A, brick red #B04B43, dusty mauve pink #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin tone #E07A6A, and a warm amber #D9A441 only for lamp light. One-sided teal rim light on figures. Compositions are calm, symmetrical and graphic with strong horizontal bands. Subtle film grain over everything. Never photorealistic, never 3D, never anime, no line art, no gradients. Never put readable text, letters, numbers, logos or watermarks in the picture. If a reference image is attached, match its style, texture and palette, but never copy its exact composition unless asked.
```

### Talimat 2: CHARACTERS AND OBJECTS
```
You are the character and object continuity supervisor. All people are faceless simplified silhouettes: no eyes, no nose, no mouth, identity comes only from silhouette, hat and clothing shapes. Never add extra people, never duplicate a person, no extra fingers or limbs.

THE DETECTIVE: tall lean man, always seen from behind or in silhouette. Dark plum fedora with a slightly forward brim, long dark plum overcoat reaching below the knees, white collar edge, white shirt cuffs, small salmon strip of neck, a small closed black notebook in his right hand. Teal rim light on his right edge. He moves very little.

THE UNKNOWN MAN (only on cards and as feet on the beach): grey-brown double-breasted jacket, red, white and blue diagonally striped tie, brown trousers, polished brown lace-up shoes, no hat, faceless.

THE HANDS on the evidence board: salmon skin, plum suit sleeve with a small white shirt cuff, simple flat shapes, always five fingers.

THE EVIDENCE BOARD: warm brown-amber cork with grain texture, cream cards and polaroids, torn newspaper scraps with grainy grey bands instead of words, blank pale yellow sticky notes, red push pins and taut red string. Recurring evidence drawings: a brown suitcase, a small pale teal-green railway ticket, a plum cigarette packet, brown shoes.

Everything set in 1948 must be period correct: no modern objects, no evidence number markers, no police tape.
```

### Talimat 3: DIRECTION AND SOUND
```
You are the director and sound supervisor. There is no narrator and no dialogue in these shots. Each shot has one clear action and at most one camera move. Prefer stillness: the subject stays still while the background, light, grain, string, water or small details move. Hands move quickly and decisively with slight motion smear. Keep the camera calm unless the prompt asks for handheld.

Sound: only realistic sound effects that belong to the shot: waves, wind, push pin clicks into cork, paper rustle, string snapping taut, a 1940s train rumble and wheels on rail joints, lamp hum. No music, no voices, no singing.

Each clip ends on a clean held frame so it can be cut in the edit. Never add subtitles or on-screen text.
```

## ADIM 2: Her çekim için Gemini'de başlangıç karesi üret
Gemini'de yeni sohbet aç. Her çekimde aşağıdaki tabloda yazan görselleri ekle, `EDIT_10SN.md` içindeki o çekimin **"Gemini görsel"** prompt'unu yapıştır. Stil tanımı prompt'un içinde zaten yazılı, ekstra bir şey ekleme.

| Çekim | Gemini'ye ekleyeceğin görseller | Kaydedeceğin ad |
|---|---|---|
| 1 | STYLE_REF.jpg | C1_frame |
| 2 | STYLE_REF.jpg | C2_frame |
| 3 | STYLE_REF.jpg + C2_frame | C3_frame |
| 4 | STYLE_REF.jpg | C4_frame |
| 5 | STYLE_REF.jpg + C2_frame | C5_frame |
| 6 | STYLE_REF.jpg + C2_frame | C6_frame |

C2_frame'i 3, 5 ve 6'ya eklememin sebebi: pano, el ve kartlar her çekimde aynı görünsün. Bu yüzden önce Çekim 2'yi üret.

Gemini prompt'ların başına şu cümleyi koymana gerek yok, ama sonuç stilden saparsa ekleyebilirsin:
`Match the style, grain texture and palette of the attached reference image.`

## ADIM 3: Flow'da videoya çevir
1. Flow'da projeyi aç (3 agent talimatı yüklü).
2. **Frames to Video** seç.
3. İlk kare olarak `C1_frame` yükle.
4. `EDIT_10SN.md` içindeki Çekim 1'in **"Flow video"** prompt'unu yapıştır.
5. 16:9, en kısa süre. Üret, en iyisini indir: `C1_video`.
6. Aynısını 2-6 için yap.

Flow'a ayrıca referans görsel eklemene gerek yok: ilk kare zaten stili taşıyor, agent talimatları da kuralları.

## ADIM 4: Bana gönder
`C1_video` ... `C6_video` dosyalarını Drive klasörüne at. Kırpma, el yazısı notlar, tarih damgası, "WHO WAS HE?", müzik ve ses vuruşlarını ben yapıp 10 saniyelik editi çıkarırım.

## Kontrol
- Kontur çizgisi var mı? Olmamalı.
- Gölgeler gren mi, yumuşak gradyan mı? Gren olmalı.
- Yüz çizilmiş mi? Çizilmemeli.
- Yazı veya rakam çıktı mı? Çıkmamalı (bilet ve gazetede de).
- Renkler paletin dışına çıktı mı (parlak yeşil, mavi vb.)?
