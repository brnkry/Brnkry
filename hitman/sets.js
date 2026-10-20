// Sets and props: bedroom, cafe terrace, hospital room.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { clay, mesh, lumpy, sphereG, capsuleG, paintTex, wobblyText, rng } from './lib.js';

const RB = (w, h, d, r = .02) => new RoundedBoxGeometry(w, h, d, 3, r);
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const MARKER = '"Permanent Marker"', TYPE = '"Special Elite"', HAND = '"Patrick Hand"';

function tube(points, r, mat, seg = 40) { return mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points), seg, r, 8), mat); }
function paperMat(tex, o = {}) { return clay(0xffffff, { map: tex, rough: .9, bump: o.bump ?? .5, unique: true }); }
function woodTex(base = '#9a6a40', seed = 4) {
  return paintTex(512, 512, (g) => { const R = rng(seed); g.fillStyle = base; g.fillRect(0, 0, 512, 512); for (let i = 0; i < 90; i++) { g.strokeStyle = `rgba(${R() < .5 ? '60,30,10' : '255,220,170'},${.08 + R() * .12})`; g.lineWidth = 1 + R() * 3; g.beginPath(); const y = R() * 512; g.moveTo(0, y); for (let x = 0; x <= 512; x += 32) g.lineTo(x, y + Math.sin(x * .02 + i) * 4 + (R() - .5) * 3); g.stroke(); } });
}

