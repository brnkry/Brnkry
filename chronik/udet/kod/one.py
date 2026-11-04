# full-size single frames: one.py out.jpg t [crop x0 y0 x1 y1]
import sys; sys.argv = [sys.argv[0], 'list'] + sys.argv[1:]; out, t = sys.argv[2], float(sys.argv[3]); box = [int(v) for v in sys.argv[4:8]] if len(sys.argv) > 4 else None
sys.argv = sys.argv[:1] + ['x']
exec(open(__file__.replace('one.py', 'jshort.py')).read().split("if __name__ == '__main__':")[0])
im = frame(t); im = im.crop(box) if box else im; im.save(B + out, quality=90)
