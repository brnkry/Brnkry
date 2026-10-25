# stick01: "World War 1" yorum kavgası, çöp adam podcast animasyonu

Kaynak: Instagram yorumlarında tartışan iki kişi (shaun_73 ve ben_soir4) videosu, 57,5 sn, 9:16. Ses kaynaktan aynen alındı.

- Shaun (solda, salak): pervaneli şapka, şaşı gözler, tavşan dişleri, salyası akıyor, sesi ince (~350 Hz).
- Ben (sağda, bilgili): yuvarlak gözlük, düzgün saç, papyon, kahve kupası, kitap.
- Baloncuk: Instagram yorumu gibi (avatar, kullanıcı adı, Reply, beğeni sayısı). Kelimeler sese göre tek tek gelir. Vurgu: Shaun kırmızı, Ben mavi.
- Meme ara kesitleri sahnede canlandırıldı: "HE" (Shaun'a zoom, kırmızı daire ve ok), aslan kükremesi (Ben aslan yelesiyle kükrer), ekşi limon (Ben'in yüzü yeşil, büzük dudak, kahveyi püskürtür).
- Son: Ben kameraya bakar, gözlüğü çatlar.

## Akış
1. `python3 align_chunks.py src_audio.wav chunks.json align.json` (pocketsphinx, satır satır). Shaun'un ince sesi bazı yerlerde hizalanmadı; o kelimeler ses parçalarından elle verildi. Zamanlar `lines.js` içinde.
2. `python3 mouth.py src_audio.wav mouth.js` (dudak senkronu).
3. Önizleme: `node render.js scene.html preview 3.9 18.9 29.6`.
4. Render: 4 işçi, `node render.js scene.html full 57.5 0 432 &` ... (yaklaşık 4 dk).
5. Encode: kareler + kaynak videonun sesi, x264 crf 18, AAC 192k. Çıktı `exports/ww1_stickman.mp4`.
