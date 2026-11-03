import hashlib, subprocess, time, urllib.parse, os
names = {0:"Heinz Wolfgang Schnaufer 1944.jpg",2:"Calw schnaufer1.jpg",3:"Bundesarchiv Bild 101I-680-8274A-15A, Funkleitstelle für Nachtjäger.jpg",6:"Bf 110 SM.jpg",7:"RAAF 462 Sqn crew with Me 110 of W Schnaufer 1945.jpg",8:"Heinz-Wolfgang Schnaufer tail fin.JPG"}
for rnd in range(4):
    for i,n in names.items():
        f = n.replace(' ','_'); out = 'w%02d.%s' % (i, f.rsplit('.',1)[1].lower())
        if os.path.exists(out) and open(out,'rb').read(3) == b'\xff\xd8\xff': continue
        h = hashlib.md5(f.encode()).hexdigest()
        url = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (h[0], h[:2], urllib.parse.quote(f))
        r = subprocess.run(['curl','-sS','-A','BrnkryResearch/1.0 (history education)','-o',out,'-w','%{http_code}',url],capture_output=True,text=True)
        print(rnd, out, r.stdout, flush=True); time.sleep(30)
