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
  el.style.transform = tf; el.style.opacity = kind === 'cut' ? 1 : Math.min(clamp(a * 1.6), o);
  return true
}

/* ---------- word lookup ---------- */
const norm = s => s.toLocaleLowerCase('tr').replace(/[^a-zçğıöşü0-9]/g, '');
const WW = window.WORDS.words.map(([s, e, t]) => [s, e, norm(t)]);
const MISSING = [];
function W(key, after = 0, def) {
  const k = norm(key);
  for (const [s, , t] of WW) if (s >= after && (t.startsWith(k) || (k === 'iki' && t === '2') || (k === 'bir' && t === '1'))) return s;
  MISSING.push(key + '@' + after); return def !== undefined ? def : after + .5;
}
function SEQ(keys, after) { const r = []; let a = after; for (const k of keys) { const t = W(k, a); r.push(t); a = t + .05 } return r }
const ANNE = window.WORDS.marks.anne;

/* ---------- SECTIONS ---------- */
const T = {
  intro: [0, W('çünkü', 13)], joke: [W('çünkü', 13), W('sett', 30)], passive: [W('sett', 30), W('q', 46)],
  q: [W('q', 46), W('w', 56)], w: [W('w', 56), W('sett', 74)], e: [W('sett', 74), W('ultisi', 84)], r: [W('ultisi', 84), W('kombolara', 99)],
  combo: [W('kombolara', 99), W('eşleşmelerde', 113)], match: [W('eşleşmelerde', 113), W('rune', 129)], runes: [W('rune', 129), W('dora', 138)],
  items: [W('dora', 138), W('yetenek', 150)], skills: [W('yetenek', 150), W('sihirdar', 160)], summ: [W('sihirdar', 160), W('early', 163)],
  early: [W('early', 163), W('midgame', 203)], mid: [W('midgame', 203), W('late', 210)], late: [W('late', 210), W('bir', 227)], cta: [W('bir', 227), 240.5]
};
window.CUES = { T, flash: W('sıçra', T.summ[0]), ignite: W('tutuştur', T.summ[0]), anne: ANNE };

