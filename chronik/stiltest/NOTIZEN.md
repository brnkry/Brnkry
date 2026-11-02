# Kolaj stil denemesi (Laconia, ilk 28,6 sn)

Referans: Boran'ın Drive'daki iki ekran kaydı (storytelling edit, Samwer kardeşler edit).

Stilin unsurları ve koddaki karşılıkları (`kod/style.py`):
- Açık gri kâğıt zemin, kenarları koyulaşan radyal geçiş, ince doku; bazı sahnelerde mavi kareli kâğıt: `paper(grid, dark)`
- Dekupe figürler (rembg, isnet-general-use), siyah beyaz, yumuşak gölge; düz siyah siluet seçeneği: `cut()`, `place()`
- Tek vurgu rengi (sarı): büyüyen bant `band()`, sekerek açılan daire `disc()`, çapraz şeritler `stripes()`
- Katmanlı tipografi (daire, büyük yazı, figür sırası), kelimeler sesle tek tek: `word()` (rise, slam, wipe)
- Harfleri karışarak oturan slab başlık `scramble()`, daktilo etiket `typed()`, el yazısı (Caveat)
- Hareket bulanıklığıyla giriş `mover()` ve `place(mblur)`, hareket içinde kesme geçişi (test30.py frame), sürekli yavaş yakınlaşma `push()`
- Süs: köşe çerçeveleri `brackets()`, gri paragraf çizgileri `bodylines()`, kıvrık ok, zeminde yansımalı sayaç, ışık huzmesi, insan ikonlu infografik

Dekupe kaynakları `cut/` klasöründe (scratchpad); gamalı haç bulanıklaştırmaları dekupeden önce yapılır.

## Deneme 2 (Laconia 0:00-0:57)
- Font: Historic Mystique ücretli; en yakın ücretsiz karşılık Bigelow Rules (`disp()`), ince konturla kalınlaştırılmış. Boran lisanslı dosyayı yüklerse onunla değiştirilir.
- Şekil ve harf içinde film: `filmfill()`, `textmask()`, `spritemask()` (gemi siluetinde patlama filmi, LACONIA ve HILFERUFE harflerinde film, U-Boot siluetinde yüzeye çıkış filmi).
- Gri zemin yerine tonlanmış film (B-24 sahnesi).
- Yeni öğeler: yırtık kâğıt `torn()`, bant `tape()`, polaroid `polaroid()`, kırmızı mürekkep dairesi `inkcircle()`, elle çizilmiş ok `harrow()`, U-Boot ve filika siluetleri `uboat()`, `lifeboat()`, telsiz halkaları ve telgraf.
- YouTube güvenli alanı: yazılar x 60..900 ve y 300..1560 arasında, merkez x 480.
