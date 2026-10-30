# music bed of any length: Steel_and_Salt without its fading tail (after 146 s), looped back to 24 s with a 4 s crossfade, levelled
# usage: bed.sh <seconds> <out.wav>
L=$1; OUT=$2; D=$(dirname $0)/..
ffmpeg -v error -y -i $D/music.mp3 -filter_complex "[0:a]atrim=0:146,asetpts=N/SR/TB[a];[0:a]atrim=24:146,asetpts=N/SR/TB[b];[0:a]atrim=24:146,asetpts=N/SR/TB[c];[a][b]acrossfade=d=4:c1=tri:c2=tri[ab];[ab][c]acrossfade=d=4:c1=tri:c2=tri,dynaudnorm=f=750:g=31:p=0.9,atrim=0:$L,aresample=48000[o]" -map "[o]" -ac 2 $OUT