// ---------------- props ----------------
export function briefcase() {
  const g = new THREE.Group(), black = clay(0x1a1718, { rough: .5, bump: 2 }), metal = clay(0x9a968e, { rough: .35, metal: .6, bump: .3 });
  const W = .5, H = .1, D = .34;
  const body = mesh(lumpy(RB(W, H, D, .03), .004, 8, 3), black); body.position.y = H / 2; g.add(body);
  const hinge = new THREE.Group(); hinge.position.set(0, H, -D / 2); g.add(hinge);
  const lid = mesh(lumpy(RB(W, .045, D, .022), .004, 8, 5), black); lid.position.set(0, .022, D / 2); hinge.add(lid);
  const handle = tube([V(-.07, 0, 0), V(-.06, .045, 0), V(.06, .045, 0), V(.07, 0, 0)], .011, black, 20); handle.position.set(0, .0, D + .005); handle.rotation.x = Math.PI / 2; hinge.add(handle);
  const latches = [-1, 1].map(s => { const l = mesh(RB(.045, .035, .015, .005), metal); l.position.set(s * .15, H - .01, D / 2 + .008); g.add(l); return l; });
  const inside = mesh(new THREE.PlaneGeometry(W - .04, D - .04), clay(0x5a1e22, { rough: 1 })); inside.rotation.x = -Math.PI / 2; inside.position.y = H - .005; g.add(inside);
  g.userData = { hinge, latches, setOpen: (o) => { hinge.rotation.x = -o * 1.95; } };
  return g;
}
export function hitmanBook() {
  const cover = paintTex(512, 700, (g, w, h) => {
    g.fillStyle = '#d93a2c'; g.fillRect(0, 0, w, h); g.fillStyle = '#f4e9d0'; g.fillRect(28, 28, w - 56, h - 56);
    g.fillStyle = '#1b1a1c'; g.fillRect(28, 28, w - 56, 150);
    wobblyText(g, 'HITMAN', w / 2, 290, 120, MARKER, '#1b1a1c', 3); wobblyText(g, '101', w / 2, 420, 150, MARKER, '#d93a2c', 5);
    wobblyText(g, 'FOR BEGINNERS', w / 2, 103, 54, MARKER, '#f4e9d0', 6);
    g.strokeStyle = '#1b1a1c'; g.lineWidth = 8; g.beginPath(); g.arc(w / 2, 560, 52, 0, 7); g.stroke(); g.beginPath(); g.moveTo(w / 2 - 75, 560); g.lineTo(w / 2 + 75, 560); g.moveTo(w / 2, 485); g.lineTo(w / 2, 635); g.stroke();
  });
  const g = new THREE.Group(); const pages = mesh(RB(.2, .035, .27, .006), clay(0xf2ead8, { rough: .9 })); g.add(pages);
  const c = mesh(new THREE.PlaneGeometry(.205, .275), paperMat(cover)); c.rotation.x = -Math.PI / 2; c.position.y = .019; g.add(c);
  const back = mesh(RB(.205, .006, .275, .003), clay(0xd93a2c)); back.position.y = -.019; g.add(back);
  return g;
}
export function sandwich() {
  const g = new THREE.Group(), bread = clay(0xe8c48a, { rough: .9 }), crust = clay(0xb07a3e);
  const tri = new THREE.Shape(); tri.moveTo(-.07, -.05); tri.lineTo(.07, -.05); tri.lineTo(0, .07); tri.closePath();
  const sl = (y, m) => { const s = mesh(new THREE.ExtrudeGeometry(tri, { depth: .016, bevelEnabled: true, bevelSize: .008, bevelThickness: .006, bevelSegments: 2 }), m); s.rotation.x = -Math.PI / 2; s.position.y = y; g.add(s); };
  sl(0, bread); const let_ = mesh(lumpy(new THREE.CylinderGeometry(.075, .075, .01, 16), .01, 20, 2), clay(0x8fc248)); let_.position.y = .028; let_.scale.set(1, 1, .8); g.add(let_);
  const ch = mesh(new THREE.BoxGeometry(.1, .008, .08), clay(0xf2c230)); ch.position.y = .036; ch.rotation.y = .4; g.add(ch); sl(.04, bread);
  return g;
}
export function duck() {
  const g = new THREE.Group(), y = clay(0xffd21f, { rough: .35, bump: .6 }), o = clay(0xff8a1a, { rough: .4 }), b = clay(0x111111, { rough: .2 });
  const body = mesh(lumpy(sphereG(1), .05, 3, 1), y); body.scale.set(.06, .045, .075); body.position.y = .04; g.add(body);
  const head = mesh(sphereG(.037), y); head.position.set(0, .1, .035); g.add(head);
  const beak = mesh(sphereG(1), o); beak.scale.set(.022, .01, .026); beak.position.set(0, .095, .072); g.add(beak);
  for (const s of [-1, 1]) { const e = mesh(sphereG(.007), b); e.position.set(s * .02, .112, .062); g.add(e); }
  return g;
}
export function balloon(color, text) {
  const g = new THREE.Group(); const m = text ? clay(0xffffff, { map: text, rough: .3, bump: .3, unique: true }) : clay(color, { rough: .28, bump: .3 });
  const b = mesh(lumpy(sphereG(1, 32, 24), .02, 2, 3), m); b.scale.set(.15, .18, .15); b.position.y = .18; g.add(b);
  const k = mesh(new THREE.ConeGeometry(.02, .03, 10), clay(color)); k.position.y = -.005; k.rotation.x = Math.PI; g.add(k);
  return g;
}
export function cupSaucer() {
  const g = new THREE.Group(), w = clay(0xf5f0e6, { rough: .3, bump: .4 }), cof = clay(0x2b170c, { rough: .2, bump: .2 });
  const sau = mesh(new THREE.LatheGeometry([[0, 0], [.07, .0], [.08, .012], [.075, .016], [0, .012]].map(([x, y]) => new THREE.Vector2(x, y)), 28), w); g.add(sau);
  const cup = new THREE.Group(); cup.position.y = .012; g.add(cup);
  cup.add(mesh(new THREE.LatheGeometry([[0, 0], [.03, 0], [.042, .03], [.045, .06], [.041, .062], [.037, .03], [0, .008]].map(([x, y]) => new THREE.Vector2(x, y)), 28), w));
  const c = mesh(new THREE.CircleGeometry(.039, 24), cof, false); c.rotation.x = -Math.PI / 2; c.position.y = .052; cup.add(c);
  const h = mesh(new THREE.TorusGeometry(.018, .006, 8, 16, Math.PI * 1.3), w); h.position.set(.048, .035, 0); h.rotation.z = -Math.PI * .65; cup.add(h);
  const powder = mesh(lumpy(sphereG(1, 16, 10), .2, 4, 3), clay(0xf6f6f2, { rough: 1 }), false); powder.scale.set(.025, .006, .025); powder.position.y = .054; powder.visible = false; cup.add(powder);
  g.userData = { cup, powder, coffee: c };
  return g;
}
export function cake() {
  const g = new THREE.Group(); const plate = mesh(new THREE.CylinderGeometry(.11, .1, .012, 28), clay(0xf5f0e6, { rough: .3 })); g.add(plate);
  const slice = new THREE.Group(); slice.position.y = .006; g.add(slice);
  const tri = new THREE.Shape(); tri.moveTo(0, -.06); tri.lineTo(.09, .03); tri.quadraticCurveTo(0, .1, -.09, .03); tri.closePath();
  const L = [[0xf0d6a8, .028], [0xffffff, .01], [0x6a3a22, .028], [0xffffff, .012]]; let y = 0; const layers = [];
  for (const [c, h] of L) { const m = mesh(lumpy(new THREE.ExtrudeGeometry(tri, { depth: h, bevelEnabled: true, bevelSize: .004, bevelThickness: .003, bevelSegments: 2 }), .003, 30, 4), clay(c, { rough: .85 })); m.rotation.x = -Math.PI / 2; m.position.y = y; slice.add(m); layers.push(m); y += h; }
  const cherry = mesh(sphereG(.018), clay(0xc0101e, { rough: .2 })); cherry.position.set(0, y + .02, .02); slice.add(cherry);
  const cream = mesh(lumpy(sphereG(1, 16, 12), .15, 4, 2), clay(0xffffff)); cream.scale.set(.03, .018, .03); cream.position.set(0, y + .004, .02); slice.add(cream);
  g.userData = { slice, cherry };
  return g;
}
export function poisonBottle() {
  const g = new THREE.Group(); g.scale.setScalar(1.7); const glass = clay(0x6e3fa0, { rough: .2, bump: .2 });
  g.add(mesh(new THREE.LatheGeometry([[0, 0], [.022, 0], [.025, .01], [.025, .045], [.012, .06], [.01, .075], [0, .075]].map(([x, y]) => new THREE.Vector2(x, y)), 20), glass));
  const lbl = paintTex(256, 128, (c, w, h) => { c.fillStyle = '#f2ead8'; c.fillRect(0, 0, w, h); c.fillStyle = '#111'; c.beginPath(); c.arc(w / 2, 52, 30, 0, 7); c.fill(); c.fillRect(w / 2 - 18, 70, 36, 22); c.fillStyle = '#f2ead8'; c.beginPath(); c.arc(w / 2 - 12, 50, 9, 0, 7); c.arc(w / 2 + 12, 50, 9, 0, 7); c.fill(); });
  const label = mesh(new THREE.CylinderGeometry(.0255, .0255, .028, 20, 1, true), clay(0xffffff, { map: lbl, unique: true, bump: .3 }), false); label.position.y = .027; label.rotation.y = -Math.PI / 2; g.add(label);
  const cork = mesh(new THREE.CylinderGeometry(.011, .009, .016, 10), clay(0xb98a55)); cork.position.y = .08; g.add(cork); g.userData.cork = cork;
  return g;
}
export function newspaper(holes = true) {
  const tex = paintTex(1024, 1300, (g, w, h) => {
    g.fillStyle = '#ece4d0'; g.fillRect(0, 0, w, h); g.fillStyle = '#1d1b1b';
    g.font = `92px ${TYPE}`; g.textAlign = 'center'; g.fillText('THE DAILY BUGLE', w / 2, 110);
    g.fillRect(40, 140, w - 80, 5); g.fillRect(40, 152, w - 80, 2);
    g.textAlign = 'left'; wobblyText(g, 'LOCAL HITMAN', w / 2, 260, 128, TYPE, '#111', 9, 0); wobblyText(g, 'STARTS TODAY', w / 2, 390, 128, TYPE, '#111', 10, 0);
    g.fillStyle = '#5a5550'; for (let col = 0; col < 3; col++) for (let ln = 0; ln < 26; ln++) { if (ln > 3 && ln < 12 && col === 1) continue; g.fillRect(50 + col * 320, 500 + ln * 30, 270 - (ln % 5 === 4 ? 90 : 0), 9); }
    g.fillStyle = '#b5ab98'; g.fillRect(380, 600, 260, 220);
  });
  const W = .5, H = .64, geo = new THREE.PlaneGeometry(W, H, 20, 20);
  const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i); p.setZ(i, -Math.abs(x) * .08 + Math.sin(y * 9) * .004); } geo.computeVertexNormals();
  const m = mesh(geo, clay(0xffffff, { map: tex, rough: .95, bump: .3, unique: true }));
  m.material.side = THREE.DoubleSide; if (holes) { m.material.alphaTest = .5; m.material.alphaMap = paintTex(256, 330, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = '#000'; for (const x of [-.075, .075]) { g.beginPath(); g.ellipse(w / 2 + x * w / W, 240, 22, 19, 0, 0, 7); g.fill(); } }); }
  const grp = new THREE.Group(); grp.add(m); return grp;
}
function bistroChair() {
  const g = new THREE.Group(), iron = clay(0x26262a, { rough: .5 });
  const seat = mesh(new THREE.CylinderGeometry(.21, .21, .035, 28), clay(0x8a4a2a)); seat.position.y = .45; g.add(seat);
  for (const [x, z] of [[-.15, -.15], [.15, -.15], [-.15, .15], [.15, .15]]) { const l = mesh(new THREE.CylinderGeometry(.012, .012, .45, 8), iron); l.position.set(x, .225, z); g.add(l); }
  const back = tube([V(-.17, .45, -.17), V(-.18, .8, -.2), V(0, .88, -.22), V(.18, .8, -.2), V(.17, .45, -.17)], .014, iron, 30); g.add(back);
  return g;
}
function plant(scale = 1) {
  const g = new THREE.Group(); const pot = mesh(new THREE.LatheGeometry([[0, 0], [.07, 0], [.09, .14], [.1, .145], [.1, .16], [0, .16]].map(([x, y]) => new THREE.Vector2(x, y)), 24), clay(0xc4693c)); g.add(pot);
  const leaf = clay(0x4f8a3a, { rough: .6 }); const R = rng(5);
  for (let i = 0; i < 7; i++) { const l = mesh(lumpy(sphereG(1, 16, 10), .1, 3, i), leaf); l.scale.set(.03, .1, .012); const a = i / 7 * 6.28; l.position.set(Math.cos(a) * .03, .24, Math.sin(a) * .03); l.rotation.set(Math.sin(a) * .5, 0, -Math.cos(a) * .5); g.add(l); }
  g.scale.setScalar(scale); return g;
}