/* ---------- INTRO + JOKE (over blurred Sett gameplay) ---------- */
const ishade = h(`<div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(8,5,14,.82) 0,rgba(8,5,14,.15) 36%,rgba(8,5,14,.15) 64%,rgba(8,5,14,.82) 100%),linear-gradient(0deg,rgba(8,5,14,.88) 0,rgba(8,5,14,0) 42%)"></div>`);
const introTitle = h(`<div class="abs big" style="top:850px;font-size:150px;letter-spacing:.04em">NEDEN <span style="color:var(--gold)">SETT?</span></div>`);
function listCol(x, title, color, rows) {
  const c = h(`<div class="abs" style="left:${x}px;top:120px;width:560px"></div>`);
  const t = h(`<div style="font-size:64px;font-weight:700;letter-spacing:.08em;color:${color};margin-bottom:18px">${title}</div>`); c.appendChild(t);
  const rs = rows.map(([txt, t0]) => { const r = h(`<div class="chip ${color === 'var(--green)' ? 'green' : 'red'}" style="font-size:40px">${txt}</div>`); const w = document.createElement('div'); w.className = 'chipwrap'; w.appendChild(r); c.appendChild(w); return [r, t0] });
  return [c, t, rs]
}
const pros = listCol(70, 'ARTILAR', 'var(--green)', [['Doğuştan tank', W('dayanıklı', 0)], ['Dev alan kontrolü', W('alan', 2)], ['Split push + takım savaşı', W('split', 3)], ['Tek hamlede takım siler', W('tek', 6)]]);
const cons = listCol(1290, 'EKSİLER', 'var(--red)', [['Hareket kabiliyeti düşük', W('hareket', 9)], ['Uzun bekleme süreleri', W('bekleme', 9)]]);
// joke lines
const jA = h(`<div class="abs big" style="top:300px;font-size:84px">Çünkü Sett sadece güçlü değil...</div>`);
const jB = h(`<div class="abs big" style="top:430px;font-size:120px;color:var(--gold)">Dünyanın en iyi evladı</div>`);
const jC = h(`<div class="abs big" style="top:600px;font-size:84px">Annesini çok seviyor <span class="heart">♥</span></div>`);
const jD = h(`<div class="abs big" style="top:420px;font-size:96px">Annesi hakkında tek kelime etsen...</div>`);
const crash = h(`<div class="abs crash"><div class="img"></div><div class="vig"></div></div>`);
const crashImg = crash.querySelector('.img');
const shout = h(`<div class="abs shout">"Anamı karıştırma demedim mi ben?!"</div>`);
const jE = h(`<div class="abs big" style="top:360px;font-size:130px;color:var(--gold)">A, pardon pardon!</div>`);
const jF = h(`<div class="abs big" style="top:540px;font-size:80px">Annene laf yok, devam ediyoruz</div>`);
function introR(t) {
  const [i0, i1] = T.intro, [j0, j1] = T.joke;
  show(ishade, t, 0, j1, 'cut');
  show(introTitle, t, 0, i1, 'cut');
  show(pros[0], t, 0, i1, 'cut'); pros[1].style.opacity = 1; pros[2].forEach(([r, t0]) => show(r, t, t0, i1, 'slideL'));
  show(cons[0], t, W('ama', 9), i1, 'slideR'); cons[2].forEach(([r, t0]) => show(r, t, t0, i1, 'slideR'));
  const a0 = ANNE[0], a1 = ANNE[1];
  show(jA, t, j0, W('aynı', j0), 'up'); show(jB, t, W('dünyanın', j0), W('hatta', j0), 'pop'); show(jC, t, W('annesini', j0), W('hatta', j0), 'up');
  show(jD, t, W('hatta', j0), a0, 'up');
  if (show(crash, t, a0, a1 + .15, 'cut')) {
    const p = (t - a0);
    const z = p < .12 ? 1 + 1.7 * eo(p / .12) : 2.7 + .1 * p;
    const sh = p < .9 ? (Math.sin(p * 90) * 14 * (1 - p / .9)) : 0;
    const fx = .49, fy = .10, ty = Math.min(430, fy * 1080 * z); crashImg.style.transform = `translate(${960 - fx * 1920 * z + sh}px,${ty - fy * 1080 * z - sh * .6}px) scale(${z})`;
  }
  show(shout, t, a0 + .05, a1 + .15, 'pop', .18);
  if (show(jE, t, W('pardon', a1), j1, 'pop', .25)) jE.style.transform += ` rotate(${Math.sin(t * 30) * 2 * clamp(1 - (t - W('pardon', a1)) / .6)}deg)`;
  show(jF, t, W('annene', a1), j1, 'up');
}

/* ---------- ABILITY BADGES + CHIPS ---------- */
function badge(key, name, sub, icon, small) { return h(`<div class="abs panel badge"><div class="key ${small ? 'small' : ''}">${key}</div><img src="${A}${icon}"><div class="txt"><div class="sub">${sub}</div><div class="nm">${name}</div></div></div>`) }
const badges = [
  [badge('P', 'Dövüşçü İnadı', 'PASİF', 'SettP.png', true), ...T.passive],
  [badge('Q', 'Yapıştır', 'YETENEK · Q', 'SettQ.png'), ...T.q],
  [badge('W', 'Balyoz Gibi', 'YETENEK · W', 'SettW.png'), ...T.w],
  [badge('E', 'Surat Dağıtan', 'YETENEK · E', 'SettE.png'), ...T.e],
  [badge('R', 'Yürek Hoplatan', 'ULTİ · R', 'SettR.png'), ...T.r]];
