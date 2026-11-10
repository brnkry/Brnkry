#!/bin/bash
# usage: preview.sh BASE.mp4 OUT.jpg t1 t2 ...
B=$1; O=$2; shift 2; D=$(dirname "$0"); node $D/render.js preview "$@" >/dev/null
python3 - "$B" "$O" "$@" <<'P'
import sys,subprocess,io
from PIL import Image
B,O,ts=sys.argv[1],sys.argv[2],sys.argv[3:]
import os;D=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])) if False else '.','prev')
W,H=270,480;n=len(ts);cols=min(n,8);rows=(n+cols-1)//cols
sheet=Image.new('RGB',(W*cols,H*rows))
for i,t in enumerate(ts):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',t,'-i',B,'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,stdin=subprocess.DEVNULL).stdout
    bg=Image.open(io.BytesIO(raw)).convert('RGBA');ov=Image.open(f'prev/{t}.png').convert('RGBA')
    bg.alpha_composite(ov);sheet.paste(bg.convert('RGB').resize((W,H)),((i%cols)*W,(i//cols)*H))
sheet.save(O)
P
