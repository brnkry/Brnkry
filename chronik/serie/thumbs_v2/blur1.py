from PIL import Image, ImageDraw, ImageFilter
im=Image.open('t1_fist.jpg').convert('RGB'); cx,cy,r=426,438,11
bl=im.filter(ImageFilter.GaussianBlur(6)); m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse((cx-r,cy-r,cx+r,cy+r),fill=255)
Image.composite(bl,im,m.filter(ImageFilter.GaussianBlur(2))).save('t1_fist_b.jpg',quality=95)
