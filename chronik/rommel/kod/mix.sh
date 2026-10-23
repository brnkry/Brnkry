# usage: mix.sh <T> <out.wav> <sfx.wav>  (voice vcut.wav ends at 549.86, bed.wav must be at least T long)
T=$1; OUT=$2; SFX=$3; TV=549.86
F=$(python3 -c "print(round($T-1.6,2))"); VF=$(python3 -c "print(round($TV-0.12,2))")
ffmpeg -v error -y -i vcut.wav -i bed.wav -i $SFX -filter_complex "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,atrim=0:$TV,afade=t=out:st=$VF:d=0.12,apad=whole_dur=$T,asplit=2[v][vsc];[1:a]aresample=48000,atrim=0:$T,volume=0.40,afade=t=in:d=0.6,afade=t=out:st=$F:d=1.6[m0];[m0][vsc]sidechaincompress=threshold=0.05:ratio=2.5:attack=40:release=400[m];[2:a]aresample=48000,atrim=0:$T,volume=0.95[s];[v][m][s]amix=inputs=3:normalize=0:duration=first,atrim=0:$T,alimiter=limit=0.93[a]" -map "[a]" -c:a pcm_s16le $OUT
