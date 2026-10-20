// Shared helpers: clay materials, lumpy geometry, noise, easing, keyframes, text textures.
import * as THREE from 'three';

// ---------- deterministic random + noise ----------
export function rng(seed) { let s = seed >>> 0 || 1; return () => ((s = Math.imul(s ^ (s >>> 15), 1 | s) + 0x6D2B79F5 | 0, s ^= s + Math.imul(s ^ (s >>> 7), 61 | s), ((s ^ (s >>> 14)) >>> 0) / 4294967296)); }
function hash3(x, y, z, seed) { let h = (x * 374761393 + y * 668265263 + z * 2147483647 + seed * 144665) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
const sm = t => t * t * (3 - 2 * t);
export function noise3(x, y, z, seed = 0) {
  const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = sm(x - xi), yf = sm(y - yi), zf = sm(z - zi);
  const L = (a, b, t) => a + (b - a) * t; const h = (i, j, k) => hash3(xi + i, yi + j, zi + k, seed);
  return L(L(L(h(0,0,0), h(1,0,0), xf), L(h(0,1,0), h(1,1,0), xf), yf), L(L(h(0,0,1), h(1,0,1), xf), L(h(0,1,1), h(1,1,1), xf), yf), zf) * 2 - 1;
}
export function fbm(x, y, z, seed = 0) { return noise3(x, y, z, seed) * .6 + noise3(x * 2.1, y * 2.1, z * 2.1, seed + 7) * .3 + noise3(x * 4.3, y * 4.3, z * 4.3, seed + 13) * .1; }

// displace vertices along normals: hand-made, slightly uneven clay
export function lumpy(geo, amp = .01, freq = 6, seed = 1) {
  geo.computeVertexNormals();
  const p = geo.attributes.position, n = geo.attributes.normal, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i); const d = fbm(v.x * freq, v.y * freq, v.z * freq, seed) * amp;
    p.setXYZ(i, v.x + n.getX(i) * d, v.y + n.getY(i) * d, v.z + n.getZ(i) * d);
  }
  geo.computeVertexNormals(); return geo;
}
export function sphereG(r = 1, ws = 40, hs = 28) { const g = new THREE.SphereGeometry(r, ws, hs); g.rotateY(-Math.PI / 2); return g; }
export function capsuleG(r, len, seg = 24) { return new THREE.CapsuleGeometry(r, len, 8, seg); }

// ---------- clay textures ----------
function canvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
let _bump, _tint, _streak;
export function clayBump() {
  if (_bump) return _bump;
  const c = canvas(1024, 1024), g = c.getContext('2d'), R = rng(7);
  g.fillStyle = '#808080'; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 900; i++) { // thumb smudges
    const x = R() * 1024, y = R() * 1024, r = 6 + R() * 40, l = R() < .5;
    const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, l ? 'rgba(255,255,255,.10)' : 'rgba(0,0,0,.10)'); gr.addColorStop(1, 'rgba(128,128,128,0)');
    g.fillStyle = gr; g.beginPath(); g.ellipse(x, y, r, r * (.4 + R() * .6), R() * 6, 0, 7); g.fill();
  }
  for (let i = 0; i < 26; i++) { // fingerprints
    const x = R() * 1024, y = R() * 1024, a = R() * 6; g.save(); g.translate(x, y); g.rotate(a);
    for (let k = 2; k < 16; k++) { g.strokeStyle = `rgba(${R() < .5 ? 0 : 255},${R() < .5 ? 0 : 255},${R() < .5 ? 0 : 255},.07)`; g.strokeStyle = k % 2 ? 'rgba(0,0,0,.09)' : 'rgba(255,255,255,.06)'; g.lineWidth = 1.4; g.beginPath(); g.ellipse(0, 0, k * 2.6, k * 1.9, 0, 0.3, Math.PI * 1.7); g.stroke(); }
    g.restore();
  }
  for (let i = 0; i < 260; i++) { // tool scratches
    const x = R() * 1024, y = R() * 1024, a = R() * 6, l = 5 + R() * 22;
    g.strokeStyle = R() < .5 ? 'rgba(0,0,0,.18)' : 'rgba(255,255,255,.12)'; g.lineWidth = .8 + R() * 1.5;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
  }
  const id = g.getImageData(0, 0, 1024, 1024), d = id.data; // grain
  for (let i = 0; i < d.length; i += 4) { const n = (R() - .5) * 14; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  g.putImageData(id, 0, 0);
  _bump = new THREE.CanvasTexture(c); _bump.wrapS = _bump.wrapT = THREE.RepeatWrapping; return _bump;
}
export function clayTint() {
  if (_tint) return _tint;
  const c = canvas(512, 512), g = c.getContext('2d'), R = rng(3);
  g.fillStyle = '#f2f2f2'; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 400; i++) { const x = R() * 512, y = R() * 512, r = 10 + R() * 50; const gr = g.createRadialGradient(x, y, 0, x, y, r); const v = R() < .5 ? 255 : 200; gr.addColorStop(0, `rgba(${v},${v},${v},.25)`); gr.addColorStop(1, 'rgba(242,242,242,0)'); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  _tint = new THREE.CanvasTexture(c); _tint.colorSpace = THREE.SRGBColorSpace; _tint.wrapS = _tint.wrapT = THREE.RepeatWrapping; return _tint;
}
// directional streaks (hair, suit cloth carved with a tool)
export function streakBump() {
  if (_streak) return _streak;
  const c = canvas(512, 512), g = c.getContext('2d'), R = rng(11);
  g.fillStyle = '#808080'; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 700; i++) { const x = R() * 512, y = R() * 512, l = 20 + R() * 60; g.strokeStyle = R() < .5 ? 'rgba(0,0,0,.35)' : 'rgba(255,255,255,.25)'; g.lineWidth = 1 + R() * 2.5; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + (R() - .5) * 10, y + l / 2, x + (R() - .5) * 8, y + l); g.stroke(); }
  _streak = new THREE.CanvasTexture(c); _streak.wrapS = _streak.wrapT = THREE.RepeatWrapping; return _streak;
}

