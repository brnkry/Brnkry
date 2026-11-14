from PIL import Image, ImageDraw, ImageFilter
B='/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/bolt/'
L={'p03':[(942,2413,48),(273,1751,60),(1396,1679,58)],'p04':[(927,1856,34),(312,1383,45),(1043,1354,34),(850,128,48)],'p02':[(879,2093,40)]}
for n,ps in L.items():
    im=Image.open(B+'img_orig/%s.jpg'%n).convert('RGB')
    for x,y,r in ps:
        m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse((x-r,y-r,x+r,y+r),fill=255)
        im=Image.composite(im.filter(ImageFilter.GaussianBlur(max(6,r*0.45))),im,m.filter(ImageFilter.GaussianBlur(4)))
    im.save(B+'img/%s.jpg'%n,quality=95)
