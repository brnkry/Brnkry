# Long 02: Tire pressure light (TPMS), 16:9, ~4.5 min

Her parça ayrı mp3 olabilir ya da hepsi tek dosya (hizalama aracı ikisiyle de çalışıyor).
Seslendirme notu: "P S I" harf harf okunsun diye boşluklu yazıldı, altyazıda "PSI" görünecek.

## 01 hook
It's the first cold morning of the year. You start your car, and this light comes on. You walk around the car, and all four tires look perfectly fine. So what's going on? Here's the strange part. By lunchtime, the light might turn itself off. Problem solved, right? Not exactly, and that's the trap. And if this light is flashing instead of staying on, it means something completely different. In the next few minutes you'll know exactly what your car is trying to tell you, and how to fix it in about five minutes.

## 02 what
This is the tire pressure warning light. The symbol is a cross section of a tire with an exclamation point in the middle. The system behind it is called T P M S, short for tire pressure monitoring system, and every new car and light truck sold in the US has had one since the 2008 model year. Here's what most people don't realize. By law, the light has to come on when a tire is 25 percent below the pressure your car's maker recommends. So if your tires should be at 35 P S I, the light may not come on until one of them drops to around 26. When you see this light, a tire isn't a little low. It's already very low.

## 03 cold
So why does it love cold mornings? Air shrinks when it gets cold. A good rule of thumb is that tire pressure drops about one P S I for every 10 degrees Fahrenheit. Let's say your tires were set on a warm 70 degree afternoon, and tonight it drops to 30. That's 40 degrees, so roughly four P S I gone, without a single leak. Overnight, the tires sit at the coldest temperature of the day, so that's when the light comes on. Then you drive, the tires warm up, the pressure climbs back, and the light goes off. But tomorrow morning, it's back. The light didn't lie. Your tires really are low every time they're cold, and cold is when you should measure them.

## 04 flashing
Now, the flashing version. If the light flashes for about a minute when you start the car and then stays on, that's not a low tire. It means the monitoring system itself has a problem. On most cars, each wheel has a small sensor with its own battery inside, and those batteries usually last somewhere between five and ten years. A dead sensor, a damaged one, or a wheel swap without the right sensors can all cause it. Your tires might be fine, but the system can't watch them anymore, so get it checked at a tire shop.

## 05 pressure
So what is the right pressure? Here's the most common mistake. The big number printed on the side of your tire is not the number you want. That's the maximum the tire can safely hold. The right number is on a sticker inside the driver's door frame, and it's also in your owner's manual. Some cars use a different pressure for the front and rear tires, so read it carefully. And always check when the tires are cold, which means the car has been parked for a few hours or driven less than a mile.

## 06 fix
Here's the five minute fix. Find the number on the door sticker. Get a tire gauge, or use the air machine at a gas station. Check all four tires, and on some cars the spare too, because a few systems watch the spare as well. Add air until each tire matches the sticker. Then drive for a few minutes, and the light should go off on its own. Some cars need you to reset the system, and your owner's manual will show you how. If the light comes back within a day or two, one tire is probably losing air, maybe from a nail or a bad valve, so have it checked.

## 07 why
Why does this matter? Low tires flex more and run hotter, they wear out faster, and they make the car handle and brake worse. They also cost you money at the pump. According to the US Department of Energy, every one P S I drop in average pressure lowers your gas mileage by about 0.2 percent. So don't wait for the light. Check your tires once a month, and every time the weather turns cold.

## 08 close
So the next time this light shows up on a cold morning, you'll know exactly what to do. Did this light ever surprise you on a cold day? Tell me in the comments. And if this helped, subscribe to What the Car? so you don't miss the next one.

## Üretim notları
- BMW sesi bu videoda YOK. Yerine sentez `warn` sesi (audio_hook.py içinde, iki notalı ding). Lamba yine sadece ses gelince yanar.
- Parça 1+2 tek ses: `01_02.mp3`, sahne `scene01_02.html`, hizalama `align_01_02.json`.
- Kanca dış mekân (kırağı, bereli sürücü), parça 2'den itibaren stüdyoda anlatıcı.
- Birleştirme: `parts.json` + `./build.sh cikti.mp4` (kesintisiz müzik).
- Parça 3-8 tek ses `03_08.mp3`, sahne `scene03_08.html`. Tam video `tpms_full.mp4` (3:59), export: `wtc/exports/tpms_light_full.mp4`.
- Kontrol: köşede kalan obje taraması (her saniye #ill > g grupları sol üst köşede mi diye bakar) yeni sahnelerde de çalıştırılmalı.
