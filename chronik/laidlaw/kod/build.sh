set -e
rm -f p_*.mp4
for r in "0 27.3" "27.3 54.6" "54.6 81.9" "81.9 109.2"; do set -- $r; python3 code/laid.py render p_$1.mp4 $1 $2 > log_$1.txt 2>&1 & done; wait
printf "file 'p_0.mp4'\nfile 'p_27.3.mp4'\nfile 'p_54.6.mp4'\nfile 'p_81.9.mp4'\n" > list.txt
ffmpeg -v error -y -i v.wav -ss 2.0 -i ../ars/Documentary_Show.mp3 -i sfx.wav -filter_complex "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur=109.2,asplit=2[v][vsc];[1:a]aresample=48000,atrim=0:109.2,volume='0.44*(1+1.0*max(0,(3.2-t)/3.2))':eval=frame,afade=t=out:st=107.0:d=2.2[m0];[m0][vsc]sidechaincompress=threshold=0.06:ratio=2:attack=60:release=450[m];[2:a]volume=0.85[s];[v][m][s]amix=inputs=3:normalize=0:duration=longest,atrim=0:109.2,alimiter=limit=0.93[a]" -map "[a]" -c:a pcm_s16le mix.wav
ffmpeg -v error -y -f concat -i list.txt -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset medium -b:v 16M -maxrate 22M -bufsize 32M -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart Jean_Laidlaw_Shorts.mp4
echo DONE
