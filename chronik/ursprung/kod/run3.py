# shots and crossfaded cut only (the finish, subtitles, labels and sound come once for the whole film)
import sys
from engine import Part, build_shots, xfade, U
from shots import P
import shutil, os
k = sys.argv[1]; SH, LAB = P[k]; part = Part(U + k)
clips = build_shots(part, SH, part.d + 'shots/'); xfade(clips, part.d + 'cut.mp4', part.end)
shutil.rmtree(part.d + 'shots'); print('CUT DONE', flush=True)
