# "The True Origin of World War II: It Didn't Start in 1939": analiz ve Almanca uyarlama planı

Çalışma adı (CDM): **"Der wahre Ursprung des Zweiten Weltkriegs: Er begann nicht 1939"**

## 1. Orijinal video nasıl yapılmış?
- **Süre ve format:** 30:38, 16:9, 720p, 30 fps. Konuşma 30:24'te bitiyor, son 14 saniye abone çağrısı.
- **Görüntüler:** Hepsi **yapay zekâ ile üretilmiş, hareketli sahneler** (görüntüden videoya). Gerçek arşiv kaydı yok denecek kadar az.
  - Sepya ve siyah beyaz "1920'ler fotoğrafı" görünümünde sahneler: insanlar kafa çeviriyor, kalabalık hafifçe kıpırdıyor.
  - Yüzler ve yazılar yer yer bozuk. Ör. "Bürgerbräu-Keller" tabelası, uydurma belgeler, "DIPLOMATIC AGREEMENT" yazılı yırtık kâğıt.
  - Hitler, Mussolini, Chamberlain ve Churchill'in yapay zekâyla üretilmiş "fotoğrafları" var.
  - Sonda modern sahneler var: Yunan bayraklı bir gösteri, gazete okuyan yaşlı adam.
- **Kurgu:** Yaklaşık 150 sahne, her biri ortalama 10-12 saniye. Geçişler hep aynı: 1,5 saniyelik yumuşak çapraz geçiş.
  - Sert kesme, efekt, müzik vurgusu yok denecek kadar az.
  - Kamera sabit, hareketi sadece sahnenin kendisi veriyor.
- **Eklenenler:**
  - **Sol alt köşede küçük etiket kartı:** krem renkli zemin, solunda küçük kırmızı kare, daktilo yazısı (monospace, büyük harf). Yazı harf harf yazılıyor.
  - Etiket örnekleri: "JUNE 28, 1919", "$33 BILLION DOLLARS", "HITLER CHANCELLOR 30 JAN 1933", "FRANCISCO FRANCO".
  - Toplam yaklaşık 10-12 etiket var, sadece kritik tarih, isim ve rakamlarda.
- **Harita, grafik, sayaç yok.** 10:50'de silik bir çizim haritası dışında bilgi grafiği yok. Bu, bizim için en büyük fırsat (bkz. bölüm 5).
- **Ses:** Tek erkek anlatıcı, sakin ve ağır. Altta çok kısık, değişmeyen bir piyano/drone müziği var. Ses efekti yok.

## 2. Altyazı (birebir kopyalanacak stil)
| Özellik | Değer (720p ölçümü → 1080p karşılığı) |
|---|---|
| Yazı tipi | Klasik serif, Times / Liberation Serif / Tinos benzeri, düz (italik değil) |
| Boyut | ~30 px → **~45 px** (1080p) |
| Renk | Sıcak altın sarısı **#CDC370** civarı, hafif şeffaf |
| Kontur | Yok. Çok hafif yumuşak gölge var. |
| Zemin | Satırın arkasında, metni ancak saran **%35 siyah, çok hafif bir bant** |
| Konum | Ortada, alttan ~%10 yukarıda: 720p'de y ≈ 638-663 → **1080p'de y ≈ 955-995** |
| Satır | Tek satır, cümlenin bir parçası (6-10 kelime), en fazla ~65 karakter |
| Animasyon | Her parça **~0,4 saniyede belirerek** (fade in) geliyor, sonraki parça gelince değişiyor |

Almanca altyazıyı **Tinos** (açık lisanslı, Times metrikli) ile, aynı renk ve konumda, kelime zamanlamasından otomatik keserek yaparım.

