const A = 'assets/';
const root = document.getElementById('root');
function h(html) { const d = document.createElement('div'); d.innerHTML = html.trim(); const e = d.firstChild; root.appendChild(e); return e }
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const eo = x => 1 - Math.pow(1 - clamp(x), 3);
const eb = x => { x = clamp(x); const c = 1.70158, c3 = c + 1; return 1 + c3 * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2) };
function show(el, t, t0, t1, kind = 'pop', dur = .32) {
  if (t < t0 || t >= t1) { el.style.display = 'none'; return false }
  el.style.display = '';
  const a = (t - t0) / dur, o = clamp((t1 - t) / .22);
  let tf = '';
  if (kind === 'pop') tf = `scale(${.7 + .3 * eb(a)})`;
  else if (kind === 'slideL') tf = `translateX(${-70 * (1 - eo(a))}px)`;
  else if (kind === 'slideR') tf = `translateX(${70 * (1 - eo(a))}px)`;
  else if (kind === 'up') tf = `translateY(${50 * (1 - eo(a))}px)`;
  else if (kind === 'drop') tf = `translateY(${-60 * (1 - eo(a))}px)`;
  else if (kind === 'slam') tf = `scale(${1 + 1.4 * (1 - eo(a / .6))}) rotate(-6deg)`;
  el.style.transform = tf; el.style.opacity = kind === 'cut' ? 1 : Math.min(clamp(a * 1.6), o);
  return true
}
/* ---------- word lookup ---------- */
const norm = s => s.toLocaleLowerCase('tr').replace(/[^a-zçğıöşü0-9]/g, '');
const WW = window.WORDS.words.map(([s, e, t]) => [s, e, norm(t)]);
const MISSING = [];
function W(key, after = 0, def) {
  const k = norm(key);
  for (const [s, , t] of WW) if (s >= after && t.startsWith(k)) return s;
  MISSING.push(key + '@' + after); return def !== undefined ? def : after + .5;
}
const M = window.WORDS.marks;
/* ---------- SECTIONS ---------- */
const T = {};
T.hook = [0, W('bugün', 4)]; T.hook2 = [T.hook[1], W('neden', 12)];
T.why = [T.hook2[1], W('bu', 23)]; T.nanami = [T.why[1], W('locke', 41, W('lock', 41))];
T.passive = [T.nanami[1], W('q', 46)]; T.q = [T.passive[1], W('w', 64)]; T.w = [T.q[1], W('e', 78)];
T.e = [T.w[1], W('ve', 89)]; T.r = [T.e[1], W('kombolara', 111)]; T.combo = [T.r[1], W('eşleşmelerde', 126)];
T.match = [T.combo[1], W('rune', 144, W('rün', 144))]; T.runes = [T.match[1], W('dora', 151)];
T.items = [T.runes[1], W('yetenek', 163)]; T.skills = [T.items[1], W('sihirdar', 170)]; T.summ = [T.skills[1], W('bu', 173)];
T.roast = [T.summ[1], W('örlü', 187, 188.7)]; T.early = [T.roast[1], W('midgame', 202, W('mid', 202))];
T.mid = [T.early[1], W('late', 208)]; T.late = [T.mid[1], W('ve', 219.5)]; T.cta = [T.late[1], 240.5];
const finT = W('4', 233, 235.2);
window.CUES = { T, flash: W('sıçra', T.summ[0]), ignite: W('tutuştur', T.summ[0]), uc: W('kafana', 3), marks: M };

/* ---------- COUNTDOWN (covers the burned-in timer) ---------- */
const cd = h(`<div class="abs" style="z-index:50;right:0;top:0;width:300px;height:104px;background:#010A13;border-left:4px solid #C8AA6E;border-bottom:4px solid #C8AA6E;box-sizing:border-box;display:flex;align-items:center;gap:14px;padding-left:22px">
 <div style="font-family:Ant;font-size:64px;color:#FFC23D;text-shadow:0 4px 0 #000;letter-spacing:.02em" id="cdv">4:00</div>
 <div style="font-family:Osw;font-weight:700;font-size:20px;letter-spacing:.18em;color:#0AC8B9;line-height:1.2">KALAN<br>SÜRE</div></div>`);
const cdv = cd.querySelector('#cdv');

