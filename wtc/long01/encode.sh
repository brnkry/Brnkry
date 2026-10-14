#!/bin/bash
# usage: ./encode.sh <frames_dir> <mix.wav> <out.mp4>   (two-pass loudnorm to -14 LUFS, TP -1.5)
set -e
J=$(ffmpeg -hide_banner -i "$2" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
II=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -framerate 30 -i "$1/f_%05d.jpg" -i "$2" -af "loudnorm=I=-14:TP=-1.5:LRA=11:$II:linear=true" -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$3"
