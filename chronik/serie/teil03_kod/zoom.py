import sys
from PIL import Image, ImageDraw
# zoom.py name x0 y0 x1 y1 out [scale]  (pixel coords of original)
n,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
s=float(sys.argv[7]) if len(sys.argv)>7 else 4
im=Image.open(f'/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3l/img/{n}.jpg').convert('RGB').crop((x0,y0,x1,y1))
im=im.resize((int((x1-x0)*s),int((y1-y0)*s)),Image.LANCZOS)
d=ImageDraw.Draw(im)
st=10 if (x1-x0)<=120 else 20
for x in range((x0//st+1)*st,x1,st):
    X=(x-x0)*s; d.line([(X,0),(X,im.height)],fill=(255,0,0) if x%(st*5)==0 else (255,160,160),width=1); d.text((X+2,2),str(x),fill=(255,0,0))
for y in range((y0//st+1)*st,y1,st):
    Y=(y-y0)*s; d.line([(0,Y),(im.width,Y)],fill=(255,0,0) if y%(st*5)==0 else (255,160,160),width=1); d.text((2,Y+2),str(y),fill=(255,0,0))
im.save(out,quality=88)
