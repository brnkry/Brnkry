# The Somerton Man: 1 dakikalık video (70 sn), tüm prompt'lar

Anlatım: ElevenLabs "Matt - Deep Authoritative Narrator", eleven_v3. Dosya: `exports/somerton_anlatim_v1.mp3` (sessizlikler kısaltıldı, 70 sn).

## Kullanım
- Flow agent talimatları aynen kalıyor (3 tane, değiştirme).
- Her yeni çekim: Gemini'de tabloda yazan görselleri ekle + "Gemini" prompt'unu yapıştır → kaydet. Flow'da **Frames to Video**, ilk kare o görsel + "Flow" prompt'u.
- Her Flow prompt'unda süre yazılı. Flow uzun klip üretse bile hareket o sürede bitip donuyor, ben gerisini keserim.
- "MEVCUT" yazan çekimler: elindeki C1-C6 videoları. Yeniden üretme.

## Sahne planı (anlatıma göre)
| # | Zaman | Anlatım | Görüntü | Kaynak |
|---|---|---|---|---|
| 01 | 0.0-3.1 | December first, 1948. | Kumda ayakkabılar | MEVCUT C1 |
| 02 | 3.1-9.5 | Somerton Beach... found lying against the sea wall. | Geniş sahil | YENİ N1 (6 sn) |
| 03 | 9.5-12.0 | Neat suit. Polished shoes. | Ceket ve kravat yakın | YENİ N2 (3 sn) |
| 04 | 12.0-14.9 | No hat. No papers. No name. | Kart iğneleniyor | MEVCUT C2 |
| 05 | 14.9-17.6 | Every label... cut away. | Kesilmiş etiket | YENİ N3 (3 sn) |
| 06 | 17.6-20.8 | ...a train ticket he never used. | Bilet makro | MEVCUT C5 |
| 07 | 20.8-23.6 | Six weeks later... | Peron ve tren | MEVCUT C4 |
| 08 | 23.6-27.5 | ...a brown suitcase... Inside, more clothes. | Emanette bavul açılıyor | YENİ N4 (4 sn) |
| 09 | 27.5-30.3 | Most of the labels? Cut out too. | Not ve kırmızı ip | MEVCUT C3 |
| 10 | 30.3-32.7 | Then, the strangest clue of all. | Lamba altında dedektif | YENİ N5 (3 sn) |
| 11 | 32.7-37.4 | Rolled up in a tiny hidden pocket... | Gizli cepten kağıt | YENİ N6 (5 sn) |
| 12 | 37.4-40.1 | Tamam Shud. It is ended. | Açılan kağıt parçası | YENİ N7 (3 sn) |
| 13 | 40.1-43.2 | ...a book of Persian poetry. | Eski şiir kitabı | YENİ N8 (3 sn) |
| 14 | 43.2-46.9 | ...the last page was missing. | Yırtık son sayfa | YENİ N9 (4 sn) |
| 15 | 46.9-50.5 | ...a code that no one has ever cracked. | Şifre sayfası | YENİ N10 (4 sn) |
| 16 | 50.5-54.0 | Doctors suspected poison... | Laboratuvar | YENİ N11 (4 sn) |
| 17 | 54.0-56.8 | For seventy-four years, he had no name. | Mezar taşı | YENİ N12 (3 sn) |
| 18 | 56.8-60.4 | Then, in 2022, DNA gave him one. | DNA sarmalı | YENİ N13 (4 sn) |
| 19 | 60.4-63.4 | Carl Webb, an engineer from Melbourne. | Kartın altına isim | YENİ N14 (3 sn) |
| 20 | 63.4-67.0 | But how he died, and why... | Akşam sahilde dedektif | YENİ N15 (4 sn) |
| 21 | 67.0-70.3 | So who was the Somerton Man? | Geniş pano + başlık | MEVCUT C6 |

**Yazıları ben ekleyeceğim:** tarih, "LABELS CUT", "TAMÁM SHUD", şifre satırları, "UNKNOWN MAN", "CARL WEBB", "WHO WAS HE?". Bu yüzden prompt'larda yazı yasak.

---

