# Chronik der Macht: Boran'ın düzeltmelerinden kalıcı kurallar

Her yeni video (Shorts veya uzun) başlamadan önce bu dosyayı oku.

## Senkron (en önemli)
- Yazı, ses o kelimeyi söylediği anda gelir. Erken ya da geç gelmez.
- Sahne, önceki cümle bitmeden değişmez: her sahne kendi cümlesinin ilk kelimesine bağlanır (0,15 sn önce).
- Her yazı ekranda en az ~1,5 sn kalır; kalamıyorsa yazı cümlenin başında gelir ya da sonraki sahne biraz bekler.
- Animasyonlar bittikten sonra sahne ~1 sn daha ekranda kalır, hemen geçmez.
- Kelime eşleştirmesi: `werkzeuge/align_ps.py` (pocketsphinx, akustik modelle zorlamalı hizalama). align3.py duraklamalardan cümleyi yanlış bölebiliyor ve 0,5 sn kayıyor (Yamamoto'da "warned", "oil"). Kulakla/enerjiyle elle düzeltme de güvenilir değil; hizalayıcıya güven, sonra kritik kelimeleri önizlemede kontrol et. Almanca için pocketsphinx Almanca modeli gerekir; yoksa align3 + kelime kelime kontrol.
- Ses parça parça gelirse birleştirince cümle araları kısaltılır ama cümleler birbirine yapışmaz (~0,4 sn).

- Almanca hizalama: `werkzeuge/align_de.py` (pocketsphinx + CMU VoxForge Almanca modeli, SourceForge'dan indirilir). Sözlükte olmayan kelimeler sayılarla/parçalarla açılır veya fonem olarak eklenir. `free` argümanı kaydın senaryoya uyduğunu da kontrol eder.

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

## Altyazı ve ekran metni (Manstein'dan itibaren)
- Shorts'ta altyazı var: İngilizce kanaldaki gibi Oswald 600, 64 px, söylenen kelime sarı, y≈1520.
- Altyazı olduğu için ekrana altyazıyı tekrar eden başlık konmaz. Sahne başına en fazla bir-iki önemli kelime, mümkünse görselin içine yazılır (harita kâğıdı, gökyüzü, kapı, kumaş, perde).
- Altyazıda ß büyük harfte ẞ olarak kalır (Oswald'da var), sıra sayıları ("20.") ifadeyi bölmez.
- Render öncesi `kod/uicheck.py` ile her 0,2 sn'de metin katmanının sağ butonlara, üst bara ve alt başlık alanına girmediği ölçülür.
- Görsel içine yazı: kafa, el ve rozetlerden uzak, yüzeyin eğimini takip eden quad (üniforma göğsü, şapka yanı, omuz, kapı, tepe yamacı, panel).
- Haber filmindeki filigran (arşiv logosu) kadraja girmez; kırpma o bölgeden uzak tutulur.

## Metinler
- İsimler tam yazılır (Heinrich Lehmann-Willenbrock gibi).
- Kanal açıklaması/etiketleri kanaldaki tüm içeriği kapsar, sadece birkaç asker türüyle sınırlanmaz.
- Uzun tire yok. Övgü yok.

## Render öncesi kontrol (zorunlu)
- Render'dan ÖNCE her sahnenin önizlemesi alınır ve şunlar tek tek kontrol edilir: üst üste binen yazı (bölüm kartı ile tarih satırı dahil), ekran dışına taşan yazı, UI alanları (9:16), bulanıklaştırma yerleri.
- Özellikle sahne geçişleri ve bölüm başları için ayrıca kare alınır (kart görünürken + kart kaybolurken).
- Hata render bittikten sonra bulunursa bu bir süreç hatasıdır: önce önizleme, sonra render.

## Kapak ve story (Manstein'dan)
- Kapakta bütün yazılar ve logo y 330..1450 bandında; isim en büyük satır, ortanın biraz altında (y ≈ 1100..1300). Üst 330 ve alt 470 piksel telefonda kesiliyor.
- Kapakta kahramanlaştırma yok: zafer ve övgü yazısı konmaz; olgu (mahkeme, ceza) veya sorgulayan cümle kullanılır.
- Story kartında arka plan durmaz ve bulanıklaşmaz: kesitin son çekimi (Manstein'da Stuka'lar) kartın arkasında karartılmış olarak oynamaya devam eder. Bir sonraki sahneye geçilmez.
- Story çağrısı: "Schnell ins Profil und ansehen!" ("Jetzt ansehen" değil). Düzeltme istenince yalnız istenen değişir, gerisi aynı kalır.

## Knispel yeniden çekimi (Ekim 2026) dersleri
- El yazısı kelimeler (ör. "unbequem", "ausgeschmückt?", üstü çizilen "Ritterkreuz") için Caveat yazı tipi: Boran bunu beğendi, el yazısı gereken her yerde kullan.
- Yazıyı nesnenin üstüne yaz: tank yazısı taretin kavisine kazınır (metal uçla çizik), plaka yazısı plakanın açısına boyanır, miğfer yazısı miğferin ovaline oturur. Düz başlık yerine bunu tercih et ama yazı yüzü kapatmayacak kadar küçük kalsın.
- Animasyonun arkasındaki film hafif bulanık olur, izlenebilir kalır; ağır çekim yok, film normal hızda akar. Film biterse sahne biraz daha erken başlatılır, kare donmaz.
- Ekran kayıtlarında durdurulan yerler ve tekrarlanan kareler çıkarılır (kare farkı ile tespit), video pürüzsüz akar.
- Bir video ya da fotoğraf bir kez kullanılır; aynı videonun farklı kesitleri bile ayrı sahnelerde tekrar edilmez, uzun kaynak videodan yeni kesit bulunur.
- Sondaki "Kanntet ihr diese Geschichte? Schreibt es in die Kommentare!" kutusu küçük ve hareketli: balon sallanır, soru işareti zıplar, yazılar soldan sağa açılır.
- Yanlış kişi gösterilmez: grup fotoğrafında kadraj anlatılan kişiye ortalanır; başka birinin fotoğrafı (ör. SS subayı) kahramanmış gibi kullanılmaz.
- Documentary_Show.mp3 2,27 sn sessizlikle başlar: müzik her zaman 2,27 sn'den kesilir, video başlar başlamaz duyulur. Sonda müzik son 2,5 sn'de azalarak biter.
- Videoların başında siyahtan açılma (fade-in) yok: video ilk karede doğrudan görüntüyle başlar (kaydırırken siyah ekran görünmesin).
- Story'nin arka plan filmi, kartın süresinden uzun bir kesitten alınır; sonda video donmaz.
- Kapakta kanalda daha önce kullanılmış fotoğraf kullanılmaz (aynı kişinin uzun videosu dahil).
- Küçük bir düzeltmede bütün videoyu yeniden render etme: sadece etkilenen saniyeleri render edip parçaları birleştir.

## Unternehmen Greif (Ekim 2026) dersleri
- Boran yan duran kırmızı dikdörtgenli damga yazılardan (stamp) sıkıldı: artık kullanılmaz. Vurgu yazıları düz durur ve sahneye göre değişir (alt çizgi akan başlık, üstü çizilip elle düzeltilen kelime, zıplayan soru işareti, iki ince çizgi arasında karar yazısı).
- Boran'ın çok beğendiği efekt: "GEKAPPT" yazısı, önce ince kırmızı bir çizgi kelimenin ortasından geçer, sonra üst yarı kayıp kelime ikiye bölünür (`sliced` fonksiyonu, chronik/greif/kod/_gscenes.py). Kesme, kopma, bölünme anlatılan yerlerde tekrar kullan.
- Kâğıtlar, defterler, mahkeme kâğıtları düz durur (eğik koyma).
- Grafik efekt scripte uymalı: "Passwort" için giriş kutusu fazla süslü ve uyumsuz bulundu; sade başlık tercih edilir.
- Boran'ın verdiği bir görselin renklendirilmiş hali varsa siyah beyaz film yerine o kullanılır. Drive'daki bütün görseller bir şekilde kullanılır.
- Bir çizim (üstünü çizme vb.) bittikten sonra geçişten önce en az yarım saniye görünür kalır; işaret oku da nesneyle birlikte kısa bir süre ekranda kalır.
- Haritalar kontrol noktalarıyla (bilinen şehirlerin koordinatları) doğrulanır ve kadraj anlatılan bölgeye daraltılır.

## Başlık ve kapak (Ekim 2026)
- Başlık kısa: yaklaşık 40-45 karakter (mobil akışta sonrası kesiliyor). İsim, sayı veya tarih içersin.
- Başlık ile kapak yazısı aynı şeyi söylemez: kapak bir vaat, başlık başka bir merak açar.

## Otto Kretschmer (Ekim 2026) dersleri
- Bulanıklaştırma sadece gamalı haçın üstüne, küçük ve tam yerinde: kartalın tamamı, nişanın tamamı, kasket bulanıklaştırılmaz. Her nokta yakın çekimde kontrol edilir; filmde haç merkezi kare kare takip edilir.
- Ekranda büyük yazıyla söylenen cümle (hook, ünvan cümlesi) altyazıda tekrar görünmez; o aralıkta başlayan altyazı ifadeleri gizlenir.
- Her sahneye büyük yazı konmaz: görüntünün öne çıkacağı yerlerde yazı yok. Yazı yüzü veya başı kapatmaz; yer seçerken görsel kontrol edilir.
- Yazı stillerini değiştir: el yazısı (Caveat), italik Anton, zıplayan sayaç, kayan italik sayaç, nesneyi gösteren oklar. Hep aynı yer ve aynı tarz sıkıcı.
- İsimler mümkünse yüzeye yazılır (gemi adı geminin önündeki denize perspektifle, denizaltı adı denize).
- Animasyonun arkasındaki blur film sahneden kısa olursa donar: her animasyon sahnesine kendi uzunluğunda ayrı klip. Render öncesi tüm sahneler için süre kontrolü (FV ve BG).
- Haritalar: kaynakta göller yok; gerekli göl (ör. Ontario) elle çizilir, anlatılan ülke renkle vurgulanır, noktalar bilinen şehirlerle doğrulanır.
- Geçiş sesleri eskisinin yarısı seviyede.
- Tarih aralığı "1912 - 1998" (normal tire, uzun tire değil), italik.