/* ---------- HOOK ---------- */
function scene(bg, a, b, pos = 'center', blur = false) { const s = h(`<div class="abs scene"><div class="abs" style="inset:0;background:url(${A}${bg}) ${pos}/cover;${blur ? 'filter:blur(14px) brightness(.32) saturate(1.2);inset:-60px' : ''}"></div></div>`); fulls.push([s, a, b]); return s }
const fulls = [];
const hookS = scene('splash_0.jpg', 0, T.hook[1], '60% 30%');
hookS.insertAdjacentHTML('beforeend', `<div class="abs" style="inset:0;background:radial-gradient(ellipse at 60% 40%,rgba(1,10,19,0) 25%,rgba(1,10,19,.85) 100%)"></div>`);
const hookImg = hookS.firstChild;
const nails = h(`<div class="abs" style="left:0;right:0;top:380px;text-align:center;display:flex;gap:40px;justify-content:center"></div>`); hookS.appendChild(nails);
const nailEls = [0, 1, 2].map(i => { const e = h(`<img src="${A}LockeQ.png" style="width:170px;height:170px;border-radius:18px;border:5px solid #C8AA6E;box-shadow:0 0 50px rgba(120,140,255,.7)">`); nails.appendChild(e); return e });
const x3 = h(`<div class="abs" style="left:0;right:0;top:600px;text-align:center;font-family:Ant;font-size:120px;color:#FFF8EC;text-shadow:0 8px 0 #000">KAFANA <span style="color:#FFC23D">3 ÇİVİ</span></div>`); hookS.appendChild(x3);
const title = h(`<div class="abs" style="left:0;right:0;top:300px;text-align:center"><div style="font-family:Ant;font-size:130px;color:#FFF8EC;text-shadow:0 8px 0 #000;line-height:1.15"><span style="font-size:190px;color:#FFC23D;display:inline-block;transform:skewX(-12deg);margin-right:20px">4</span>DAKİKADA <span style="color:#FFC23D">LOCKE</span></div></div>`);
const promise = h(`<div class="abs" style="left:0;right:0;top:560px;text-align:center"><span class="chip red" style="font-size:44px">VİDEONUN SONUNDA: Locke'un <b>Nocturne'e</b> söylediği laf</span></div>`);

/* ---------- WHY ---------- */
function listCol(x, ttl, color, rows) {
  const c = h(`<div class="abs" style="left:${x}px;top:140px;width:660px"></div>`);
  c.appendChild(h(`<div style="font-family:Ant;font-size:72px;color:${color};text-shadow:0 5px 0 #000;margin-bottom:14px">${ttl}</div>`));
  const rs = rows.map(([txt, t0]) => { const r = h(`<div class="chip ${color === 'var(--green)' ? 'green' : 'red'}" style="font-size:40px">${txt}</div>`); const w = document.createElement('div'); w.className = 'chipwrap'; w.appendChild(r); c.appendChild(w); return [r, t0] });
  return [c, rs]
}
const w0 = T.why[0];
const pros = listCol(70, 'ARTILAR', 'var(--green)', [['Yüksek patlama hasarı', W('patlama', w0)], ['Alan etkili infaz', W('alan', w0)], ['İnanılmaz hareketli', W('inanılmaz', w0)], ['Erken kill tehdidi', W('erken', w0)]]);
const cons = listCol(1150, 'EKSİLER', 'var(--red)', [['Dalan biri için kırılgan', W('ama', w0)], ['Q tutturmak şart', W('q', w0 + 4)]]);
// Nanami + lore
const n0 = T.nanami[0], loreT = W('corvin', n0, W('locke', n0 + 4)), aileT = W('aile', n0);
const nan = scene('splash_0.jpg', n0, loreT, '62% 25%');
nan.insertAdjacentHTML('beforeend', `<div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(1,10,19,.92) 0,rgba(1,10,19,.4) 45%,rgba(1,10,19,0) 70%)"></div>`);
const nanTags = ['GÖZLÜKLÜ', 'TAKIM ELBİSELİ', 'SARIŞIN'].map((tx, i) => { const e = h(`<div class="abs chip gold" style="left:80px;top:${200 + i * 100}px;font-size:56px">${tx}</div>`); nan.appendChild(e); return e });
const nanTagT = [W('gözlüklü', n0), W('takım', n0), W('sarışın', n0)];
const nanStamp = h(`<div class="abs" style="left:70px;top:560px"><span style="display:inline-block;font-family:Ant;font-size:120px;color:#FF3B4E;text-shadow:0 8px 0 #000;transform:rotate(-4deg)">NANAMİ DEĞİL.</span></div>`); nan.appendChild(nanStamp);
const nanT = W('hayır', n0);
const lore = scene('splash_0.jpg', loreT, T.nanami[1], '50% 20%', true);
lore.insertAdjacentHTML('beforeend', `<div class="abs" style="left:0;right:0;top:250px;text-align:center;font-family:Ant;font-size:130px;color:#FFF8EC;text-shadow:0 8px 0 #000">CORVIN <span style="color:#FFC23D">LOCKE</span></div>
<div class="abs" style="left:0;right:0;top:430px;text-align:center"><span class="chip purple" style="font-size:48px">Demacialı okültistlerin oğlu</span></div>`);
const aile = h(`<div class="abs" style="left:0;right:0;top:640px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:96px;color:#FFC23D;text-shadow:0 7px 0 #000;transform:rotate(-3deg)">AİLE YEMEKLERİ EĞLENCELİ GEÇİYORDUR</span></div>`); lore.appendChild(aile);

