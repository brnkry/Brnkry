# Devir notu: "What the Car?" (İngilizce Shorts kanalı)

Yeni sohbete bu dosyayı ve `wtc_starter_kit.zip` dosyasını ekle. Kitteki her şey, ilk video (01, check engine light) üretilirken test edildi ve sorunsuz çalıştı.

## Kullanıcı
- Adı Boran. Sohbet her zaman **Türkçe**, kanal içeriği **İngilizce**.
- Senaryolarda, altyazılarda, başlıklarda ve gönderilerde uzun tire (— veya –) asla kullanılmaz.
- Seslendirmeyi ElevenLabs ile kendisi yapıp mp3 olarak gönderiyor. Görüntüyü, efektleri, müziği ve miksi Claude üretiyor.
- Senaryoyu ElevenLabs için **düz metin** olarak ister: yıldız veya işaret olmadan, tek paragraf. Vurgu işaretlerini Claude altyazıya kendisi ekler.
- Paralel olarak Almanca **Drehmoment** kanalı (@drehmoment_auto) da test ediliyor. Hangisi tutarsa ona devam edilecek.

## Kanal kimliği (Drehmoment'ten tamamen ayrı)
- **Hedef pazar:** ABD (gas, tire, psi, °F, "state inspection / emissions testing").
- **Renkler:** Asphalt #121216 (zemin), Chalk #F4F1EA (yazı), Hi-Vis Lime #D4FF3A (vurgu), Brake Red #FF3D5A (soru işareti ve uyarılar), Graphite #22222A (kartlar), Smoke #8A8A96 (etiketler). Gerçek ikaz lambaları gerçek renginde çizilir (motor lambası amber #FFB000).
- **Font:** Bricolage Grotesque (variable, OFL lisanslı). `npm i playwright @fontsource-variable/bricolage-grotesque`. Kullanılan dosya: `bricolage-grotesque-latin-standard-normal.woff2`.
  - Altyazı: 700, font-stretch 88%
  - Vurgu kelimesi: 800, font-stretch 75%, lime, 1.06em, aynı satır çizgisinde
  - Üst etiket: 600, stretch 90%, harf aralığı .16em, büyük harf, Smoke rengi. Format: `SERİ ADI · EPISODE N`. Bu etiket her videoda sabit kalır.
- **Maskot:** Önden görünen, kafası karışık araba. Farlar göz, sağ kaşı kalkık, ağzı dalgalı çizgi, üstünde kırmızı "?". `brand.js` içindeki `makeFace(parent, opts)` ile çizilir. `look(dx,dy)` göz bebeklerini hareket ettirir. `browL`, `browR`, `mouth` ve `q` canlandırılabilir. `question:false` ile soru işareti kaldırılır.
- `makeCar(parent, opts)`: yandan görünüm hatchback (1000×340, merkezde). `makeWordmark(host, opts)`: HTML wordmark.
- Logolar, profil resmi (800×800) ve banner (2560×1440) `brand_assets/` klasöründe.
- **Ad ve marka uyarısı:** "WHAT THE CAR?" adı, Triband'in oyunu için ABD'de marka başvurusuna sahip (seri no 79371772, oyun yazılımı). @whatthecar kullanıcı adı alınmış. Önerilenler: @WhatTheCarExplained, @whatthecar_hq, @whatthecarshow. Kullanıcı hangisini aldığını henüz söylemedi, kapanış kartına kullanıcı adı eklenmedi.

## Kanal açıklaması (seri adları OLMADAN, kullanıcı böyle istedi)
```
Ever looked at your dashboard and thought "what the...?" This channel explains your car from zero, one part, one light and one button at a time. Every video is under a minute, with clear animations and no jargon.

New here? Start with the check engine light.

Disclaimer: The content on this channel is general information for educational purposes only. It is not a substitute for your owner's manual or a qualified mechanic. Always follow your manufacturer's instructions. This channel is not affiliated with any car manufacturer or brand.
```
Kanal etiketleri:
```
car maintenance, how engines work, dashboard warning lights, automotive basics, mechanic tips, repair tutorials, driving advice, electric vehicles, tire pressure, regenerative braking, beginners, DIY garage, fuel economy, octane rating, TPMS, ABS, alternator, suspension, owners manual, road safety, motoring explained, under the hood, winter prep, pickup truck, SUV, sedan, hybrid, battery range, physics, commute hacks, roadside help, STEM, odometer, gearbox, spark plugs, coolant
```

