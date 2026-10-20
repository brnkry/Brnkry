# First Day as a Hitman (claymation tarzı Short)

Three.js ile hamur görünümlü 3D sahneler, 12 fps stop-motion, kodla sentezlenmiş müzik ve efektler.

## Dosyalar
- `lib.js`: hamur malzemesi (parmak izi ve ezik dokusu), engebeli geometri, anahtar kare yardımcıları
- `chars.js`: Rookie ve Big Tony; IK kollar/bacaklar, yüz ifadeleri (kaş, göz kapağı, ağız, dil, ter)
- `sets.js`: oda, kafe terası, hastane odası ve rekvizitler (çanta, kitap, ördek, zehir şişesi, gazete, fincan, pasta)
- `film.js`: çekim listesi ve koreografi (`window.R(t)` t saniyedeki kareyi çizer)
- `audio.py`: piziçato müzik, foley, ambiyans
- `render.js`, `stills.js`: Playwright ile kare render ve test kareleri

## Çalıştırma
```
npm i                                  # hitman/ içinde (three + fontlar)
(cd ../wtc && npm i)                   # playwright
python3 -m http.server 8765 &          # hitman/ içinde
node render.js frames 12               # 12 fps kareler
python3 audio.py mix.wav
./encode.sh                            # 1080x1920 mp4
```

## Senaryo (61 sn)
1. Odada "FIRST DAY AS A HITMAN!" pankartı. Çantaya HITMAN 101 kitabı, sandviç ve lastik ördek. Aynaya başparmak.
2. Kafe: Tony gözleri kapalı pasta yiyor. Rookie minicik saksının arkasında, sonra göz delikli gazete ("LOCAL HITMAN STARTS TODAY").
3. Parmak ucunda yaklaşma, Tony dönünce heykel pozunda donma.
4. Espressoya zehir, parmakla karıştırma, parmak tozlu.
5. İz kalmasın diye parmağı yalama, gurur, sonra şaşı gözler.
6. Tahta gibi pastaya kapaklanma. Tony fincanı bırakıp itiyor.
7. Hastane: Tony aynı espressoyu getirip göz kırpıyor.
8. Rookie geri itiyor, Tony bir dikişte içiyor ve hiçbir şey olmuyor, Rookie korkudan bayılıyor.
