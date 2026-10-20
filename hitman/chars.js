// Clay characters with a simple rig: hips/torso/head hierarchy, IK arms and legs, animatable face.
import * as THREE from 'three';
import { clay, mesh, lumpy, sphereG, capsuleG, paintTex, lerp } from './lib.js';

const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const UP = V(0, 1, 0);

// 2-bone IK in a common space. returns elbow/knee position.
function ik2(S, T, a, b, pole) {
  const d = T.clone().sub(S); let L = d.length(); const dir = d.normalize();
  L = Math.min(L, (a + b) * .999); T.copy(S).addScaledVector(dir, L);
  const cosA = (a * a + L * L - b * b) / (2 * a * L), sinA = Math.sqrt(Math.max(0, 1 - cosA * cosA));
  const perp = pole.clone().sub(dir.clone().multiplyScalar(pole.dot(dir))).normalize();
  return S.clone().addScaledVector(dir, a * cosA).addScaledVector(perp, a * sinA);
}
function placeSeg(m, P, Q) { // capsule along local Y from P to Q
  m.position.copy(P).add(Q).multiplyScalar(.5);
  m.quaternion.setFromUnitVectors(UP, Q.clone().sub(P).normalize());
}

function makeHand(skin) {
  const g = new THREE.Group(), fingers = [];
  const palm = mesh(lumpy(sphereG(1, 24, 18), .04, 3, 5), skin); palm.scale.set(.046, .052, .024); g.add(palm);
  for (let i = 0; i < 4; i++) {
    const piv = new THREE.Group(); piv.position.set(-.03 + i * .02, -.036, 0);
    const f = mesh(capsuleG(.0105, .038 - Math.abs(i - 1.5) * .006, 10), skin); f.position.y = -.022; piv.add(f); g.add(piv); fingers.push(piv);
  }
  const tip = mesh(sphereG(.013, 10, 8), clay(0xf6f6f2, { rough: 1 }), false); tip.position.y = -.042; tip.scale.set(1.1, .8, 1.1); tip.visible = false; fingers[3].add(tip);
  const th = new THREE.Group(); th.position.set(.04, -.005, .01); const tm = mesh(capsuleG(.012, .03, 10), skin); tm.position.y = -.02; th.add(tm); th.rotation.z = .9; g.add(th);
  g.userData = { fingers, thumb: th, tip };
  return g;
}
// pose: curl 0..1 for fingers, thumbUp, point(index straight)
function poseHand(h, p) {
  const { fingers, thumb } = h.userData; const c = p.curl ?? .15;
  fingers.forEach((f, i) => { f.rotation.x = (i === 3 && p.point ? 0 : c) * 1.9 + (p.spread ?? 0) * 0; f.rotation.z = (i - 1.5) * (p.spread ?? .05); });
  if (p.point) fingers[3].rotation.x = 0;
  thumb.rotation.set(p.thumbX ?? 0, 0, p.thumbZ ?? .9);
}

