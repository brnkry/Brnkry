#!/bin/bash
# 12 fps stop-motion frames -> 24 fps 1080x1920 mp4 with warm grade, vignette, film grain and loudness-normalized audio.
# usage: ./encode.sh frames mix.wav out.mp4
F=${1:-frames}; A=${2:-mix.wav}; O=${3:-exports/first_day_as_a_hitman.mp4}
mkdir -p "$(dirname "$O")"
ffmpeg -v error -y -framerate 12 -i "$F/f%05d.jpg" -i "$A" \
  -filter_complex "[0:v]fps=24,tpad=stop_mode=clone:stop_duration=0.5,eq=saturation=1.08:contrast=1.04,colorbalance=rs=.03:gs=.01:bs=-.03,vignette=PI/5,noise=alls=3:allf=t,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 23 -maxrate 14M -bufsize 28M -profile:v high -c:a aac -b:a 192k -shortest -movflags +faststart "$O"
echo "$O"
