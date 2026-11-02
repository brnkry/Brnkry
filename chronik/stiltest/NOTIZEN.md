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

## Stil A (a.mov) ve Laconia 30 sn denemesi (`kod/styleA.py`)
- Koyu lacivert-gri, lekeli ve çizikli masa zemini, bazen arkada mavi tonlu silik film; kumlanma, toz, vinyet.
- Siyah-beyaz hafif mavi tonlu eski baskılar, beyaz kırık kenarlık, yamuk açılarla yığılır, hareket bulanıklığıyla uçarak gelir; altta el yazısı tarih.
- Kamera masa üstünde yavaşça kayar, döner, yakınlaşır (`drift`).
- Başlık bloğu: büyük krem sayı + iki satır sarı başlık + yırtık beyaz şerit üstünde küçük koyu harfler (`titleblock`). Font: Montserrat 900, sıkı harf arası, aşınma dokusu (`gtext`).
- Alıntı: beyaz büyük harfler, kelimeler sesle, harfler maskeden yukarı çıkar (`quote`, `reveal`).
- Geçiş: kısa bulanıklaşma. Fotoğrafların içinde arşiv filmi oynayabilir.

## ElevenLabs ses tasarımı (`sounds/`, `kod/sfx_el.py`)
ElevenLabs Flow: "Laconia Short – Sounddesign". Model eleven_text_to_sound_v2.
- Zemin katmanları (döngü): `sea.mp3` gece açık deniz dalgası ve rüzgâr (30 sn), `drone.mp3` koyu sinematik drone (30 sn), `proj.mp3` eski film projektörü tıkırtısı (15 sn).
- Tek vuruşlar: `slap.mp3` fotoğraf masaya düşüş, `swish.mp3` kâğıt savrulması, `tear.mp3` kâğıt yırtılması, `hit.mp3` derin vuruş, `torp.mp3` uzak torpido patlaması.
- Not: süre verilmezse model 0,5 ile 2 sn arası üretiyor; zemin katmanlarında `duration_seconds` ve `loop` ayarlanmalı.
- ElevenLabs bağlantısı müzik üretmiyor (kısıtlı connector); müzik Documentary Show olarak kaldı.

## Stil A v2 (birebir referans kopyası, 2 Kasım)
- Referans a.mov kare kare incelendi:
  - alıntı mavi tonlu tam ekran fotoğraf üstünde kelime kelime fade ile geliyor, çıkışta son kelimeden geriye siliniyor;
  - kartlar kenarlardan kayarak giriyor ve hiç durmuyor (sürekli drift);
  - sarı başlık harf harf, sayı rakam rakam, yırtık şerit soldan siliniyor ve yazısı sonra beliriyor;
  - geçişler: masa üstünde dikey kamera kayması (whip) ve yakından geçen büyük bulanık kart (sweep).
- Her sahnede mavi tonlu foto yığını arka plan, giriş cümlesinde mavi tonlu Hartenstein.
- Müzik: ElevenLabs Music (eleven_music_v2_5), 2 versiyon; v2 seçildi (15. saniyeden sonra yükseliyor).
- Ses: yırtılma ve fotoğraf "slap" sesleri kaldırıldı; deniz + drone yatağı, geçişlerde yarım sesli whoosh, sayaçlarda low hit, "torpedierte"de torpido.
- Ses değişmedi: eski anlatım (vcut.wav). Vitali sesiyle deneme yapıldı ama Boran vazgeçti.
- Kod: kod/styleB.py (styleA.py'deki yardımcıları kullanır), kod/sfx_B.py, kod/renderB.sh.

## Stil C (gazete, referans c.mov), Egon Mayer 18 sn testi (2 Kasım)
- c.mov analizi:
  - Katmanlı eski gazete sayfaları; bazı katmanlar flu, sayfa krem renkli, kenarlar gri vinyet.
  - Fotoğraf ya da video kâğıda basılmış gibi: sepya-gri, kâğıtla çarpılıyor (multiply), mürekkep fırçası gibi düzensiz kenar yavaşça açılıyor.
  - Daktilo başlık rastgele harflerden çözülüyor; ⊠ ikon, çerçeveli italik alt başlık, noktalı çizgi.
  - Küçük kalın yıl sayacı akıyor, büyük serif paragraf var.
  - Sahne geçişi flu ile (defocus); kamera sürekli yavaşça yaklaşıyor.
- Uygulama: kod/stylec.py (egon/code/eg.py'yi kaynak, klip ve kelime zamanı için kullanır).
- Fontlar npm'den: @fontsource/special-elite (başlık), old-standard-tt (paragraf, sayaç, gazete), courier-prime (alt başlık).
- Gazete metinleri nötr dolgu kelimelerden üretiliyor; gerçek dönem gazetesi kullanılmıyor.
- C v2 (kod/stylec_v2.py):
  - Tek büyük gazete sayfası (dünya koordinatı). Kamera sahneler arasında sağa, aşağı ve sola kayıyor; geçişte hareket bulanıklığı ve hafif flu var.
  - Arkadaki silik gazete katmanı daha yavaş kayıyor (derinlik).
  - Fotoğraflar ekranı kaplayacak kadar büyük, soluk renkli ve kâğıtla çarpılmış.
  - Fotoğraf kamera gelirken mürekkep gibi açılıyor, biraz büyük gelip oturuyor. Yıl sayacı noktalı çizginin ortasında.
