// "First Day as a Hitman": shot timeline. window.R(t) renders the frame at time t (seconds).
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { rookie, tony } from './chars.js';
import { bedroom, cafe, hospital } from './sets.js';
import { K, seg, lerp, clamp, ease, rng, clay as clayM, lumpy as lumpyM } from './lib.js';

const W = 1080, H = 1920;
const fonts = [['Permanent Marker', 'permanent-marker'], ['Special Elite', 'special-elite'], ['Patrick Hand', 'patrick-hand']];
await Promise.all(fonts.map(async ([n, f]) => { const ff = new FontFace(n, `url(/node_modules/@fontsource/${f}/files/${f}-latin-400-normal.woff2)`); await ff.load(); document.fonts.add(ff); }));

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H); renderer.setPixelRatio(1); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05; document.body.appendChild(renderer.domElement);
const cam = new THREE.PerspectiveCamera(36, W / H, .05, 60);
const SETS = { bed: bedroom(), cafe: cafe(), hosp: hospital() };
const A = rookie(), T = tony();
const extras = (() => {
  const g = { band: new THREE.Group(), cream: new THREE.Group() }; const white = clayM(0xf7f4ec, { rough: .95 });
  const band = new THREE.Mesh(new THREE.TorusGeometry(.2, .028, 10, 40), white); band.rotation.x = Math.PI / 2 - .25; band.scale.set(.95, 1.0, 1); band.position.y = .1; band.castShadow = true; g.band.add(band);
  const pad = new THREE.Mesh(new THREE.BoxGeometry(.07, .06, .02), white); pad.position.set(.08, .14, .16); pad.rotation.set(-.4, .4, .2); g.band.add(pad);
  [[0, -.03, .23, .035], [.07, -.1, .18, .03], [-.08, -.08, .18, .025], [.03, .12, .17, .022], [-.05, -.14, .17, .02]].forEach(([x, y, z, r]) => { const c = new THREE.Mesh(lumpyM(new THREE.SphereGeometry(r, 14, 10), r * .25, 60, x * 50), clayM(0xfffaf0, { rough: .6 })); c.scale.z = .6; c.position.set(x, y, z); g.cream.add(c); });
  const ch = new THREE.Mesh(new THREE.SphereGeometry(.016, 12, 10), clayM(0xc0101e, { rough: .2 })); ch.position.set(.02, .02, .25); g.cream.add(ch);
  A.head.add(g.band, g.cream); g.band.visible = g.cream.visible = false; return g;
})();
const composer = new EffectComposer(renderer); const rp = new RenderPass(SETS.bed.scene, cam); composer.addPass(rp);
const bokeh = new BokehPass(SETS.bed.scene, cam, { focus: 3, aperture: .004, maxblur: .008 }); composer.addPass(bokeh); composer.addPass(new OutputPass());

const v3 = (a) => new THREE.Vector3(...a);
// ---------- pose helpers ----------
function reset(C) {
  C.root.position.set(0, 0, 0); C.root.rotation.set(0, 0, 0); C.hips.position.set(0, C === T ? .76 : .76, 0); C.hips.rotation.set(0, 0, 0);
  C.torso.rotation.set(0, 0, 0); C.neckPiv.rotation.set(0, 0, 0); C.head.rotation.set(0, 0, 0);
  C.handT = [v3([-.24, .74, .06]), v3([.24, .74, .06])]; C.handRot = [null, null]; C.handPose = [{ curl: .3 }, { curl: .3 }]; C.handRoll = [0, 0];
  C.footT = [v3([-.11, .05, .02]), v3([.11, .05, .02])]; C.footPitch = [0, 0]; C.visibleLegs = true;
  C.elbowPole = [v3([-1, -.4, -.6]), v3([1, -.4, -.6])]; C.kneePole = [v3([0, 0, 1]), v3([0, 0, 1])];
  C.arm.forEach(a => a.hand.userData.tip.visible = false); if (C === A && typeof extras !== 'undefined') extras.band.visible = extras.cream.visible = false;
  C.face = { lx: 0, ly: 0, lid: C === T ? [.35, .35] : [.2, .2], lidB: [0, 0], brow: [0, 0], browA: [0, 0], mw: C === T ? .08 : .07, curve: 0, open: 0, teeth: 0, wob: 0, tongue: 0, sweat: 0, sweatSlide: 0, cross: 0 };
}
function pose(C, p) {
  if (p.pos) C.root.position.set(...p.pos); if (p.ry !== undefined) C.root.rotation.y = p.ry;
  if (p.rootRot) C.root.rotation.set(...p.rootRot, 'YXZ');
  if (p.hip) C.hips.position.set(...p.hip);
  if (p.lean !== undefined) C.torso.rotation.x = p.lean; if (p.side !== undefined) C.torso.rotation.z = p.side; if (p.twist !== undefined) C.torso.rotation.y = p.twist;
  if (p.head) C.head.rotation.set(...p.head, 'YXZ');
  C.root.updateMatrixWorld(true);
  if (p.hands) p.hands.forEach((h, i) => { if (h) C.handT[i] = v3(h); });
  if (p.handsW) p.handsW.forEach((h, i) => { if (h) C.handT[i] = C.root.worldToLocal(v3(h)); });
  if (p.hp) p.hp.forEach((h, i) => { if (h) C.handPose[i] = h; });
  if (p.hr) p.hr.forEach((h, i) => { if (h !== undefined) C.handRot[i] = h; });
  if (p.roll) C.handRoll = p.roll;
  if (p.feet) p.feet.forEach((f, i) => { if (f) C.footT[i] = v3(f); });
  if (p.pitch) C.footPitch = p.pitch; if (p.legs !== undefined) C.visibleLegs = p.legs;
  if (p.elbow) p.elbow.forEach((e, i) => { if (e) C.elbowPole[i] = v3(e); }); if (p.knee) p.knee.forEach((k, i) => { if (k) C.kneePole[i] = v3(k); });
  if (p.face) Object.assign(C.face, p.face);
}
// seated pose (chair seat height ~.47)
const seated = (C, extra = {}) => pose(C, Object.assign({ hip: [0, .5, -.02], feet: [[-.13, .05, .42], [.13, .05, .42]], knee: [[0, 1, 1], [0, 1, 1]] }, extra));
// crouch
const crouch = (C, d, extra = {}) => pose(C, Object.assign({ hip: [0, .76 - d * .38, -d * .12], lean: d * .3, feet: [[-.13, .05, .1], [.13, .05, .1]], knee: [[-.2, 0, 1], [.2, 0, 1]] }, extra));
const lerp3 = (a, b, u) => a.map((x, i) => lerp(x, b[i], u));