const chipBox = h(`<div class="abs chips"></div>`);
const q0 = T.q[0], w0 = T.w[0], e0 = T.e[0], r0 = T.r[0], E0 = T.early[0], M0 = T.mid[0], L0 = T.late[0];
const chipDefs = [
  ['Saldırı sıfırlama', 'gold', q0 + .4, T.q[1]], ['Sonraki 2 saldırı: <b>+menzil +hasar</b>', 'gold', W('iki', q0), T.q[1]], ['Şampiyona koşarken <b>+hız</b>', 'gold', W('hareket', q0), T.q[1]],
  ['Aldığın hasar = <b>İnat</b>', 'gold', W('aldığı', w0), W('sonra', w0)], ['Tüm İnat → <b>kalkan</b>', 'purple', W('kalkan', w0), T.w[1]], ['Koni hasarı İnat ile artar', 'gold', W('sonra', w0) + .6, T.w[1]], ['Merkez = <b>gerçek hasar</b>', 'red', W('ortasında', w0), T.w[1]], ['Geç oyun: <b>tek atar</b>', 'red', W('resmen', w0), T.w[1]],
  ['Ön + arka, dikdörtgen', 'gold', W('önüne', e0), T.e[1]], ['Hasar + yavaşlatma', 'gold', W('yavaşlıyor', e0), T.e[1]], ['İki taraftan çek = <b>SERSEMLET</b>', 'red', W('iki', e0 + 3), T.e[1]],
  ['Hedefli: yakala, zıpla, <b>çak</b>', 'gold', W('yakalayıp', r0), T.r[1]], ['İndiği alana hasar + yavaşlatma', 'gold', W('çevresindeki', r0), T.r[1]], ['Hasar = hedefin <b>ekstra canı</b>', 'purple', W('ekstra', r0), T.r[1]], ['Tank yakala = <b>takım silinir</b>', 'red', W('tankı', r0), T.r[1]],
  ['Bol farm, görevi erken bitir', 'gold', W('farm', E0), W('bunun', E0)], ['Seviye 1\'de çok güçlüsün', 'green', W('güçlü', E0), W('bunun', E0)],
  ['Kitin = <b>trade</b> aramak', 'gold', W('trade', E0), W('ama', E0 + 20)], ['E: minyon + rakip → <b>SERSEMLET</b>', 'red', W('minyonu', E0), W('ama', E0 + 20)], ['2 bedava oto', 'gold', W('bedava', E0), W('ama', E0 + 20)], ['Q + 2 oto + hareket hızı', 'gold', W('ardından', E0 + 15), W('ama', E0 + 20)], ['W ile <b>bitir</b>', 'purple', W('bitiriyorsun', E0), W('ama', E0 + 20)],
  ['E kaçtı mı? <b>Dikkatli oyna</b>', 'red', W('kaçırırsan', E0), T.early[1]], ['Seviye 6: dalış güçlenir', 'green', W('6', E0 + 25), T.early[1]], ['Kule altına çek, <b>çak</b>', 'gold', W('kulenin', E0 + 30), T.early[1]],
  ['Kuleyi erken al', 'gold', W('kuleni', M0), T.mid[1]], ['Split push ya da takım savaşı', 'gold', W('split', M0), T.mid[1]],
  ['Hedef: <b>dev bir ulti</b>', 'gold', W('dev', L0), T.late[1]], ['Tankı yakala, arka hatta <b>çak</b>', 'purple', W('tankını', L0), T.late[1]], ['E ile takımı sersemlet', 'red', W('sonra', L0 + 6), T.late[1]], ['W ile <b>tek at</b>', 'red', W('tek', L0 + 6), T.late[1]], ['Fırsat yoksa: önden arkaya', 'green', W('önden', L0), T.late[1]]
];
const chips = chipDefs.map(([tx, c, t0, t1]) => { const w = document.createElement('div'); w.className = 'chipwrap'; const e = h(`<div class="chip ${c}">${tx}</div>`); w.appendChild(e); chipBox.appendChild(w); return [w, e, t0, t1] });
const pcard = h(`<div class="abs panel pcard"><div class="hd"><img src="${A}SettP.png">DÖVÜŞÇÜ İNADI</div>
<div class="ln">Eksik canı arttıkça <b>can yenilenmesi artar</b>.</div>
<div class="ln">Sol yumruk: normal saldırı.</div>
<div class="ln">Sağ yumruk: <b>+menzil, +saldırı hızı, +hasar</b>.</div></div>`);
const pl = [...pcard.querySelectorAll('.ln')];
const plT = [W('eksik', T.passive[0]), W('sol', T.passive[0] + 5), W('sağ', T.passive[0] + 9)];
const grit = h(`<div class="abs panel grit"><div class="lbl"><span>İNAT</span><span id="gv">0</span></div><div class="bar"><div class="fill" id="gf"></div></div></div>`);
const gf = grit.querySelector('#gf'), gv = grit.querySelector('#gv');
const gA = w0 + .6, gB = W('harcayıp', w0), gC = gB + .8;

