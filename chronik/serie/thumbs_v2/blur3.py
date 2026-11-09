from PIL import Image, ImageDraw, ImageFilter
P=[(140, 383), (310, 383), (470, 371), (563, 363), (782, 383), (1000, 399), (1147, 410), (1203, 415), (233, 410), (363, 396), (693, 406), (893, 431), (1067, 448), (93, 399)]
im=Image.open('T3_foto.jpg').convert('RGB'); bl=im.filter(ImageFilter.GaussianBlur(5)); m=Image.new('L',im.size,0); d=ImageDraw.Draw(m)
for x,y in P: d.ellipse((x-12,y-13,x+12,y+13),fill=255)
Image.composite(bl,im,m.filter(ImageFilter.GaussianBlur(2))).save('T3_foto.jpg',quality=93)