// ---------------- sets ----------------
function floorWall(scene, floorMat, wallMat, wallZ) {
  const f = mesh(new THREE.PlaneGeometry(14, 14), floorMat, false); f.rotation.x = -Math.PI / 2; scene.add(f);
  const w = mesh(new THREE.PlaneGeometry(14, 8), wallMat, false); w.position.set(0, 4, wallZ); scene.add(w);
}
function addLights(scene, o) {
  const key = new THREE.SpotLight(o.key ?? 0xffcf96, o.ki ?? 110, 0, o.angle ?? .55, .8, 1.6); key.position.set(...o.kp); key.target.position.set(...(o.kt ?? [0, 1, 0])); key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.bias = -.0004; key.shadow.radius = 8; key.shadow.blurSamples = 16; scene.add(key, key.target);
  const hemi = new THREE.HemisphereLight(o.sky ?? 0xffe6c8, o.ground ?? 0x5a3418, o.hi ?? .8); scene.add(hemi);
  const rim = new THREE.DirectionalLight(o.rim ?? 0xffc28a, o.ri ?? 1.6); rim.position.set(...(o.rp ?? [-3, 3, -2])); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xffe2c0, o.fi ?? .5); fill.position.set(-2, 2, 4); scene.add(fill);
  return { key, hemi, rim };
}

