#!/bin/bash
cd "$(dirname "$0")"; O=/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/ocak/out
node render.js preview "$@" >/dev/null
for t in "$@"; do ffmpeg -v error -y -ss $t -i $O/base.mp4 -i prev/$t.png -filter_complex "[0][1]overlay,scale=640:360" -frames:v 1 prev/c_$t.png; done
python3 -c "
import sys;from PIL import Image
ts=sys.argv[1:];W=Image.new('RGB',(640*4,360*((len(ts)+3)//4)))
[W.paste(Image.open(f'prev/c_{t}.png'),((i%4)*640,(i//4)*360)) for i,t in enumerate(ts)];W.save('prev/m.jpg',quality=80)" "$@"
