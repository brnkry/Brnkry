import json,subprocess,os,time,sys
D=sys.argv[1]
for x in json.load(open('ba_sel.json')):
    f=f"{D}/{x['key']}.jpg"
    if os.path.exists(f) and os.path.getsize(f)>1e5: continue
    for k in range(3):
        subprocess.run(['curl','-sSL','-m','180','-A','Mozilla/5.0 (CDM research)','-o',f,x['url']])
        if os.path.exists(f) and os.path.getsize(f)>1e5: break
        time.sleep(30)
    print(x['key'], os.path.getsize(f) if os.path.exists(f) else 'FAIL', flush=True); time.sleep(2)
print('ALLDONE')
