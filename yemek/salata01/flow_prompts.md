# Salata 01: Pancarlı renkli salata (Google Flow adım adım)

Referans: Yemek_Kelebegi, Facebook Reels. Format: 9:16, 16 çekim, her çekim yaklaşık 1 sn, sonsuz döngü, seslendirme yok.
Malzemeler: pancar, havuç, kırmızı lahana, mısır, nar, maydanoz, ceviz. Sos: sarımsak, limon, zeytinyağı, nar ekşisi.

## ADIM 1: Proje
Flow'da yeni proje aç. En boy oranı **9:16 (dikey)**.

## ADIM 2: 3 referans görseli üret (görsel modu)
Her prompt için 4 görsel üret, en iyisini indir.

**Görsel A: SET**
```
Photorealistic food photography, vertical 9:16. An empty large light acacia wood salad bowl on a woven bamboo placemat, on a bright white marble kitchen counter. Camera at a 45 degree high angle, close, the bowl fills the lower half of the frame. Soft natural daylight from a window on the left. A small terracotta pot of fresh basil softly blurred in the background on the right. Shallow depth of field, clean, bright, no text, no people.
```

**Görsel B: EL VE KASE**
```
Photorealistic close-up, a hand wearing a clear transparent food-safe disposable glove holding a small round white porcelain bowl tilted forward, plain white background, soft daylight, no text.
```

**Görsel C: SOS SÜRAHİSİ**
```
Photorealistic close-up, a small white porcelain sauce jug with a thin black rim and a spout, empty, standing on a woven bamboo placemat on a white marble counter, soft daylight from the left, shallow depth of field, no text.
```

## ADIM 3: Agent'ları ekle
| Agent | Görsel | Ad | Açıklama |
|---|---|---|---|
| 1 | A | SET | Large light acacia wood salad bowl on a woven bamboo placemat, white marble counter, basil pot blurred in the background, camera fixed at a 45 degree high angle. Always the same scene. |
| 2 | B | HAND | Hand in a clear transparent food-safe glove, always gloved, never shows a face or arm tattoo. Holds small round white porcelain bowls. |
| 3 | C | JUG | Small white porcelain sauce jug with a thin black rim and spout, used for the salad dressing. |

## ADIM 4: Video ayarları
Video modu, model **Veo (Fast)**, 9:16, her prompt için 2 çıktı. Beğendiğin çekim olursa Quality ile yeniden üret.

## ADIM 5: 16 çekim
Her satırda hangi agent'ların seçileceği yazıyor. Promptları olduğu gibi yapıştır.

