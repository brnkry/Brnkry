# Franz Stigler ve Charlie Brown (Chronik der Macht Shorts)

Bu video **Chronik der Macht** kanalı için, What the Car? kanalıyla ilgisi yok.

- Ses: ElevenLabs "Helmut" (112,77 sn). Müzik: Documentary_Show.mp3, seviye 0.24 (kalp atışında kısılıyor).
- `words.json`: kelime zamanlaması (sessizlik + hece çekirdeği hizalaması, `kod/dp.py` ve `kod/words2.py`).
- `kod/scenes.py`: 22 sahne, sırayla fotoğraf ve animasyon. Atlas tonlarında harita (parşömen kara, arduvaz deniz, pas kırmızısı rota).
- `kod/sfx.py`: efektler (4 motorlu B-17 uğultusu, tek motorlu Bf 109, uzak Flak, kalp atışı, kalem, mühür, daktilo).
- Render: `python3 kod/scenes.py render part.mp4 <bas> <son>` (4 paralel parça), ardından ffmpeg ile miks (ses 1.0, müzik 0.24, efekt 0.85, alimiter 0.93).
- Fotoğraflar (p01–p11) Boran'ın Arşiv.zip dosyasından geliyor. p04 (John D. Shaw tablosu) telifli olduğu için kullanılmadı.
- Blur uygulanan yerler: p08 şapka kartalı ve göğüs kartalı; p03 Şövalye Haçı merkezi, göğüs kartalı ve pilot rozeti; p02 kuyruktaki svastika.