// expressions
const X = {
  nervous: { brow: [.6, .9], browA: [-.5, -.5], curve: -.15, wob: 1, mw: .06 },
  proud: { brow: [.4, .4], browA: [0, 0], curve: .7, mw: .08, lid: [.25, .25] },
  grin: { brow: [.9, .9], browA: [-.4, -.4], curve: -.35, open: .45, teeth: 1, mw: .085, wob: .6 },
  shock: { brow: [1.1, 1.1], browA: [-.2, -.2], open: .7, mw: .05, curve: 0, lid: [0, 0] },
  think: { brow: [-.3, .8], browA: [.3, -.3], curve: -.2, mw: .05, lid: [.4, .25], lx: .4, ly: .3 },
  sly: { brow: [.2, -.1], browA: [.2, .4], curve: .5, mw: .07, lid: [.4, .4] },
  blank: { brow: [0, 0], browA: [0, 0], curve: 0, open: 0, teeth: 0, wob: 0 },
};
const mix = (a, b, u) => { const o = {}; for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) { const x = a[k] ?? A.face[k], y = b[k] ?? A.face[k]; o[k] = Array.isArray(x) ? x.map((v, i) => lerp(v, y[i], u)) : lerp(x, y, u); } return o; };
const blink = (t, at, d = .15) => { const u = (t - at) / d; return u > 0 && u < 1 ? Math.sin(u * Math.PI) : 0; };
function lidsBlink(F, t, times) { let b = 0; for (const x of times) b = Math.max(b, blink(t, x)); F.lid = (F.lid ?? [.2, .2]).map(l => lerp(l, 1, b)); return F; }

function camSet(p, at, fov, focusAt, ap = .004) {
  cam.position.set(...p); cam.lookAt(...at); cam.fov = fov; cam.updateProjectionMatrix();
  const fd = cam.position.distanceTo(v3(focusAt ?? at)); bokeh.uniforms.focus.value = fd; bokeh.uniforms.aperture.value = ap; bokeh.uniforms.maxblur.value = .01;
}
function camFace(C, dist, yaw = 0, dy = 0, fov = 34, look = [0, -.05, 0], ap = .006) {
  C.root.updateMatrixWorld(true); const h = C.head.getWorldPosition(new THREE.Vector3());
  const f = new THREE.Vector3(0, 0, 1).applyQuaternion(C.root.getWorldQuaternion(new THREE.Quaternion())); f.y = 0; f.normalize(); f.applyAxisAngle(new THREE.Vector3(0, 1, 0), yaw);
  const at = h.clone().add(v3(look)); camSet(h.clone().addScaledVector(f, dist).add(v3([0, dy, 0])).toArray(), at.toArray(), fov, h.toArray(), ap);
}
let prev = null;
function useSet(k) {
  const S = SETS[k]; if (prev !== k) { [A.root, T.root].forEach(r => r.parent && r.parent.remove(r)); prev = k; }
  rp.scene = S.scene; bokeh.scene = S.scene; return S;
}

// ======================= SHOTS =======================
const shots = [];
const shot = (d, fn) => { const s = shots.length ? shots[shots.length - 1].end : 0; shots.push({ start: s, end: s + d, fn }); };

