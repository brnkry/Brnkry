# usage: python3 sheet.py out.jpg files...  (3 columns, 640x360 tiles, time label)
import sys
from PIL import Image, ImageDraw
fs=sys.argv[2:];W,H=640,360;cols=3;rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(W*cols,H*rows),'black');d=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    im=Image.open(f).resize((W,H));x,y=(i%cols)*W,(i//cols)*H;S.paste(im,(x,y));d.text((x+8,y+6),f.split('_')[-1][:-4],fill='yellow')
S.save(sys.argv[1],quality=80)
