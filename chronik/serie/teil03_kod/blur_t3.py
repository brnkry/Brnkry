import json
from PIL import Image, ImageDraw, ImageFilter
B='/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t3l/'
L={
 'manstein':[(178,1135,40,34)],
 'guderian_enigma':[(482,207,9,9),(420,94,10,7)],
 'comp_hitler':[(497,208,7,6),(428,228,6,5),(427,323,7,7),(552,392,11,10)],
 'bluecher_col':[(28,460,13,10)],
 'rommel_maps':[(162,344,10,8),(683,323,10,8)],
 'lux_border':[(415,507,8,7)],
 'comp_wagon':[(493,668,8,7)],
 'paris_parade':[(568,401,7,6)],
 'floing':[(512,297,6,5)],
}
json.dump(L,open(B+'blur_t3.json','w'),indent=1)
for n,es in L.items():
    im=Image.open(B+'img_orig/'+n+'.jpg').convert('RGB')
    for cx,cy,rx,ry in es:
        r=max(rx,ry)
        bl=im.filter(ImageFilter.GaussianBlur(max(3,r*0.6)))
        m=Image.new('L',im.size,0); d=ImageDraw.Draw(m)
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255)
        m=m.filter(ImageFilter.GaussianBlur(2))
        im=Image.composite(bl,im,m)
    im.save(B+'img/'+n+'.jpg',quality=95)
print('ok')
