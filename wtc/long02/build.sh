#!/bin/bash
# Assemble the long video: all part frame folders joined with 0.35 s crossfades + master.wav.
# parts.json: [[events_json, voice_mp3, duration], ...] ; frame folders listed in FRAMES below, same order.
set -e
python3 master_audio.py
FR=($(python3 -c "import json;print(' '.join('frames_'+p[0][7:-5] for p in json.load(open('parts.json'))))"))
IN=""; for f in "${FR[@]}"; do IN="$IN -framerate 30 -i $f/f_%05d.jpg"; done
FC=$(python3 - <<'PY'
import json
o=json.load(open('offsets.json'));offs=o['offsets'];xf=o['xf']
n=len(offs);s='';prev='[0:v]'
for i in range(1,n):
    out=f'[x{i}]' if i<n-1 else '[v]'
    s+=f'{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={offs[i]}{out};';prev=out
if n==1: s='[0:v]null[v];'
print(s+'[v]format=yuv420p[vo]')
PY
)
NA=${#FR[@]}
J=$(ffmpeg -hide_banner -i master.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
II=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y $IN -i master.wav -filter_complex "$FC" -map "[vo]" -map $NA:a -af "loudnorm=I=-14:TP=-1.5:LRA=11:$II:linear=true" -c:v libx264 -crf 17 -preset slow -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "${1:-full.mp4}"
ffprobe -v error -show_entries format=duration -of csv=p=0 "${1:-full.mp4}"
