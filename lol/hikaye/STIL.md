# LoL hikaye videoları: sabit thumbnail stili

Boran onayladı, bundan sonra tüm videolarda bu kullanılır.

- Font: Marcellus (Google Fonts, `@fontsource/marcellus`, latin-ext ile Türkçe harfler tam). Riot'un "Beaufort for LoL" fontuna en yakın serbest font.
- Düzen (Riot'un "Yol, Bir Ionia Efsanesi" tanıtım görseli gibi): sol altta iki satır büyük krem başlık (#F3E6D3, 86-96 px, satır aralığı 1.08, harf aralığı -0.01em, 2.2 px kalınlaştırma), altında eğik altın alt başlık (#E2B967, 46 px): "<ŞAMPİYON>'UN HİKAYESİ".
- Arka planda sinematik kare ya da splash, sol ve alttan koyu geçiş, Ruh Çiçeği yaprakları.
- Thumbnail yazısı başlığı tekrar etmez: thumbnail duyguyu ve merakı verir, başlık soruyu ve arama kelimelerini.
- Şablon: yone/build/thumb3.html, çekim: yone/build/shoot_thumb3.js.
