#!/bin/bash
# usage: ./rerender.sh scene.html DUR  -> events json + all frames (4 workers)
set -e
S=$1; D=$2; T=$(basename $S .html); NF=$(python3 -c "import math;print(math.ceil($D*30))")
node render.js $S events
rm -rf frames_$T
Q=$(( (NF+3)/4 ))
for i in 0 1 2 3; do A=$((i*Q)); B=$(( (i+1)*Q )); [ $B -gt $NF ] && B=$NF; node render.js $S full $D $A $B & done; wait
echo "$T frames: $(ls frames_$T | wc -l)/$NF"
