import re,html,json,sys,urllib.parse,subprocess
out={}
for q in sys.argv[2:]:
    u="https://www.bild.bundesarchiv.de/dba/de/search/?query="+urllib.parse.quote_plus(q)+"&limit=50"
    t=html.unescape(subprocess.run(["curl","-s","-m","40",u],capture_output=True,text=True).stdout)
    for m in re.finditer(r'"DC5Signatur":"([^"]+)","zoomurl":"([^"]*)","orignalurl":"([^"]*)","date":"([^"]*)"',t):
        sig,z,o,d=m.groups(); seg=t[max(0,m.start()-6000):m.start()]
        ti=re.findall(r'\{"values":\["((?:[^"\\]|\\.)*)"\],"label":"Archivtitel"\}',seg)
        title=json.loads('"'+ti[-1]+'"') if ti else ''
        out.setdefault(sig,dict(sig=sig,title=title,date=d,url="https://bild.bundesarchiv.de/device_barch"+urllib.parse.unquote(z).replace('/barch/device',''),q=q))
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=1); print(len(out))