/* ---------- COMBO BAND ---------- */
const band = h(`<div class="abs band"><div class="ttl" id="bt"></div><div class="row" id="br"></div></div>`);
const bt = band.querySelector('#bt'), br = band.querySelector('#br');
const ic = { Q: 'SettQ.png', W: 'SettW.png', E: 'SettE.png', R: 'SettR.png' };
function comboRow(steps) {
  br.innerHTML = ''; const els = []; steps.forEach(([k, t0], i) => {
    if (i) br.insertAdjacentHTML('beforeend', '<div class="arrow">›</div>');
    const e = ic[k] ? h(`<div class="step"><img src="${A}${ic[k]}"><div class="k">${k}</div></div>`) : h(`<div class="step auto">${k}</div>`);
    br.appendChild(e); els.push([e, t0])
  }); return els
}
const c0 = T.combo[0], c2 = W('dalış', c0);
const s1 = SEQ(['e', 'iki', 'q', 'iki', 'ulti', 'iki', 'w'], c0 + .5);
const s2 = SEQ(['ulti', 'e', 'iki', 'q', 'bir', 'w'], c2);
const combo1 = ['E', '2 OTO', 'Q', '2 OTO', 'R', '2 OTO', 'W'].map((k, i) => [k, s1[i]]);
const combo2 = ['R', 'E', '2 OTO', 'Q', 'OTO', 'W'].map((k, i) => [k, s2[i]]);
let curCombo = 0, comboEls = [];

