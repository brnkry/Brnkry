# Turkish forced alignment with pocketsphinx's English acoustic model: each Turkish word gets an
# ARPAbet pronunciation from letter rules (Turkish spelling is phonetic). usage: python3 align_tr.py voice.mp3 script.txt out.json
import sys, subprocess, json, re
from pocketsphinx import Decoder
SR = 16000
raw = subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
M = {'a':'AA','b':'B','c':'JH','ç':'CH','d':'D','e':'EH','f':'F','g':'G','ğ':'','h':'HH','ı':'IH','i':'IY','j':'ZH','k':'K','l':'L','m':'M','n':'N',
     'o':'OW','ö':'ER','p':'P','r':'R','s':'S','ş':'SH','t':'T','u':'UW','ü':'UW','v':'V','y':'Y','z':'Z','â':'AA','î':'IY','û':'UW','w':'W','x':'K S','q':'K'}
SPELL = {'wtc':'dabılyu ti si','nmf':'en em ef','ph':'pe ha','expert':'ekspört'}
def low(w): return w.replace('I','ı').replace('İ','i').lower()
def phones(w):
    p=[M[c] for c in w if c in M and M[c]]
    out=[];[out.append(x) for x in ' '.join(p).split() if not out or out[-1]!=x or x in('AA','EH','IY','UW','IH','OW','ER')]
    return ' '.join(out)
text = open(sys.argv[2]).read()
words = [low(w) for w in re.findall(r"[A-Za-zÇçĞğİıÖöŞşÜüÂâÎîÛû']+", text)]
d = Decoder(samprate=SR, bestpath=False)
toks=[];merge=[]
for i,w in enumerate(words):
    w0=w.replace("'","")
    sub=SPELL.get(w0, w0).split()
    for j,sw in enumerate(sub):
        key=f'w{i}_{j}'; d.add_word(key, phones(sw), False); toks.append(key)
    merge.append((w0,len(sub)))
d.set_align_text(' '.join(toks)); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
seg=[[s.word, round(s.start_frame/100,2), round((s.end_frame+1)/100,2)] for s in d.seg() if s.word not in ('<s>','</s>','<sil>','[NOISE]')]
out=[];k=0
for w,n in merge:
    part=seg[k:k+n];k+=n
    if part: out.append([w,part[0][1],part[-1][2]])
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False)
print(len(words),'words,',len(out),'aligned')