## İlk 10 video planı
Her videonun "Next time" kısmı bir sonraki videoyu haber verir.

| # | Üst etiket | Konu | Durum |
|---|---|---|---|
| 01 | DASHBOARD LIGHTS · EPISODE 1 | Motor arıza lambası | **Bitti** |
| 02 | WEIRD BUTTONS · EPISODE 1 | Hava sirkülasyon düğmesi (araba ve kıvrık ok) | Sırada |
| 03 | DASHBOARD LIGHTS · EPISODE 2 | Akü lambası (genelde şarj sistemi, alternatör) | |
| 04 | UNDER THE HOOD · EPISODE 1 | Gaza basınca ne oluyor | |
| 05 | DASHBOARD LIGHTS · EPISODE 3 | Soğukta yanan lastik basıncı lambası (TPMS) | |
| 06 | WEIRD BUTTONS · EPISODE 2 | Yakıt göstergesindeki küçük ok | |
| 07 | UNDER THE HOOD · EPISODE 2 | Normal ve premium benzin | |
| 08 | UNDER THE HOOD · EPISODE 3 | Gıcırdayan frenler (aşınma uyarı sacı) | |
| 09 | DASHBOARD LIGHTS · EPISODE 4 | ABS ve titreyen fren pedalı | |
| 10 | EV BASICS · EPISODE 1 | Rejeneratif frenleme | |

Video 01'in sonu şöyle bitiyor: "Next time: the button with the little car and the curved arrow." Yani 02 mutlaka sirkülasyon düğmesi olmalı.