/* ---------- FULL SCENES ---------- */
const fulls = [];
function scene(bgimg, sec) { const s = h(`<div class="abs scene"><div class="bg" style="background-image:url(${A}${bgimg})"></div></div>`); fulls.push([s, ...T[sec]]); return s }
// matchups
const sm = scene('splash_0.jpg', 'match'); const m0 = T.match[0];
sm.insertAdjacentHTML('beforeend', `<div class="title">EŞLEŞMELER</div>
<div class="abs" style="left:660px;top:200px;width:600px;height:760px;background:url(${A}splash_0.jpg) 58% 30%/auto 130%;border-radius:26px;box-shadow:0 0 0 4px rgba(255,255,255,.25)"></div>`);
const sEasy = h(`<div class="side" style="left:70px;background:linear-gradient(180deg,rgba(30,120,70,.92),rgba(12,50,30,.92))"><h2>KOLAY</h2><div class="icons"><img src="${A}champ_Yasuo.png"><img src="${A}champ_Irelia.png"><img src="${A}champ_Rumble.png"></div><div class="cap">Yüksek hasar, düşük dayanıklılık.</div><div class="cap" style="color:#d9ffe9">Sana bol İnat verir, tek atarsın.</div></div>`);
const sHard = h(`<div class="side" style="left:1290px;background:linear-gradient(180deg,rgba(150,30,45,.92),rgba(60,10,18,.92))"><h2>ZOR</h2><div class="icons"><img src="${A}champ_Quinn.png"><img src="${A}champ_Teemo.png"><img src="${A}champ_Kennen.png"></div><div class="cap">Uzaktan kite atanlar.</div><div class="cap" style="color:#ffd9dd">Alan kontrolüyle seni uzak tutanlar.</div></div>`);
sm.appendChild(sEasy); sm.appendChild(sHard);
const vs = h(`<div class="vs"><div class="ring"></div><div class="t">VS</div></div>`); sm.appendChild(vs);
for (let i = 0; i < 12; i++) { const r = document.createElement('div'); r.className = 'ray'; r.style.transform = `rotate(${i * 30}deg) translateY(150px)`; vs.insertBefore(r, vs.firstChild) }
const vsRing = vs.querySelector('.ring'), vsT = vs.querySelector('.t'), rays = [...vs.querySelectorAll('.ray')];
const hardIc = [W('queen', m0, m0 + .8), W('teemo', m0), W('kennen', m0)], easyIc = [W('yasuo', m0), W('Irelia', m0), W('rumble', m0)];
// runes
const sr = scene('splash_56.jpg', 'runes'); const ru0 = T.runes[0];
sr.insertAdjacentHTML('beforeend', `<div class="title">RÜN<span>LER</span></div>
<div class="tag" style="left:250px;top:215px"><img src="${A}rune_7201_Precision.png" style="width:44px;vertical-align:middle;margin-right:12px">İSABET</div>
<div class="tag" style="left:1260px;top:215px"><img src="${A}rune_7204_Resolve.png" style="width:44px;vertical-align:middle;margin-right:12px">AZİM</div>`);
function rcard(parent, x, y, img, name, big) { const c = h(`<div class="card ${big ? 'lg' : ''}" style="left:${x}px;top:${y}px"><img src="${A}${img}" style="border-radius:50%;background:#140d22"><div class="n">${name}</div></div>`); parent.appendChild(c); return c }
const runeCards = [[rcard(sr, 140, 300, 'rune_Conqueror.png', 'Yenilmez', 1), W('yenilmez', ru0)], [rcard(sr, 430, 320, 'rune_Triumph.png', 'Zafer'), W('zafer', ru0)], [rcard(sr, 680, 320, 'rune_LegendAlacrity.png', 'Efsane: Çeviklik'), W('efsane', ru0)], [rcard(sr, 430, 600, 'rune_LastStand.png', 'Son Direniş'), W('son', ru0)],
[rcard(sr, 1180, 320, 'rune_SecondWind.png', 'İkinci Şans'), W('ikinci', ru0)], [rcard(sr, 1450, 320, 'rune_Unflinching.png', 'Gözü Kara'), W('gözü', ru0)]];
const shards = h(`<div class="abs" style="left:1130px;top:640px;width:700px"></div>`); sr.appendChild(shards);
const shT = runeCards[5][1] + .7;
const shardEls = ['Saldırı hızı', 'Uyarlanabilir güç', 'Ölçeklenen can'].map((s, i) => { const w = document.createElement('div'); w.className = 'chipwrap'; const e = h(`<div class="chip purple" style="font-size:34px">${s}</div>`); w.appendChild(e); shards.appendChild(w); return [e, shT + i * .25] });
const conqT = W('set', ru0 + 4);
const conqGlow = h(`<div class="abs chip red" style="left:110px;top:880px;font-size:40px">Yenilmez'i <b>çok kolay doldurur</b></div>`); sr.appendChild(conqGlow);
// items
const si = scene('splash_66.jpg', 'items'); const it0 = T.items[0];
si.insertAdjacentHTML('beforeend', `<div class="title">EŞYA<span>LAR</span></div>`);
function rowLabel(p, y, txt) { p.insertAdjacentHTML('beforeend', `<div class="tag" style="left:110px;top:${y}px">${txt}</div>`) }
rowLabel(si, 250, 'BAŞLANGIÇ'); rowLabel(si, 500, 'ÇEKİRDEK'); rowLabel(si, 780, 'DURUMA GÖRE');
function icard(x, y, id, name) { const c = h(`<div class="card" style="left:${x}px;top:${y}px"><img src="${A}item_${id}.png" style="width:130px;height:130px"><div class="n" style="font-size:28px">${name}</div></div>`); si.appendChild(c); return c }
const itemCards = [[icard(420, 200, 1055, "Doran'ın Kılıcı"), W('dora', it0)], [icard(660, 200, 2003, 'Can İksiri'), W('can', it0)],
[icard(420, 450, 6631, 'Hızkesen'), W('hız', it0)], [icard(700, 450, 3047, 'Çelik Kaplamalı Çizme'), W('çelik', it0)], [icard(980, 450, 3071, 'Kara Balta'), W('kara', it0)], [icard(1260, 450, 2501, 'Savaş Beyinin Kan Zırhı'), W('savaş', it0)],
[icard(420, 730, 3053, "Sterak'ın Güvencesi"), W('sterak', it0)], [icard(700, 730, 3181, 'Omurgakıran'), W('omurga', it0)]];
const itemArrows = [[620, 505, 3], [900, 505, 4], [1180, 505, 5]].map(([x, y, k]) => { const a = h(`<div class="abs arrow" style="left:${x}px;top:${y}px;font-size:70px">›</div>`); si.appendChild(a); return [a, itemCards[k][1]] });
// skills
const ss = scene('splash_45.jpg', 'skills'); const sk0 = T.skills[0];
ss.insertAdjacentHTML('beforeend', `<div class="title">YETENEK <span>SIRASI</span></div>`);
const order = ['E', 'Q', 'W', 'Q', 'Q', 'R', 'Q', 'W', 'Q', 'W', 'R', 'W', 'W', 'E', 'E', 'R', 'E', 'E'];
let gh = '<tr><td class="hd ic"></td>' + order.map((_, i) => `<td class="hd">${i + 1}</td>`).join('') + '</tr>';
['Q', 'W', 'E', 'R'].forEach(k => { gh += `<tr><td class="ic"><img src="${A}${ic[k]}"></td>` + order.map((o, i) => `<td data-k="${k}" data-l="${i}"></td>`).join('') + '</tr>' });
const grid = h(`<table class="grid">${gh}</table>`); ss.appendChild(grid);
const sq = SEQ(['e', 'q', 'w'], sk0 + .5); const maxT = W('ardından', sk0), ultT = W('ulti', sk0 + 3);
const lvlT = order.map((_, i) => i < 3 ? sq[i] : maxT + (i - 3) * ((T.skills[1] - .6 - maxT) / 15));
const cells = [...grid.querySelectorAll('td[data-k]')].filter(c => order[+c.dataset.l] === c.dataset.k);
const maxChip = h(`<div class="abs chip" style="left:170px;top:760px;font-size:44px">Maks sırası: <b>Q › W › E</b></div>`); ss.appendChild(maxChip);
const ultChip = h(`<div class="abs chip purple" style="left:820px;top:760px;font-size:44px">Ultiyi her fırsatta al: <b>6 · 11 · 16</b></div>`); ss.appendChild(ultChip);
// summoners
const su = scene('splash_8.jpg', 'summ');
su.insertAdjacentHTML('beforeend', `<div class="title">SİHİRDAR <span>BÜYÜLERİ</span></div>`);
const sF = h(`<div class="card lg" style="left:600px;top:340px"><img src="${A}SummonerFlash.png" style="width:260px;height:260px"><div class="n" style="font-size:48px">Sıçra</div></div>`);
const sI = h(`<div class="card lg" style="left:1060px;top:340px"><img src="${A}SummonerDot.png" style="width:260px;height:260px"><div class="n" style="font-size:48px">Tutuştur</div></div>`);
su.appendChild(sF); su.appendChild(sI);
const flashFx = h(`<div class="abs" style="inset:0;background:radial-gradient(circle at 730px 470px,rgba(240,255,160,.9),rgba(240,255,160,0) 40%)"></div>`); su.appendChild(flashFx);
const ignFx = h(`<div class="abs" style="inset:0;background:radial-gradient(circle at 1190px 470px,rgba(255,120,40,.85),rgba(255,120,40,0) 40%)"></div>`); su.appendChild(ignFx);

