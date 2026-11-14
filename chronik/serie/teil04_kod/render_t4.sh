cd /tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/t4l/code
T=588.27; N=8
for i in $(seq 0 7); do a=$(python3 -c "print(round($T*$i/$N/ (1/30))*(1/30))"); b=$(python3 -c "print(round($T*($i+1)/$N/(1/30))*(1/30))"); nohup python3 teil4.py $a $b ../out/part$i.mp4 > ../out/log$i.txt 2>&1 & done
wait; echo ALLDONE > ../out/done.txt
