cd $(dirname $0)
T=$(python3 -c "import sys; sys.path.insert(0,'code'); sys.argv=['x','x']; import styleA as V; print(V.TEND)")
P=$(python3 -c "print(' '.join('%.4f'%(i*$T/4) for i in range(5)))"); set -- $P
OMP_NUM_THREADS=1 python3 code/styleA.py a0.mp4 $1 $2 > r0.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/styleA.py a1.mp4 $2 $3 > r1.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/styleA.py a2.mp4 $3 $4 > r2.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/styleA.py a3.mp4 $4 $5 > r3.log 2>&1 &
wait; printf "file 'a0.mp4'\nfile 'a1.mp4'\nfile 'a2.mp4'\nfile 'a3.mp4'\n" > partsA.txt; echo DONE $T