// ---------------- 1. BEDROOM ----------------
const caseP = [0, .78, -.48];
function bedBase(S, t) {
  S.scene.add(A.root); reset(A); pose(A, { pos: [0, 0, -.98], legs: false, lean: .12 });
  const P = S.props; P.case.userData.setOpen(1); P.case.position.set(...caseP);
  P.book.position.set(.3, .8, -.62); P.book.rotation.set(0, -.25, 0); P.sand.position.set(-.3, .79, -.62); P.sand.rotation.set(0, .3, 0); P.duck.position.set(-.48, .78, -.58); P.duck.rotation.set(0, .5, 0); P.duck.scale.setScalar(1);
  [P.book, P.sand, P.duck].forEach(p => p.visible = true); P.case.userData.latches.forEach(l => l.position.y = .09);
}
// 1a hook: looks up at the banner, deep breath
shot(2.6, (t, S) => {
  bedBase(S, t);
  const br = Math.sin(seg(t, .6, 2.0) * Math.PI);
  pose(A, { hip: [0, .76 + br * .015, 0], head: [K(t, [[0, -.32], [1.7, -.32], [2.3, 0]]), 0, 0], hands: [[-.22, .8, .32], [.22, .8, .32]], hp: [{ curl: .2 }, { curl: .2 }],
    face: lidsBlink(Object.assign({}, mix(X.proud, X.nervous, seg(t, 1.6, 2.3)), { ly: K(t, [[0, .8], [1.7, .8], [2.3, 0]]) }), t, [1.2]) });
  camSet(K(t, [[0, [0, 1.62, 3.0]], [2.6, [0, 1.58, 2.6], 'lin']]), [0, 1.62, -1], 36, [0, 1.5, -.9], .003);
});
// 1b packing: book (showing cover) + sandwich
shot(3.4, (t, S) => {
  bedBase(S, t); const P = S.props;
  // book path (world)
  const bk = K(t, [[0, [.3, .8, -.62]], [.5, [.3, .8, -.62]], [1.2, [.14, 1.08, -.5]], [1.7, [.14, 1.08, -.5]], [2.2, [.02, .84, -.5]]]);
  P.book.position.set(...bk); P.book.rotation.set(K(t, [[.5, 0], [1.2, 1.25], [1.7, 1.25], [2.2, 0]]), K(t, [[.5, -.25], [1.2, 0], [2.2, 0]]), 0);
  const sw = K(t, [[1.9, [-.3, .79, -.62]], [2.6, [-.12, .98, -.52]], [3.1, [-.12, .87, -.46]]]);
  P.sand.position.set(...sw);
  const hL = t < .5 ? lerp3([.22, .8, .32].map((v, i) => v), [0, 0, 0], 0) : null;
  pose(A, { lean: .3 + Math.sin(seg(t, .3, 2.2) * Math.PI) * .1, hands: [[-.22, .8, .32], [.22, .8, .32]] });
  const bookHand = [bk[0] + .1, bk[1] - .02, bk[2] - .02];
  const lH = t < .5 ? lerp3([.22, .82, -.66], bookHand, ease.io(seg(t, 0, .5))) : t < 2.2 ? bookHand : lerp3(bookHand, [.25, .82, -.66], ease.io(seg(t, 2.2, 2.7)));
  const sH = [sw[0] - .02, sw[1] + .04, sw[2] - .04];
  const rH = t < 1.9 ? lerp3([-.22, .82, -.66], [-.3, .84, -.66], seg(t, 1.4, 1.9)) : t < 3.1 ? sH : lerp3(sH, [-.22, .9, -.6], seg(t, 3.1, 3.4));
  pose(A, { handsW: [rH, lH], hp: [{ curl: t > 1.9 && t < 3.1 ? .7 : .3 }, { curl: t > .5 && t < 2.2 ? .75 : .3 }],
    head: [.42, K(t, [[0, .15], [1.5, .1], [2.0, -.15], [3.4, -.1]]), 0],
    face: lidsBlink(Object.assign(mix(X.proud, X.blank, seg(t, 1.8, 2.2)), { lx: K(t, [[0, .5], [1.6, .3], [2.0, -.4]]), ly: -.6 }), t, [1.8]) });
  camSet(K(t, [[0, [.32, 1.38, .5]], [3.4, [.26, 1.34, .38], 'lin']]), [.02, 1.0, -.6], 38, [.08, 1.0, -.55], .005);
});
// 1c rubber duck: squeeze, think, pack it anyway
shot(2.6, (t, S) => {
  bedBase(S, t); const P = S.props; P.book.visible = P.sand.visible = false;
  const dk = K(t, [[0, [-.48, .78, -.58]], [.15, [-.48, .78, -.58]], [.8, [-.16, 1.24, -.6]], [1.9, [-.16, 1.24, -.6]], [2.4, [-.02, .86, -.5]]]);
  P.duck.position.set(...dk); P.duck.rotation.set(0, K(t, [[.15, .5], [.8, -.3]]), 0);
  const sq = Math.sin(seg(t, 1.0, 1.25) * Math.PI); P.duck.scale.set(1 + sq * .15, 1 - sq * .25, 1);
  pose(A, { lean: .2, head: [K(t, [[0, .35], [.8, .05], [1.9, .05], [2.4, .35]]), K(t, [[0, .2], [.8, .05]]), K(t, [[1.3, 0], [1.6, .14], [1.9, 0]])],
    handsW: [[dk[0] - .015, dk[1] + .02, dk[2] - .06], [.24, .82, -.66]], hp: [{ curl: .8 + sq * .2 }, { curl: .3 }],
    face: lidsBlink(Object.assign(t < 1.0 ? Object.assign({}, X.blank, { lx: .2, ly: -.4 }) : t < 1.35 ? Object.assign({}, X.shock, { open: .3, lx: .2, ly: -.2 }) : t < 1.95 ? Object.assign({}, X.think, { lx: .5, ly: .5 }) : Object.assign({}, X.proud, { ly: -.6 })), t, [.6]) });
  camSet([-.2, 1.45, .3], [-.12, 1.28, -.8], 38, [-.14, 1.3, -.7], .006);
});
// 1d close the case, thumbs up to the mirror (camera)
shot(2.8, (t, S) => {
  bedBase(S, t); const P = S.props; P.book.visible = P.sand.visible = P.duck.visible = false;
  const op = K(t, [[0, 1], [.7, 0, 'in']]); P.case.userData.setOpen(op); P.case.position.y = caseP[1] - (t > .7 && t < .85 ? .006 : 0);
  P.case.userData.latches.forEach((l, i) => { l.position.y = .09 - (t > .9 + i * .2 && t < 1.0 + i * .2 ? .008 : 0); });
  const lidY = .78 + .1 + Math.sin(op * 1.95) * .3, lidZ = -.65 + Math.cos(op * 1.95) * .3 + .02;
  const up = seg(t, 1.3, 1.7);
  pose(A, { lean: lerp(.3, 0, up), hip: [0, .76 + up * .01, 0],
    handsW: t < 1.3 ? [[-.15, lidY + .05, lidZ], [.15, lidY + .05, lidZ]] : null,
    head: [lerp(.4, .02, up), 0, Math.sin(t * 30) * .006 * up], hp: [{ curl: .25 }, { curl: .25 }],
    face: lidsBlink(Object.assign(mix(Object.assign({}, X.blank, { ly: -.6 }), X.grin, up), { sweat: seg(t, 1.9, 2.2), sweatSlide: seg(t, 2.1, 2.8), mw: .09 }), t, [2.45]) });
  if (t >= 1.3) {
    pose(A, { hands: [lerp3([-.18, .9, .3], [-.3, 1.36, .36], ease.back(seg(t, 1.3, 1.75))), [.22, .82, .3]], hp: [{ curl: 1, thumbZ: 2.7 }, { curl: .3 }], hr: [[0, 0, Math.sin(t * 40) * .05], null] });
  }
  camSet(K(t, [[0, [0, 1.3, .9]], [1.3, [0, 1.3, .9]], [1.35, [0, 1.52, 1.25]], [2.8, [0, 1.52, 1.05], 'lin']]), t < 1.3 ? [0, .95, -.6] : [0, 1.42, -.9], t < 1.3 ? 36 : 34, t < 1.3 ? caseP : [0, 1.5, -.95], .005);
});

