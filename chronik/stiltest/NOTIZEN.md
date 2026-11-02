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
