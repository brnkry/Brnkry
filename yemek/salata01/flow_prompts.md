# Salata 01: Pancarlı renkli salata (Google Flow / Veo promptları)

Referans: Yemek_Kelebegi, Facebook Reels ("Tam bi şifa ve lezzet deposu"). Ekran kaydı 19,5 sn, video yaklaşık 17 sn ve döngü (loop).

## Referans videonun analizi

- **Format:** 9:16, yaklaşık 17 sn, 16 çekim, her çekim 0,7 ile 1,2 sn. Seslendirme yok, ekranda yazı yok. Ses "Orijinal Ses" (malzeme dökme sesleri, ASMR tarzı).
- **Kamera:** Hep aynı açı. Yaklaşık 45 derece yukarıdan, kase kadrajın alt yarısında, çok yakın. Kamera sabit. Arada sadece kaşık ve çatal yakın çekimleri var.
- **Set:** Bambu hasır altlık, büyük açık renk tahta kase, beyaz porselen kaselerden dökülen malzemeler, eldivenli eller. Arka planda beyaz tezgah ve yeşil yapay bitki (bu bitki o sayfanın imzası, **biz kullanmayacağız**).
- **Kurgu mantığı:** Her çekim bir malzeme. Renkler katman katman birikiyor: mor, bordo, turuncu, sarı, kırmızı, yeşil, kahverengi. Sos ayrı fincanda hazırlanıp dökülüyor, sonra karıştırma ve "lezzetli" yakın çekimleri.
- **Kanca:** İlk kare boş değil. Video karıştırılmış salatayla bitip dökme çekimiyle başladığı için sonsuz döngü hissi veriyor. İzleyici nerede başladığını fark etmeden ikinci kez izliyor (izlenme süresini artırır).
- **Tarif (videodan okunan):** Rendelenmiş kırmızı lahana, pancar, havuç, mısır, nar, ince kıyılmış maydanoz, ceviz. Sos: ezilmiş sarımsak, limon, zeytinyağı, nar ekşisi (sosun kırmızı kahve rengi), tuz.

## Flow'da çalışma yöntemi

1. **Önce ana kareyi üret** (görsel modeliyle): boş kase setimiz. Bütün çekimleri bu kareden veya bunun varyasyonlarından başlat ki kase, ışık ve masa her çekimde aynı kalsın.
2. Her çekimi **Frames to Video** ile, kasenin o anki durumunu gösteren bir başlangıç karesiyle üret. Bir önceki çekimin son karesini sonraki çekimin başlangıç karesi yap. Böylece malzemeler birikir, kase "sıfırlanmaz".
3. Veo 8 sn üretir, biz her çekimden en iyi 1 sn'yi alacağız. Önce Fast modda dene, beğenilen çekimi Quality ile yeniden üret.
4. Her prompta aşağıdaki **STİL BLOĞU** aynen eklenir.

### STİL BLOĞU (her promptun sonuna)
```
Vertical 9:16 food video, close-up from a fixed camera at a 45 degree high angle, large light acacia wood salad bowl filling the lower half of the frame, on a woven bamboo placemat, bright white marble kitchen counter, soft natural daylight from a window on the left, a small terracotta pot of fresh basil softly blurred in the background, shallow depth of field, vivid saturated natural colors, crisp detail, real-time speed, no text, no logos, no faces.
```

### NEGATİF (Flow'da varsa negatif alana)
```
text, watermark, logo, cartoon, CGI look, plastic food, distorted hands, extra fingers, morphing objects, camera shake, slow motion
```

## Çekim listesi (16 çekim, yaklaşık 16 sn)

| # | Süre | Prompt (stil bloğundan önce) |
|---|---|---|
| 01 | 1,0 sn | A hand in a clear food-safe glove tips a white ceramic bowl of finely julienned raw beetroot into the empty wooden bowl, the deep crimson strands tumble down and land in a loose pile. |
| 02 | 1,0 | A white ceramic bowl of finely grated bright orange carrot is tipped into the wooden bowl, the carrot falls on top of the crimson beetroot. |
| 03 | 1,0 | A white bowl of finely shredded purple red cabbage is poured into the wooden bowl, covering one side, purple strands bounce as they land. |
| 04 | 0,8 | A small white bowl of sweet corn kernels is tipped into the center of the salad, the yellow kernels scatter over the purple and orange. |
| 05 | 0,8 | Glistening red pomegranate seeds pour from a small white bowl and rain down onto the salad, bouncing like jewels. |
| 06 | 1,0 | A white bowl of finely chopped fresh flat leaf parsley is tipped onto the salad, a bright green layer covers the top. |
| 07 | 1,0 | A knife scrapes roughly chopped walnuts off a small wooden cutting board into the bowl, the walnut pieces slide off and land on the parsley. |
| 08 | 1,0 | Close-up of a small white ceramic jug on the bamboo mat, a gloved hand squeezes a garlic press and fresh crushed garlic drops into the jug. (Arka planda kase dolu ve bulanık.) |
| 09 | 0,8 | A gloved hand squeezes a lemon half in a black citrus press over the white jug, fresh lemon juice streams down. |
| 10 | 0,8 | Golden extra virgin olive oil pours in a thin stream from a dark green glass bottle into the white jug. |
| 11 | 0,8 | Thick dark red pomegranate molasses drizzles from a spoon into the jug. |
| 12 | 1,0 | A gloved hand whisks the dressing in the white jug with a small spoon, it turns into a glossy pinkish brown emulsion. |
| 13 | 1,2 | The white jug pours the pink dressing in a smooth stream over the walnuts and parsley in the wooden bowl. |
| 14 | 1,2 | Two wooden salad servers toss the whole salad, purple, orange, green and red strands mix together and glisten with dressing. |
| 15 | 1,2 | The fully mixed colorful salad sits glistening in the bowl, the camera stays fixed, a single parsley leaf gently settles on top. |
| 16 | 1,4 | A fork lifts a generous bite of the mixed beet and cabbage salad toward the camera, dressing glistens on the strands, a walnut piece and pomegranate seeds on the fork. |

Döngü için: 16'nın son karesi ile 01'in ilk karesi arasında kesim yapılır. Video 01 ile başlamaz, **14'ün ortasından** (karışık salata) başlar, 13'e kadar gider ve tekrar başa döner.

## Ses planı (biz ekleriz)

- Veo'nun ürettiği sesler (dökme, hışırtı) kullanılabilir ama genelde tutarsız. Daha temiz yol: Veo sesini kapat, her çekim için ayrı ASMR efekti (dökme, kıtır, sıvı akışı, karıştırma) ElevenLabs Sound Effects ile üret, üstüne hafif bir akustik müzik.
- Kurgu, kesimler, renk eşitleme, döngü ve miks bizim ffmpeg akışımızla yapılır (WTC'deki gibi). Loudness hedefi -14 LUFS.

## Açıklama taslağı (dil seçilince güncellenir)

TR: `Tam bir vitamin deposu 🥗 Pancarlı, narlı, cevizli renkli salata. Tarif aşağıda 👇` + malzeme listesi + soru ("Siz sosuna ne eklersiniz?")
EN: `This salad is pure color and crunch 🥗 Beet, pomegranate and walnut slaw. Recipe below 👇`
