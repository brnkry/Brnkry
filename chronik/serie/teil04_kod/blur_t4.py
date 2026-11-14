# small, exact blurs of swastikas / eagles / Knight's Cross centres; positions as fractions of width/height, radius as fraction of width
import json
from PIL import Image, ImageDraw, ImageFilter
L='/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t4l/'
B={
 'reichstag':[(0.505,0.235,0.09),(0.505,0.115,0.03)],
 'goering_kess':[(0.188,0.12,0.02),(0.474,0.18,0.022),(0.565,0.17,0.02),(0.48,0.33,0.02),(0.30,0.27,0.018)],
 'kesselring':[(0.546,0.118,0.05),(0.292,0.918,0.05),(0.52,0.668,0.036)],
 'he111_form':[(0.234,0.145,0.028),(0.654,0.335,0.028),(0.476,0.388,0.024)],
 'do17_form':[(0.401,0.626,0.025),(0.737,0.529,0.018),(0.816,0.36,0.014)],
 'ju88_crew':[(0.013,0.47,0.03)],
 'ju87':[(0.092,0.44,0.03)],
 'bf109_beach':[(0.24,0.495,0.025)],
 'bf109_beach_a':[(0.31,0.83,0.012)],
 'galland':[(0.49,0.777,0.035),(0.072,0.87,0.06),(0.84,0.955,0.03)],
 'moelders':[(0.351,0.114,0.06),(0.533,0.767,0.04)],
 'do17_spit':[(0.263,0.185,0.035),(0.145,0.17,0.035)],
 'goering_galland':[(0.188,0.2,0.02),(0.39,0.229,0.02),(0.566,0.21,0.02),(0.68,0.27,0.016),(0.2,0.31,0.018),(0.556,0.33,0.018),(0.59,0.39,0.018)],
 'he111_channel':[(0.202,0.382,0.012),(0.397,0.333,0.012),(0.538,0.265,0.012),(0.701,0.223,0.012),(0.889,0.238,0.012),(0.621,0.32,0.012),(0.303,0.417,0.012),(0.99,0.112,0.014),(0.09,0.41,0.012)],
 'k7_he111_formation':[(0.759,0.398,0.05),(0.506,0.575,0.04),(0.332,0.67,0.035),(0.18,0.76,0.03),(0.188,0.847,0.03)],
 'he111_cockpit':[(0.17,0.477,0.03)],
 'seel_tank':[(0.4,0.52,0.015)],
}
json.dump(B,open(L+'blur_t4.json','w'))
for n,pts in B.items():
    im=Image.open(L+'img_orig/'+n+'.jpg').convert('RGB'); w,h=im.size
    for fx,fy,fr in pts:
        r=max(8,int(fr*w)); x,y=int(fx*w),int(fy*h); box=(max(0,x-2*r),max(0,y-2*r),min(w,x+2*r),min(h,y+2*r))
        reg=im.crop(box); bl=reg.filter(ImageFilter.GaussianBlur(r*0.45))
        m=Image.new('L',reg.size,0); ImageDraw.Draw(m).ellipse((x-r-box[0],y-r-box[1],x+r-box[0],y+r-box[1]),fill=255); m=m.filter(ImageFilter.GaussianBlur(r*0.2))
        reg.paste(bl,(0,0),m); im.paste(reg,box[:2])
    im.save(L+'img/'+n+'.jpg',quality=94)
print('ok')
