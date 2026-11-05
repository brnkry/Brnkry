cd $(dirname $0)
T=$(python3 -c "import sys; sys.path.insert(0,'code'); import wk as pr; print(pr.TEND)")
ffmpeg -v error -y -i vcut.wav -i bed.wav -i sfx.wav -filter_complex \
"[0:a]loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000,aformat=channel_layouts=stereo,apad,asplit=3[v][k1][k2];\
[1:a]aresample=48000,atrim=0:$T,volume=0.8,afade=t=out:st=$(python3 -c "print($T-0.3)"):d=0.3[b];[b][k1]sidechaincompress=threshold=0.08:ratio=1.8:attack=20:release=400[bd];\
[2:a]aresample=48000[x];[x][k2]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=300[xd];\
[v][bd][xd]amix=inputs=3:normalize=0:duration=shortest,atrim=0:$T,alimiter=limit=0.93[o]" -map "[o]" -ar 48000 mix.wav
ffmpeg -v error -y -f concat -safe 0 -i parts2.txt -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart Wick_Shorts_DE_v1.mp4
echo MIXED
