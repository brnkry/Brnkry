import sys
from PIL import Image, ImageDraw
fs=sys.argv[2:];W,H=360,640;cols=6;rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(W*cols,H*rows),'black');d=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    im=Image.open(f).resize((W,H));x,y=(i%cols)*W,(i//cols)*H;S.paste(im,(x,y));d.text((x+6,y+6),f.split('_')[-1][:-4],fill='red')
S.save(sys.argv[1],quality=82)
