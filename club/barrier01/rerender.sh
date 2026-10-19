#!/bin/bash
# usage: ./rerender.sh scene.html DUR  -> events json + all frames (4 workers)
set -e
S=$1; D=$2; T=$(basename $S .html); NF=$(python3 -c "import math;print(math.ceil($D*30))")
node render.js $S events
rm -rf frames_$T
W=${W:-4}; Q=$(( (NF+W-1)/W ))
for i in $(seq 0 $((W-1))); do A=$((i*Q)); B=$(( (i+1)*Q )); [ $B -gt $NF ] && B=$NF; node render.js $S full $D $A $B & done; wait
echo "$T frames: $(ls frames_$T | wc -l)/$NF"
