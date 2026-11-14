import sys
from PIL import Image, ImageDraw, ImageFont
L='/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t4l/'
names=sys.argv[2:]; out=sys.argv[1]; W=760
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
tiles=[]
for n in names:
    im=Image.open(L+'img/'+n+'.jpg').convert('RGB'); w,h=im.size; s=W/w; t=im.resize((W,int(h*s))); d=ImageDraw.Draw(t)
    for i in range(1,10):
        x=int(W*i/10); y=int(t.size[1]*i/10)
        d.line((x,0,x,t.size[1]),fill=(255,0,255),width=1); d.line((0,y,W,y),fill=(255,0,255),width=1)
        d.text((x+2,2),str(i),font=f,fill=(255,255,0)); d.text((2,y+2),str(i),font=f,fill=(0,255,255))
    d.rectangle((0,t.size[1]-22,W,t.size[1]),fill=(0,0,0)); d.text((6,t.size[1]-20),'%s %dx%d'%(n,w,h),font=f,fill=(255,255,255))
    tiles.append(t)
cols=2; rows=(len(tiles)+1)//2; H=max(t.size[1] for t in tiles)
P=Image.new('RGB',(cols*W+10,rows*(H+10)),(40,40,40))
for i,t in enumerate(tiles): P.paste(t,((i%2)*(W+10),(i//2)*(H+10)))
P.save(L+'grid/'+out,quality=85)