const matCache = {};
export function clay(color, o = {}) {
  const key = color + JSON.stringify(o); if (matCache[key] && !o.unique) return matCache[key];
  const bump = (o.streak ? streakBump() : clayBump()).clone(); bump.needsUpdate = true;
  const rep = (o.rep ?? 2) * 2; bump.repeat.set(rep, rep);
  const tint = clayTint().clone(); tint.needsUpdate = true; tint.repeat.set(rep * .5, rep * .5);
  const m = new THREE.MeshStandardMaterial({ color, roughness: o.rough ?? .78, metalness: o.metal ?? 0, bumpMap: bump, bumpScale: (o.bump ?? 1.4) * 3, map: o.map ?? (o.noTint ? null : tint), transparent: !!o.opacity, opacity: o.opacity ?? 1, emissive: o.emissive ?? 0x000000, emissiveIntensity: o.ei ?? 1 });
  if (!o.unique) matCache[key] = m; return m;
}
export function mesh(geo, mat, cast = true) { const m = new THREE.Mesh(geo, mat); m.castShadow = cast; m.receiveShadow = true; return m; }

// ---------- text / painted textures ----------
export function paintTex(w, h, draw) {
  const c = canvas(w, h), g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData.canvas = c; return t;
}
// hand-wobbly text: each letter slightly rotated / offset, like painted by hand
export function wobblyText(g, text, x, y, size, font, color, seed = 1, spacing = 0) {
  const R = rng(seed); g.font = `${size}px ${font}`; g.fillStyle = color; g.textBaseline = 'middle';
  const w = [...text].reduce((s, ch) => s + g.measureText(ch).width + spacing, 0) - spacing; let cx = x - w / 2;
  for (const ch of text) { const cw = g.measureText(ch).width; g.save(); g.translate(cx + cw / 2, y + (R() - .5) * size * .06); g.rotate((R() - .5) * .09); g.fillText(ch, -cw / 2, 0); g.restore(); cx += cw + spacing; }
}

// ---------- animation helpers ----------
export const ease = {
  lin: t => t, io: t => t < .5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2, out: t => 1 - (1 - t) ** 3, in: t => t * t * t,
  back: t => { const c = 1.9; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2; }, step: t => t < 1 ? 0 : 1,
};
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, t) => a + (b - a) * t;
// keys: [[t, value, easeName?], ...]; value may be number or array
export function K(t, keys) {
  if (t <= keys[0][0]) return keys[0][1]; const last = keys[keys.length - 1]; if (t >= last[0]) return last[1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, v0] = keys[i], [t1, v1, e] = keys[i + 1];
    if (t >= t0 && t <= t1) { const u = (ease[e || 'io'])((t - t0) / (t1 - t0)); return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], u)) : lerp(v0, v1, u); }
  }
}
export const seg = (t, a, b) => clamp((t - a) / (b - a));