**Sirkülasyon düğmesinin doğru görünümü** (kullanıcı gerçek fotoğrafını gönderdi, 01'in kapanışında böyle çizildi):
- Koyu, yuvarlak köşeli dikdörtgen düğme. Üstte yatay LED (yanınca sarı-yeşil).
- Ortada beyaz çizgiyle sedan silüeti, alttaki tekerlekler küçük daireler.
- Ok **tamamen arabanın içinde**: üst çizgi camların hizasında sola gidiyor, solda C gibi kıvrılıyor, alt çizgi sağa uzanıp sağı gösteren ok ucuyla bitiyor. Ok ucu arka tekerleğe değmiyor. Kod `scene01.html` içinde `S10 next` bölümünde.

## Format
- 9:16, 1080×1920, 30 fps, yaklaşık 50 saniye. İngilizcede senaryo 750 ile 850 karakter (01: yaklaşık 800 karakter, 49 saniyelik ses).
- Kinetik tipografi: kelime kelime beliren altyazılar. Yanında SVG animasyonlar.
- Her videoda **araba bağlamı görünmeli**. Drehmoment'in sadece motor parçası gösteren 02 numaralı videosu tutmadı.
- Her sahnede farklı bir animasyon. Kalıp tekrarlanmaz.
- Görsel alan: y 820 ile 1560 arası, x 150 ile 930 arası. Altyazı kutusu: left 150, top 425, 780×355. Üst etiket y=322'de.

## Kanca ve kapanış kuralları
- İlk cümle izleyicinin kendi arabasında yaşadığı bir anı anlatır ve "car" kelimesini içerir.
- Kanca cümlesi ilk karede tam görünür. İlk kare dolu olmalı.
- Kapanış sırası: soru, "Tell me in the comments.", "Next time: …", "Follow What the Car? so you don't miss it."

## Güvenli alanlar (YouTube Shorts)
- İçerik y ≈ 290'dan sonra başlar.
- y > 680 iken x > 930 bölgesi boş kalır (sağdaki buton sütunu).
- **Hiçbir şey y ≈ 1580'in altına inmez.**
- Kontrol için `yt_overlay.png` önizleme karelerinin üstüne bindirilir.

## Teknik akış (kitteki dosyalar)
Tüm dosyalar aynı klasörde durur. `node_modules` da bu klasörde olmalı.
1. **Zamanlama:** `ffmpeg -i vo.mp3 -af silencedetect=noise=-30dB:d=0.1 -f null -` ile konuşma parçaları çıkarılır ve senaryo cümleleri parçalara eşlenir. Altyazı grubu `G` içinde `[başlangıç, bitiş, "metin *vurgu*"]` olarak yazılır. Kelimeler parça içinde karakter sayısına göre dağıtılır. `W_('g4','start')` ifadesi kelimenin zamanını verir. Whisper kullanılamıyor, HuggingFace engelli.
2. **Sahne:** `scene01.html`. `window.render(t)` saf fonksiyondur. `window.EV` efekt olaylarını, `window.DUR` toplam süreyi tutar. Yeni video için bu dosya kopyalanır, sahneler yeniden yazılır.
3. **Önizleme:** `node render.js preview 0 6.4 …` komutu `prev/` klasörüne kare kaydeder. Kontak sayfası yapılıp `yt_overlay.png` ile kontrol edilir.
4. **Ses:** `node ev.js` komutu `events01.json` dosyasını üretir. `python3 audio01.py` efektleri sentezler, 104 BPM müziği (Fmaj7 Cmaj7 Dm7 Bbmaj7) seslendirme sırasında kısar ve hepsini `mix01.wav` dosyasında birleştirir. Dosya adları: `vo.mp3`, `chime.mp3`. DUR değeri `audio01.py` içinde elle güncellenir.
5. **Render:** `node render.js full 51.3 0 770 & node render.js full 51.3 770 1539 & wait` (iki paralel işçi, 51 saniye için yaklaşık 1,5 dakika).
6. **Encode:** loudnorm iki geçişte yapılır (önce `print_format=json` ile ölçülür, sonra `measured_*` değerleri ve `linear=true` ile uygulanır). Hedef -14 LUFS, TP -1.5. x264 crf 17, preset slow, yuv420p, AAC 192k, `+faststart`.
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (executablePath).

## BMW uyarı sesi (kullanıcının şakası, `chime.mp3`)
- Dosyada her 2,2 saniyede bir tek "ding" var. Atak yaklaşık 0,03 ile 0,12 saniye, ses yaklaşık 1 saniyede sönüyor.
- Kullanıcının kuralı: **Lamba sönük başlar, ding çaldığı anda yanar.** Ses gelmeden lamba asla yanık olmaz. Başta 2 ding, sonda 2 ding.
- 01'deki ayar: başta 0,45 ve 2,65 saniyelerde, sonda 40,25 ve 42,25 saniyelerde. Lamba her ding'de c+0,03 ile c+1,0 arasında yanık, diğer zamanlarda sönük (`lampBlink`). Sondaki gösterge sahnesi de lamba sönükken açılır.
- Seviye: başta 0.42 (kanca cümlesini bastırmasın diye), sonda 0.55.
- **Content ID riski:** Ses bir kütüphaneden alındıysa telif talebi gelebilir. Önce liste dışı yükleyip kontrol etmesi önerildi. Talep gelirse sentezlenmiş bir ding-dong ile değiştirilir.

## Video 01 (bitti): check engine light
ElevenLabs metni:
```
This light just came on in your car. Do you have to stop? It's the check engine light. It lights up briefly when you start the car. That's a self test. If it stays on, your car has stored a fault code. You can usually keep driving, but get it checked soon. If it's flashing, that's serious. The engine is usually misfiring, and unburned fuel can overheat your catalytic converter. Drive gently and only as far as needed. Common causes? A loose gas cap, an oxygen sensor, or worn spark plugs. Many auto parts stores read the code for free through the OBD port. And heads up: in most states with emissions testing, this light means you fail. Ever seen this light in your car? Tell me in the comments. Next time: the button with the little car and the curved arrow. Follow What the Car? so you don't miss it.
```
Metadata:
- Başlık: `🚨 Check engine light in your car: stop or drive?`
- Açıklama: ilk satır kanca, emoji maddeler, sonunda `#checkenginelight #carmaintenance #cartips`
- Sabitlenmiş yorum: `Has this light ever come on in your car? What was the cause? 👇`

Kullanıcının 01'de istediği düzeltmeler (yeni videolarda baştan doğru yap):
- Düğme ve kart içindeki yazılar şeklin içinde kalmalı (ENGINE START STOP düğmesi büyütüldü).
- Önemli simgeler belirgin olmalı, etiketlerin veya pill'lerin altında kalmamalı.
- Gerçek bir nesne çizilecekse kullanıcının gönderdiği fotoğrafa birebir uyulmalı.

## Metadata kuralları
- Başlıkta bir emoji, en fazla 50 karakter, arabayla ilgili bir kelime.
- Açıklamanın ilk 100 karakteri kanca. Altında emoji madde işaretleri, en sonda 3 hashtag.
- Etiketler yaklaşık 500 karakter, virgülle ayrılmış, # yok, yıl yok, "Shorts" yok, kanal adı yok, **hiçbir kelime ve türevi tekrar etmez** (car/cars, brake/braking gibi).
- Facebook Reels için 3 ile 5 hashtag.
- Sorumluluk reddi sadece kanal açıklamasında.

## Telif ve marka
Gerçek marka logoları ve markaya özgü gösterge paneli tasarımları kullanılmaz. Göstergeler genel tasarımdır (MPH ve RPM).

## Kullanım ve kredi notları
- Uzun sohbet pahalıya patlar: 01'in sohbeti sonunda her adımda yaklaşık 275 bin token yeniden okunuyordu. **Her video için yeni sohbet açılmalı.**
- 1 dakikalık video (ilk sürüm ve iki düzeltme turu), sohbetin toplam kullanımının yaklaşık yarısını tuttu. Düzeltmeleri tek mesajda toplamak tasarruf sağlar.
- Kullanıcının 100 dolarlık "Cloud session" bonus kredisi var (son kullanma 4 Kasım 2026). Bu Claude uygulaması sohbetleri krediden düşmüyor, Pro plan limitine yazılıyor. Krediyi kullanmak için GitHub repo bağlanarak Claude Code bulut oturumu açılması gerekebilir.

## Sonraki adımlar
- Video 02: sirkülasyon düğmesi. Önce senaryo (düz metin), sonra kullanıcı ElevenLabs mp3'ünü gönderir.
- Kullanıcı 16:9 uzun video fikrini de konuştu: motor lambası konusu 5 ile 7 dakika (yaklaşık 1.000 kelime) taşır. Bölümler: kanca, OBD-II geçmişi (ABD'de 1996 model yılından beri zorunlu), ECU ve bekleyen kod mantığı, sabit yanma ve yanıp sönme, en sık 5 sebep, P0300 kodunun çözümü, kodu silip muayeneye gitme hatası (izleme testleri sıfırlanır), kontrol listesi, kapanış.

## Uzun video 01 (16:9): check engine light, BİTTİ (6:42)
- Klasör: `wtc/long01/`. Not ve akış: `wtc/long01/script.md`. Anlatıcı karakter `guy.js`, ortak kod `lib.js`.
- Zamanlama artık **kelime kelime hizalama** ile: `python3 align.py ses.mp3 metin.txt align_x.json` (pocketsphinx, model paketin içinde). Sahnede `buildCaptionsA(G, window.ALIGN)`. Sözlükte olmayan kelimeler `align.py` içindeki SUBS ile verilir.
- Birleştirme: `parts.json` + `./build.sh cikti.mp4`. Tüm video için tek kesintisiz müzik (`master_audio.py`), parçalar arası 0,35 sn görüntü geçişi.
- Kapanışta "Next time" yok.

## KARAR (Ekim 2026): Shorts yok, sadece 16:9 normal video
- Kanal artık sadece 16:9 video yapıyor, 1-2 dakikalık olsa bile. Yukarıdaki 9:16 / Shorts kuralları eski videolar için geçerli.
- Seri planı ve durum tablosu: `wtc/DASHBOARD_LIGHTS.md`. Sıradaki video: TPMS (lastik basıncı).

## Kanal anahtar kelimeleri (Ekim 2026, genel araba kanalı)
```
car explained, how cars work, car parts explained, automotive explained, under the hood, how engines work, dashboard warning lights, check engine light, car maintenance, car basics, car tips for beginners, new drivers, transmission, brakes, suspension, steering, ignition system, fuel system, cooling system, car battery, tires, electric vehicles, hybrid cars, car safety, car technology, OBD2, owners manual, car animation
```
- Kanal artık arabayla ilgili her şeyi adım adım anlatan genel bir kanal (lambalar, parçalar, sistemler, elektrikli araçlar). Kanal anahtar kelimelerinin etkisi küçük; başlık, thumbnail ve açıklama asıl önemli olanlar.
- Her 4-5 videoda bir gözden geçir.

## Video etiketi kuralı (v2, Ekim 2026 araştırması)
- Eski "hiçbir kelime tekrar etmesin" kuralı kaldırıldı. Kaynaklar (YouTube Yardım, Briggsby/Search Engine Land) ana anahtar kelimenin varyasyonlarını öneriyor.
- İlk etiket = videonun ana anahtar kelimesi (başlıktaki). Sonra aramada kullanılan varyasyonlar ve soru kalıpları, 2-4 kelimelik ifadeler.
- Tek kelimelik genel etiketlerden ve videoda olmayan konulardan kaçın. Yaygın yazım hatası ve alternatif yazım ekle (ör. tyre).
- 500 karakter sınırına çok kelimeli etiketlerin tırnakları (+2) da dahil.