## N1: Geniş sahil (6 sn)
**Gemini'ye ekle:** STYLE_REF + C1_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A. Faceless people. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Match the beach colors of the attached beach image.
Wide, calm, symmetrical shot of Somerton Beach, South Australia, early morning in 1948. Pale cream sky, a flat teal sea band with soft cream foam lines, wide salmon-beige sand. A low cream-and-mauve stone sea wall runs horizontally across the middle of the frame. Small in the left third, a man in a grey-brown suit lies on the sand with his head and shoulders against the base of the wall, legs stretched out, ankles crossed, peaceful. Far right, two small faceless figures walk along the shoreline toward him: one in a dark plum police uniform with a peaked cap, one in a plum overcoat and fedora. Long soft grainy shadows. Lots of empty space. Quiet and eerie.
```
**Flow (ilk kare N1):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 6 seconds long. Video length: 6 seconds.
0 to 6 seconds: the two small figures walk slowly from the right toward the man by the wall, steady pace, still far from him at the end. Gentle waves roll in and out along the shore, foam lines slide sideways. A very slow camera push in toward the man lying by the wall. The man by the wall never moves.
Sound: soft waves, light wind, distant gull. No music, no voices.
Avoid: people running, faces, blood, text, numbers, modern objects, outlines, 3D.
```

## N2: Ceket ve kravat (3 sn)
**Gemini'ye ekle:** STYLE_REF + C1_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark.
Close-up from above of the chest of a man lying on pale sand: a neat grey-brown double-breasted jacket with four buttons, a brown knitted pullover, a cream shirt collar and a tie with thin red, white and blue diagonal stripes. His face is out of frame at the top edge. A few grains of sand on the lapel. Soft grainy morning shadow from the right. Calm, still, respectful. Nothing graphic.
```
**Flow (ilk kare N2):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 3 seconds: very slow camera slide upward along the tie toward the collar, stopping before any face appears. A light breeze lifts the tip of the tie slightly and a few sand grains roll off the lapel. The man does not move.
Sound: light wind, faint distant waves. No music, no voices.
Avoid: showing the face, blood, text, outlines, 3D.
```

## N3: Kesilmiş etiket (3 sn)
**Gemini'ye ekle:** STYLE_REF + C2_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Match the hands and sleeves of the attached board image.
Macro close-up of the inside back collar of a grey-brown jacket lying on a dark plum table under warm amber lamp light. Two hands with plum suit sleeves and white cuffs fold the collar open with the fingertips. Inside the collar, a small empty rectangle of slightly darker fabric with a few short loose threads where a clothing label has been cut away. Shallow depth of field, everything outside the collar softly blurred.
```
**Flow (ilk kare N3):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 1 second: the fingers fold the collar open a little wider.
1 to 3 seconds: the hands hold still, the loose threads in the empty label spot tremble slightly. Slow push in on the empty rectangle.
Sound: soft fabric rustle. No music, no voices.
Avoid: a label appearing, scissors, text, extra fingers, outlines, 3D.
```

## N4: Emanette bavul (4 sn)
**Gemini'ye ekle:** STYLE_REF + C4_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Match the colors of the attached railway image.
Frontal, symmetrical view of a 1940s railway station cloakroom counter: a long brick-red wooden counter, behind it tall shelves of luggage in plum and mauve shapes. In the center of the counter, a closed brown leather suitcase with two straps, facing the camera. Two hands with plum sleeves and white cuffs rest on its two latches. Warm amber light from a hanging lamp above. Grainy shadows.
```
**Flow (ilk kare N4):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 4 seconds long. Video length: 4 seconds.
0 to 1 second: the hands flip both latches open with a snap.
1 to 3 seconds: the lid lifts up and back, revealing neatly folded clothes inside in plum, grey-brown and cream shapes.
3 to 4 seconds: hold. The hanging lamp sways very slightly.
Sound: two latch snaps, leather creak, quiet station echo. No music, no voices.
Avoid: faces, readable labels, text, extra fingers, outlines, 3D.
```

## N5: Lamba altında dedektif (3 sn)
**Gemini'ye ekle:** STYLE_REF + C4_frame + C6_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. The detective must look exactly like the man on the railway platform image; the board like the attached evidence board image.
A dim office at night. The detective stands with his back to the camera in the center: faceless, dark plum fedora, long dark plum overcoat, white collar edge, teal rim light on his right side. In front of him, the cork evidence board on the wall under a single amber lamp, cards and red strings. Everything outside the lamp cone falls into grainy plum darkness. Symmetrical.
```
**Flow (ilk kare N5):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 3 seconds: slow camera push in over the detective's shoulder toward the board. The detective stays completely still. The lamp flickers once. Dust specks drift in the light cone.
Sound: low lamp hum, one faint flicker buzz. No music, no voices.
Avoid: the detective turning, a face, readable text, outlines, 3D.
```

