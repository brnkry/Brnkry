# Salata 01: Pancarlı renkli salata (Google Flow, devam ettirmeli plan)

Referans: Yemek_Kelebegi, Facebook Reels. Hedef: 9:16, yaklaşık 18 sn, döngü, seslendirme yok.
Yöntem: Tek sabit kamera, kesintisiz çekim. 5 parça üretilir, her parça bir öncekinin son karesinden devam eder (Extend). 40 sn ham görüntüden kurguda hızlı kesimlerle 18 sn çıkarılır.

## Referans görseller (önce bunlar üretilir)

**Görsel A (başlangıç karesi, boş kase)**
```
Photorealistic food photography, vertical 9:16. An empty large light acacia wood salad bowl on a woven bamboo placemat, on a bright white marble kitchen counter. Camera at a 45 degree high angle, close, the bowl fills the lower half of the frame. Soft natural daylight from a window on the left. A small terracotta pot of fresh basil softly blurred in the background on the right. Shallow depth of field, clean, bright, no text, no people.
```

**Görsel C (sos parçasının başlangıç karesi)**
```
Photorealistic food photography, vertical 9:16. A small white porcelain sauce jug with a thin black rim and a spout, empty, on a woven bamboo placemat on a white marble counter, close-up at a 45 degree high angle, a large wooden salad bowl full of colorful shredded salad softly blurred behind it, soft daylight from the left, shallow depth of field, no text, no people.
```

## Parça planı

| Parça | Yöntem | Referans | İçerik |
|---|---|---|---|
| P1 | Frames to Video | Görsel A (ilk kare) | Pancar, havuç, lahana |
| P2 | Extend | P1 | Mısır, nar, maydanoz, ceviz |
| P3 | Frames to Video | Görsel C (ilk kare) | Sos: sarımsak, limon, zeytinyağı, nar ekşisi, karıştırma |
| P4 | Extend | P2 | Sosu dökme, karıştırma |
| P5 | Extend | P4 | Durgun final ve çatalla lokma |

Promptlar sohbette ve aşağıda.

### P1
```
One continuous shot, fixed locked-off camera at a 45 degree high angle, no camera movement. An empty large light acacia wood salad bowl on a woven bamboo placemat, white marble kitchen counter, soft daylight from the left, a basil pot blurred in the background.
0 to 2 seconds: a hand in a clear transparent food-safe glove enters from the top left holding a small white porcelain bowl and tips it, finely julienned raw beetroot tumbles down and lands in a loose crimson pile in the center of the bowl, the hand leaves the frame.
3 to 5 seconds: the gloved hand returns with another small white bowl and tips finely grated bright orange carrot onto the right side of the beetroot, then leaves.
6 to 8 seconds: the gloved hand returns and pours finely shredded purple red cabbage onto the left side, the purple strands bounce as they land.
Photorealistic, appetizing, vivid natural colors, crisp detail, shallow depth of field, real-time speed. Audio: crisp ASMR sounds of vegetables landing in a wooden bowl, soft rustling, no music, no voice. No text, no faces, no logos.
```

### P2 (Extend)
```
Continue the same continuous shot, exact same fixed camera angle, same bowl, same lighting, the salad stays in place.
0 to 2 seconds: the gloved hand tips a small white bowl of sweet yellow corn kernels into the center, the kernels scatter over the purple, orange and crimson strands.
2 to 4 seconds: the gloved hand pours glistening red pomegranate seeds over the salad, they bounce like jewels.
4 to 6 seconds: the gloved hand tips a small white bowl of finely chopped fresh flat leaf parsley on top, a bright green layer covers the middle.
6 to 8 seconds: the gloved hand scrapes roughly chopped walnuts off a small wooden cutting board with a knife onto the parsley.
Photorealistic, vivid natural colors, real-time speed. Audio: ASMR sounds of corn and pomegranate seeds pattering, soft herb rustle, walnuts sliding, no music, no voice. No text, no faces.
```

### P3
```
One continuous shot, fixed locked-off close-up camera at a 45 degree high angle on a small white porcelain sauce jug with a thin black rim, standing on a bamboo placemat, a colorful salad bowl blurred behind it, soft daylight from the left.
0 to 2 seconds: a hand in a clear transparent food-safe glove squeezes a metal garlic press over the jug, fresh crushed garlic drops inside.
2 to 4 seconds: the gloved hand squeezes half a lemon in a black citrus press, juice streams into the jug.
4 to 5.5 seconds: golden olive oil pours in a thin glossy stream from a dark green glass bottle into the jug.
5.5 to 6.5 seconds: thick dark red pomegranate molasses drizzles in from a spoon.
6.5 to 8 seconds: the gloved hand whisks it with a small spoon into a glossy pinkish brown dressing.
Photorealistic, real-time speed. Audio: garlic press crunch, lemon squeeze, liquid pouring, spoon clinking on porcelain, no music, no voice. No text, no faces.
```

### P4 (Extend P2)
```
Continue the same continuous shot, exact same fixed camera angle, same bowl and salad.
0 to 3 seconds: the gloved hand tilts a small white porcelain sauce jug with a thin black rim and pours a smooth stream of pinkish brown dressing over the walnuts and parsley in a circle.
3 to 8 seconds: two wooden salad servers toss the whole salad, purple cabbage, orange carrot, crimson beetroot, green parsley, corn, walnuts and pomegranate seeds mix together evenly and glisten with dressing, the salad turns a rich deep red with color flecks.
Photorealistic, vivid natural colors, real-time speed. Audio: dressing pouring, crisp wet tossing sounds, no music, no voice. No text, no faces.
```

### P5 (Extend P4)
```
Continue the same continuous shot, exact same fixed camera angle.
0 to 3 seconds: the servers leave the frame, the fully mixed glistening salad sits still in the wooden bowl, a single parsley leaf settles on top.
3 to 8 seconds: a gloved hand with a silver fork lifts a generous forkful of the salad slowly up toward the camera, dressing glistens on the crimson and orange strands, a walnut piece and pomegranate seeds visible on the fork, the bowl blurs behind.
Photorealistic, appetizing, shallow depth of field, real-time speed. Audio: soft fork scrape and crunch, no music, no voice. No text, no faces.
```

## Kurgu (bizde)
P1 + P2 + P3 + P4 + P5 = yaklaşık 40 sn ham. Her malzeme dökümünden en iyi 1 sn alınır, video P4'teki karıştırma ile başlar, döngü kurulur. Hedef 17 ile 19 sn. Veo sesi beğenilirse kullanılır, değilse ElevenLabs efektleri ve hafif müzik eklenir.

## Notlar
- Facebook'ta yüklerken "AI ile oluşturuldu" etiketini aç.
- Set ve tarif bizim, referans sayfanın yeşil bitkisi ve birebir kurgusu kopyalanmıyor.
