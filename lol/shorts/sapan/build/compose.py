"""Final composite for the Sapan Short: hook zoom (champion kept fixed) + keyed q-ping + BOZGUN green screens + overlay frames + mix.
usage: python3 compose.py BASE.mp4 OVERLAY_DIR OUT.mp4"""
import sys, subprocess
BASE, OVF, OUT = sys.argv[1:4]
QP = '/tmp/claude-0/-home-user-Brnkry/65f4241b-0184-50ef-a7c2-5a98c9618836/scratchpad/vl/qping.mp4'
BZ = '../../gizli_minyon/src/bozgun_greenscreen.mp4'
P = [(0, 600, 1500), (2.5, 583, 1425), (3.5, 518, 1253), (5.0, 648, 1080), (6.2, 518, 994), (7.4, 505, 980)]
Z = [(3.35, 1.12), (4.05, 1.25), (4.80, 1.40)]
HOOK = 7.40
def lin(i):  # piecewise linear in t for champion coordinate i
    e = str(P[-1][i])
    for (t0, *a), (t1, *b) in reversed(list(zip(P, P[1:]))):
        e = f"if(lt(t,{t1}),{a[i-1]}+({b[i-1]}-{a[i-1]})*(t-{t0})/{t1 - t0},{e})"
    return e
def zoom():
    parts, prev = [], 1
    for t, z in Z: parts.append((t, prev, z)); prev = z
    e = '1'
    for t, a, b in parts: e = f"if(gte(t,{t}),{a}+({b}-{a})*min(1,(t-{t})/0.12),{e})"
    return e
cx, cy, z = lin(1), lin(2), zoom()
# zoom via scale up + crop with per-frame expressions
import re
cx, cy, z = (re.sub(r'\bt\b', 'it', x) for x in (cx, cy, z))
zf = (f"[0]trim=0:{HOOK},setpts=PTS-STARTPTS,zoompan=z='{z}':x='({cx})*(1-1/zoom)':y='({cy})*(1-1/zoom)':d=1:s=1080x1920:fps=30,setsar=1[h]")
# step 1: hook zoom baked into an intermediate base (keeps timestamps clean for the overlays)
ZB = OUT.replace('.mp4', '_zbase.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', BASE, '-filter_complex', zf + f";[0]trim={HOOK},setpts=PTS-STARTPTS[r];[h][r]concat=n=2:v=1:a=0,fps=30,format=yuv420p[b]",
                '-map', '[b]', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', ZB], check=True)
BASE = ZB
fc = ['[0]null[b]',
      "[2]colorkey=0x0FFF00:0.3:0.1,scale=1080:-1,fps=30,format=rgba,setpts=PTS-STARTPTS,tpad=start_duration=7.05:color=black@0[q]",
      "[b][q]overlay=x=0:y=660:eof_action=pass[b2]",
      "[3]fps=30,chromakey=0x007E02:0.15:0.08,despill=green,scale=2400:-1,crop=1080:1350:660:0,format=rgba,setpts=PTS-STARTPTS,tpad=start_duration=70.06:color=black@0[z]",
      "[b2][1]overlay=0:0[b3]", "[b3][z]overlay=0:250:eof_action=pass[v]"]
cmd = ['ffmpeg', '-v', 'error', '-y', '-i', BASE, '-framerate', '30', '-i', f'{OVF}/%05d.png', '-i', QP, '-ss', '4.9', '-t', '1.6', '-i', BZ, '-i', '../ses/mix.wav',
       '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '4:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '192k', '-t', '73.38', '-movflags', '+faststart', OUT]
subprocess.run(cmd, check=True)
import os; os.remove(ZB)