## N6: Gizli cepten kağıt (5 sn)
**Gemini'ye ekle:** STYLE_REF + C2_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Match the hands of the attached board image.
Macro close-up of the waistband of brown trousers lying flat on a dark plum table under amber lamp light. Just below the waistband, a tiny hidden fob pocket. Two fingertips with a plum sleeve and white cuff have just pulled out the end of a tiny tightly rolled cream paper scroll, half out of the pocket. Very shallow depth of field.
```
**Flow (ilk kare N6):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 5 seconds long. Video length: 5 seconds.
0 to 2 seconds: the fingertips slowly draw the tiny rolled paper all the way out of the pocket.
2 to 4 seconds: the fingers lift it toward the camera into the lamp light and turn it once.
4 to 5 seconds: hold, slight push in on the tiny scroll.
Sound: tiny fabric rub, paper rustle, lamp hum. No music, no voices.
Avoid: the paper unrolling, text, extra fingers, outlines, 3D.
```

## N7: Açılan kağıt (3 sn)
**Gemini'ye ekle:** STYLE_REF + C2_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark.
Top-down macro of a dark plum desk under a warm amber lamp. In the exact center, a small curled strip of cream paper, still partly rolled at both ends, held flat by two brass tweezers tips at the left and right edges. The middle of the strip is blank and empty. Grainy soft shadow under the paper. Locked, centered composition.
```
**Flow (ilk kare N7):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 1.5 seconds: the tweezers slowly pull the two ends apart and the paper strip flattens out fully, staying in the exact center of the frame.
1.5 to 3 seconds: hold perfectly still. Static locked camera.
Sound: soft paper uncurl, lamp hum. No music, no voices.
Avoid: any writing on the paper, text, letters, camera movement, outlines, 3D.
```

## N8: Şiir kitabı (3 sn)
**Gemini'ye ekle:** STYLE_REF + C2_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark.
A small old hardback book lying closed on a dark plum desk under amber lamp light, seen from a low three-quarter angle. Its cover is muted teal with a simple brick-red and cream ornamental border pattern of Persian style arches and vines, no title, no letters. Soft grainy shadow. Shallow depth of field.
```
**Flow (ilk kare N8):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 1 second: the cover lifts open on its own as if by a draft.
1 to 3 seconds: cream pages flutter and turn quickly from right to left, then settle. Slow push in.
Sound: book cover creak, pages fluttering. No music, no voices.
Avoid: readable text on pages, hands, outlines, 3D.
```

## N9: Yırtık son sayfa (4 sn)
**Gemini'ye ekle:** STYLE_REF + N8_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Same book as the attached image.
Top-down view of the same small book lying open near its end on the dark plum desk. On the right-hand page, only grainy grey bands where lines of text would be, and at the bottom of the page a rough torn-out gap where a piece of the paper has been ripped away, showing the plum desk through it. A hand with a plum sleeve and white cuff rests at the left edge, one finger pointing at the torn gap. Warm amber light.
```
**Flow (ilk kare N9):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 4 seconds long. Video length: 4 seconds.
0 to 1 second: the finger slides slowly toward the torn gap and stops at its edge.
1 to 4 seconds: hold, slow push in on the torn gap, its ragged paper fibres tremble slightly.
Sound: soft paper rustle, lamp hum. No music, no voices.
Avoid: readable text, the gap closing, extra fingers, outlines, 3D.
```

## N10: Şifre sayfası (4 sn)
**Gemini'ye ekle:** STYLE_REF + N8_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Same book as the attached image.
Straight-on close-up of the inside back cover of the same small book, a plain cream page filling most of the frame, completely blank, with only a faint diagonal grainy smudge. On the right edge, a short pencil lies on the desk. Warm amber light from the upper left, soft grainy vignette. Static, centered.
```
**Flow (ilk kare N10):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 4 seconds long. Video length: 4 seconds.
0 to 4 seconds: a very slow push in on the blank cream page. A soft beam of light slowly sweeps across the page from left to right like a torch. The page stays blank and still.
Sound: low ominous room tone. No music, no voices.
Avoid: any writing or marks appearing on the page, hands, text, letters, numbers, outlines, 3D.
```

## N11: Laboratuvar (4 sn)
**Gemini'ye ekle:** STYLE_REF
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark.
A 1940s pathology laboratory bench seen straight on and symmetrical. Teal tiled wall behind. On the bench: a row of glass bottles and flasks in mauve and cream shapes, a brass microscope in the center, a rack of test tubes on the right. A faceless doctor in a cream lab coat stands behind the bench, holding one test tube up at eye level with a salmon hand, a little teal liquid inside. Cool teal light from a high window on the left.
```
**Flow (ilk kare N11):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 4 seconds long. Video length: 4 seconds.
0 to 2 seconds: the doctor gently swirls the test tube; the teal liquid circles inside.
2 to 4 seconds: he lowers it slowly and holds still. A tiny bubble rises in one flask. Slow push in on the test tube.
Sound: glass clink, quiet liquid swirl, distant clock tick. No music, no voices.
Avoid: a face, smoke, skulls, blood, text, labels, outlines, 3D.
```