// ---------------- 2-6. CAFE ----------------
const cupHome = [-.3, .76, -.62], cakeHome = [.12, .762, -.45];
function cafeBase(S, t) {
  S.scene.add(A.root, T.root); reset(A); reset(T); const P = S.props;
  P.cup.position.set(...cupHome); P.cup.userData.cup.position.set(0, .012, 0); P.cup.userData.cup.rotation.set(0, 0, 0); P.cup.userData.powder.visible = false;
  P.cake.position.set(...cakeHome); P.cake.userData.slice.scale.set(1, 1, 1); P.cake.userData.slice.position.set(0, .006, 0);
  P.plant.position.set(-.74, 0, -1.4); P.plant.scale.setScalar(1);
  P.chair.position.set(0, 0, -1.02);
  P.fork.position.set(.24, .762, -.42); P.fork.rotation.set(0, .3, 0);
  P.bottle.parent || S.scene.add(P.bottle); P.bottle.visible = false; P.paper.parent || S.scene.add(P.paper); P.paper.visible = false;
  seated(T, { elbow: [[-1, -1, .2], [1, -1, .2]], pos: [0, 0, -1.0], hands: [[-.17, .74, .3], [.26, .82, .38]], hp: [{ curl: .6 }, { curl: .6 }], legs: true });
}
// Tony eats cake with eyes closed in bliss (fork in his left hand = +x)
function tonyEats(S, t, phase = 0) {
  const P = S.props; const c = ((t + phase) % 2.4) / 2.4; // cycle: plate -> mouth -> chew
  const up = c < .35 ? ease.io(c / .35) : c < .55 ? 1 : 1 - ease.io((c - .55) / .3);
  const plate = [cakeHome[0] + .02, .8, cakeHome[2] + .02], mouth = [.06, 1.42, -.76];
  const fp = lerp3(plate, mouth, up); P.fork.position.set(...fp); P.fork.rotation.set(-up * .9, .5, 0);
  pose(T, { handsW: [null, [fp[0] + .04, fp[1] - .02, fp[2] - .05]], hp: [null, { curl: .8 }] });
  const chew = c > .5 && c < .95 ? Math.abs(Math.sin((c - .5) * 28)) : 0;
  pose(T, { face: { lid: [1, 1], curve: .55 - chew * .3, open: up > .8 && c < .5 ? .5 : chew * .15, brow: [.5, .5], browA: [-.3, -.3], mw: .07 }, head: [-.05 + up * -.08, 0, Math.sin(t * 2) * .04] });
}
// 2a establishing: Rookie "hiding" behind a tiny plant, behind Tony's back
const hideP = [-1.15, 0, -1.62], hideRy = 1.07;
shot(3.2, (t, S) => {
  cafeBase(S, t); tonyEats(S, t);
  const peek = K(t, [[0, 0], [.6, 0], [1.1, 1], [2.6, 1], [2.9, .6]]);
  crouch(A, 1 - peek * .3, { pos: hideP, ry: hideRy, head: [0, K(t, [[0, 0], [1.6, 0], [2.0, -.6], [2.6, -.6], [2.9, 0]]), 0], hands: [[-.14, .86, .3], [.14, .86, .3]], hp: [{ curl: .5 }, { curl: .5 }],
    face: lidsBlink(Object.assign({}, X.nervous, { lx: K(t, [[1.6, 0], [2.0, .9], [2.6, .9], [2.9, 0]]), ly: -.1 }), t, [1.3]) });
  camSet(K(t, [[0, [-.4, 1.4, 2.5]], [3.2, [-.42, 1.38, 2.3], 'lin']]), [-.55, 1.08, -1.0], 44, [-1.0, 1.0, -1.5], .003);
});
// 2b newspaper with eye holes
shot(3.3, (t, S) => {
  cafeBase(S, t); tonyEats(S, t, 1.2); const P = S.props; P.paper.visible = true;
  const raise = K(t, [[0, 0], [1.7, 0], [2.0, .06]]);
  pose(A, { pos: hideP, ry: .75, legs: false, head: [0, 0, 0] });
  A.root.updateMatrixWorld(true);
  const pp = A.root.localToWorld(v3([0, 1.755 + raise, .3])); P.paper.position.copy(pp); P.paper.rotation.set(0, A.root.rotation.y, 0);
  pose(A, { hands: [[-.23, 1.62 + raise, .27], [.23, 1.62 + raise, .27]], hp: [{ curl: .5 }, { curl: .5 }], elbow: [[-1, -1, 0], [1, -1, 0]],
    face: Object.assign({}, X.nervous, { lx: K(t, [[0, -.8], [.5, .9], [1.0, -.8], [1.5, .9], [1.7, .2]]), ly: 0, lid: [0, 0], brow: [1, 1] }) });
  if (t > 1.7) pose(A, { head: [0, 0, 0] });
  camFace(A, K(t, [[0, 1.45], [3.3, 1.3], 'lin']), 0, .1, 34, [0, .12, 0], .006);
  bokeh.uniforms.focus.value = cam.position.distanceTo(pp);
});
// 3a tiptoe behind Tony
shot(3.6, (t, S) => {
  cafeBase(S, t); tonyEats(S, t, .4);
  const path = [[hideP[0], hideP[2]], [-.9, -1.58], [-.62, -1.48]]; const u = seg(t, .2, 3.4);
  const pos = u < .5 ? lerp3(path[0], path[1], u * 2) : lerp3(path[1], path[2], (u - .5) * 2);
  const step = (u * 8) % 1, sL = Math.floor(u * 8) % 2;
  const lift = Math.sin(step * Math.PI);
  pose(A, { pos: [pos[0], 0, pos[1]], ry: K(t, [[0, 1.3], [3.4, 1.0]]), hip: [0, .78 + lift * .04, 0], lean: .05,
    feet: [[-.12, .05 + (sL ? 0 : lift * .14), .02 + (sL ? -.05 : .1 * lift)], [.12, .05 + (sL ? lift * .14 : 0), .02 + (sL ? .1 * lift : -.05)]], pitch: [.5, .5],
    hands: [[-.3, 1.32, .12], [.3, 1.32, .12]], hp: [{ curl: .1, spread: .2 }, { curl: .1, spread: .2 }], elbow: [[-1, -.5, 0], [1, -.5, 0]],
    head: [0, K(t, [[0, -.5], [3.4, .1]]), 0], face: Object.assign({}, X.nervous, { open: .15, lx: K(t, [[0, -.9], [3.4, -.3]]) }) });
  camSet(K(t, [[0, [-.3, 1.35, 2.0]], [3.6, [-.3, 1.35, 1.8], 'lin']]), [-.45, 1.1, -1.0], 38, [-.8, 1.2, -1.5], .003);
});
// 3b Tony turns: Rookie freezes into a "statue"
shot(3.4, (t, S) => {
  cafeBase(S, t); const P = S.props; P.fork.position.set(.2, .78, -.48);
  const turn = K(t, [[0, 0], [.35, 1, 'out'], [2.3, 1], [2.8, 0]]);
  pose(T, { head: [0, -1.25 * turn, 0], twist: -.2 * turn, face: { lid: [K(t, [[.4, .2], [.9, .6], [2.3, .6], [2.6, .35]]), K(t, [[.4, .2], [.9, .6], [2.3, .6], [2.6, .35]])], brow: [K(t, [[.5, 0], [.9, -.6]]), K(t, [[.5, 0], [.9, .3]])], browA: [.4, -.2], curve: -.1, lx: -.6 } });
  const froz = t > .35;
  pose(A, { pos: [-.6, 0, -1.45], ry: 1.4, hip: [0, .78, 0], feet: [[-.12, .05, .02], [.14, froz ? .28 : .1, froz ? .12 : .05]], pitch: [.5, .2], knee: [[0, 0, 1], [.4, .3, 1]],
    hands: froz ? [[-.38, 1.62, .0], [.32, 1.75, .08]] : [[-.3, 1.32, .12], [.3, 1.32, .12]], hp: froz ? [{ curl: .0, spread: .3 }, { curl: .0, spread: .3 }] : [{ curl: .1 }, { curl: .1 }],
    elbow: [[-1, 0, 0], [1, 0, 0]], head: [-.1, 0, froz ? .25 : 0],
    face: froz ? Object.assign({}, X.grin, { lid: [0, 0], lx: K(t, [[.4, 0], [1.2, -.6], [2.2, -.6]]), sweat: seg(t, 1.0, 1.6), sweatSlide: seg(t, 1.6, 3.2), open: .2 }) : Object.assign({}, X.nervous, { lx: .7 }) });
  if (t > 2.8) pose(A, { face: Object.assign({}, X.nervous, { open: .4, mw: .05, curve: 0, brow: [.8, .8], sweat: 1, sweatSlide: 1 }) });
  camSet(K(t, [[0, [-.25, 1.45, 1.25]], [3.4, [-.27, 1.45, 1.1], 'lin']]), [-.35, 1.3, -1.1], 36, [-.55, 1.5, -1.45], .004);
});
// 4a poison into the espresso
shot(3.2, (t, S) => {
  cafeBase(S, t); tonyEats(S, t, .8); const P = S.props; P.bottle.visible = true;
  pose(A, { pos: [-.55, 0, -1.2], ry: .3, lean: .42, legs: false });
  A.root.updateMatrixWorld(true);
  const tilt = K(t, [[0, 0], [.6, 0], [1.0, 2.1], [2.4, 2.1], [2.8, 0]]);
  const bp = K(t, [[0, [-.45, 1.0, -.8]], [.6, [-.33, .9, -.66]]]);
  P.bottle.position.set(...bp); P.bottle.rotation.set(0, 0, -tilt); P.bottle.userData.cork.visible = false;
  P.cup.userData.powder.visible = t > 1.2; const pw = seg(t, 1.2, 2.4); P.cup.userData.powder.scale.set(.012 + pw * .015, .004 + pw * .004, .012 + pw * .015);
  pose(A, { handsW: [[-.6, .92, -.9], [bp[0] - .02, bp[1] + .17, bp[2] - .06]], hp: [{ curl: .3 }, { curl: .9 }] });
  pose(A, { face: Object.assign({}, X.nervous, { ly: -.7, lx: .3 }), head: [.4, .2, 0] });
  camSet([.12, 1.12, -.02], [-.32, .86, -.66], 34, [-.3, .82, -.62], .007);
});
// 4b stirring with his finger; finger comes out covered in powder
shot(2.8, (t, S) => {
  cafeBase(S, t); tonyEats(S, t, 1.4); const P = S.props; P.cup.userData.powder.visible = t < .9;
  pose(A, { pos: [-.55, 0, -1.2], ry: .3, lean: K(t, [[0, .42], [1.3, .42], [1.8, .15]]), legs: false });
  A.root.updateMatrixWorld(true);
  const stir = t < 1.3 ? [cupHome[0] + Math.cos(t * 14) * .015, .82 + (t < .2 ? (.2 - t) * .5 : 0), cupHome[2] + Math.sin(t * 14) * .015] : null;
  const look = A.root.localToWorld(v3([.0, 1.35, .32])).toArray();
  const fin = stir ?? lerp3([cupHome[0], .86, cupHome[2]], look, ease.io(seg(t, 1.3, 1.9)));
  pose(A, { handsW: [[-.6, .95, -.9], [fin[0], fin[1] + .05, fin[2] - .03]], hp: [{ curl: .3 }, { curl: 1, point: true, thumbZ: 1.6 }], hr: [null, stir ? [0, 0, Math.PI] : [0, -.5, Math.PI + .6]] });
  A.arm[1].hand.userData.tip.visible = t > 1.2;
  const looking = t > 1.9;
  pose(A, { head: [lerp(.45, .05, seg(t, 1.3, 1.9)), lerp(.25, .1, seg(t, 1.3, 1.9)), 0], face: looking ? Object.assign({}, X.shock, { lx: .3, ly: -.1, open: .25, mw: .045, cross: seg(t, 2.0, 2.4) * .35 }) : Object.assign({}, X.nervous, { ly: -.7, lx: .3 }) });
  if (t < 1.3) camSet([.12, 1.12, -.02], [-.32, .86, -.66], 34, [-.3, .82, -.62], .007); else camFace(A, 1.1, .2, -.12, 34, [0, -.12, 0]);
});
// 5. the lick
shot(7.0, (t, S) => {
  cafeBase(S, t); tonyEats(S, t, 2.0);
  pose(A, { pos: [-.55, 0, -1.2], ry: .3, lean: .1, legs: false });
  A.root.updateMatrixWorld(true);
  // 0-1.6 panic glance, 1.6-3.6 lick each finger, 3.6-4.6 proud, 4.6-5.4 pause, 5.4-7 poison kicks in
  const lick = seg(t, 1.6, 3.6), cyc = (lick * 3) % 1, licking = t > 1.6 && t < 3.6;
  const mouthP = [0, 1.52 - .1, .2];
  const hand = t < 1.6 ? [.0, 1.3, .3] : licking ? [mouthP[0] + .01, mouthP[1] - .06 - Math.sin(cyc * Math.PI) * .04, mouthP[2] + .1] : lerp3([.01, 1.33, .3], [.24, .86, .1], seg(t, 3.6, 4.0));
  pose(A, { hands: [[-.22, .9, .15], hand], hp: [{ curl: .3 }, { curl: licking ? .6 : 1, point: true, thumbZ: 1.6 }], hr: [null, licking ? [0, 0, Math.PI - .1] : [0, -.5, Math.PI + .6]] });
  A.arm[1].hand.userData.tip.visible = t < 1.6 + .6;
  let F;
  if (t < 1.6) F = Object.assign({}, X.nervous, { lx: K(t, [[0, .3], [.3, -1], [.7, -1], [.9, 1], [1.3, 1], [1.5, .2]]), ly: K(t, [[0, -.2], [1.5, -.4]]) });
  else if (licking) F = Object.assign({}, X.blank, { open: .45 + Math.sin(cyc * Math.PI) * .1, mw: .05, tongue: Math.sin(cyc * Math.PI), lid: [.5, .5], ly: -.6, brow: [.3, .3] });
  else if (t < 4.6) F = Object.assign({}, X.proud, { curve: .9, lid: [.55, .55], mw: .085 });
  else if (t < 5.4) F = Object.assign({}, X.proud, { curve: .9, mw: .085, lid: [0, 0], brow: [.7, .7] });
  else { const k = seg(t, 5.4, 6.4); F = Object.assign({}, X.blank, { cross: k * .9, lid: [k * .35, k * .15], open: k * .5, mw: .05, wob: k, brow: [lerp(.7, 1.2, k), lerp(.7, -.3, k)], browA: [k * -.4, k * .4], tongue: k > .7 ? (k - .7) * 1.5 : 0 }); }
  pose(A, { face: F, head: [t > 5.4 ? Math.sin(t * 7) * .05 : -.03, licking ? 0 : t < 1.6 ? K(t, [[0, 0], [.3, -.3], [.7, -.3], [.9, .3], [1.3, .3], [1.5, 0]]) : 0, t > 5.4 ? Math.sin(t * 5) * .15 * seg(t, 5.4, 6.4) : 0] });
  camFace(A, K(t, [[0, 1.15], [7, .95], 'lin']), .2, .05, 34, [0, -.1, 0]);
});
// 6a stiff fall face-first into the cake; 6b Tony's reaction
const fallX = -1.2;
shot(3.0, (t, S) => {
  cafeBase(S, t); const P = S.props;
  const f = K(t, [[0, 0], [.7, 0], [1.25, 1, 'in']]), bounce = t > 1.25 ? Math.sin(seg(t, 1.25, 1.55) * Math.PI) * .04 : 0;
  const ang = f * .98 - bounce;
  pose(A, { pos: [fallX, 0, -.45], rootRot: [Math.PI / 2, 0, 0], legs: true, hands: [[-.24, .74, .02], [.24, .74, .02]], hp: [{ curl: .1 }, { curl: .1 }] });
  A.root.rotation.set(0, Math.PI / 2, 0); A.root.rotateX(ang);
  pose(A, { face: Object.assign({}, X.blank, { cross: .9, lid: [.35, .15], open: .5, mw: .05, wob: 1, brow: [1.2, -.3], browA: [-.4, .4], tongue: .45 }), head: [0, 0, Math.sin(t * 6) * .12 * (1 - f)] });
  const squash = t > 1.25 ? 1 : 0; P.cake.userData.slice.scale.set(1 + squash * .5, 1 - squash * .6, 1 + squash * .5);
  // Tony lifts the cup to sip, freezes on impact
  const lift = K(t, [[0, 0], [.6, 1]]); const cp = lerp3(cupHome, [-.12, 1.22, -.7], lift);
  P.cup.userData.cup.position.set(cp[0] - cupHome[0], cp[1] - cupHome[1] + .012, cp[2] - cupHome[2]);
  pose(T, { handsW: [[cp[0] + .06, cp[1] + .02, cp[2] - .02], null], hp: [{ curl: .8 }, null], face: { lid: t < 1.25 ? [.6, .6] : [0, 0], brow: t < 1.25 ? [.2, .2] : [1, 1], curve: t < 1.25 ? .3 : 0, open: t < 1.25 ? .15 : .3, lx: t < 1.25 ? 0 : -.6, ly: t < 1.25 ? 0 : -.8 } });
  camSet(K(t, [[0, [-.5, 1.35, 2.4]], [3, [-.5, 1.3, 2.25], 'lin']]), [-.55, 1.0, -.6], 46, [-.5, .9, -.5], .003);
});
shot(4.2, (t, S) => {
  cafeBase(S, t); const P = S.props;
  pose(A, { pos: [fallX, 0, -.45], legs: true, hands: [[-.24, .74, .02], [.24, .74, .02]] }); A.root.rotation.set(0, Math.PI / 2, 0); A.root.rotateX(.98);
  pose(A, { face: Object.assign({}, X.blank, { lid: [1, 1], open: .4, mw: .05 }) });
  P.cake.userData.slice.scale.set(1.5, .4, 1.5);
  // look down at Rookie, look at cup, put it down, push it away
  const down = K(t, [[0, 1], [1.6, 1], [2.4, 0]]), push = K(t, [[2.4, 0], [3.4, 1]]);
  const cp = down > 0 ? lerp3([-.18, .8, -.66], [-.12, 1.22, -.7], down) : lerp3([-.18, .76, -.66], [-.02, .76, -.36], push);
  P.cup.position.set(cp[0], cp[1] - .012, cp[2]); P.cup.userData.cup.position.set(0, .012, 0);
  pose(T, { handsW: [[cp[0] + .07, cp[1] + .04, cp[2] - .03], null], hp: [{ curl: .8 }, null],
    head: [K(t, [[0, .35], [.8, .35], [1.1, .05], [2.6, .05], [3.0, .2]]), K(t, [[0, -.3], [.8, -.3], [1.1, -.1]]), 0],
    face: { lid: [0, 0], brow: [K(t, [[0, 1], [1.0, .2]]), K(t, [[0, 1], [1.0, 1.1]])], browA: [.2, -.3], curve: -.2, open: K(t, [[0, .3], [.6, 0]]), lx: K(t, [[0, -.6], [.8, -.6], [1.1, 0]]), ly: K(t, [[0, -.9], [.8, -.9], [1.1, -.1], [2.6, -.6]]) } });
  camSet(K(t, [[0, [.95, 1.75, .3]], [4.2, [.9, 1.73, .18], 'lin']]), [-.1, 1.12, -.85], 40, [0, 1.3, -1.0], .005);
});