## 3. Metin ve karakter sayısı
- İngilizce orijinal: 35.086 karakter, 5.625 kelime.
- **Almanca metin: 35.739 karakter** (boşluklar dahil, tek paragraf), 4.964 kelime → `script_de.txt`.
- Tahmini Almanca okuma süresi **~31-33 dakika** (Robert Ranger hızıyla, duraklar kırpılınca ~30 dakika).
- **ElevenLabs:** Tek seferde verilen metin sınırı nedeniyle 8 parçaya bölmek gerekiyor, her parça ~4.500 karakter ve paragraf sınırında. Parçalar aynı ses ve ayarla üretilip birleştirilir.
  - Toplam kredi ≈ **35.700 karakter** (eleven_v4'te yaklaşık bir karakter bir kredi).
  - Uzun video olduğu için başa `[quickly reads]` konmayacak.
- Türkçe karşılığı: `script_tr.txt`.

### Almancada orijinalden farklı yaptıklarım
1. **Yanlış rakamlar düzeltildi.** Giriş ve akış aynı kaldı.
   - "50 milyon ölü" → **"über 60 Millionen"** (güncel kabul gören rakam).
   - Sömürgeler "4,5 milyon km²" → **"fast drei Millionen km²"** (gerçek değer ~2,9 milyon).
   - 1923 kurları: "Haziranda 192.000, Ekimde 170 milyar" yanlış → **"Temmuzda 350.000'in üstü, Ekim sonunda 70 milyarın üstü"**. Kasım 1923'teki 4,2 trilyon doğru, kaldı.
   - Tazminat: "33 milyar dolar" yanına **"132 Milliarden Goldmark"** eklendi (Almanca izleyici bunu bilir).
   - Franco: "darbeyi Franco yönetti" yerine **"Franco'nun da aralarında olduğu askerler"**. Darbenin lideri başlangıçta Mola/Sanjurjo idi.
2. **CDM üslubu:** Abartılı ve tarafgir ifadeler yumuşatıldı. "Political cowardice" yerine "politisches Wegsehen", "negligence on a civilizational scale" yerine "Fahrlässigkeit in historischem Ausmaß" oldu.
3. **Final:** Orijinaldeki "bugün de aynı ritimleri duyuyoruz" bölümü günümüz siyasetine göndermeydi. Bunu tarafsız bir genel ders cümlesine çevirdim (kanal güvenliği için).
4. **Sorular:** Retorik sorular düz cümle yapıldı. Sadece "Wer trug wirklich die Verantwortung?" kaldı; o bir bölüm başlığı işlevi görüyor.
5. Abone çağrısı CDM'e uyarlandı. Uzun tire hiç yok.
6. Almanca terimler doğru kullanıldı: Dolchstoßlegende, Diktat, Festungshaft, Rentenmark, Reichskanzler, Anschluss, Rest-Tschechoslowakei, Hitler-Stalin-Pakt.

## 4. Bölümler (orijinal zaman kodlarıyla)
| Süre | Bölüm |
|---|---|
| 0:00 | Giriş: "1 Eylül 1939 değil" |
| 0:39 | Versay, 28 Haziran 1919, Aynalı Salon |
| 1:54 | Madde 231, imza ya da abluka |
| 2:31 | Toprak kayıpları (Alsas-Loren, Koridor, Saar, Danzig, sömürgeler) |
| 3:44 | Askeri kısıtlamalar, Ren bölgesi |
| 4:05 | Tazminatlar (132 milyar altın mark) |
| 4:28 | Alman bakış açısı, Diktat, Dolchstoßlegende |
| 5:44 | Para basma, hiperenflasyon 1923 |
| 7:47 | Orta sınıfın çöküşü, Hitler darbesi, Mein Kampf |
| 8:59 | Rentenmark, Dawes Planı, Wall Street kredileri |
| 9:50 | Altın Yirmiler |
| 10:17 | Para döngüsü (ABD → Almanya → İngiltere/Fransa → ABD) |
| 10:54 | 1929 krizi, Büyük Buhran |
| 11:34 | Almanya'da işsizlik (1,5 → 4 → 6 milyon) |
| 12:40 | NSDAP oyları (%2,6 → %18,3 → %37), 30 Ocak 1933 |
| 13:46 | Japonya, ırk eşitliği maddesi, buhran |
| 14:50 | Mukden 1931, Mançukuo, Lytton Raporu |
| 16:30 | Mussolini, Etiyopya 1935, Haile Selassie, Hoare-Laval |
| 18:00 | Hitler Versay'ı parçalıyor: 1933, 1935, Deniz Antlaşması |
| 18:58 | Ren bölgesi, 7 Mart 1936 |
| 20:20 | İspanya İç Savaşı, Condor Lejyonu, Guernica |
| 21:50 | Anschluss 1938 |
| 22:19 | Südet krizi, Münih, "Peace for our time", Churchill |
| 23:47 | Mart 1939 Prag, Polonya garantisi |
| 24:48 | Hitler-Stalin Paktı, 1 Eylül 1939 |
| 25:40 | Özet ve "her durakta önlenebilirdi" |
| 27:00 | Ders: kriz, aşağılanma, günah keçisi, güçlü adam |
| 28:27 | Kim sorumluydu? |
| 29:07 | Final ve abone |

## 5. Bizim versiyon: daha ilgi çekici nasıl yaparız?
Orijinal 30 dakika boyunca hep aynı tempoda: yapay zekâ sahnesi, çapraz geçiş, yapay zekâ sahnesi. Biz aynı akışı koruyup şunları ekleriz:

1. **Gerçek arşiv, yapay zekâ yok.** CDM'in gücü gerçek görüntü. Bundesarchiv fotoğrafları, archive.org'daki Wochenschau ve haber filmleri, Library of Congress ve NARA kullanılır. Yavaş yakınlaşma ve kaydırma (Ken Burns), film grenli sepya ton, orijinaldeki gibi 1,5 saniyelik çapraz geçişler.
2. **Haritalar** (Teil serisindeki motorla):
   - Versay toprak kayıpları: bölgeler tek tek kırmızı yanar, sayaç %13'e çıkar.
   - Polonya Koridoru ile Doğu Prusya'nın kopması.
   - Ren bölgesinin taranması, 1936'da Alman okları.
   - Mançurya, Etiyopya, İspanya: dünya haritasında atlamalar.
   - 1938-39 genişleme sırası: Avusturya → Südet → Prag → Polonya.
3. **Sayaçlar ve grafikler:**
   - Dolar kuru sayacı: 17.000 → 350.000 → 70 milyar → 4,2 trilyon. Hiperenflasyonun en çarpıcı anı.
   - İşsizlik sayacı: 1,5 → 4 → 6 milyon.
   - NSDAP oy çubukları: %2,6 → %18,3 → %37.
   - **Para döngüsü animasyonu:** ABD → Almanya → İngiltere/Fransa → ABD dairesi; 1929'da halka kopar.
4. **Etiket kartları:** Orijinaldeki krem zeminli, kırmızı kareli daktilo etiketlerini Almanca yaparız: "28. JUNI 1919", "132 MRD. GOLDMARK", "30. JANUAR 1933" vb.
5. **Belge görüntüleri:** Madde 231'in gerçek metni, Mein Kampf'ın ilk baskısı, Münih Antlaşması, Chamberlain'in kâğıdı.
6. **Müzik:** Teil serisindeki gibi bölüm bölüm değişen, sakin ama tek düze olmayan müzik.

## 6. Gereken görseller (bölüm bölüm, kaynak önerisiyle)
| Bölüm | Görsel / film | Kaynak |
|---|---|---|
| Giriş | Polonya sınır bariyerinin kaldırılması, 1 Eylül 1939 (gerçek fotoğraf) | Bundesarchiv ("Schlagbaum" fotoğrafları) |
| Versay | Aynalı Salon'da imza, 28.6.1919 (fotoğraf ve film) | Bundesarchiv, Library of Congress, archive.org "Versailles 1919" haber filmleri |
| Versay | Clemenceau, Wilson, Lloyd George ("Big Four") | LoC (kamu malı) |
| Madde 231 | Antlaşma metni ve imza sayfası | Wikimedia, Politisches Archiv AA |
| Abluka | Almanya'da açlık, kuyruklar 1918-19 | Bundesarchiv |
| Toprak | Harita animasyonu (bizim motor) | Natural Earth ve 1914/1920 sınırları |
| Ordu | Reichswehr 1920'ler, sökülen toplar ve tanklar (Interalliierte Kontrollkommission) | Bundesarchiv |
| Tazminat | Fransa'ya giden kömür trenleri, Ruhr işgali 1923 | Bundesarchiv |
| Kaiser | Wilhelm II sürgünde, Doorn | Bundesarchiv |
| Dolchstoß | Dönemin karikatür ve afişleri (afişlerde sembol bulanık) | Bundesarchiv Plak |
| Enflasyon | Para tomarları, el arabaları, parayla oynayan çocuklar, para yakılan soba, 1923 | Bundesarchiv (çok sayıda), Wikimedia |
| Darbe | Münih 9 Kasım 1923, Bürgerbräukeller, Odeonsplatz | Bundesarchiv |
| Mein Kampf | Landsberg hücresi, ilk baskı kapağı (bulanık sembol) | Bundesarchiv |
| Dawes | Charles Dawes portresi, Londra Konferansı 1924 | LoC, Bundesarchiv |
| 20'ler | Berlin gece hayatı, Potsdamer Platz trafiği, sinema | archive.org "Berlin: Symphony of a Metropolis" (1927, kamu malı) |
| Wall Street | 1929 Wall Street kalabalıkları | LoC, NARA |
| Buhran | Aşevi kuyrukları (ABD ve Berlin), işsizlik büroları | LoC, Bundesarchiv |
| Seçimler | 1930 ve 1932 seçim afişleri, sandık başında kuyruk | Bundesarchiv |
| 1933 | 30 Ocak 1933 meşale yürüyüşü (sembol bulanık) | Bundesarchiv |
| Japonya | Paris'te Japon heyeti, Mukden 1931, Mançurya'da Japon askerleri | Wikimedia (Japon kamu malı), archive.org |
| Lytton | Lytton Komisyonu Mançurya'da | Wikimedia |
| Etiyopya | Haile Selassie Cenevre'de (1936 konuşma filmi), İtalyan birlikleri | archive.org, LoC |
| Cemiyet | Cenevre'de Völkerbund toplantıları | UN Archives Geneva, Bundesarchiv |
| 1935 | Luftwaffe ve askerlik yeniden başlıyor | Bundesarchiv |
| Rheinland | 7 Mart 1936, Köln Hohenzollernbrücke'de askerler | Bundesarchiv |
| İspanya | Franco, Condor Lejyonu, Guernica yıkıntıları | Bundesarchiv, Wikimedia |
| Anschluss | Mart 1938 Viyana | Bundesarchiv |
| Südet | Çekoslovak sınır tahkimatları, Südet bölgesi 1938 | Bundesarchiv, Wikimedia |
| Münih | Chamberlain, Daladier, Hitler, Mussolini, 29-30.9.1938 | Bundesarchiv (Bild 183-R69173 serisi) |
| Heston | Chamberlain kâğıdı sallıyor (film) | archive.org British Pathé kamu malı kopyaları ya da IWM |
| Churchill | Churchill 1938-39 | LoC, IWM |
| Prag | 15 Mart 1939 Prag, ağlayan kalabalık | Bundesarchiv |
| Pakt | Molotov imzalıyor, arkada Stalin ve Ribbentrop, 23.8.1939 | Bundesarchiv Bild 183-H27337 |
| 1 Eylül | Westerplatte, Schleswig-Holstein zırhlısı, sınır bariyeri | Bundesarchiv |
| Final | Hızlı görsel özet: Versay → enflasyon → Wall Street → Münih → Polonya | yukarıdakilerden |

Notlar:
- Gamalı haç ve benzeri semboller fotoğraflarda ve afişlerde bulanıklaştırılır.
- British Pathé ve AP filmleri telifli. Sadece kamu malı kopyalar (archive.org, LoC, NARA) ve Bundesarchiv kullanılır.

## 7. Onaydan sonraki iş sırası
1. Ses: 8 parça, Robert Ranger, eleven_v4. Duraklar kırpılır, kelime zamanlaması çıkarılır.
2. Görseller: Bundesarchiv ve archive.org'dan indirilir, eksikler için sana link listesi verilir.
3. Haritalar, sayaçlar ve para döngüsü animasyonları.
4. Kurgu, altyazı (orijinal stil), etiket kartları, müzik.
5. Bölüm bölüm render ve kontrol, ardından teslim.
