# Devir notu: Chronik der Macht (CDM), Teil 2 ve Helmut Wick

Yeni oturum önce bu dosyayı, sonra `CLAUDE.md` ve `chronik/DERSLER.md` dosyalarını okusun. Branch: `claude/admiring-fermat-o69lm8`.

## Boran'ın kuralları (özet)
- Sohbet Türkçe, kanal içeriği Almanca (CDM) veya İngilizce (CoP). Uzun tire (— –) asla yok.
- Tarafsız, doğrulanmış bilgi. CDM üslubu: paradoks kancası, "Sein Name war …", sakin bitiş, retorik soru yok.
- Gamalı haç ve bayraklar küçük ve tam yerinde bulanık. Hitler görünebilir.
- API anahtarı sohbete yazılmaz. Bot korumaları aşılmaz (Google, Yandex, DuckDuckGo kapalı; Wikimedia ve Bundesarchiv yavaşlatıyorsa beklenir).
- ElevenLabs: Robert Ranger – Cool Storyteller (voice_id ML23UVoFL5mI6APbRAeR), eleven_v4, stability 0, similarity 0.75, TEK üretim.
- SHORTS (9:16): metnin başına MUTLAKA "[quickly reads]" eklenir. Uzun videolarda (Teil 2 gibi) eklenmez, hız kesilmez, sadece aşırı duraklamalar kısaltılır.
- Bir seferde bir iş. Yükleme paketi istendiğinde sohbete de yazılır.
- Sayfa geçişlerinde uzun bekleme yok: anlatım bitince yaklaşık yarım saniye, sonra sayfa döner (Teil 2 v3'teki gibi).
- Seri (Deutschland im Zweiten Weltkrieg) Facebook ve Instagram'a yüklenmiyor, sadece YouTube.
- Gamalı haç kontrolü HER görselde ve kapakta: Ritterkreuz ve Demir Haç ortası (kapak portresinde büyük görünür!), şapka ve göğüs kartalları, uçak kuyrukları, bayraklar. Kapak üretildikten sonra haç merkezi yakından kontrol edilir.
- Dosyalar GitHub'a yüklenir; küçük olanlar (kapak, görsel) ayrıca sohbete de gönderilir. Küçük düzeltmeler hızlı yapılır: önce isteneni düzelt ve teslim et, ek kontrol ve ek işler sonra ve kısa.
- Büyük videolar sohbete 400 MB altında, tercihen küçük parçalar halinde gönderilir (40 MB'lık parçalar test ediliyor).

## Teil 2 "Der Überfall auf Polen" (16:9, 10:42) — bitti, v3
- Kod: `chronik/serie/teil02_kod/` (teil2b.py ana motor, t2core.py, drawings2.py, gaps.py, mix2.py, render_v2.sh, srt_t2.py, thumbs_t2.py, story_t2.py, post_t2.py).
- Paket: `chronik/serie/teil02/metadata.md` (3 başlık + 3 thumbnail, bölümlü açıklama v3 sürelerine göre, etiketler, sabit yorum, topluluk gönderisi + anket, FB, IG, story'ler, EN çeviri). Thumbnail, story, post görseli, DE/EN SRT aynı klasörde.
- Render çıktısı (mp4) repoda yok; bulut bilgisayarı kapanınca silinir. Yeniden üretmek için: ses `teil02_stimme_a/b.mp3` → vcut.wav (a + 0,6 s sessizlik + b), gaps.py, mix2.py, render_v2.sh (8 paralel parça), concat + mux.
- Kalan: Boran videonun geri kalanını kendisi kontrol edecek; gelen düzeltmeler v4 olur.

## Helmut Wick (CDM, sıradaki)
- Senaryo: `chronik/wick/script_de.txt` (tarihsiz başlıyor). Boran'ın onayı bekleniyor, sonra tek seslendirme.
- Materyal kataloğu: `chronik/wick/material.md`, arama kodu `chronik/wick/kod/`.
  - Bundesarchiv: Wick'in 10 fotoğrafı (Porträt 101I-404-0512-17, Cockpit 101I-404-0546-09, Sperrle ile 146-2015-0025 …) ve 22 çevre fotoğrafı. `bild.bundesarchiv.de` arama sayfasındaki JSON'da DC5FileURL tam çözünürlük veriyor.
  - Film: Deutsche Wochenschau Nr. 531 (6.11.1940) yaklaşık 17:27–17:52, Göring Kanal kıyısında, "Major Wick … meldet dem Reichsmarschall das Richthofengeschwader". Nr. 532 HD (archive.org youtube-zUU-LNi7FBc) 14:01–17:06 Bf 109 ve Spitfire. Why We Fight: Battle of Britain (gemeinfrei) RAF sahneleri. Kamera-MG Bf 109.
  - Eksik: Commons'tan 16 dosya (Wick'in kupası ve nişanı, Dundas portresi ve anıtı, 609 Squadron, Isle of Wight), Bundesarchiv'den 6 dosya. İndirilen materyal Boran'a `Wick_Material.zip` olarak gönderildi; bulut bilgisayarı kapanınca kopyası silinir, gerekirse katalogdan yeniden indirilir.

## Diğer açık işler
- Wainwright v2, Balck v2 düzeltmeleri, Bismarck CDM Short (eski görev listesinden).