// ---------------- 7-8. HOSPITAL ----------------
function hospBase(S, t) {
  S.scene.add(A.root, T.root); reset(A); reset(T); const P = S.props;
  pose(A, { pos: [-.12, 0, -1.28], hip: [0, .7, 0], lean: -.42, legs: false, hands: [[-.26, .74, .38], [.26, .74, .38]], hp: [{ curl: .3 }, { curl: .3 }] });
  seated(T, { elbow: [[-1, -1, .2], [1, -1, .2]], pos: [.9, 0, -1.0], ry: -1.3, hands: [[-.17, .74, .3], [.17, .74, .3]], hp: [{ curl: .6 }, { curl: .6 }] });
  P.cup.position.set(.25, 1.015, -.67); P.tray.position.z = -.65; extras.band.visible = extras.cream.visible = true;
}
// 7. hospital: Tony visits, slides THE espresso over, winks
shot(8.0, (t, S) => {
  hospBase(S, t); const P = S.props; S.ecg(t, 72, false);
  const slide = K(t, [[2.6, 0], [4.0, 1]]); const cp = lerp3([.25, 1.015, -.67], [-.02, 1.015, -.69], slide);
  P.cup.position.set(...cp);
  pose(T, { lean: K(t, [[2.2, 0], [2.8, .35], [4.0, .35], [4.6, 0]]), handsW: [slide > 0 && t < 4.3 ? [cp[0] + .06, cp[1] + .05, cp[2]] : null, null], hp: [{ curl: .6 }, null],
    head: [0, K(t, [[0, -.3], [4.6, -.3], [5.0, .55]]), 0],
    face: { lid: [t > 5.4 && t < 6.2 ? 1 : .35, .35], brow: [t > 5.4 && t < 6.2 ? -.3 : .2, .6], curve: K(t, [[4.6, .1], [5.4, .7]]), mw: .085, lx: K(t, [[0, -.6], [4.6, -.6], [5.0, .1]]) } });
  pose(A, { head: [K(t, [[0, .1], [1.0, .1], [1.4, 0]]), K(t, [[0, 0], [1.4, .25]]), .1], face: lidsBlink(Object.assign({}, X.blank, { lid: [K(t, [[0, .8], [1.2, .5]]), K(t, [[0, .8], [1.2, .5]])], lx: K(t, [[1.4, .6], [3.0, .4], [4.0, -.3]]), ly: K(t, [[3.0, -.2], [4.0, -.7], [5.0, -.1]]), curve: -.1, brow: [.3, .3] }), t, [2.2, 6.8]) });
  camSet(K(t, [[0, [.62, 1.55, 2.5]], [8, [.6, 1.52, 2.2], 'lin']]), [.42, 1.15, -.8], 44, [.4, 1.2, -1.1], .003);
});
// 8. pushes it back; Tony drinks it all and is totally fine; Rookie faints
shot(8.0, (t, S) => {
  hospBase(S, t); const P = S.props;
  const faint = t > 6.0; S.ecg(t, faint && t < 6.9 ? 160 : 72 + seg(t, 0, 2) * 60 - (t > 6.9 ? 60 : 0), faint && t > 6.25 && t < 6.9);
  // 0-2 sweat + push back, 2-4 Tony drinks, 4-6 Rookie stares, 6+ faint
  const back = K(t, [[.8, 0], [2.0, 1]]); const cp = lerp3([-.02, 1.015, -.69], [.25, 1.015, -.67], back);
  const drink = K(t, [[2.2, 0], [2.7, 1], [3.6, 1], [4.0, 0]]); const sip = seg(t, 2.7, 3.6);
  const cup = drink > 0 ? lerp3(cp, [.62, 1.42, -.42], drink) : cp; P.cup.position.set(cp[0], cp[1], cp[2]);
  P.cup.userData.cup.position.set(cup[0] - cp[0], cup[1] - cp[1] + .012, cup[2] - cp[2]); P.cup.userData.cup.rotation.set(0, 0, drink * sip * 1.6);
  pose(A, { hands: [[-.26, .74, .38], back > 0 && back < 1 ? null : [.26, .74, .38]], hp: [{ curl: .3 }, { curl: 1, point: true, thumbZ: 1.6 }] });
  if (t > .5 && t < 2.2) pose(A, { handsW: [null, [cp[0] - .06, cp[1] + .04, cp[2] + .02]], hr: [null, [0, -1.6, Math.PI / 2]] });
  pose(T, { lean: K(t, [[1.6, 0], [2.2, .25], [4.0, .25], [4.4, 0]]), handsW: [drink > 0 ? [cup[0] + .05, cup[1] + .03, cup[2] - .02] : null, null], hp: [{ curl: .8 }, null],
    head: [K(t, [[2.6, 0], [3.0, -.45], [3.6, -.45], [3.9, 0]]), K(t, [[0, .55], [4.0, .45]]), 0],
    face: { lid: [t > 2.8 && t < 3.6 ? 1 : .35, t > 2.8 && t < 3.6 ? 1 : .35], curve: t > 3.9 ? .8 : .2, open: t > 2.8 && t < 3.6 ? .3 : 0, brow: [.4, .4], mw: .09, lx: .2 } });
  let F;
  if (t < 2.2) F = Object.assign({}, X.nervous, { ly: -.7, lx: -.2, sweat: seg(t, 0, .8) * 1.1, sweatSlide: seg(t, .8, 2.4), mw: .05, lid: [0, 0] });
  else if (t < 4.0) F = Object.assign({}, X.shock, { lx: .8, ly: .15, sweat: 1.1, sweatSlide: 1, open: K(t, [[2.6, .2], [3.4, .7]]) });
  else if (t < 6.0) F = Object.assign({}, X.grin, { lx: .7, ly: .1, sweat: 1.1, sweatSlide: 1, brow: [1.2, 1.2], lid: [0, 0], wob: 1.4 });
  else F = Object.assign({}, X.blank, { lid: [lerp(0, 1, seg(t, 6.0, 6.3)), lerp(0, 1, seg(t, 6.0, 6.3))], open: .5, tongue: .5, mw: .05, sweat: 1.1, sweatSlide: 1, brow: [1, 1] });
  pose(A, { face: F, head: t < 6 ? [K(t, [[0, .1], [2.2, .2], [2.6, 0]]), K(t, [[0, 0], [2.2, .1], [2.6, .45]]), .1] : [K(t, [[6.0, 0], [6.3, -.5, 'in']]), .2, .4], lean: t < 6 ? -.42 : K(t, [[6.0, -.42], [6.3, -.6, 'in']]) });
  const cm = t < 2.2 ? 0 : t < 4.2 ? 1 : t < 6.0 ? 0 : 2;
  if (cm === 0) camSet(K(t, [[0, [.05, 1.5, .15]], [6, [.04, 1.48, .05], 'lin']]), [-.05, 1.2, -1.0], 36, [-.12, 1.4, -1.1], .005);
  else if (cm === 1) camFace(T, 1.75, .35, 0, 34, [-.05, -.25, 0]);
  else camSet(K(t, [[6, [.5, 1.5, 1.9]], [8, [.5, 1.48, 1.7], 'lin']]), [.35, 1.15, -.8], 42, [-.1, 1.2, -1.2], .004);
});

export const DURATION = shots[shots.length - 1].end;
let frameNo = 0;
window.R = (t) => {
  const s = shots.find(x => t >= x.start && t < x.end) ?? shots[shots.length - 1];
  const which = s.fn.toString().includes('bedBase') ? 'bed' : s.fn.toString().includes('hospBase') ? 'hosp' : 'cafe';
  const S = useSet(which); s.fn(t - s.start, S);
  // stop-motion "boil": tiny random nudges per frame
  const r = rng(Math.floor(t * 12) + 1); [A, T].forEach(C => { C.root.position.x += (r() - .5) * .002; C.root.position.z += (r() - .5) * .002; C.head.rotation.z += (r() - .5) * .006; });
  A.setFace(A.face); T.setFace(T.face); A.solve(); T.solve(); S.update(t);
  composer.render(); frameNo++;
};
window.DURATION = DURATION; window.SHOTS = shots.map(s => [s.start, s.end]);
window.ready = 1;
