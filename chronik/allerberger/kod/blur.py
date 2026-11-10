from PIL import Image, ImageDraw, ImageFilter
B='/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/allb2/'
L={'a07':[(410,2070,38),(982,112,34)],'a10':[(980,1180,20),(1052,1235,34),(930,1290,36)],'a03':[(800,140,24)]}
for n,ps in L.items():
    im=Image.open(B+'img_orig/%s.jpg'%n).convert('RGB')
    for x,y,r in ps:
        m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse((x-r,y-r,x+r,y+r),fill=255)
        im=Image.composite(im.filter(ImageFilter.GaussianBlur(max(5,r*0.4))),im,m.filter(ImageFilter.GaussianBlur(3)))
    im.save(B+'img/%s.jpg'%n,quality=95)
print('ok')
