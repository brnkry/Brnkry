#!/bin/bash
# usage: ./prev.sh t1 t2 ... -> composites overlay on base at those times into prev/c_t.png
cd "$(dirname "$0")"; O=/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/lol2/out2
node render.js preview "$@" >/dev/null
for t in "$@"; do ffmpeg -v error -y -ss $t -i $O/base.mp4 -i prev/$t.png -filter_complex "[0][1]overlay,scale=540:960" -frames:v 1 prev/c_$t.png; done
