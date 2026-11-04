set -e
cd code
read T TV < <(python3 full9.py T)
P=$(python3 -c "print(round($T/4,2))")
rm -f ../v_*.mp4
for i in 0 1 2 3; do a=$(python3 -c "print(round($i*$P,2))"); b=$(python3 -c "print(round(($i+1)*$P,2) if $i<3 else $T)"); python3 full9.py v_$i.mp4 $a $b > ../log9_$i.txt 2>&1 & done; wait
cd ..
printf "file 'v_0.mp4'\nfile 'v_1.mp4'\nfile 'v_2.mp4'\nfile 'v_3.mp4'\n" > vlist.txt
F=$(python3 -c "print(round($T-1.6,2))"); VF=$(python3 -c "print(round($TV-0.12,2))")
ffmpeg -v error -y -i vcut.wav -i bed_full.wav -i sfx_full.wav -filter_complex "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,atrim=0:$TV,afade=t=out:st=$VF:d=0.12,apad=whole_dur=$T,asplit=2[v][vsc];[1:a]aresample=48000,atrim=0:$T,volume=0.30,afade=t=out:st=$F:d=1.6[m0];[m0][vsc]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=400[m];[2:a]aresample=48000,atrim=0:$TV,apad=whole_dur=$T,volume=0.95[s];[v][m][s]amix=inputs=3:normalize=0:duration=first,atrim=0:$T,alimiter=limit=0.93[a]" -map "[a]" -c:a pcm_s16le mix9.wav
ffmpeg -v error -y -f concat -i vlist.txt -i mix9.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart Lauri_Toerni_Doku_9x16.mp4
echo DONE