export class Character {
  constructor(o) {
    this.o = o; const S = o.scale ?? 1; this.root = new THREE.Group(); this.root.scale.setScalar(S);
    const skin = clay(o.skin, { rough: .7, rep: 3 }), suit = clay(o.suit, { streak: true, rep: 3, bump: 2, map: o.suitMap }), shirt = clay(0xf0ebe0, { rough: .8 }), tie = clay(o.tie, { rough: .6 }), shoe = clay(0x141214, { rough: .45 });
    this.mats = { skin, suit };
    const hips = this.hips = new THREE.Group(); hips.position.y = o.hipY ?? .76; this.root.add(hips);
    const torso = this.torso = new THREE.Group(); hips.add(torso);
    // torso lathe
    const W = o.width ?? 1, pts = [];
    const prof = o.belly ? [[.0, .2], [.08, .245], [.2, .27], [.32, .255], [.44, .235], [.52, .2], [.57, .12], [.6, .06]] : [[0, .16], [.1, .165], [.22, .18], [.36, .205], [.46, .215], [.52, .19], [.57, .11], [.6, .055]];
    for (const [y, r] of prof) pts.push(new THREE.Vector2(r * W, y));
    const tg = lumpy(new THREE.LatheGeometry(pts, 40), .006, 8, 3); const body = mesh(tg, suit); body.scale.z = o.belly ? .82 : .66; torso.add(body);
    const front = (o.belly ? .27 * .82 : .205 * .66) * W;
    // shirt V + tie + lapels
    const sh = new THREE.Shape(); sh.moveTo(-.075 * W, 0); sh.lineTo(.075 * W, 0); sh.lineTo(0, -.24); sh.closePath();
    const shirtM = mesh(new THREE.ExtrudeGeometry(sh, { depth: .01, bevelEnabled: true, bevelSize: .006, bevelThickness: .006, bevelSegments: 2 }), shirt, false);
    shirtM.position.set(0, .57, front * .62); shirtM.rotation.x = -.42; torso.add(shirtM);
    const tieG = new THREE.Shape(); tieG.moveTo(-.016, 0); tieG.lineTo(.016, 0); tieG.lineTo(.026, -.17); tieG.lineTo(0, -.2); tieG.lineTo(-.026, -.17); tieG.closePath();
    const tieM = mesh(new THREE.ExtrudeGeometry(tieG, { depth: .008, bevelEnabled: true, bevelSize: .004, bevelThickness: .004, bevelSegments: 2 }), tie, false);
    tieM.position.set(0, .555, front * .62 + .028); tieM.rotation.x = -.38; torso.add(tieM);
    const knot = mesh(sphereG(.022, 12, 10), tie); knot.position.set(0, .56, front * .55 + .035); torso.add(knot);
    for (const s of [-1, 1]) {
      const lp = new THREE.Shape(); lp.moveTo(0, 0); lp.lineTo(.03, 0); lp.lineTo(.085, -.25); lp.lineTo(.06, -.26); lp.closePath();
      const lm = mesh(new THREE.ExtrudeGeometry(lp, { depth: .012, bevelEnabled: true, bevelSize: .005, bevelThickness: .005, bevelSegments: 2 }), suit, false);
      lm.position.set(s * .07 * W, .575, front * .6 + .012); lm.scale.x = s; lm.rotation.x = -.38; lm.rotation.z = s * -.08; torso.add(lm);
    }
    const neck = mesh(new THREE.CylinderGeometry(.06, .065, .1, 16), skin); neck.position.y = .62; torso.add(neck);
    const collar = mesh(new THREE.TorusGeometry(.066, .014, 8, 20), shirt); collar.rotation.x = Math.PI / 2 - .2; collar.position.set(0, .6, .005); torso.add(collar);
    this.shoulder = [V(-.2 * W, .49, 0), V(.2 * W, .49, 0)]; this.front = front;
    for (const s of this.shoulder) { const b = mesh(sphereG(.062, 16, 12), suit); b.position.copy(s).multiplyScalar(.93); torso.add(b); }
    // head
    this.neckPiv = new THREE.Group(); this.neckPiv.position.y = .63; torso.add(this.neckPiv);
    const head = this.head = new THREE.Group(); head.position.y = o.headLift ?? .17; this.neckPiv.add(head);
    this.buildFace(skin);
    // limbs (root space)
    this.arm = [0, 1].map(() => ({ up: mesh(capsuleG(.052, .2, 14), suit), lo: mesh(capsuleG(.046, .19, 14), suit), cuff: mesh(new THREE.CylinderGeometry(.046, .046, .025, 14), shirt), hand: makeHand(skin) }));
    this.arm.forEach(a => { a.lo.geometry.translate(0, 0, 0); this.root.add(a.up, a.lo, a.cuff, a.hand); });
    this.leg = [0, 1].map(() => ({ up: mesh(capsuleG(.075, .26, 14), suit), lo: mesh(capsuleG(.066, .26, 14), suit), shoe: mesh(lumpy(sphereG(1, 20, 14), .05, 3, 9), shoe) }));
    this.leg.forEach(l => { l.shoe.scale.set(.065, .05, .13); this.root.add(l.up, l.lo, l.shoe); });
    this.armLen = [.27, .26]; this.legLen = [o.thigh ?? .37, o.shin ?? .37];
    // defaults
    this.handT = [V(-.24, .78, .12), V(.24, .78, .12)]; this.handRot = [null, null]; this.handPose = [{}, {}]; this.handRoll = [0, 0];
    this.footT = [V(-.11, .05, .02), V(.11, .05, .02)]; this.footPitch = [0, 0];
    this.elbowPole = [V(-1, -.4, -.6), V(1, -.4, -.6)]; this.kneePole = [V(0, 0, 1), V(0, 0, 1)];
    this.visibleLegs = true;
  }
  buildFace(skin) {
    const o = this.o, h = this.head, R = o.headR ?? .2, sc = o.headScale ?? [.92, 1.06, .95];
    this.hR = R; this.hS = sc;
    const hm = mesh(lumpy(sphereG(R, 48, 36), .006, 9, o.seed ?? 2), skin); hm.scale.set(...sc); h.add(hm);
    const surf = (x, y, out = 0) => { const sx = x / (R * sc[0]), sy = y / (R * sc[1]); return R * sc[2] * Math.sqrt(Math.max(0, 1 - sx * sx - sy * sy)) + out; };
    this.surf = surf;
    for (const s of [-1, 1]) { const e = mesh(sphereG(.045, 14, 10), skin); e.scale.set(.45, 1, .75); e.position.set(s * R * sc[0] * .97, -.01, -.01); h.add(e); }
    const nose = mesh(lumpy(sphereG(1, 20, 14), .05, 3, 4), skin); const nr = o.nose ?? .036; nose.scale.set(nr * .9, nr * .85, nr * 1.15); nose.position.set(0, -.03, surf(0, -.03) + nr * .4); h.add(nose);
    // eyes
    const white = clay(0xf7f4ee, { rough: .25, bump: .3 }), black = clay(0x0d0b0c, { rough: .15, bump: .2 }), lidM = skin;
    const er = o.eyeR ?? .058, ex = o.eyeX ?? .074, ey = o.eyeY ?? .045;
    this.eyes = [-1, 1].map(s => {
      const g = new THREE.Group(); g.position.set(s * ex, ey, surf(s * ex, ey) - er * .45); h.add(g);
      const w = mesh(sphereG(er, 24, 18), white); w.scale.set(1, 1.08, .85); g.add(w);
      const p = mesh(sphereG(er * (o.pupil ?? .42), 14, 10), black); g.add(p);
      const lid = mesh(new THREE.SphereGeometry(er * 1.1, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), lidM); lid.scale.set(1, 1.08, .9); g.add(lid);
      const lidB = mesh(new THREE.SphereGeometry(er * 1.08, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), lidM); lidB.scale.set(1, 1.08, .9); g.add(lidB);
      return { g, p, lid, lidB, r: er };
    });
    // brows
    const browM = clay(o.browC ?? 0x2a1c14, { streak: true }); const br = o.browR ?? .014;
    this.brows = [-1, 1].map(s => { const g = new THREE.Group(); const m = mesh(capsuleG(br, o.browLen ?? .07, 10), browM); m.rotation.z = Math.PI / 2; g.add(m); h.add(g); g.userData.s = s; return g; });
    this.browBase = ey + er + .028;
    // mouth
    this.mouthG = new THREE.Group(); const my = o.mouthY ?? -.098; this.my = my; this.mouthG.position.set(0, my, surf(0, my)); h.add(this.mouthG);
    this.mouthDark = mesh(new THREE.BufferGeometry(), clay(0x3a1212, { rough: .5, bump: .2 }), false); this.mouthG.add(this.mouthDark);
    this.teethM = mesh(new THREE.BufferGeometry(), clay(0xf6f2e6, { rough: .4, bump: .2 }), false); this.teethM.position.z = .002; this.mouthG.add(this.teethM);
    this.teethLine = mesh(new THREE.BoxGeometry(1, .0035, .002), clay(0x3a1212)); this.teethLine.position.z = .0045; this.mouthG.add(this.teethLine);
    this.tongue = mesh(capsuleG(.022, .03, 12), clay(0xd8606a, { rough: .4 })); this.tongue.rotation.x = Math.PI / 2; this.tongue.scale.set(1, 1, .5); this.mouthG.add(this.tongue);
    // hair
    if (o.hair === 'rookie') {
      const hm2 = clay(0x2b1d15, { streak: true, rep: 2, bump: 2.5 });
      const cap = mesh(lumpy(new THREE.SphereGeometry(R * 1.035, 40, 20, 0, Math.PI * 2, 0, 1.35), .012, 8, 6), hm2); cap.scale.set(...sc); cap.rotation.x = -.62; cap.position.set(0, -.005, -.012); h.add(cap);
      const q = mesh(lumpy(sphereG(1, 24, 16), .08, 3, 8), hm2); q.scale.set(.15, .055, .1); q.position.set(.025, R * sc[1] * .86, .085); q.rotation.set(.55, .2, -.2); h.add(q);
      const q2 = mesh(lumpy(sphereG(1, 20, 14), .08, 3, 3), hm2); q2.scale.set(.09, .045, .07); q2.position.set(-.07, R * sc[1] * .8, .11); q2.rotation.set(.5, -.3, .3); h.add(q2);
      for (const s of [-1, 1]) { const sb = mesh(sphereG(1, 16, 12), hm2); sb.scale.set(.02, .045, .035); sb.position.set(s * R * sc[0] * .96, .06, .03); h.add(sb); }
    }
    if (o.hair === 'tony') {
      const hm2 = clay(0x77726c, { streak: true, bump: 2 });
      const band = mesh(lumpy(new THREE.TorusGeometry(R * .93, .045, 12, 32, Math.PI * 1.15), .01, 8, 2), hm2); band.rotation.set(Math.PI / 2 - .25, 0, -Math.PI * .07 + Math.PI); band.position.set(0, .03, -.02); band.scale.set(sc[0], sc[2], 1); h.add(band);
    }
    if (o.mustache) {
      const mm = clay(0x1c1514, { streak: true, bump: 2.5 }); const my2 = (o.mouthY ?? -.1) + .035;
      for (const s of [-1, 1]) {
        const c = new THREE.CatmullRomCurve3([V(0, 0, 0), V(s * .05, -.005, -.006), V(s * .1, -.02, -.03), V(s * .135, .01, -.05), V(s * .125, .04, -.05)]);
        const tg = new THREE.TubeGeometry(c, 30, .022, 10); const pos = tg.attributes.position; // taper
        for (let i = 0; i < pos.count; i++) { const seg = Math.floor(i / 11) / 30; const k = 1 - seg * .65; const cp = c.getPoint(Math.min(1, seg)); pos.setXYZ(i, cp.x + (pos.getX(i) - cp.x) * k, cp.y + (pos.getY(i) - cp.y) * k, cp.z + (pos.getZ(i) - cp.z) * k); }
        tg.computeVertexNormals(); const m = mesh(tg, mm); m.position.set(0, my2, surf(0, my2) + .012); h.add(m);
      }
      const mid = mesh(sphereG(.028, 14, 10), mm); mid.scale.set(1.3, .8, .8); mid.position.set(0, my2, surf(0, my2) + .012); h.add(mid);
    }
    if (o.chin) { const c = mesh(lumpy(sphereG(1, 24, 16), .03, 4, 7), skin); c.scale.set(.12, .055, .09); c.position.set(0, -R * sc[1] * .86, .045); h.add(c); }
    // sweat drops
    const sw = clay(0x9fd8f0, { rough: .12, bump: .1, noTint: true, opacity: .9 });
    this.sweat = [[-.11, .14], [.12, .12], [-.02, .17], [.14, .02], [-.15, .03]].map(([x, y], i) => {
      const g = new THREE.Group(); const b = mesh(sphereG(.014, 12, 10), sw, false); const c = mesh(new THREE.ConeGeometry(.0128, .024, 12), sw, false); c.position.y = .016; g.add(b, c);
      g.userData.base = V(x, y, surf(x, y) + .008); g.lookAt(0, 0, 0); h.add(g); g.visible = false; return g;
    });
    this.face = { lx: 0, ly: 0, lid: [o.lid ?? .2, o.lid ?? .2], lidB: [0, 0], brow: [0, 0], browA: [0, 0], mw: .07, curve: 0, open: 0, teeth: 0, wob: 0, tongue: 0, sweat: 0, sweatSlide: 0, cross: 0, squint: 0 };
  }
  setFace(f) {
    const F = Object.assign({}, this.face, f); const R = this.hR, sc = this.hS;
    this.eyes.forEach((e, i) => {
      const s = i ? 1 : -1; let lx = F.lx + (F.cross ? -s * F.cross : 0), ly = F.ly;
      const d = V(lx * .55, ly * .5, 1).normalize(); e.p.position.copy(d).multiplyScalar(e.r * .72); e.p.scale.set(1, 1, .6); e.p.quaternion.setFromUnitVectors(V(0, 0, 1), d);
      e.lid.rotation.x = lerp(-1.25, 1.62, F.lid[i]); e.lidB.rotation.x = lerp(Math.PI + 1.3, Math.PI - .05, F.lidB[i] ?? 0);
    });
    this.brows.forEach((b, i) => {
      const s = b.userData.s, x = s * (this.o.eyeX ?? .074), y = this.browBase + F.brow[i] * .03;
      b.position.set(x, y, this.surf(x, y) + .008); b.rotation.set(-.35 * (y / .2), s * .25, s * F.browA[i] * .5);
    });
    // mouth shape
    const w = F.mw, N = 22, up = [], lo = [];
    for (let k = 0; k <= N; k++) {
      const u = k / N * 2 - 1, x = u * w / 2, bow = 1 - u * u, wob = F.wob * Math.sin(u * 9 + 1) * .005;
      const mid = -F.curve * bow * .018 + F.curve * .006 + wob, hgt = Math.sqrt(Math.max(0, bow));
      up.push([x, mid + .003 + F.open * .022 * hgt]); lo.push([x, mid - .003 - F.open * .032 * hgt]);
    }
    const mk = (sh, pts) => { pts.forEach(([x, y], i) => i ? sh.lineTo(x, y) : sh.moveTo(x, y)); };
    const s1 = new THREE.Shape(); mk(s1, [...up, ...lo.slice().reverse()]);
    const wrap = (g, dz) => { const p = g.attributes.position, z0 = this.surf(0, this.my); for (let i = 0; i < p.count; i++) p.setZ(i, this.surf(p.getX(i), this.my + p.getY(i)) - z0 + dz); g.computeVertexNormals(); return g; };
    this.mouthDark.geometry.dispose(); this.mouthDark.geometry = wrap(new THREE.ShapeGeometry(s1, 2), .0025);
    this.teethM.visible = this.teethLine.visible = F.teeth > 0;
    if (F.teeth > 0) {
      const s3 = new THREE.Shape(); mk(s3, [...up.map(([x, y]) => [x * .86, y - .0025]), ...lo.slice().reverse().map(([x, y]) => [x * .86, y + .0025])]);
      this.teethM.geometry.dispose(); this.teethM.geometry = wrap(new THREE.ShapeGeometry(s3, 2), .0035);
      this.teethLine.scale.x = w * .8; this.teethLine.position.y = (up[N / 2][1] + lo[N / 2][1]) / 2;
    }
    this.tongue.visible = F.tongue > 0; this.tongue.position.set(0, -.01, -.01 + F.tongue * .045);
    // sweat
    this.sweat.forEach((g, i) => { g.visible = F.sweat > i * .2 + .01; const b = g.userData.base; g.position.set(b.x, b.y - F.sweatSlide * (.03 + i * .01), b.z); g.rotation.set(0, 0, 0); g.rotateX(-.3); });
    this.face = F;
  }
  // per-frame solve of limbs
  solve() {
    const r = this.root; r.updateMatrixWorld(true);
    const toRoot = (obj, p) => r.worldToLocal(obj.localToWorld(p.clone()));
    for (let i = 0; i < 2; i++) {
      const a = this.arm[i], S = toRoot(this.torso, this.shoulder[i]), T = this.handT[i].clone();
      const E = ik2(S, T, this.armLen[0], this.armLen[1], this.elbowPole[i].clone().normalize());
      placeSeg(a.up, S, E);
      const W = T.clone().sub(E).normalize(); const Tw = T.clone().addScaledVector(W, -.035);
      placeSeg(a.lo, E, Tw); a.cuff.position.copy(Tw); a.cuff.quaternion.copy(a.lo.quaternion);
      a.hand.position.copy(T).addScaledVector(W, .03);
      if (this.handRot[i]) a.hand.quaternion.setFromEuler(new THREE.Euler(...this.handRot[i], 'YXZ'));
      else { a.hand.quaternion.setFromUnitVectors(V(0, -1, 0), W); a.hand.rotateY(this.handRoll[i] + (i ? -1 : 1) * .4); }
      a.hand.scale.set(i ? -1 : 1, 1, 1); poseHand(a.hand, this.handPose[i]);
    }
    for (let i = 0; i < 2; i++) {
      const l = this.leg[i]; [l.up, l.lo, l.shoe].forEach(m => m.visible = this.visibleLegs);
      if (!this.visibleLegs) continue;
      const H = toRoot(this.hips, V(i ? .095 : -.095, -.02, 0)), F = this.footT[i].clone();
      const Ft = F.clone().add(V(0, .045, -.03));
      const Kn = ik2(H, Ft, this.legLen[0], this.legLen[1], this.kneePole[i].clone().normalize());
      placeSeg(l.up, H, Kn); placeSeg(l.lo, Kn, Ft);
      l.shoe.position.set(F.x, F.y + .01, F.z + .05); l.shoe.rotation.set(-this.footPitch[i], 0, 0);
    }
  }
}

export function rookie() {
  return new Character({ skin: 0xe3a47a, suit: 0x232025, tie: 0x141217, hair: 'rookie', seed: 2 });
}
export function tony() {
  const stripes = paintTex(256, 256, (g) => { g.fillStyle = '#f0f0f0'; g.fillRect(0, 0, 256, 256); g.fillStyle = '#b8bccb'; for (let x = 0; x < 256; x += 32) g.fillRect(x, 0, 3, 256); });
  stripes.wrapS = stripes.wrapT = THREE.RepeatWrapping; stripes.repeat.set(3, 1);
  return new Character({ skin: 0xd8936b, suit: 0x3a3f50, suitMap: stripes, tie: 0xa8232b, hair: 'tony', mustache: true, chin: true, belly: true, width: 1.18, headR: .225, headScale: [.98, 1.0, .95], eyeR: .045, eyeX: .072, eyeY: .05, pupil: .5, browR: .022, browLen: .08, browC: 0x1c1514, nose: .05, mouthY: -.128, seed: 9, scale: 1.08 });
}
