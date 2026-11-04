# download chosen Commons files (2000px thumbs), honouring Retry-After
import json, time, urllib.request, os, re
UA = 'CDM-research/1.0 (history documentary research)'; m = json.load(open('commons_meta.json')); os.makedirs('cm', exist_ok=True)
PICK = ['Bf109E-3 Farbe.jpg', 'Fliegerpokal Wick.jpg', 'Helmut Wick EK I und Eichenlaub Stecknadel.JPG', 'John Dundas by Cuthbert Orde.jpg',
        'Memorial to John Charles Dundas, at Freshwater Bay, Isle of Wight.jpg', 'He 111 hit near Bristol in September 1940.jpg', 'Spitfires camera gun film shows tracer ammunition.jpg',
        'RAF Fighter Command 1940 HU104509.jpg', 'Ministry of Information Second World War Press Agency Print Collection MH21983.jpg', 'The Battle of Britain HU67701.jpg',
        'The Battle of Britain HU76146.jpg', 'Spitfire and Me 109 in flight 1940.jpg', 'The Battle of Britain 1940 CH2064.jpg', 'Horse Sand Fort gun 24-08-1940 IWM H 4618.jpg',
        '9.2 inch gun and crew Culver Point Battery 24-08-1940 IWM H 3233.jpg', 'Royal Air Force Fighter Command, 1939-1945. CH1826.jpg', 'Heinkel He 111 fly over Southampton.jpg']
for p in PICK:
    k = 'File:' + p; v = m.get(k)
    if not v: print('missing', p); continue
    fn = 'cm/' + re.sub(r'[^A-Za-z0-9._-]+', '_', p)
    if os.path.exists(fn): continue
    for a in range(6):
        try:
            d = urllib.request.urlopen(urllib.request.Request(v['url'], headers={'User-Agent': UA}), timeout=90).read(); open(fn, 'wb').write(d); print('ok', fn, len(d), flush=True); break
        except urllib.error.HTTPError as e:
            w = int(e.headers.get('Retry-After', '30')) + 2 if e.code == 429 else 10; print(e.code, 'wait', w, flush=True); time.sleep(w)
    time.sleep(3)
