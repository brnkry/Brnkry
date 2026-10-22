# Chronik der Macht: Boran'ın düzeltmelerinden kalıcı kurallar

Her yeni video (Shorts veya uzun) başlamadan önce bu dosyayı oku.

## Senkron (en önemli)
- Yazı, ses o kelimeyi söylediği anda gelir. Erken ya da geç gelmez.
- Sahne, önceki cümle bitmeden değişmez: her sahne kendi cümlesinin ilk kelimesine bağlanır (0,15 sn önce).
- Her yazı ekranda en az ~1,5 sn kalır; kalamıyorsa yazı cümlenin başında gelir ya da sonraki sahne biraz bekler.
- Animasyonlar bittikten sonra sahne ~1 sn daha ekranda kalır, hemen geçmez.
- Kelime eşleştirmesi: `werkzeuge/align_ps.py` (pocketsphinx, akustik modelle zorlamalı hizalama). align3.py duraklamalardan cümleyi yanlış bölebiliyor ve 0,5 sn kayıyor (Yamamoto'da "warned", "oil"). Kulakla/enerjiyle elle düzeltme de güvenilir değil; hizalayıcıya güven, sonra kritik kelimeleri önizlemede kontrol et. Almanca için pocketsphinx Almanca modeli gerekir; yoksa align3 + kelime kelime kontrol.
- Ses parça parça gelirse birleştirince cümle araları kısaltılır ama cümleler birbirine yapışmaz (~0,4 sn).

## Yerleşim
- Yazılar birbirinin, okların ve harita etiketlerinin üstüne binmez. Tarih/yıl yazıları rotanın ve şehir etiketinin olmadığı yere konur.
- Hiçbir yazı ekranın dışına taşmaz (sol kenardaki etiketler sağa açılır).
- Harita kadrajı: okun gittiği yer ekranda olmalı (ör. Helsinki → Wien).
- Rota bitince varış noktasında bir nokta/işaret kalır, boşluk kalmaz.
- Önce söylenen önce görünür (ör. "1949" sonra "SCHWEDEN").
- Bölüm kartları ekranın en üstünde, ~3 sn kalır, kendiliğinden kaybolur. Seslendirmeye sessizlik eklenmez.

## Fotoğraflar
- Aynı fotoğraf iki kez kullanılmaz. Fotoğraf yetmezse fotoğrafsız animasyon (belge, damga, sayaç, çizim, zaman çizgisi).
- Her fotoğraf hareket eder (sabit durmaz); kare fotoğraflar hafif yakınlaştırılıp kaydırılır. Zoom titremez.
- Kişinin kafası kesilmez; gerekirse kadraj aşağı kaydırılır.
- Grup fotoğrafında anlatılan kişi okla gösterilir (ok yazıların üstüne gelmez, yanına kısa isim).
- Nazi sembolleri küçük blur.

## Animasyon dili
- Her şey haritayla anlatılmaz; farklı animasyonlar (Mannerheim-Kreuz çizimi gibi çizim animasyonları Boran'ın favorisi).
- Logo fontu (Anton) kullanılır ama logo birebir kopyalanmaz: video içinde sarı kutu + kırmızı çizgi yok, vurgu kelimesi sarı yazı.
- Dikey fotoğraf: tamamı net ortada, kenarlar bulanık kopya. Çapraz/zig-zag hareket yok.
- Shorts'ta fotoğraflar her zaman tam ekran 9:16 (ekranı kaplar). Bulanık arka planlı geniş bant sadece uzun videolarda; Shorts'ta Boran istemedikçe yok.
- İşaret halkaları (harf, yüz) nesneyi tamamen ve rahatça içine alır; kenardan taşma olmaz.
- Ekranı karartıp dar yarık bırakma gibi anlaşılmayan efektler yok; anlatımı ok, yazı, çizim ile yap.
- Bir animasyon, ait olduğu cümle boyunca sürer; cümlenin son kelimesinde başlayıp hemen geçmez (ör. batan gemi ikonları "verlor" ile başlar).
- Ok uçları tam çizilir.
- Ses efektleri bol: her ok, rota, damga, sayaç, geçiş kendi sesini alır.

## Ses ve müzik
- Arka plan müziği hiç düşmez, sonu sönen parçalar kesilip döngüyle birleştirilir.
- Kanal logo animasyonu son cümleyle ("abonniert Chronik der Macht...") birlikte başlar, ayrı en sona eklenmez.
- Kapanışta "Wir sehen uns" yok.

## Metinler
- İsimler tam yazılır (Heinrich Lehmann-Willenbrock gibi).
- Kanal açıklaması/etiketleri kanaldaki tüm içeriği kapsar, sadece birkaç asker türüyle sınırlanmaz.
- Uzun tire yok. Övgü yok.

## Render öncesi kontrol (zorunlu)
- Render'dan ÖNCE her sahnenin önizlemesi alınır ve şunlar tek tek kontrol edilir: üst üste binen yazı (bölüm kartı ile tarih satırı dahil), ekran dışına taşan yazı, UI alanları (9:16), bulanıklaştırma yerleri.
- Özellikle sahne geçişleri ve bölüm başları için ayrıca kare alınır (kart görünürken + kart kaybolurken).
- Hata render bittikten sonra bulunursa bu bir süreç hatasıdır: önce önizleme, sonra render.