/* ---------- BADGES + CHIPS ---------- */
function badge(key, name, sub, icon, small) { return h(`<div class="abs panel badge"><div class="key ${small ? 'small' : ''}">${key}</div><img src="${A}${icon}"><div class="txt"><div class="sub">${sub}</div><div class="nm">${name}</div></div></div>`) }
const labelCover = h(`<div class="abs" style="left:60px;top:88px;width:640px;height:226px;background:#0d0916;border-radius:20px"></div>`);
const badges = [[badge('P', 'Gümüş Kazık', 'PASİF', 'LockeP.png', true), ...T.passive], [badge('Q', 'Ayin Çivisi', 'YETENEK · Q', 'LockeQ.png'), ...T.q],
[badge('W', 'Ruh Yangını', 'YETENEK · W', 'LockeW.png'), ...T.w], [badge('E', 'Külgezen', 'YETENEK · E', 'LockeE.png'), ...T.e], [badge('R', 'Araf', 'ULTİ · R', 'LockeR.png'), ...T.r]];
const pcard = h(`<div class="abs panel pcard"><div class="hd"><img src="${A}LockeP.png">GÜMÜŞ KAZIK</div>
<div class="ln">Saldırılar ekstra <b>büyü hasarı</b> verir.</div>
<div class="ln">Rakibin <b>eksik canı</b> arttıkça hasar artar.</div></div>`);
const pl = [...pcard.querySelectorAll('.ln')];
const chipBox = h(`<div class="abs chips"></div>`);
const q0 = T.q[0], wq = T.w[0], e0 = T.e[0], r0 = T.r[0], E0 = T.early[0], M0 = T.mid[0], L0 = T.late[0];
const chipDefs = [
  ['Çivi: hasar + yavaşlatma + <b>işaret</b>', 'gold', W('düz', q0), T.q[1]], ['4 sn içinde <b>3 çivi</b>, bedava', 'purple', W('4', q0, W('dört', q0)), T.q[1]], ['2 işaret = <b>DEV YAVAŞLATMA</b>', 'red', W('2', q0 + 6, W('iki', q0 + 6)), T.q[1]], ['Saldırı ya da E işaretleri <b>patlatır</b>', 'gold', W('sonraki', q0), T.q[1]],
  ['+Saldırı hızı +<b>hareket hızı</b>', 'gold', W('locke', wq, wq + 1.5), T.w[1]], ['Kendi canını <b>yakar</b>', 'red', W('ama', wq), T.w[1]], ['Hasar → gri can → <b>geri iyileşir</b>', 'purple', W('şampiyonlardan', wq), T.w[1]],
  ['Işınlan + <b>alan hasarı</b>', 'gold', W('bir', e0), T.e[1]], ['Sonraki saldırı: <b>hedefe atıl</b>', 'purple', W('sonraki', e0), T.e[1]], ['Kill = <b>E yenilenir</b>', 'red', W('bir', e0 + 7), T.e[1]],
  ['Hasar + yavaşlatma + <b>5 sn işaret</b>', 'gold', W('içindeki', r0), T.r[1]], ['Eşik altı = <b>İNFAZ</b>', 'red', W('işaretli', r0), T.r[1]], ['Yadigârı topla: <b>bekleme ↓</b>', 'purple', W('onu', r0), T.r[1]], ['Her mühür: eşik ↑ <b>SINIRSIZ</b>', 'red', W('yani', r0 + 15), T.r[1]],
  ['Farm, dürt, <b>trade</b> ara', 'gold', E0 + .3, T.early[1]], ['3 Q = rakip <b>neredeyse durur</b>', 'red', W('üç', E0, W('3', E0)), T.early[1]], ['Seviye 6: <b>saçma hasar</b>', 'purple', W('altıncı', E0), T.early[1]],
  ['Yan koridora geç, <b>dalgayı it</b>', 'gold', M0 + .3, T.mid[1]], ['Rotasyonda <b>pick</b> ara', 'gold', W('rotasyonlarda', M0, M0 + 3), T.mid[1]],
  ['Savaşın başlamasını <b>bekle</b>', 'gold', W('savaşın', L0), T.late[1]], ['Duvardan arka hatta <b>ışınlan</b>', 'purple', W('duvarların', L0, L0 + 3.5), T.late[1]], ['Ulti → <b>herkese</b>', 'red', W('ultini', L0), T.late[1]], ['Her kill: <b>E yenilenir</b>', 'gold', W('her', L0 + 6), T.late[1]]
];
const chips = chipDefs.map(([tx, c, t0, t1]) => { const w = document.createElement('div'); w.className = 'chipwrap'; const e = h(`<div class="chip ${c}">${tx}</div>`); w.appendChild(e); chipBox.appendChild(w); return [w, e, t0, t1] });
const plT = [T.passive[0] + .4, W('eksik', T.passive[0])];
// Q nail marks counter
const marks3 = h(`<div class="abs panel" style="left:660px;top:36px;width:600px;height:96px;padding:14px 22px;box-sizing:border-box"><div style="font-family:Osw;font-weight:700;font-size:24px;letter-spacing:.14em;color:#FFC23D">ÇİVİ İŞARETİ</div><div style="display:flex;gap:14px;margin-top:8px" id="pips">${'<div style="flex:1;height:26px;border-radius:8px;background:#2a2238"></div>'.repeat(3)}</div></div>`);
const pips = [...marks3.querySelectorAll('#pips div')];
const sonT = (M.son_dualar || [r0 + 10])[0];
const redFlash = h(`<div class="abs" style="inset:0;background:radial-gradient(ellipse at center,rgba(60,90,255,0) 25%,rgba(40,60,200,.75) 100%)"></div>`);

