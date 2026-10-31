import numpy as np, cv2
def load(p): return cv2.imread(p)
def ecc(A, B, mode=cv2.MOTION_AFFINE, scale=0.25):
    """B'yi A'ya hizalayan 2x3 matris (tam çözünürlük)."""
    a = cv2.cvtColor(cv2.resize(A, None, fx=scale, fy=scale), cv2.COLOR_BGR2GRAY).astype(np.float32)
    b = cv2.cvtColor(cv2.resize(B, None, fx=scale, fy=scale), cv2.COLOR_BGR2GRAY).astype(np.float32)
    M = np.eye(2, 3, dtype=np.float32)
    try:
        _, M = cv2.findTransformECC(a, b, M, mode, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
    except cv2.error:
        pass
    M[:, 2] /= scale
    return M
def warp_to(A, B, M):
    return cv2.warpAffine(B, M, (A.shape[1], A.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
def diffbox(A, Bw, thr=40):
    d = cv2.GaussianBlur(np.abs(A.astype(int) - Bw.astype(int)).sum(2).astype(np.float32), (0, 0), 6)
    ys, xs = np.where(d > thr)
    return (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None, d
