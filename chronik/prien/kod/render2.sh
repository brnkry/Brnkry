cd $(dirname $0)
T=$(python3 -c "import sys; sys.path.insert(0,'code'); import pr; print(pr.TEND)")
P=$(python3 -c "print(' '.join('%.4f'%(i*$T/8) for i in range(9)))"); set -- $P
for i in 0 1 2 3 4 5 6 7; do eval a=\${$((i+1))}; eval b=\${$((i+2))}; OMP_NUM_THREADS=1 python3 code/ps.py v$i.mp4 $a $b > s$i.log 2>&1 & done
wait; for i in 0 1 2 3 4 5 6 7; do echo "file 'v$i.mp4'"; done > parts2.txt; echo DONE $T