/* ---------- COMBO BAND ---------- */
const band = h(`<div class="abs band"><div class="ttl" id="bt"></div><div class="row" id="br"></div></div>`);
const bt = band.querySelector('#bt'), br = band.querySelector('#br');
const ic = { Q: 'LockeQ.png', W: 'LockeW.png', E: 'LockeE.png', R: 'LockeR.png' };
function comboRow(steps) {
  br.innerHTML = ''; const els = []; steps.forEach(([k, t0], i) => {
    if (i) br.insertAdjacentHTML('beforeend', '<div class="arrow">›</div>');
    const e = ic[k] ? h(`<div class="step" style="width:104px;height:104px"><img src="${A}${ic[k]}" style="width:90px;height:90px"><div class="k">${k}</div></div>`) : h(`<div class="step auto" style="width:120px;height:104px;font-size:30px">${k}</div>`);
    br.appendChild(e); els.push([e, t0])
  }); return els
}
const c0 = T.combo[0], c2 = W('tam', c0);
function seqT(a, b, n) { return Array.from({ length: n }, (_, i) => a + (b - a) * i / (n - 1)) }
const s1 = seqT(W('üç', c0, c0 + 1), c2 - .8, 6), s2 = seqT(c2 + .4, T.combo[1] - .6, 9);
const combo1 = ['Q', 'Q', 'Q', 'W', 'E', 'OTO'].map((k, i) => [k, s1[i]]), combo2 = ['W', 'R', 'Q', 'E', 'OTO', 'Q', 'OTO', 'Q', 'OTO'].map((k, i) => [k, s2[i]]);
let curCombo = 0, comboEls = [];

