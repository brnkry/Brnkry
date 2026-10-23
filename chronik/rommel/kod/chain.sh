# wait for the 16:9 parts, mux them; then render the 9:16 version in 4 parts and mux it
cd $(dirname $0)/..
while pgrep -f "code/full[.]py v2/p" >/dev/null; do sleep 20; done
printf "file 'v2/p1.mp4'\nfile 'v2/p2.mp4'\nfile 'v2/p3.mp4'\nfile 'v2/p4.mp4'\n" > v2/list.txt
ffmpeg -v error -y -f concat -i v2/list.txt -i mix_v2.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart Erwin_Rommel_Doku_16x9_v2.mp4
ffmpeg -v error -y -i Erwin_Rommel_Doku_16x9_v2.mp4 -c:v libx264 -b:v 5.2M -maxrate 7M -bufsize 12M -preset fast -pix_fmt yuv420p -c:a copy -movflags +faststart Erwin_Rommel_Doku_16x9_v2_web.mp4 &
mkdir -p v9
python3 code/full9.py v9/p1.mp4 0 138 > v9/r1.log 2>&1 &
python3 code/full9.py v9/p2.mp4 138 276 > v9/r2.log 2>&1 &
python3 code/full9.py v9/p3.mp4 276 414 > v9/r3.log 2>&1 &
python3 code/full9.py v9/p4.mp4 414 551.46 > v9/r4.log 2>&1 &
wait
printf "file 'v9/p1.mp4'\nfile 'v9/p2.mp4'\nfile 'v9/p3.mp4'\nfile 'v9/p4.mp4'\n" > v9/list.txt
ffmpeg -v error -y -f concat -i v9/list.txt -i mix_9x16.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart Erwin_Rommel_Doku_9x16.mp4
ffmpeg -v error -y -i Erwin_Rommel_Doku_9x16.mp4 -c:v libx264 -b:v 5.2M -maxrate 7M -bufsize 12M -preset fast -pix_fmt yuv420p -c:a copy -movflags +faststart Erwin_Rommel_Doku_9x16_web.mp4
ls -la Erwin_Rommel_Doku_*; tail -n1 v2/r?.log v9/r?.log