### 01 (SET + HAND)
```
The gloved hand tips a small white porcelain bowl of finely julienned raw beetroot into the empty wooden salad bowl, deep crimson strands tumble down and land in a loose pile. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 02 (SET + HAND)
```
The wooden salad bowl already holds a pile of crimson julienned beetroot. The gloved hand tips a small white bowl of finely grated bright orange carrot into it, the carrot falls on top of the beetroot. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 03 (SET + HAND)
```
The wooden salad bowl holds crimson beetroot and orange grated carrot. The gloved hand pours a small white bowl of finely shredded purple red cabbage into it, the purple strands bounce as they land and cover one side. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 04 (SET + HAND)
```
The wooden salad bowl is full of shredded purple cabbage, orange carrot and crimson beetroot. The gloved hand tips a small white bowl of sweet yellow corn kernels into the center, the kernels scatter over the colorful strands. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 05 (SET + HAND)
```
The wooden salad bowl is full of shredded purple cabbage, orange carrot and beetroot with yellow corn in the center. The gloved hand tips a small white bowl and glistening red pomegranate seeds rain down onto the salad, bouncing like jewels. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 06 (SET + HAND)
```
The wooden salad bowl is full of shredded purple cabbage, orange carrot, yellow corn and red pomegranate seeds. The gloved hand tips a small white bowl of finely chopped fresh flat leaf parsley onto it, a bright green layer covers the top. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 07 (SET + HAND)
```
The wooden salad bowl is topped with chopped green parsley over purple cabbage and pomegranate seeds. The gloved hand uses a knife to scrape roughly chopped walnuts off a small wooden cutting board into the bowl, the walnut pieces slide off and land on the parsley. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 08 (SET + HAND + JUG)
```
Close-up of the white sauce jug standing on the bamboo placemat, the full colorful salad bowl softly blurred behind it. The gloved hand squeezes a metal garlic press over the jug and fresh crushed garlic drops inside. Fixed camera at a 45 degree high angle, soft daylight from the left, shallow depth of field, real-time speed, no text, no faces.
```
### 09 (SET + HAND + JUG)
```
Close-up of the white sauce jug on the bamboo placemat, the salad bowl blurred behind. The gloved hand squeezes half a lemon in a black citrus press above the jug, fresh lemon juice streams down into it. Fixed camera at a 45 degree high angle, soft daylight from the left, shallow depth of field, real-time speed, no text, no faces.
```
### 10 (SET + JUG)
```
Close-up of the white sauce jug on the bamboo placemat, the salad bowl blurred behind. Golden extra virgin olive oil pours in a thin glossy stream from a dark green glass bottle into the jug. Fixed camera at a 45 degree high angle, soft daylight from the left, shallow depth of field, real-time speed, no text, no faces.
```
### 11 (SET + HAND + JUG)
```
Close-up of the white sauce jug on the bamboo placemat, the salad bowl blurred behind. The gloved hand drizzles thick dark red pomegranate molasses from a spoon into the jug, it sinks into the olive oil and lemon juice. Fixed camera at a 45 degree high angle, soft daylight from the left, shallow depth of field, real-time speed, no text, no faces.
```
### 12 (SET + HAND + JUG)
```
Close-up of the white sauce jug on the bamboo placemat. The gloved hand whisks the dressing inside with a small spoon, it turns into a glossy pinkish brown emulsion. Fixed camera at a 45 degree high angle, soft daylight from the left, shallow depth of field, real-time speed, no text, no faces.
```
### 13 (SET + HAND + JUG)
```
The wooden salad bowl is layered with purple cabbage, carrot, beetroot, corn, pomegranate seeds, green parsley and chopped walnuts on top. The gloved hand tilts the white sauce jug and pours a smooth stream of pinkish brown dressing over the walnuts and parsley. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 14 (SET + HAND)
```
In the wooden salad bowl, two wooden salad servers toss the whole salad, purple cabbage, orange carrot, crimson beetroot, green parsley, corn, walnuts and pomegranate seeds mix together and glisten with dressing. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```
### 15 (SET)
```
The fully mixed beetroot, carrot and purple cabbage salad sits glistening with dressing in the wooden bowl, flecks of green parsley, yellow corn, walnuts and red pomegranate seeds throughout, completely still, a single parsley leaf gently settles on top. Fixed camera at a 45 degree high angle, close-up, soft daylight from the left, shallow depth of field, vivid natural colors, no text, no people.
```
### 16 (SET + HAND)
```
The gloved hand lifts a generous forkful of the mixed beetroot and cabbage salad out of the wooden bowl toward the camera, dressing glistens on the crimson and orange strands, a walnut piece and pomegranate seeds on the fork. Close-up, soft daylight from the left, shallow depth of field, vivid natural colors, real-time speed, no text, no faces.
```

## ADIM 6: Teslim
Her çekimden beğendiğini indir, adlarını `01.mp4` ... `16.mp4` yap, Drive klasörüne yükle, linki at. Kurgu, döngü (video 14'ün ortasından başlar), ASMR efektleri, müzik ve miks bizden.

## Notlar
- Facebook'ta yüklerken "AI ile oluşturuldu" etiketini aç (Meta gerçekçi yapay zeka videoları için istiyor).
- Set ve tarif bizim; referans sayfanın yeşil bitkisi ve birebir kurgusu kopyalanmıyor.