/* ---------- MATCHUPS ---------- */
const m0 = T.match[0], yT = (M.yone || [T.match[1]])[0];
const sm = scene('splash_0.jpg', m0, yT, 'center', true);
sm.insertAdjacentHTML('beforeend', `<div class="title">EŞLEŞMELER</div><div class="abs" style="left:660px;top:200px;width:600px;height:760px;background:url(${A}splash_0.jpg) 60% 30%/auto 125%;border-radius:26px;box-shadow:0 0 0 4px rgba(255,255,255,.25)"></div>`);
const sEasy = h(`<div class="side" style="left:70px;background:linear-gradient(180deg,rgba(30,120,70,.92),rgba(12,50,30,.92))"><h2>KOLAY</h2><div class="icons"><img src="${A}champ_Viktor.png"><img src="${A}champ_Sylas.png"><img src="${A}champ_Syndra.png"></div><div class="cap">Hareketsiz büyücüler.</div><div class="cap" style="color:#d9ffe9">Üstüne ışınlan, patlat.</div></div>`);
const sHard = h(`<div class="side" style="left:1290px;background:linear-gradient(180deg,rgba(150,30,45,.92),rgba(60,10,18,.92))"><h2>ZOR</h2><div class="icons"><img src="${A}champ_Zed.png"><img src="${A}champ_Katarina.png"><img src="${A}champ_Akali.png"></div><div class="cap">Kilitleyen ya da</div><div class="cap" style="color:#ffd9dd">uzak tutan şampiyonlar.</div></div>`);
sm.appendChild(sEasy); sm.appendChild(sHard);
const vs = h(`<div class="vs"><div class="ring"></div><div class="t">VS</div></div>`); sm.appendChild(vs);
for (let i = 0; i < 12; i++) { const r = document.createElement('div'); r.className = 'ray'; vs.insertBefore(r, vs.firstChild) }
const vsRing = vs.querySelector('.ring'), vsT = vs.querySelector('.t'), rays = [...vs.querySelectorAll('.ray')];
const easyIc = [W('viktor', m0), W('sylas', m0), W('syndra', m0)], hardT = W('ama', m0), hardIc = [W('zed', hardT), W('katarina', hardT), W('akali', hardT)];
// Yone line scene
function roastScene(champ, splash, a, b, sub) {
  const s = scene(splash, a, b, 'center');
  s.insertAdjacentHTML('beforeend', `<div class="abs" style="inset:0;background:linear-gradient(0deg,rgba(1,10,19,.9) 0,rgba(1,10,19,0) 45%)"></div>
  <div class="abs" style="left:70px;bottom:70px;display:flex;align-items:center;gap:24px"><img src="${A}champ_Locke.png" style="width:120px;height:120px;border-radius:16px;border:4px solid #C8AA6E"><span style="font-family:Ant;font-size:110px;color:#FFC23D;text-shadow:0 7px 0 #000">→</span><img src="${A}champ_${champ}.png" style="width:120px;height:120px;border-radius:16px;border:4px solid #FF3B4E"><span style="font-family:Ant;font-size:96px;color:#FFF8EC;text-shadow:0 7px 0 #000">${sub}</span></div>`);
  return s
}
const yone = roastScene('Yone', 'splash_Yone.jpg', yT - .15, T.match[1], "LOCKE'TAN YONE'YE");
/* ---------- BUILD ---------- */
const sr = scene('splash_1.jpg', ...T.runes, 'center', true); const ru0 = T.runes[0];
sr.insertAdjacentHTML('beforeend', `<div class="title">RÜN<span>LER</span></div>
<div class="tag" style="left:250px;top:215px"><img src="${A}rune_7200_Domination.png" style="width:44px;vertical-align:middle;margin-right:12px">HÂKİMİYET</div>
<div class="tag" style="left:1260px;top:215px"><img src="${A}rune_7204_Resolve.png" style="width:44px;vertical-align:middle;margin-right:12px">AZİM</div>`);
function rcard(p, x, y, img, name, big) { const c = h(`<div class="card ${big ? 'lg' : ''}" style="left:${x}px;top:${y}px"><img src="${A}${img}" style="border-radius:50%;background:#140d22"><div class="n">${name}</div></div>`); p.appendChild(c); return c }
const runeCards = [[rcard(sr, 140, 300, 'rune_Electrocute.png', 'Elektrik Ver', 1), W('elektrik', ru0)], [rcard(sr, 430, 320, 'rune_SuddenImpact.png', 'Ani Darbe'), W('ani', ru0)], [rcard(sr, 680, 320, 'rune_SixthSense.png', 'Altıncı His'), W('altıncı', ru0)], [rcard(sr, 430, 600, 'rune_UltimateHunter.png', 'Mükemmel Avcı'), W('mükemmel', ru0)],
[rcard(sr, 1180, 320, 'rune_BonePlating.png', 'Kemik Zırh'), W('kemik', ru0)], [rcard(sr, 1450, 320, 'rune_Revitalize.png', 'Canlandır'), W('canlandır', ru0)]];
const si = scene('splash_0.jpg', ...T.items, 'center', true); const it0 = T.items[0];
si.insertAdjacentHTML('beforeend', `<div class="title">EŞYA<span>LAR</span></div>`);
function rowLabel(p, y, txt) { p.insertAdjacentHTML('beforeend', `<div class="tag" style="left:110px;top:${y}px">${txt}</div>`) }
rowLabel(si, 250, 'BAŞLANGIÇ'); rowLabel(si, 500, 'ÇEKİRDEK'); rowLabel(si, 780, 'DURUMA GÖRE');
function icard(x, y, id, name) { const c = h(`<div class="card" style="left:${x}px;top:${y}px"><img src="${A}item_${id}.png" style="width:130px;height:130px"><div class="n" style="font-size:28px">${name}</div></div>`); si.appendChild(c); return c }
const itemCards = [[icard(420, 200, 1056, "Doran'ın Yüzüğü"), W('dora', it0)], [icard(660, 200, 2003, 'Can İksiri ×2'), W('iki', it0, W('can', it0))],
[icard(420, 450, 3100, 'Lich Boğan'), W('lich', it0)], [icard(700, 450, 3020, 'Sihirbaz Pabuçları'), W('sihir', it0)], [icard(980, 450, 4645, 'Gölgealev'), W('gölge', it0)], [icard(1260, 450, 3157, "Zhonya'nın Kumsaati"), W('zonya', it0)],
[icard(420, 730, 1082, 'Kara Mühür'), W('kara', it0)], [icard(700, 730, 4646, 'Yıldırım Asası'), W('yıldırım', it0)], [icard(980, 730, 3089, "Rabadon'un Şapkası"), W('rabodon', it0)]];
const allDesc = h(`<div class="abs chip red" style="left:1300px;top:790px;font-size:44px">HEPSİ <b>AÇIKLAMADA</b></div>`); si.appendChild(allDesc); const descT = W('hepsi', it0);
const ss = scene('splash_1.jpg', ...T.skills, 'center', true); const sk0 = T.skills[0];
ss.insertAdjacentHTML('beforeend', `<div class="title">YETENEK <span>SIRASI</span></div>`);
const order = ['Q', 'E', 'W', 'Q', 'Q', 'R', 'Q', 'E', 'Q', 'E', 'R', 'E', 'E', 'W', 'W', 'R', 'W', 'W'];
let gh = '<tr><td class="hd ic"></td>' + order.map((_, i) => `<td class="hd">${i + 1}</td>`).join('') + '</tr>';
['Q', 'W', 'E', 'R'].forEach(k => { gh += `<tr><td class="ic"><img src="${A}${ic[k]}"></td>` + order.map((o, i) => `<td data-k="${k}" data-l="${i}"></td>`).join('') + '</tr>' });
const grid = h(`<table class="grid">${gh}</table>`); ss.appendChild(grid);
const sq = [W('q', sk0), W('e', sk0 + .4), W('w', sk0 + .8)]; const maxT = W('önce', sk0), ultT = W('ulti', sk0 + 3);
const lvlT = order.map((_, i) => i < 3 ? sq[i] : maxT + (i - 3) * ((T.skills[1] - .5 - maxT) / 15));
const cells = [...grid.querySelectorAll('td[data-k]')].filter(c => order[+c.dataset.l] === c.dataset.k);
const maxChip = h(`<div class="abs chip" style="left:170px;top:760px;font-size:44px">Maks sırası: <b>Q › E › W</b></div>`); ss.appendChild(maxChip);
const ultChip = h(`<div class="abs chip purple" style="left:820px;top:760px;font-size:44px">Ultiyi her fırsatta al: <b>6 · 11 · 16</b></div>`); ss.appendChild(ultChip);
const su = scene('splash_0.jpg', ...T.summ, 'center', true);
su.insertAdjacentHTML('beforeend', `<div class="title">SİHİRDAR <span>BÜYÜLERİ</span></div>`);
const sF = h(`<div class="card lg" style="left:600px;top:340px"><img src="${A}SummonerFlash.png" style="width:260px;height:260px"><div class="n" style="font-size:48px">Sıçra</div></div>`);
const sI = h(`<div class="card lg" style="left:1060px;top:340px"><img src="${A}SummonerDot.png" style="width:260px;height:260px"><div class="n" style="font-size:48px">Tutuştur</div></div>`);
su.appendChild(sF); su.appendChild(sI);
const flashFx = h(`<div class="abs" style="inset:0;background:radial-gradient(circle at 730px 470px,rgba(240,255,160,.9),rgba(240,255,160,0) 40%)"></div>`); su.appendChild(flashFx);
const ignFx = h(`<div class="abs" style="inset:0;background:radial-gradient(circle at 1190px 470px,rgba(255,120,40,.85),rgba(255,120,40,0) 40%)"></div>`); su.appendChild(ignFx);
/* ---------- ROAST ---------- */
const ro0 = T.roast[0];
const roastIntro = scene('splash_0.jpg', ro0, (M.fiddlesticks || [ro0 + 2])[0] - .15, '60% 25%', true);
roastIntro.insertAdjacentHTML('beforeend', `<div class="abs" style="left:0;right:0;top:380px;text-align:center;font-family:Ant;font-size:120px;color:#FFF8EC;text-shadow:0 8px 0 #000">ÇİVİ DEĞİL, <span style="color:#FF3B4E">LAF</span> ATIYOR</div>`);
const rF = roastScene('FiddleSticks', 'splash_Fiddlesticks.jpg', (M.fiddlesticks || [0])[0] - .15, (M.tahm || [0])[0] - .1, 'FIDDLESTICKS');
const rT = roastScene('TahmKench', 'splash_TahmKench.jpg', (M.tahm || [0])[0] - .1, (M.shaco || [0])[0] - .1, 'TAHM KENCH');
const rS = roastScene('Shaco', 'splash_Shaco.jpg', (M.shaco || [0])[0] - .1, (M.shaco || [0, 0])[1] + .15, 'SHACO');
const lightT = W('ve', (M.shaco || [ro0])[1] - .2);
const lightest = scene('splash_0.jpg', (M.shaco || [0, 0])[1] + .15, T.roast[1], '60% 25%', true);
lightest.insertAdjacentHTML('beforeend', `<div class="abs" style="left:0;right:0;top:400px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:120px;color:#FFC23D;text-shadow:0 8px 0 #000;transform:rotate(-3deg)">BUNLAR EN HAFİFLERİ</span></div>`);
/* ---------- PHASES ---------- */
const banners = [['EARLY GAME', T.early[0]], ['MID GAME', T.mid[0]], ['LATE GAME', T.late[0]]].map(([tx, t0]) => [h(`<div class="abs banner"><div>${tx}</div></div>`), t0]);
const phase = h(`<div class="abs phase"><div id="ph"></div></div>`); const ph = phase.querySelector('#ph');
/* ---------- CTA ---------- */
const ct0 = T.cta[0], nocT = (M.nocturne || [ct0 + 2])[0];
const odim = h(`<div class="abs dim"></div>`);
const promised = h(`<div class="abs" style="left:0;right:0;top:420px;text-align:center;font-family:Ant;font-size:100px;color:#FFF8EC;text-shadow:0 7px 0 #000">SÖZ VERDİĞİM GİBİ...</div>`);
const noc = roastScene('Nocturne', 'splash_Nocturne.jpg', nocT - .15, W('gerçekler', ct0), 'NOCTURNE');
const truth = h(`<div class="abs" style="left:0;right:0;top:380px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:150px;color:#FFC23D;text-shadow:0 10px 0 #000;transform:rotate(-3deg)">GERÇEKLER ACIDIR.</span></div>`);
const truthT = W('gerçekler', ct0);
const likeSub = h(`<div class="abs" style="left:0;right:0;top:700px;text-align:center;display:flex;gap:40px;justify-content:center">
 <div class="subbtn" id="lk" style="background:#1d1530;border:4px solid #FFC23D">👍 BEĞEN</div><div class="subbtn" id="sb">▶ ABONE OL</div></div>`);
