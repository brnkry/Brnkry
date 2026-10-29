cd $(dirname $0)
T=$(python3 -c "import json;w=json.load(open('words.json'));print(w[-1][2]+0.15)")
P=$(python3 -c "print(' '.join('%.4f'%(i*$T/4) for i in range(5)))"); set -- $P
OMP_NUM_THREADS=1 python3 code/tshort.py part0.mp4 $1 $2 > r0.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/tshort.py part1.mp4 $2 $3 > r1.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/tshort.py part2.mp4 $3 $4 > r2.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/tshort.py part3.mp4 $4 $5 > r3.log 2>&1 &
wait; cat r?.log
