s=open('overlay.html').read()
s=s.replace('src="t1.js"','src="t2.js"').replace('window.T1','window.T2')
s=s.replace("BOT:'left:0;top:690px;width:1920px;align-items:center',","BOT:'left:0;top:690px;width:1920px;align-items:center',SKY2:'left:0;top:400px;width:1920px;align-items:center',")
s=s.replace("const SL=[[28.86,'diag'],[39.86,'vert']];","const SL=[];")
import re
s=re.sub(r"document.getElementById\('dk'\).style.opacity=[^;]*;","document.getElementById('dk').style.opacity=0;",s)
s=s.replace("const v=t-(SL[1][0]+.14),sm=document.getElementById('seam');","const v=-1,sm=document.getElementById('seam');")
s=s.replace(" slash(t)};"," slash(t);return T.some(b=>t>=b[0]-.01&&t<b[1])};")
assert 'SKY2' in s and 'const SL=[];' in s and 'return T.some' in s and "style.opacity=0;" in s
open('overlay2.html','w').write(s)