const lk = likeSub.querySelector('#lk'), sb = likeSub.querySelector('#sb');
const fin = h(`<div class="abs scene"><div class="abs" style="inset:0;background:url(${A}splash_0.jpg) center/cover"></div><div class="abs" style="inset:0;background:linear-gradient(0deg,rgba(1,10,19,.95) 0,rgba(1,10,19,.5) 55%,rgba(1,10,19,.2) 100%)"></div>
 <div class="abs" style="left:0;right:0;top:700px;text-align:center;font-family:Ant;font-size:120px;color:#FFF8EC;text-shadow:0 7px 0 #000"><span style="color:#FFC23D;display:inline-block;transform:skewX(-12deg);font-size:170px;margin-right:16px">4</span>DAKİKADA <span style="color:#FFC23D">FEEDLEME</span></div>
 <div class="abs" id="fn2" style="left:0;right:0;top:900px;text-align:center;font-family:Osw;font-weight:700;font-size:52px;letter-spacing:.18em;color:#0AC8B9">YANİ SEN DE FEED'LEME.</div></div>`);
const fn2 = fin.querySelector('#fn2');
/* ---------- RENDER ---------- */
const inS = (t, k) => t >= T[k][0] && t < T[k][1];
window.render = function (t) {
  const rem = Math.max(0, 240 - t); cdv.textContent = `${Math.floor(rem / 60)}:${String(Math.floor(rem % 60)).padStart(2, '0')}`;
  fulls.forEach(([s, a, b]) => show(s, t, a, b, 'cut'));
  // hook
  hookImg.style.transform = `scale(${1.05 + .08 * clamp(t / T.hook[1])})`;
  nailEls.forEach((e, i) => { const a = CUES.uc + .15 + i * .3; e.style.opacity = t >= a ? 1 : 0; e.style.transform = t >= a ? `scale(${1 + .6 * (1 - eo((t - a) / .25))}) rotate(${(i - 1) * 8}deg)` : '' });
  x3.style.opacity = t >= CUES.uc ? 1 : 0;
  show(title, t, T.hook2[0], W('videonun', 6), 'pop', .35); show(promise, t, W('videonun', 6), T.hook2[1], 'up');
  // why
  if (inS(t, 'why')) { show(pros[0], t, w0, T.why[1], 'cut'); pros[1].forEach(([r, t0]) => show(r, t, t0, T.why[1], 'slideL')); show(cons[0], t, W('ama', w0), T.why[1], 'slideR'); cons[1].forEach(([r, t0]) => show(r, t, t0, T.why[1], 'slideR')) } else { pros[0].style.display = 'none'; cons[0].style.display = 'none' }
  nanTags.forEach((e, i) => { const a = nanTagT[i]; e.style.opacity = t >= a ? 1 : 0; e.style.transform = t >= a ? `translateX(${-60 * (1 - eo((t - a) / .3))}px)` : '' });
  nanStamp.style.opacity = t >= nanT ? 1 : 0; nanStamp.firstChild.style.transform = t >= nanT ? `scale(${1 + 1.2 * (1 - eo((t - nanT) / .3))}) rotate(-4deg)` : '';
  aile.style.opacity = t >= aileT ? 1 : 0; aile.firstChild.style.transform = t >= aileT ? `scale(${.6 + .4 * eb((t - aileT) / .3)}) rotate(-3deg)` : '';
  // abilities
  labelCover.style.display = (t >= T.passive[0] - 1 / 30 && t < T.combo[0]) ? '' : 'none';
  badges.forEach(([b, a, c]) => { if (show(b, t, a, c, 'slideL', .35)) { const k = b.querySelector('.key'); const p = t - a; k.style.boxShadow = p < 1.2 ? `0 0 ${40 * (1 - p / 1.2)}px rgba(244,185,66,.9)` : '' } });
  show(pcard, t, T.passive[0] + .2, T.passive[1], 'pop'); pl.forEach((e, i) => e.style.opacity = t >= plT[i] ? 1 : 0);
  chips.forEach(([w, e, t0, t1]) => { const v = t >= t0 && t < t1; w.style.display = v ? '' : 'none'; if (v) show(e, t, t0, t1, 'slideL', .3) });
  if (show(marks3, t, q0 + .3, T.q[1], 'drop')) { const a = W('düz', q0), b = W('2', q0 + 6, W('iki', q0 + 6)); pips.forEach((p, i) => { const on = t >= a + (b - a) * i / 2; p.style.background = on ? 'linear-gradient(90deg,#6f7bff,#c9d1ff)' : '#2a2238'; p.style.boxShadow = on ? '0 0 16px #8a96ff' : '' }) }
  if (show(redFlash, t, sonT, sonT + 2.4, 'cut')) redFlash.style.opacity = clamp(1 - (t - sonT) / 2.4) * (.7 + .3 * Math.sin(t * 20));
  if (show(band, t, T.combo[0], T.combo[1], 'up')) {
    const want = t < c2 ? 1 : 2; if (want !== curCombo) { curCombo = want; comboEls = comboRow(want === 1 ? combo1 : combo2); bt.textContent = want === 1 ? 'KORİDOR TRADE KOMBOSU' : 'TAM DALIŞ KOMBOSU' }
    comboEls.forEach(([e, t0]) => { const on = t >= t0; e.classList.toggle('on', on); e.style.transform = on ? `scale(${1 + .12 * clamp(1 - (t - t0) / .3)})` : '' })
  }
  if (t >= m0 && t < yT) {
    show(sEasy, t, easyIc[0] - .3, yT, 'slideL', .4); show(sHard, t, hardT - .2, yT, 'slideR', .4);
    [...sEasy.querySelectorAll('img')].forEach((e, i) => show(e, t, easyIc[i], yT, 'pop')); [...sHard.querySelectorAll('img')].forEach((e, i) => show(e, t, hardIc[i], yT, 'pop'));
    [...sEasy.querySelectorAll('.cap')].forEach((e, i) => e.style.opacity = t >= easyIc[0] + .6 ? 1 : 0); [...sHard.querySelectorAll('.cap')].forEach((e, i) => e.style.opacity = t >= hardIc[0] + .6 ? 1 : 0);
    const vt = t - (m0 + .4);
    if (show(vs, t, m0 + .4, yT, 'pop', .35)) { vsT.style.transform = `scale(${1 + .06 * Math.sin(t * 6)}) rotate(${-6 + 3 * Math.sin(t * 2)}deg)`; vsRing.style.transform = `scale(${1 + .5 * clamp(1 - vt / .5) + .04 * Math.sin(t * 6)})`; vsRing.style.opacity = .5 + .5 * Math.abs(Math.sin(t * 3)); rays.forEach((r, i) => { r.style.opacity = .35 + .35 * Math.sin(t * 5 + i); r.style.transform = `rotate(${i * 30 + t * 25}deg) translateY(150px)` }) }
  }
  if (inS(t, 'runes')) runeCards.forEach(([c, t0]) => show(c, t, t0, T.runes[1], 'pop'));
  if (inS(t, 'items')) { itemCards.forEach(([c, t0]) => show(c, t, t0, T.items[1], 'pop')); show(allDesc, t, descT, T.items[1], 'pop') }
  if (inS(t, 'skills')) { cells.forEach(c => { const l = +c.dataset.l; const on = t >= lvlT[l]; c.classList.toggle('on', on); c.classList.toggle('r', c.dataset.k === 'R'); c.textContent = on ? c.dataset.k : ''; c.style.transform = on ? `scale(${.7 + .3 * eb((t - lvlT[l]) / .25)})` : '' }); show(maxChip, t, maxT, T.skills[1], 'up'); show(ultChip, t, ultT, T.skills[1], 'up') }
  if (inS(t, 'summ')) { const f = CUES.flash, g = CUES.ignite; show(sF, t, f - .15, T.summ[1], 'pop'); show(sI, t, g - .15, T.summ[1], 'pop'); flashFx.style.opacity = clamp(1 - Math.abs(t - f) / .35); ignFx.style.opacity = t >= g ? clamp(1 - (t - g) / .9) * (.7 + .3 * Math.sin(t * 40)) : 0 }
  banners.forEach(([b, t0]) => { if (show(b, t, t0, t0 + 1.8, 'pop', .3)) b.firstChild.style.clipPath = `inset(0 ${100 - 100 * eo((t - t0) / .35)}% 0 0)` });
  const pn = inS(t, 'early') ? 'EARLY GAME' : inS(t, 'mid') ? 'MID GAME' : inS(t, 'late') ? 'LATE GAME' : '';
  ph.textContent = pn; phase.style.display = (pn && !banners.some(([b, t0]) => t >= t0 && t < t0 + 1.8)) ? '' : 'none';
  show(odim, t, ct0, 240.5, 'fade', .4); show(promised, t, ct0 + .1, nocT - .15, 'up');
  show(truth, t, truthT, W('video', truthT), 'slam', .3);
  if (show(likeSub, t, W('video', truthT), finT, 'up')) { const lT = W('beğenmeyi', ct0), sT = W('abone', ct0); lk.style.transform = t >= lT ? `scale(${1 + .15 * clamp(1 - (t - lT) / .4)})` : ''; lk.style.background = t >= lT ? '#FFC23D' : '#1d1530'; lk.style.color = t >= lT ? '#140c22' : '#fff'; sb.style.transform = t >= sT ? `scale(${1 + .15 * clamp(1 - (t - sT) / .4)})` : '' }
  show(fin, t, finT - .2, 240.5, 'fade', .35); fn2.style.opacity = t >= W('yani', finT) ? 1 : 0;
};
window.ready = Promise.all([document.fonts.ready, ...[...document.images].map(i => i.decode().catch(() => { }))]);
window.render(0);