/* ---------- PHASES ---------- */
const banners = [['EARLY GAME', T.early[0]], ['MID GAME', T.mid[0]], ['LATE GAME', T.late[0]]].map(([tx, t0]) => [h(`<div class="abs banner"><div>${tx}</div></div>`), t0]);
const phase = h(`<div class="abs phase"><div id="ph"></div></div>`); const ph = phase.querySelector('#ph');

/* ---------- CTA ---------- */
const cta0 = T.cta[0], finT = W('koridorda', cta0);
const odim = h(`<div class="abs dim"></div>`);
const oNext = h(`<div class="abs big" style="top:300px;font-size:96px">Sıradaki şampiyon?<div style="font-size:64px;color:var(--gold);margin-top:20px">Yorumlara yaz</div></div>`);
const oSub = h(`<div class="abs sub"><div class="subbtn">▶ ABONE OL</div></div>`);
const fin = h(`<div class="abs scene"><div class="abs" style="inset:0;background:url(${A}splash_0.jpg) center/cover"></div><div class="abs" style="inset:0;background:linear-gradient(0deg,rgba(8,5,14,.95) 0,rgba(8,5,14,.5) 55%,rgba(8,5,14,.2) 100%)"></div></div>`);
const finEls = [['Koridorda acımasız ol,', finT + .1, 'var(--cream)', 700], ['ama annene iyi davran. <span class="heart">♥</span>', W('ama', finT), 'var(--gold)', 825]].map(([tx, t0, col, y]) => { const e = h(`<div class="abs big" style="top:${y}px;font-size:104px;color:${col}">${tx}</div>`); fin.appendChild(e); return [e, t0] });

