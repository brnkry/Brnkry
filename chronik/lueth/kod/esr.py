# Real-ESRGAN general x4v3 (ONNX, fixed 128x128 tiles) on one image: overlapping tiles, feathered blend
import sys, time, glob, numpy as np, onnxruntime as ort
from PIL import Image
M = glob.glob('/tmp/claude-0/-home-user-Brnkry/20fcd4ae-a45e-586b-9e5a-d5e860e017bc/scratchpad/models/rg/**/*.onnx', recursive=True)[0]
so = ort.SessionOptions(); so.intra_op_num_threads = 4
S = ort.InferenceSession(M, so)
def up(img):
    a = np.asarray(img.convert('RGB'), np.float32) / 255; H, W = a.shape[:2]; T, O = 128, 16; st = T - 2 * O
    ph, pw = max(H, T), max(W, T); a = np.pad(a, ((O, ph - H + T), (O, pw - W + T), (0, 0)), mode='reflect')
    out = np.zeros(((ph + T) * 4, (pw + T) * 4, 3), np.float32); wsum = np.zeros(out.shape[:2] + (1,), np.float32)
    win = np.ones((T * 4, T * 4, 1), np.float32); r = np.minimum(np.arange(T * 4) + 1, np.arange(T * 4)[::-1] + 1); r = np.minimum(r, O * 4) / (O * 4)
    win = (r[:, None] * r[None, :])[..., None]
    tiles = [(y, x) for y in range(0, H, st) for x in range(0, W, st)]
    for i in range(0, len(tiles), 8):
        batch = tiles[i:i + 8]
        for (y, x) in batch:
            t = a[y:y + T, x:x + T].transpose(2, 0, 1)[None]
            o = S.run(None, {'image': t})[0][0].transpose(1, 2, 0)
            out[y * 4:(y + T) * 4, x * 4:(x + T) * 4] += o * win; wsum[y * 4:(y + T) * 4, x * 4:(x + T) * 4] += win
    out = out / np.maximum(wsum, 1e-6); out = out[O * 4:(O + H) * 4, O * 4:(O + W) * 4]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
if __name__ == '__main__':
    t = time.time(); im = Image.open(sys.argv[1]); r = up(im); r.save(sys.argv[2]); print('sec', round(time.time() - t, 2), im.size, '->', r.size)