export function bedroom() {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x3a2416);
  const wallTex = paintTex(512, 512, (g) => { g.fillStyle = '#d6a978'; g.fillRect(0, 0, 512, 512); g.fillStyle = 'rgba(150,90,50,.18)'; for (let x = 0; x < 512; x += 64) g.fillRect(x, 0, 22, 512); }); wallTex.wrapS = wallTex.wrapT = THREE.RepeatWrapping; wallTex.repeat.set(5, 3);
  const floorTex = woodTex('#7a4a2a', 8); floorTex.wrapS = floorTex.wrapT = THREE.RepeatWrapping; floorTex.repeat.set(4, 4);
  floorWall(s, clay(0xffffff, { map: floorTex, unique: true }), clay(0xffffff, { map: wallTex, unique: true, rep: 6 }), -1.6);
  const L = addLights(s, { kp: [1.6, 3.4, 2.2], kt: [0, 1.2, -.8], ki: 95 });
  // banner
  const bTex = paintTex(1300, 560, (g, w, h) => {
    g.fillStyle = '#f6efdf'; g.fillRect(0, 0, w, h);
    const R = rng(4); for (let i = 0; i < 18; i++) { g.fillStyle = ['#ff3d5a', '#d4ff3a', '#3aa7ff', '#ffb000'][i % 4]; g.save(); g.translate(R() * w, R() < .5 ? R() * 60 + 20 : h - 20 - R() * 60); g.rotate(R() * 6); g.fillRect(-9, -4, 18, 8); g.restore(); }
    wobblyText(g, 'FIRST DAY', w / 2, 200, 230, MARKER, '#1b1a1c', 12, 4);
    wobblyText(g, 'AS A HITMAN!', w / 2, 420, 165, MARKER, '#e0283f', 13, 2);
  });
  const bGeo = new THREE.PlaneGeometry(1.3, .56, 30, 6); const bp = bGeo.attributes.position; for (let i = 0; i < bp.count; i++) bp.setZ(i, Math.sin(bp.getX(i) * 7) * .012 - Math.abs(bp.getY(i)) * .01); bGeo.computeVertexNormals();
  const banner = mesh(bGeo, paperMat(bTex, { bump: .4 })); banner.position.set(0, 2.08, -1.56); s.add(banner);
  const tape = clay(0xe8dcae, { opacity: .85, rough: .5 }); for (const x of [-.62, .62]) { const t = mesh(new THREE.BoxGeometry(.08, .03, .004), tape, false); t.position.set(x, 2.35, -1.545); t.rotation.z = x * .5; s.add(t); }
  // bunting
  const pts = []; for (let i = 0; i <= 12; i++) { const x = -1 + i / 6; pts.push(V(x, 2.62 - (1 - x * x) * .14, -1.5)); }
  s.add(tube(pts, .004, clay(0xf0e8d8), 60));
  const flagC = [0xff3d5a, 0xd4ff3a, 0xffb000, 0x3aa7ff];
  for (let i = 0; i < 11; i++) { const x = -.92 + i * .184, y = 2.62 - (1 - x * x) * .14; const sh = new THREE.Shape(); sh.moveTo(-.055, 0); sh.lineTo(.055, 0); sh.lineTo(0, -.12); sh.closePath(); const f = mesh(new THREE.ShapeGeometry(sh), clay(flagC[i % 4], { rough: .9 })); f.material.side = THREE.DoubleSide; f.position.set(x, y, -1.49); f.rotation.z = (Math.random() - .5) * 0; s.add(f); }
  // balloons
  const bal = []; [[-.95, 1.55, -1.2, 0xff3d5a], [-.75, 1.75, -1.3, 0xd4ff3a], [-1.05, 1.9, -1.35, 0x3aa7ff], [.95, 1.65, -1.25, 0xffb000], [.8, 1.9, -1.35, 0xff3d5a]].forEach(([x, y, z, c], i) => {
    const b = balloon(c); b.position.set(x, y, z); s.add(b); bal.push(b);
    s.add(tube([V(x, y, z), V(x + .05, y - .4, z + .1), V(x * .8, .8, -.75)], .003, clay(0xf0e8d8), 20));
  });
  // calendar
  const cTex = paintTex(400, 520, (g, w, h) => {
    g.fillStyle = '#f7f2e6'; g.fillRect(0, 0, w, h); g.fillStyle = '#e0283f'; g.fillRect(0, 0, w, 110);
    wobblyText(g, 'OCTOBER', w / 2, 58, 62, MARKER, '#f7f2e6', 2, 3); g.strokeStyle = '#8a8a96'; g.lineWidth = 2;
    for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) { g.strokeRect(14 + c * 53, 130 + r * 75, 53, 75); g.fillStyle = '#555'; g.font = `20px ${HAND}`; g.fillText(String(r * 7 + c + 1), 20 + c * 53, 152 + r * 75); }
    g.strokeStyle = '#e0283f'; g.lineWidth = 6; g.beginPath(); g.ellipse(14 + 2 * 53 + 26, 130 + 2 * 75 + 38, 36, 44, .2, 0, 6.6); g.stroke();
    g.fillStyle = '#e0283f'; g.font = `30px ${HAND}`; g.fillText('DAY 1!', 128, 315);
  });
  const cal = mesh(new THREE.PlaneGeometry(.34, .44), paperMat(cTex)); cal.position.set(-.82, 1.38, -1.585); cal.rotation.z = .03; s.add(cal);
  // certificate frame
  const certT = paintTex(500, 360, (g, w, h) => { g.fillStyle = '#f3ecd8'; g.fillRect(0, 0, w, h); g.strokeStyle = '#b08a3e'; g.lineWidth = 10; g.strokeRect(14, 14, w - 28, h - 28); wobblyText(g, 'ONLINE HITMAN', w / 2, 110, 48, TYPE, '#2a2a2a', 4); wobblyText(g, 'COURSE', w / 2, 170, 48, TYPE, '#2a2a2a', 5); wobblyText(g, 'PASSED  (C-)', w / 2, 250, 40, HAND, '#e0283f', 7); g.fillStyle = '#c9a13a'; g.beginPath(); g.arc(w - 90, h - 80, 34, 0, 7); g.fill(); });
  const cert = new THREE.Group(); cert.add(mesh(RB(.4, .3, .03, .008), clay(0x5a3a22))); const cp = mesh(new THREE.PlaneGeometry(.35, .25), paperMat(certT)); cp.position.z = .017; cert.add(cp); cert.position.set(.86, 1.45, -1.57); cert.rotation.z = -.04; s.add(cert);
  // desk
  const wood = clay(0xffffff, { map: (() => { const t = woodTex('#a8703f', 3); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })(), unique: true });
  const top = mesh(lumpy(RB(1.6, .06, .62, .02), .003, 6, 1), wood); top.position.set(0, .75, -.45); s.add(top);
  const panel = mesh(RB(1.5, .66, .04, .01), wood); panel.position.set(0, .4, -.18); s.add(panel);
  // desk props
  const lamp = new THREE.Group(), lm = clay(0x2f5a46, { rough: .4 });
  lamp.add(mesh(new THREE.CylinderGeometry(.08, .09, .025, 20), lm)); lamp.add(tube([V(0, 0, 0), V(.02, .3, 0), V(-.12, .45, .05)], .012, lm, 20));
  const shade = mesh(new THREE.ConeGeometry(.09, .12, 20, 1, true), lm); shade.material.side = THREE.DoubleSide; shade.position.set(-.15, .43, .06); shade.rotation.z = .9; lamp.add(shade);
  const bulb = mesh(sphereG(.035), new THREE.MeshBasicMaterial({ color: 0xfff1c8 }), false); bulb.position.set(-.17, .4, .06); lamp.add(bulb);
  const pl = new THREE.PointLight(0xffc27a, 1.4, 2.5, 1.5); pl.position.set(-.2, .36, .08); lamp.add(pl);
  lamp.position.set(.62, .78, -.62); s.add(lamp);
  const mug = new THREE.Group(); mug.add(mesh(new THREE.CylinderGeometry(.05, .045, .11, 20), clay(0x3aa7ff))); [0xff3d5a, 0xffb000, 0xd4ff3a].forEach((c, i) => { const p = mesh(new THREE.CylinderGeometry(.007, .007, .18, 8), clay(c)); p.position.set(-.015 + i * .015, .08, (i - 1) * .01); p.rotation.z = (i - 1) * .2; mug.add(p); }); mug.position.set(-.66, .835, -.62); s.add(mug);
  const P = { case: briefcase(), book: hitmanBook(), sand: sandwich(), duck: duck() };
  P.case.position.set(0, .78, -.5); P.book.position.set(.38, .8, -.38); P.book.rotation.y = -.25; P.sand.position.set(-.36, .79, -.36); P.duck.position.set(-.55, .78, -.33); P.duck.rotation.y = .5;
  Object.values(P).forEach(p => s.add(p));
  return { scene: s, props: P, lights: L, balloons: bal, update(t) { bal.forEach((b, i) => { b.rotation.z = Math.sin(t * 1.3 + i) * .05; b.position.y += Math.sin(t * 2 + i * 2) * .0004; }); } };
}