/* ---------- RENDER ---------- */
const inS = (t, k) => t >= T[k][0] && t < T[k][1];
window.render = function (t) {
  introR(t);
  fulls.forEach(([s, a, b]) => show(s, t, a, b, 'fade', .3));
  badges.forEach(([b, a, c]) => { if (show(b, t, a, c, 'slideL', .35)) { const k = b.querySelector('.key'); const p = t - a; k.style.boxShadow = p < 1.2 ? `0 0 ${40 * (1 - p / 1.2)}px rgba(244,185,66,.9)` : '' } });
  chips.forEach(([w, e, t0, t1]) => { const v = t >= t0 && t < t1; w.style.display = v ? '' : 'none'; if (v) show(e, t, t0, t1, 'slideL', .3) });
  show(pcard, t, T.passive[0] + .2, T.passive[1], 'pop');
  pl.forEach((e, i) => e.style.opacity = t >= plT[i] ? 1 : 0);
  if (show(grit, t, w0 + .2, T.w[1], 'drop')) {
    let v = t < gA ? 0 : t < gB ? (t - gA) / (gB - gA) : t < gC ? 1 - (t - gB) / (gC - gB) : 0; gf.style.width = (clamp(v) * 100) + '%'; gv.textContent = Math.round(clamp(v) * 100)
  }
  if (show(band, t, T.combo[0], T.combo[1], 'up')) {
    const want = t < c2 ? 1 : 2; if (want !== curCombo) { curCombo = want; comboEls = comboRow(want === 1 ? combo1 : combo2); bt.textContent = want === 1 ? 'UZUN SAVAŞ KOMBOSU' : 'DALIŞ KOMBOSU' }
    comboEls.forEach(([e, t0]) => { const on = t >= t0; e.classList.toggle('on', on); e.style.transform = on ? `scale(${1 + .12 * clamp(1 - (t - t0) / .3)})` : '' })
  }
  if (inS(t, 'match')) {
    show(sHard, t, m0 + .3, T.match[1], 'slideR', .4); show(sEasy, t, easyIc[0] - .3, T.match[1], 'slideL', .4);
    [...sHard.querySelectorAll('img')].forEach((e, i) => show(e, t, hardIc[i], T.match[1], 'pop')); [...sEasy.querySelectorAll('img')].forEach((e, i) => show(e, t, easyIc[i], T.match[1], 'pop'));
    [...sHard.querySelectorAll('.cap')].forEach((e, i) => e.style.opacity = t >= (i ? W('alan', m0) : W('kite', m0)) ? 1 : 0); [...sEasy.querySelectorAll('.cap')].forEach((e, i) => e.style.opacity = t >= (i ? W('çünkü', m0) : W('hasarı', m0)) ? 1 : 0);
    const vt = t - (m0 + .5);
    if (show(vs, t, m0 + .5, T.match[1], 'pop', .35)) {
      vsT.style.transform = `scale(${1 + .06 * Math.sin(t * 6)}) rotate(${-6 + 3 * Math.sin(t * 2)}deg)`;
      vsRing.style.transform = `scale(${1 + .5 * clamp(1 - vt / .5) + .04 * Math.sin(t * 6)})`; vsRing.style.opacity = .5 + .5 * Math.abs(Math.sin(t * 3));
      rays.forEach((r, i) => { r.style.opacity = .35 + .35 * Math.sin(t * 5 + i); r.parentNode && (r.style.transform = `rotate(${i * 30 + t * 25}deg) translateY(150px)`) })
    }
  }
  if (inS(t, 'runes')) {
    runeCards.forEach(([c, t0]) => show(c, t, t0, T.runes[1], 'pop')); shardEls.forEach(([e, t0]) => show(e, t, t0, T.runes[1], 'slideR')); show(conqGlow, t, conqT, T.runes[1], 'up');
    runeCards[0][0].querySelector('img').style.boxShadow = t >= conqT ? `0 0 ${30 + 20 * Math.sin(t * 8)}px rgba(255,190,80,.9)` : ''
  }
  if (inS(t, 'items')) { itemCards.forEach(([c, t0]) => show(c, t, t0, T.items[1], 'pop')); itemArrows.forEach(([a, t0]) => show(a, t, t0, T.items[1], 'fade')) }
  if (inS(t, 'skills')) {
    cells.forEach(c => { const l = +c.dataset.l; const on = t >= lvlT[l]; c.classList.toggle('on', on); c.classList.toggle('r', c.dataset.k === 'R'); c.textContent = on ? c.dataset.k : ''; c.style.transform = on ? `scale(${.7 + .3 * eb((t - lvlT[l]) / .25)})` : '' });
    show(maxChip, t, maxT, T.skills[1], 'up'); show(ultChip, t, ultT, T.skills[1], 'up')
  }
  if (inS(t, 'summ')) {
    const f = CUES.flash, g = CUES.ignite;
    show(sF, t, f - .15, T.summ[1], 'pop'); show(sI, t, g - .15, T.summ[1], 'pop');
    flashFx.style.opacity = clamp(1 - Math.abs(t - f) / .35); ignFx.style.opacity = t >= g ? clamp(1 - (t - g) / .9) * (.7 + .3 * Math.sin(t * 40)) : 0
  } else { flashFx.style.opacity = 0; ignFx.style.opacity = 0 }
  banners.forEach(([b, t0]) => { if (show(b, t, t0, t0 + 2.0, 'pop', .3)) { const d = b.firstChild; const p = t - t0; d.style.clipPath = `inset(0 ${100 - 100 * eo(p / .35)}% 0 0)` } });
  const pn = inS(t, 'early') ? 'EARLY GAME' : inS(t, 'mid') ? 'MID GAME' : inS(t, 'late') ? 'LATE GAME' : '';
  ph.textContent = pn; const bannerOn = banners.some(([b, t0]) => t >= t0 && t < t0 + 2); phase.style.display = (pn && !bannerOn) ? '' : 'none';
  show(odim, t, cta0, 240.5, 'fade', .4); show(oNext, t, cta0 + .1, W('abone', cta0) + .4, 'up'); show(oSub, t, W('abone', cta0), finT, 'pop', .3);
  show(fin, t, finT - .25, 240.5, 'fade', .35); finEls.forEach(([e, t0]) => show(e, t, t0, 240.5, 'up', .4));
  fin.firstChild.style.transform = `scale(${1.04 + .03 * clamp((t - finT) / 7)})`;
};
window.ready = Promise.all([document.fonts.ready, ...[...document.images].map(i => i.decode().catch(() => { }))]);
window.render(0);
