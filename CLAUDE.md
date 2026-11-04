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
- YouTube: başlık seçenekleri, açıklama, 500 karakterlik etiketler, sabitlenmiş yorum, YouTube topluluk gönderisi (görsel + metin + anket).
- Facebook: başlıksız metin, 7-8 hashtag. Instagram: metin, en fazla 5 hashtag.
- Thumbnail (sabit Yamamoto düzeni, `chronicle/brand/covers4.py`).
- Almanca kanal (CDM) için ayrıca: senkron İngilizce SRT (`untertitel/captions.en_US.srt`), story videosu ve her açıklamada CDM uyarı metni.
- İngilizce kanal (CoP) için aynı paket; SRT ve story hariç.
