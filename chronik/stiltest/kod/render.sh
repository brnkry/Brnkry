cd $(dirname $0)
T=$(python3 -c "import sys; sys.path.insert(0,'code'); sys.argv=['x','x']; import test30 as V; print(V.TEND)")
P=$(python3 -c "print(' '.join('%.4f'%(i*$T/4) for i in range(5)))"); set -- $P
for i in 0 1 2 3; do :; done
OMP_NUM_THREADS=1 python3 code/test30.py p0.mp4 $1 $2 > r0.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/test30.py p1.mp4 $2 $3 > r1.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/test30.py p2.mp4 $3 $4 > r2.log 2>&1 &
OMP_NUM_THREADS=1 python3 code/test30.py p3.mp4 $4 $5 > r3.log 2>&1 &
wait; printf "file 'p0.mp4'\nfile 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\n" > parts.txt; echo DONE $T
