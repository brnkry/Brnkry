# Brnkry: "What the Car?" Shorts kanalı

Her oturumun başında `wtc/DEVIR_NOTU.md` dosyasını oku. Kanal kimliği, format, güvenli alanlar, teknik akış ve kullanıcı kuralları orada.

Kısa kurallar:
- Kullanıcı Boran. Sohbet Türkçe, kanal içeriği İngilizce.
- Senaryo, altyazı, başlık ve gönderilerde uzun tire (— veya –) asla kullanılmaz.
- ElevenLabs senaryosu düz metin, tek paragraf, işaretsiz.
- Kit dosyaları `wtc/` klasöründe. `npm i playwright @fontsource-variable/bricolage-grotesque` komutunu `wtc/` içinde çalıştır.
- Her video için yeni oturum aç, düzeltmeleri tek mesajda topla (kredi tasarrufu).
- Bir video bitince `wtc/DEVIR_NOTU.md` içindeki video tablosunu ve sonraki adımları güncelle.

## Yükleme paketi (Chronik der Macht ve Chronicle of Power)
Boran "video tamam, yükleme için gerekli bilgileri ver" dediğinde, o videonun `metadata.md` dosyasındaki paketin tamamını ver:
- YouTube: başlık seçenekleri, açıklama, 500 karakterlik etiketler (YouTube sayımıyla 500'e yakın, SEO odaklı, kanal adı ASLA etiketlere konmaz; etiketler geniş aranan terimler olur: Zweiter Weltkrieg, U-Boot, Kriegsmarine, deutsche Geschichte, Marinegeschichte gibi; Marineschule Mürwik gibi kimsenin aramadığı dar terimler konmaz; olayın geçtiği ülke ya da yer (Dänemark gibi) konu o ülke değilse konmaz; her etiket "insanlar bu konuyu izlemek için bunu arama çubuğuna yazar mı?" sorusundan geçer), sabitlenmiş yorum, YouTube topluluk gönderisi (görsel + metin + anket).
- Facebook: başlıksız metin, 7-8 hashtag. Instagram: metin, en fazla 5 hashtag (Instagram Aralık 2025'ten beri 5 ile sınırlıyor). Hashtagler genişten dara sıralanır: önce #ZweiterWeltkrieg ve #WW2, sonra konu (#Luftwaffe, #UBoot, #Panzer), en sonda dar konu (#Bf109, #TigerI). Kanal adı, yer adı ve kimsenin aramadığı terimler hashtag olmaz.
- Thumbnail (sabit Yamamoto düzeni, `chronicle/brand/covers4.py`).
- Almanca kanal (CDM) için ayrıca: senkron İngilizce SRT (`untertitel/captions.en_US.srt`), story videosu ve her açıklamada CDM uyarı metni.
- İngilizce kanal (CoP) için aynı paket; SRT ve story hariç.

## Foto gönderileri (CDM)
Boran bir fotoğraf paylaşınca: kısa Almanca açıklama (tarih, yer, olay; gerçekleri kontrol et), "📸 Hinweis: Die historische Originalaufnahme wurde von uns restauriert, in der Qualität verbessert und koloriert." ve CDM uyarı metni. YouTube topluluk gönderisinde hashtag yok; Facebook 7-8 hashtag; Instagram en fazla 5 hashtag. Kanal adı hiçbir yerde (metin ya da hashtag) kullanılmaz. Kayıt: `chronik/fotos/`.

## Sembol bulanıklaştırma (videolar, kapaklar, görseller)
Yalnızca gamalı haçın kendisi küçük, yumuşak bir daireyle bulanıklaştırılır: kasket ve göğüs kartalının altındaki gamalı haç, Şövalye Haçı ve Demir Haç ortası, rozetlerdeki gamalı haç, uçak kuyruğundaki gamalı haç. Kartalın tamamı, nişanın tamamı ya da göğüs bölgesi bulanıklaştırılmaz. Konum yakın plan ızgarayla ölçülür, sonuç yakın planda kontrol edilir.