## N12: Mezar taşı (3 sn)
**Gemini'ye ekle:** STYLE_REF
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark.
A quiet cemetery in Adelaide, seen straight on and symmetrical. In the center, a simple upright cream headstone with a rounded top, its face completely blank and smooth. Short dry grass around it, a few small mauve flowers at its base. Behind it, rows of small plum headstones fading into a grainy teal dusk sky. One bare tree on the right. Long soft shadows.
```
**Flow (ilk kare N12):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 3 seconds: a few dry leaves drift across the frame from right to left, the grass sways gently, the light slowly dims from dusk toward night. Very slow push in on the blank headstone. The headstone stays blank.
Sound: soft wind, rustling leaves. No music, no voices.
Avoid: any writing on the headstone, people, text, outlines, 3D.
```

## N13: DNA sarmalı (4 sn)
**Gemini'ye ekle:** STYLE_REF
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark.
A single tall DNA double helix in the center of the frame, made of flat paper-cut shapes: two twisting ribbons in brick red and teal, connected by short cream and mauve rungs. Dark grainy plum background with a soft cream glow behind the helix. Clean, graphic, symmetrical.
```
**Flow (ilk kare N13):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 4 seconds long. Video length: 4 seconds.
0 to 4 seconds: the DNA helix slowly rotates around its vertical axis, rungs passing in front and behind, while the camera slowly pushes in. The cream glow pulses softly once.
Sound: soft low hum, gentle shimmer. No music, no voices.
Avoid: realistic 3D rendering, text, numbers, outlines.
```

## N14: Kartın altına isim (3 sn)
**Gemini'ye ekle:** STYLE_REF + C2_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A, amber #D9A441. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. Same board, same portrait card and same hands as the attached image.
The same cork evidence board, close-up straight on. In the center, the same pinned cream card with the faceless man in the grey-brown jacket and striped tie. Directly below it, a hand with a plum sleeve and white cuff holds a blank cream paper strip against the board, about to pin it with a red push pin held in the other hand. Warm amber light from above.
```
**Flow (ilk kare N14):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 3 seconds long. Video length: 3 seconds.
0 to 1 second: the hand pins the blank paper strip under the portrait with one firm press.
1 to 2 seconds: both hands slide out of frame to the right.
2 to 3 seconds: hold, the strip stays perfectly still and blank, slight push in.
Sound: one push pin click, paper rustle. No music, no voices.
Avoid: writing on the strip, text, letters, a face on the portrait, extra fingers, outlines, 3D.
```

## N15: Akşam sahilde dedektif (4 sn)
**Gemini'ye ekle:** STYLE_REF + C4_frame + C1_frame
```
A single still frame, 16:9 landscape. Flat 2D editorial illustration in a mid-century modernist poster style. No outlines: every shape is a flat block of color. Shading made with grainy stipple and risograph-style noise, never smooth gradients. Limited palette: aubergine plum #48283A, brick red #B04B43, dusty mauve #B0697A, muted teal #4F7A80, warm cream #F6F1E8, salmon skin #E07A6A. Subtle film grain. Not photorealistic, not 3D, no line art, no text, no letters, no numbers, no watermark. The detective must look exactly like the man on the attached railway platform image.
Somerton Beach at dusk, seen straight on and symmetrical. In the exact center, the detective stands alone on the sand with his back to the camera, faceless, dark plum fedora and long plum overcoat, teal rim light on his right edge, looking out to sea. Behind him, a flat teal sea with cream foam lines and a low brick-red sun half sunk into the horizon, a mauve sky with grainy bands. His long shadow stretches toward the camera.
```
**Flow (ilk kare N15):**
```
Continue from the provided first frame. Keep the exact flat grainy editorial illustration style and palette. Not photorealistic, not 3D. Generate a video that is exactly 4 seconds long. Video length: 4 seconds.
0 to 4 seconds: the detective stands completely still. Waves roll in slowly, foam lines slide toward his feet and back. The sun sinks a little lower, the sky darkens slightly. His coat hem moves in the wind. Locked static camera.
Sound: slow waves, wind. No music, no voices.
Avoid: the detective turning or walking, a face, text, outlines, 3D.
```
