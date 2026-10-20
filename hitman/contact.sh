#!/bin/bash
# contact sheet of rendered frames: contact.sh frames_dir every_n out.jpg [cols]
D=$1; N=$2; O=$3; C=${4:-12}
ls "$D"/f*.jpg | awk "NR%$N==1" > /tmp/claude-0/-home-user-Brnkry/288ba9c1-d9fa-5186-8853-518542915667/scratchpad/list.txt
R=$(( ($(wc -l < /tmp/claude-0/-home-user-Brnkry/288ba9c1-d9fa-5186-8853-518542915667/scratchpad/list.txt) + C - 1) / C ))
sed 's/^/file /' /tmp/claude-0/-home-user-Brnkry/288ba9c1-d9fa-5186-8853-518542915667/scratchpad/list.txt | sed "s|file |file $PWD/|" > /tmp/claude-0/-home-user-Brnkry/288ba9c1-d9fa-5186-8853-518542915667/scratchpad/cat.txt
ffmpeg -v error -y -f concat -safe 0 -i /tmp/claude-0/-home-user-Brnkry/288ba9c1-d9fa-5186-8853-518542915667/scratchpad/cat.txt -vf "scale=160:-1,tile=${C}x${R}" -frames:v 1 "$O"
