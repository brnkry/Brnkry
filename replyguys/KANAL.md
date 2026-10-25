# Reply Guys (kanal kiti)

Konsept: Yorumlarda tartışan insanlar, çöp adam podcast'i olarak canlandırılır. Karakterler her bölümde değişebilir; logo ve tabela bu yüzden karaktersizdir (iki yorum baloncuğu "?" ve "!", ortada podcast mikrofonu).

- Ad: **Reply Guys**
- Kullanıcı adı önerisi (her platformda aynı): `@ReplyGuysPod` (yedekler: `@ReplyGuysShow`, `@TheReplyGuys`)
- Renkler: neon pembe #FF3DA5, neon camgöbeği #3DE6FF, neon lime #C6FF3D, zemin #15121F
- Fontlar: Tilt Neon (logo, tabela), Patrick Hand (baloncuk yazısı), Permanent Marker (çıkartmalar). Hepsi OFL.
- Dosyalar: `brand_assets/logo_800.png` (profil), `brand_assets/logo_1024x576.png` (16:9 logo), `brand_assets/banner_2560x1440.png`. Yeniden üretmek için `node brand_assets/shot.js`.
- Videodaki neon tabela: `stick01/sign.js`. 13 saniyelik döngü: logo + REPLY GUYS (her döngüde renk değişir), sonra `window.EPISODE` yazısı (lines.js içinde), aralarda neon kıpırtısı.

## YouTube açıklaması
```
Real comment section arguments, acted out as a podcast by stick figures.

Someone drops a very confident take. Someone else replies with the facts. We sit them both down behind a mic and let it play out, word for word.

New episodes every day. Subscribe so you don't miss the next fight in the replies.
```

## YouTube kanal etiketleri (v2, genel komedi)
```
reply guys, funny comments, comment section, internet arguments, funny arguments, comment wars, dumb comments, funny instagram comments, funny tiktok comments, social media fails, hot takes, debate gone wrong, stickman animation, stick figure comedy, animated podcast, podcast animation, funny animation, animated comedy, comedy shorts, funny videos, internet comedy, try not to laugh
```
- 22 etiket, YouTube'un tırnak saymasıyla ~407/500 karakter. Konudan bağımsız (history yok); konuya özel kelimeler videonun kendi etiketlerine girer.
- Sıra: önce kanal adı, sonra içeriğin ne olduğu (yorum kavgaları), sonra format (çöp adam, animasyonlu podcast), en son geniş komedi terimleri.
- Etiketlerin etkisi küçük (YouTube Yardım). Asıl iş başlık, thumbnail ve açıklamada. Açıklamaya etiket yığmak spam sayılır.

## Video etiketi şablonu (her bölüm, ~8-12 etiket)
1. Bölümün ana konusu (ör. `world war 1`), 2. konu varyasyonu / soru kalıbı (ör. `why is it called world war 1`), 3. tartışmanın komik kancası (ör. `4 billion people died`), 4-6. sabit format etiketleri: `funny comments`, `comment section`, `stickman animation`, 7. `reply guys`.

## Facebook sayfası (kısa açıklama, 101 karakter sınırı)
```
Comment section fights, acted out as a podcast by stick figures. New episodes every day. 🎙️
```

## Instagram biyografisi (150 karakter sınırı)
```
🎙️ Comment section fights, acted out as a podcast
✏️ Stick figures. Real threads. Zero chill.
👇 New episodes every day
```

## Bölüm 01 (YouTube)
Kural: Kanal komedi kanalı. Etiket ve açıklama konuya (tarih vb.) değil, komik yorum kavgasına göre yazılır; yoksa yanlış kitle (tarihçiler) gelir. Açıklama kısa tutulur.

Başlık:
```
He thinks 4 billion people died in World War 1 💀
```
Açıklama:
```
The comment section had questions. Then it had numbers. Very wrong numbers. 💀

Real comment fights, acted out as a podcast by stick figures. New episode every day.

#funnycomments #commentsection #funny
```
Etiketler (~442/500):
```
funny instagram comments, funny comments, instagram comments, comment section, dumb comments, funniest comments, internet arguments, funny arguments, comment wars, comment section fights, dumb vs smart, stupid comments, social media fails, internet fails, hot takes, funny animation, stickman animation, stick figure comedy, animated podcast, animated comedy, comedy shorts, funny videos, try not to laugh, reply guys
```
Sabitlenmiş yorum: `Who's worse, the 4 billion guy or the "big bad war" guy? 👇`
Kategori: Comedy

