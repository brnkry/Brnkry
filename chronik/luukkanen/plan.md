# Eino Luukkanen: script ve bilgiler

## Almanca script
`script_de.txt` (tiresiz, v2: hikâye anlatımı). ElevenLabs'e olduğu gibi yapıştırılır.

## Doğrulanmış bilgiler
- 04.06.1909 Jaakkima (Karelya) doğumlu, Sortavala'da (Ladoga Gölü) büyüdü. 09.04.1964 Jyväskylä'da öldü (54 yaşında).
- 1931 pilot subay eğitimi, 1933 subay. Hava kuvvetlerinde 1931 ile 1951 arası, son rütbe yarbay.
- Kış Savaşı: 3/LLv 24 komutanı, Fokker D.XXI. 01.12.1939'da ilk zaferi (SB-2 bombardıman uçağı). Kış Savaşı toplamı 2,5.
- Devam Savaşı: 1/LLv 24, Brewster B-239 (Buffalo), 14,5 zafer.
- Mart 1943'ten itibaren binbaşı olarak LeLv 34 komutanı, Bf 109 G (39 zafer bu tiple).
- Mannerheim Haçı: 18.06.1944.
- 56. ve son zafer: 05.08.1944, Bf 109 G-6 ile bir Yak-7.
- 56 onaylı zaferle Finlandiya'nın üçüncü sıradaki pilotu (Juutilainen ve Wind'den sonra).
- Anıları: "Hävittäjälentäjänä kahdessa sodassa", İngilizcesi "Fighter over Finland" (1963).
- Finlandiya ile Sovyetler Birliği arasında ateşkes Eylül 1944.

## Bilinçli olarak dışarıda bırakılanlar
- İlk zaferin "savaşın ilk hava zaferi" olduğu iddiası (aynı gün başka pilotların da zaferi var, tartışmalı)
- Utti havaalanı (tek kaynak)
- Savaş sonrası iş (doğrulanamadı)

## Kaynaklar
- https://en.wikipedia.org/wiki/Eino_Luukkanen
- https://en.wikipedia.org/wiki/List_of_World_War_II_aces_from_Finland
- https://en.wikipedia.org/wiki/No._24_Squadron_(Finland)
- https://info.eduard.com/en/04-2024-1/page-47
- https://catalog.hathitrust.org/Record/000806145
- https://data.nationallibrary.fi/au/pn/000114865

## Yapım notları (video v1)
- Ses: ElevenLabs, 128,7 sn, kesilmedi. Kelime zamanlaması `words.json`.
- 24 fotoğrafın hepsi kullanıldı (l01-l24, eşleme `names.txt`). l14 ve l15 neredeyse aynı fotoğraf: l14 geniş, l15 kuyruktaki zafer işaretlerine yakınlaşma.
- Giriş: üç uçak fotoğrafı üst üste bantlar halinde (Fokker, Brewster, Bf 109), sonra l01 portre, 56 zafer çizgisi ve isim.
- Yeni animasyonlar: zafer çizgisi sayacı (56 ve 14,5), Karelya haritası ve 1940'ta bırakılan bölge, takvim yaprağı (30 Kasım 1939), 1'e karşı çok uçak, "VERALTET" üstü çizme, Mannerheim-Kreuz ışık geçişi, 1909-1964 yaşam çizgisi, beyaz flaş geçişi.
- Müzik: Documentary Show 2,0 sn'den başlar, ilk 3,2 sn güçlendirilir, ses altında sidechain ile kısılır.
- Story: 12 sn, girişin 8,6 sn'si ve ardından "Neues Video / Die ganze Geschichte jetzt im Profil" + Folgen, Liken, Teilen.
- Fin hava kuvvetleri arması (mavi hakaristi) l07 ve girişteki Fokker bandında görünüyor, blur yok.

## v2 (Boran'ın düzeltmeleri)
- 56 çizgileri kaldırıldı: büyük italik "56", önce 5 sonra 6. İsim italik (Montserrat Italic).
- Harita sahneleri kaldırıldı. Yerine fotoğraf (l13 ve l18), üstünde şeffaf harita penceresi.
- Takvim şeffaf cam panel. Fokker fotoğrafı daha geniş gösteriliyor (bulanık arka plan üstünde).
- Fin uçaklarındaki gamalı haçlar küçük blur: l23, l12, l07, l24 (girişteki bantlar dahil).
- Senkron düzeltildi: 1:05 "finnische Piloten", 1:22 "Major / Jagdstaffel 34", 1:24 "Messerschmitt" (`align2.py`, elle düzeltilmiş `words.json`).
- l15 (l14'ün kopyası) çıkarıldı. 14,5 sahnesinde l08, Übermacht sahnesinde l06; 23 fotoğrafın her biri bir kez.
- 14,5 ve 56. italik, çizgiler yok, "LETZTER LUFTSIEG" 56.'nın altında.
- 1:32 sahnesi en sağdaki adamdan (Luukkanen) başlar. 2:03 fotoğrafı sağdan alındı.
- Story: portre sona kadar kesintisiz kayar, 7-8. saniyedeki takılma giderildi.

## v3
- İtalik: aynı Anton fontu, sadece eğik (56, isim, 14,5, 56.). İsim boyut ve aralığı eski haliyle.
- Harita penceresi yumuşak köşeli dikdörtgen; FINNLAND yazısı Finlandiya alanının sol üstünde.
- Takvim yine yarı şeffaf panelde.
- 1:05 hatası: "finnische" araması 18. saniyedeki "finnischen" kelimesini buluyordu; artık 60. saniyeden sonra aranıyor. "finnische" 66,78 sn.
- 14,5 yukarı alındı, virgül alttaki yazıya değmiyor.
- Metadaten: `metadata.md`.