export function cafe() {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x6a4a30);
  const cob = paintTex(512, 512, (g) => { const R = rng(9); g.fillStyle = '#7d6a58'; g.fillRect(0, 0, 512, 512); for (let y = 0; y < 512; y += 42) for (let x = (y / 42 % 2) * 30; x < 540; x += 62) { const v = 140 + R() * 50; g.fillStyle = `rgb(${v},${v * .86},${v * .72})`; g.beginPath(); g.ellipse(x, y + 20, 27, 17, R() * .3, 0, 7); g.fill(); } }); cob.wrapS = cob.wrapT = THREE.RepeatWrapping; cob.repeat.set(6, 6);
  const wallT = paintTex(512, 512, (g) => { g.fillStyle = '#e2b98c'; g.fillRect(0, 0, 512, 512); const R = rng(2); for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(160,100,60,${R() * .12})`; g.beginPath(); g.ellipse(R() * 512, R() * 512, 30 + R() * 60, 20 + R() * 40, 0, 0, 7); g.fill(); } }); wallT.wrapS = wallT.wrapT = THREE.RepeatWrapping; wallT.repeat.set(4, 2);
  floorWall(s, clay(0xffffff, { map: cob, unique: true, bump: 2.5 }), clay(0xffffff, { map: wallT, unique: true }), -2.1);
  const L = addLights(s, { kp: [2.2, 3.8, 1.8], kt: [0, .9, -.4], ki: 120, angle: .6, sky: 0xffe8cc, hi: .9, rp: [-2.5, 3, -3], ri: 2 });
  // window with warm interior
  const winT = paintTex(512, 600, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#ffcf7a'); gr.addColorStop(1, '#d9822b'); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(90,40,20,.55)'; for (const y of [180, 330]) g.fillRect(30, y, w - 60, 14); for (let i = 0; i < 9; i++) { g.fillStyle = ['#7a2a1a', '#2a4a3a', '#d9c39a'][i % 3]; g.fillRect(50 + i * 48, 120, 30, 60); g.fillRect(60 + i * 46, 270, 26, 60); } g.fillStyle = 'rgba(255,255,255,.18)'; g.beginPath(); g.moveTo(40, h); g.lineTo(200, 0); g.lineTo(260, 0); g.lineTo(100, h); g.fill(); });
  const win = mesh(new THREE.PlaneGeometry(1.0, 1.15), new THREE.MeshBasicMaterial({ map: winT }), false); win.position.set(.75, 1.35, -2.08); s.add(win);
  const frameM = clay(0x2f4a3c); for (const [x, y, w, h] of [[.75, .76, 1.1, .06], [.75, 1.94, 1.1, .06], [.22, 1.35, .06, 1.2], [1.28, 1.35, .06, 1.2], [.75, 1.35, .04, 1.15]]) { const b = mesh(RB(w, h, .05, .01), frameM); b.position.set(x, y, -2.06); s.add(b); }
  // awning
  const awT = paintTex(512, 256, (g, w, h) => { for (let x = 0; x < w; x += 64) { g.fillStyle = (x / 64) % 2 ? '#f4efe4' : '#2f7a5a'; g.fillRect(x, 0, 64, h); } });
  const aw = mesh(new THREE.PlaneGeometry(1.4, .5, 1, 1), clay(0xffffff, { map: awT, unique: true })); aw.material.side = THREE.DoubleSide; aw.position.set(.75, 2.2, -1.88); aw.rotation.x = -.95; s.add(aw);
  for (let i = 0; i < 11; i++) { const sc = mesh(new THREE.CylinderGeometry(.064, .064, .015, 16, 1, false, 0, Math.PI), clay(i % 2 ? 0xf4efe4 : 0x2f7a5a)); sc.rotation.set(Math.PI / 2, 0, Math.PI / 2); sc.position.set(.12 + i * .127, 2.0, -1.68); s.add(sc); }
  const signT = paintTex(800, 200, (g, w, h) => { g.fillStyle = '#2f4a3c'; g.fillRect(0, 0, w, h); wobblyText(g, 'CAFFE ROMA', w / 2, h / 2 + 6, 120, MARKER, '#f4e2b8', 21, 6); });
  const sign = mesh(RB(.9, .22, .03, .01), clay(0xffffff, { map: signT, unique: true })); sign.position.set(.75, 2.52, -2.06); s.add(sign);
  // chalkboard
  const chT = paintTex(400, 560, (g, w, h) => { g.fillStyle = '#26302b'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(255,255,255,.06)'; for (let i = 0; i < 30; i++) g.fillRect(Math.random() * w, Math.random() * h, 80, 20); wobblyText(g, 'TODAY', w / 2, 80, 72, HAND, '#f2efe6', 3); wobblyText(g, 'ESPRESSO  $2', w / 2, 200, 50, HAND, '#f2efe6', 4); wobblyText(g, 'CAKE  $4', w / 2, 280, 50, HAND, '#f2efe6', 5); wobblyText(g, 'NO POISON', w / 2, 400, 48, HAND, '#ffb36a', 6); wobblyText(g, 'PLEASE', w / 2, 460, 48, HAND, '#ffb36a', 7); });
  const board = new THREE.Group(); const bm = clay(0x6b4426); board.add(mesh(RB(.46, .62, .03, .01), bm)); const bf = mesh(new THREE.PlaneGeometry(.4, .56), clay(0xffffff, { map: chT, unique: true, rough: .95, bump: .4 })); bf.position.z = .017; board.add(bf);
  for (const x of [-.18, .18]) { const leg = mesh(new THREE.BoxGeometry(.03, .9, .03), bm); leg.position.set(x, -.35, -.05); board.add(leg); }
  board.position.set(-1.55, 1.05, -2.0); board.rotation.set(-.12, .2, 0); s.add(board);
  // string lights
  const sp = []; for (let i = 0; i <= 14; i++) { const x = -1.6 + i * 3.2 / 14; sp.push(V(x, 2.95 - (1 - (x / 1.6) ** 2) * .25, -1.5)); }
  s.add(tube(sp, .005, clay(0x222222), 80));
  const bulbs = []; for (let i = 0; i < 13; i++) { const x = -1.48 + i * .247, y = 2.95 - (1 - (x / 1.6) ** 2) * .25 - .04; const b = mesh(sphereG(.025, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffd98a }), false); b.position.set(x, y, -1.5); s.add(b); bulbs.push(b); }
  // table + chair + props
  const table = new THREE.Group(); const clothT = paintTex(512, 512, (g) => { for (let y = 0; y < 512; y += 64) for (let x = 0; x < 512; x += 64) { g.fillStyle = ((x + y) / 64) % 2 ? '#f4efe6' : '#c8323a'; g.fillRect(x, y, 64, 64); } });
  const ttop = mesh(lumpy(new THREE.CylinderGeometry(.42, .42, .035, 40), .003, 6, 4), clay(0xffffff, { map: clothT, unique: true, rough: .95 })); ttop.position.y = .74; table.add(ttop);
  const drape = mesh(new THREE.CylinderGeometry(.43, .45, .12, 40, 1, true), clay(0xc8323a, { rough: .95 })); drape.position.y = .68; table.add(drape);
  const tleg = mesh(new THREE.CylinderGeometry(.03, .03, .7, 12), clay(0x26262a)); tleg.position.y = .35; table.add(tleg);
  const tfoot = mesh(new THREE.CylinderGeometry(.18, .2, .03, 24), clay(0x26262a)); tfoot.position.y = .015; table.add(tfoot);
  table.position.set(0, 0, -.35); s.add(table);
  const chair = bistroChair(); chair.position.set(0, 0, -.88); s.add(chair);
  const P = { cup: cupSaucer(), cake: cake(), plant: plant(1), paper: newspaper(true), bottle: poisonBottle(), table, chair, fork: null };
  P.cup.position.set(-.16, .76, -.24); P.cake.position.set(.1, .762, -.2);
  P.plant.position.set(-.62, 0, .45); s.add(P.cup, P.cake, P.plant);
  const fork = new THREE.Group(); fork.add(mesh(new THREE.BoxGeometry(.008, .004, .11), clay(0xbcb8b0, { metal: .6, rough: .3 }))); P.fork = fork; s.add(fork);
  return { scene: s, props: P, lights: L, update(t) { bulbs.forEach((b, i) => b.material.color.setHSL(.11, 1, .72 + Math.sin(t * 3 + i * 1.7) * .04)); } };
}

export function hospital() {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x4a5a50);
  const tiles = paintTex(512, 512, (g) => { g.fillStyle = '#cfd6cf'; g.fillRect(0, 0, 512, 512); g.strokeStyle = '#a9b2aa'; g.lineWidth = 4; for (let i = 0; i <= 512; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); } }); tiles.wrapS = tiles.wrapT = THREE.RepeatWrapping; tiles.repeat.set(8, 8);
  floorWall(s, clay(0xffffff, { map: tiles, unique: true }), clay(0xa9c9b4, { rep: 4 }), -1.7);
  const L = addLights(s, { kp: [1.8, 3.6, 2.2], kt: [0, 1, -.8], ki: 100, key: 0xffe2bc, sky: 0xf0fff4, ground: 0x4a5a4a, hi: 1, rim: 0xd8f0ff, ri: 1.2 });
  const stripe = mesh(new THREE.PlaneGeometry(14, .08), clay(0x7aa38a)); stripe.position.set(0, 1.0, -1.695); s.add(stripe);
  // window + curtains
  const sky = paintTex(256, 320, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#9fd0f0'); gr.addColorStop(1, '#e8f4fa'); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = '#fff'; for (const [x, y] of [[70, 90], [180, 160]]) { g.beginPath(); g.arc(x, y, 26, 0, 7); g.arc(x + 30, y - 8, 30, 0, 7); g.arc(x + 60, y, 24, 0, 7); g.fill(); } });
  const win = mesh(new THREE.PlaneGeometry(.75, .95), new THREE.MeshBasicMaterial({ map: sky }), false); win.position.set(.95, 1.65, -1.69); s.add(win);
  const cur = clay(0xe8d27a, { rough: .9 }); for (const x of [.5, 1.4]) { const c = mesh(lumpy(new THREE.CylinderGeometry(.12, .16, 1.2, 16), .02, 10, x * 10), cur); c.scale.z = .35; c.position.set(x, 1.6, -1.6); s.add(c); }
  // ECG monitor
  const ecgC = document.createElement('canvas'); ecgC.width = 400; ecgC.height = 260; const ecgT = new THREE.CanvasTexture(ecgC); ecgT.colorSpace = THREE.SRGBColorSpace;
  const mon = new THREE.Group(); mon.add(mesh(RB(.44, .32, .14, .03), clay(0xd8d8d0))); const scr = mesh(new THREE.PlaneGeometry(.36, .23), new THREE.MeshBasicMaterial({ map: ecgT }), false); scr.position.z = .072; mon.add(scr);
  mon.position.set(-.82, 1.7, -1.55); mon.rotation.y = .25; s.add(mon);
  const arm = mesh(new THREE.BoxGeometry(.05, .05, .2), clay(0xb8b8b0)); arm.position.set(-.82, 1.7, -1.64); s.add(arm);
  // bed (head at back, foot toward camera)
  const bed = new THREE.Group(); const frame = clay(0xe9ece6, { rough: .4 }), sheet = clay(0xf4f6f2, { rough: .95, bump: 2 });
  const mat_ = mesh(RB(.9, .16, 1.95, .05), sheet); mat_.position.set(0, .55, 0); bed.add(mat_);
  for (const z of [-.98, .98]) { const hb = mesh(RB(.98, z < 0 ? .75 : .45, .05, .02), frame); hb.position.set(0, z < 0 ? .78 : .63, z); bed.add(hb); }
  for (const [x, z] of [[-.42, -.95], [.42, -.95], [-.42, .95], [.42, .95]]) { const l = mesh(new THREE.CylinderGeometry(.02, .02, .5, 8), clay(0x9aa0a0, { metal: .5, rough: .3 })); l.position.set(x, .25, z); bed.add(l); }
  const back = mesh(lumpy(RB(.82, .7, .12, .05), .01, 5, 2), sheet); back.position.set(0, .88, -.8); back.rotation.x = -.45; bed.add(back);
  const pillow = mesh(lumpy(RB(.6, .28, .14, .07), .015, 5, 6), clay(0xffffff, { rough: .95 })); pillow.position.set(0, 1.05, -.74); pillow.rotation.x = -.45; bed.add(pillow);
  const blanket = mesh(lumpy(RB(.94, .14, 1.15, .06), .02, 4, 3), clay(0x8fb6d8, { rough: .95, bump: 2 })); blanket.position.set(0, .68, .4); bed.add(blanket);
  const fold = mesh(lumpy(new THREE.CylinderGeometry(.07, .07, .94, 16), .01, 6, 1), clay(0xf4f6f2, { rough: .95 })); fold.rotation.z = Math.PI / 2; fold.position.set(0, .74, -.17); bed.add(fold);
  bed.position.set(-.12, 0, -.7); s.add(bed);
  // over-bed tray
  const tray = new THREE.Group(); const tm = clay(0xd9c7a8, { rough: .6 }); const tt = mesh(RB(.7, .03, .32, .01), tm); tt.position.set(-.3, 1.0, 0); tray.add(tt);
  const pole = mesh(new THREE.CylinderGeometry(.018, .018, 1.0, 10), clay(0x9aa0a0, { metal: .5, rough: .3 })); pole.position.set(.08, .5, 0); tray.add(pole); tray.position.set(.27, 0, -.25); s.add(tray);
  const chair = new THREE.Group(); const cm = clay(0x5f8fb0); const seat = mesh(RB(.48, .07, .46, .03), cm); seat.position.y = .45; chair.add(seat); const cb = mesh(RB(.48, .5, .07, .03), cm); cb.position.set(0, .72, -.22); chair.add(cb);
  for (const [x, z] of [[-.2, -.2], [.2, -.2], [-.2, .2], [.2, .2]]) { const l = mesh(new THREE.CylinderGeometry(.015, .015, .45, 8), clay(0x9aa0a0)); l.position.set(x, .225, z); chair.add(l); }
  chair.position.set(.92, 0, -1.02); chair.rotation.y = -1.3; s.add(chair);
  const gwT = paintTex(512, 512, (g, w, h) => { g.fillStyle = '#ffb000'; g.fillRect(0, 0, w, h); wobblyText(g, 'GET', w / 2, 180, 92, MARKER, '#7a1020', 1); wobblyText(g, 'WELL', w / 2, 270, 92, MARKER, '#7a1020', 2); wobblyText(g, 'SOON', w / 2, 360, 92, MARKER, '#7a1020', 3); });
  const gw = balloon(0xffb000, gwT); gw.scale.setScalar(1.25); gw.position.set(1.25, 1.85, -1.35); gw.rotation.y = -.35; s.add(gw);
  s.add(tube([V(1.25, 1.85, -1.35), V(1.18, 1.4, -1.3), V(1.12, .75, -1.25)], .003, clay(0xf0e8d8), 20));
  const P = { cup: cupSaucer(), tray, bed, chair, gw };
  P.cup.position.set(-.05, 1.015, -.27); s.add(P.cup);
  let flat = 0; const ecg = (t, bpm, flatline) => {
    const g = ecgC.getContext('2d'); g.fillStyle = '#06140c'; g.fillRect(0, 0, 400, 260); g.strokeStyle = '#123a22'; g.lineWidth = 1; for (let x = 0; x < 400; x += 25) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 260); g.stroke(); }
    g.strokeStyle = '#3dff7a'; g.lineWidth = 5; g.beginPath(); const per = 60 / bpm;
    for (let x = 0; x <= 400; x += 2) { const tt = t - (400 - x) / 400 * 2.2; const ph = ((tt % per) + per) % per / per; let y = 150; if (!flatline) { if (ph > .3 && ph < .34) y = 150 - (ph - .3) / .04 * 110; else if (ph >= .34 && ph < .38) y = 40 + (ph - .34) / .04 * 160; else if (ph >= .38 && ph < .42) y = 200 - (ph - .38) / .04 * 50; } x ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke(); g.fillStyle = '#3dff7a'; g.font = `bold 34px ${'"JetBrains Mono"'}`; g.fillText(flatline ? '---' : String(Math.round(bpm)), 300, 50); ecgT.needsUpdate = true;
  };
  return { scene: s, props: P, lights: L, ecg, update(t) { gw.rotation.z = Math.sin(t * 1.1) * .06; } };
}