## Bölüm 02 (YouTube)
Başlık:
```
He asked what gaslighting is and got gaslit 💀
```
Açıklama:
```
He just wanted to know what gaslighting means. The comment section had other plans. 😭

Real comment fights, acted out as a podcast by stick figures. New episode every day.

#funnycomments #commentsection #funny
```
Etiketler (~410/500):
```
funny instagram comments, funny comments, instagram comments, comment section, gaslighting meme, gaslighting comments, getting gaslit, you know what it is, internet trolls, trolling comments, funny trolls, dumb comments, internet arguments, comment wars, stickman animation, stick figure comedy, animated podcast, funny animation, animated comedy, comedy shorts, funny videos, reply guys
```
Sabitlenmiş yorum: `So... what IS gaslighting? 👀👇`

## Bölüm 03 (YouTube)
Başlık:
```
He just wanted his photos printed 👽
```
Açıklama:
```
Bogos binted? 👽 Vorp.

Real internet chaos, acted out as a podcast by stick figures. New episode every day.

#bogosbinted #memes #funny
```
Etiketler:
```
bogos binted, bogos binted meme, photos printed, zinky zoogle, vorp, alien meme, funny texts, funny text messages, text message fails, funny chats, meme reenacted, memes animated, funny comments, stickman animation, stick figure comedy, animated podcast, funny animation, animated comedy, comedy shorts, funny videos, reply guys
```
Sabitlenmiş yorum: `Translate this for me pls 👽👇`

## Bölüm 04 (YouTube) — video4'ün ilk kesiti
Başlık:
```
Is there a word between yes and no? 🤔
```
Açıklama:
```
Someone found the answer. Someone else did not. 💀

Real comment fights, acted out as a podcast by stick figures. New episode every day.

#funnycomments #commentsection #funny
```
Etiketler:
```
yes or no, word between yes and no, maybe, funny comments, funny instagram comments, instagram comments, comment section, dumb comments, funniest comments, internet arguments, comment wars, big brain, iq test, stickman animation, stick figure comedy, animated podcast, funny animation, animated comedy, comedy shorts, funny videos, reply guys
```
Sabitlenmiş yorum: `Ok well what is it then? 🤨👇`

Thumbnail: `node replyguys/engine/thumb.js stickNN <saniye>` (ayar: `stickNN/thumb/cfg.js`).

## Bölüm 05 (YouTube) — video4'ün ikinci kesiti
Başlık:
```
Gemini made the easiest guessing game ever 🤖
```
Açıklama:
```
"I chose red. Try to guess it." 💀

Real internet chaos, acted out as a podcast by stick figures. New episode every day.

#gemini #ai #funny
```
Etiketler:
```
gemini, google gemini, gemini fail, ai fail, funny ai, ai chatbot, guess my color, ai guessing game, funny ai chat, chatbot fail, funny texts, funny comments, instagram comments, stickman animation, stick figure comedy, animated podcast, funny animation, animated comedy, comedy shorts, funny videos, reply guys
```
Sabitlenmiş yorum: `How did he guess it though? 🤔👇`
Not: Kaynağa olmayan şaka eklenmez; sahne efektleri sadece replikleri görselleştirir.

## Bölüm 06 (YouTube) — video4'ün üçüncü kesiti
Başlık:
```
She asked for the movie name 🎬💀
```
Açıklama:
```
"What's the movie name?" "ready or not" "Ready." 💀

Real comment fights, acted out as a podcast by stick figures. New episode every day.

#funnycomments #commentsection #funny
```
Etiketler:
```
ready or not, whats the movie name, ready or not movie, funny comments, funny instagram comments, instagram comments, comment section, dumb comments, funniest comments, comment fails, misunderstanding, stickman animation, stick figure comedy, animated podcast, funny animation, animated comedy, comedy shorts, funny videos, reply guys
```
Sabitlenmiş yorum: `Ready or not? 👀👇`

## Ekran düzeni (bölüm 02'den itibaren, `replyguys/engine/engine.js`)
iPhone Shorts ekran görüntüsüne göre: telefon her iki yandan ~47 px kırpıyor, üst ikonlar y<215, kanal adı ve başlık y>1530, beğen/yorum butonları x>880 ve y>1035. Bu yüzden her şey ortalı: zemin y=1500, kafalar x 160..870, baloncuklar x 110..970 (alt kenar y=950), neon tabela y≈250. Yeni bölüm = `lines.js` + `ep.js` + `scene.html` (stick02 örnek).

## Kategoriler
- YouTube: **Comedy** (Studio > Settings > Upload defaults > Advanced settings > Category). Kanalın kendi kategori ayarı yok, her videoya buradan varsayılan olarak atanır.
- Facebook sayfası: **Podcast**, **Video Creator**, **Entertainment Website** (en fazla 3).
- Instagram (profesyonel hesap, Creator): **Video creator**. Listede "Podcast" çıkarsa o da olur.
