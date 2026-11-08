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
T.hook = [0, W('bu', 4)]; T.eyes = [T.hook[1], W('bugün', 8)]; T.hook2 = [T.eyes[1], W('neden', 18)];
T.why = [T.hook2[1], W('rengar', 31)]; T.passive = [T.why[1], W('q', 71)]; T.q = [T.passive[1], W('w', 76)];
T.w = [T.q[1], W('e', 88)]; T.e = [T.w[1], W('ve', 94)]; T.r = [T.e[1], W('kombolara', 123)];
T.combo = [T.r[1], W('eşleş', 136)]; T.match = [T.combo[1], W('rün', 156)]; T.runes = [T.match[1], W('eşyalarda', 163)];
T.items = [T.runes[1], W('yetenek', 174)]; T.skills = [T.items[1], W('sihirdar', 182)]; T.summ = [T.skills[1], W('örlü', 184, 184.9)];
T.early = [T.summ[1], W('midgame', 203)]; T.mid = [T.early[1], W('late', 207)]; T.late = [T.mid[1], W('ve', 220)]; T.cta = [T.late[1], 240.5];
const finT = W('4', 234, 234.8);
window.CUES = { T, flash: W('sıçra', T.summ[0]), smite: W('çarp', T.summ[0]), uyari: W('belirdiyse', 4) - .35, tek: W('tek', 5), marks: M };

/* ---------- COUNTDOWN (covers the burned-in timer, top right) ---------- */
const cd = h(`<div class="abs" style="z-index:50;right:0;top:0;width:300px;height:104px;background:#010A13;border-left:4px solid #C8AA6E;border-bottom:4px solid #C8AA6E;box-sizing:border-box;display:flex;align-items:center;gap:14px;padding-left:22px">
 <div style="font-family:Ant;font-size:64px;color:#FFC23D;text-shadow:0 4px 0 #000;letter-spacing:.02em" id="cdv">4:00</div>
 <div style="font-family:Osw;font-weight:700;font-size:20px;letter-spacing:.18em;color:#0AC8B9;line-height:1.2">KALAN<br>SÜRE</div></div>`);
const cdv = cd.querySelector('#cdv');

/* ---------- quote subtitles for Rengar's own lines ---------- */
const QUOTES = { avin_kokusu: 'Avın kokusu...' };
const quoteEls = Object.entries(QUOTES).filter(([k, v]) => v && M[k]).map(([k, v]) => [h(`<div class="abs" style="left:0;right:0;top:${k === 'avin_kokusu' ? 430 : 820}px;text-align:center"><span style="font-family:Ant;font-size:${k === 'avin_kokusu' ? 150 : 92}px;color:#FFF8EC;text-shadow:0 6px 0 #000,0 0 30px rgba(0,0,0,.9);padding:0 30px">"${v}"</span></div>`), M[k][0], M[k][1] + .35]);

/* ---------- HOOK ---------- */
const redv = h(`<div class="abs" style="inset:0;background:radial-gradient(ellipse at center,rgba(120,0,10,0) 30%,rgba(120,0,10,.75) 100%)"></div>`);
const veil = h(`<div class="abs" style="inset:0;background:#000"></div>`);
const eyes = h(`<div class="abs" style="left:510px;top:90px;width:900px;height:900px;background:url(${A}mark_hd.png) center/contain no-repeat"></div>`);
const nameHide = h(`<div class="abs" style="left:640px;top:340px;width:620px;height:100px;background:radial-gradient(ellipse at center,rgba(18,28,22,.97) 55%,rgba(18,28,22,0) 100%)"></div>`);
const ring = h(`<div class="abs" style="left:814px;top:470px;width:280px;height:150px;border:10px solid #FF3B4E;border-radius:50%;box-shadow:0 0 40px #FF3B4E"></div>`);
const arrow = h(`<div class="abs" style="left:1130px;top:300px;font-family:Ant;font-size:120px;color:#FF3B4E;text-shadow:0 6px 0 #000;transform-origin:left">↙</div>`);
const hookTxt = h(`<div class="abs" style="left:0;right:0;top:860px;text-align:center"><span style="font-family:Ant;font-size:86px;color:#FFF8EC;text-shadow:0 6px 0 #000,0 0 30px rgba(0,0,0,.9)">KAFANIN ÜSTÜNDE <span style="color:#FF3B4E">BU</span> BELİRDİYSE...</span></div>`);
const tekStamp = h(`<div class="abs" style="left:0;right:0;top:330px;text-align:center"><span style="font-family:Ant;font-size:300px;color:#FFC23D;text-shadow:0 12px 0 #000,0 0 60px rgba(255,60,60,.8);display:inline-block">TEK!</span></div>`);
const title = h(`<div class="abs" style="left:0;right:0;top:300px;text-align:center"><div style="font-family:Ant;font-size:130px;color:#FFF8EC;text-shadow:0 8px 0 #000;line-height:1.15"><span style="font-size:190px;color:#FFC23D;display:inline-block;transform:skewX(-12deg);margin-right:20px">4</span>DAKİKADA <span style="color:#FFC23D">RENGAR</span></div></div>`);
const promise = h(`<div class="abs" style="left:0;right:0;top:560px;text-align:center"><span class="chip red" style="font-size:44px">VİDEONUN SONUNDA: Rengar'a karşı <b>tek yememenin</b> tek yolu</span></div>`);
const flashW = h(`<div class="abs" style="inset:0;background:#fff"></div>`);
function hookR(t) {
  const he = T.hook[1];
  if (show(veil, t, 0, he, 'cut')) veil.style.opacity = 1 - .55 * eo(t / he);
  if (show(eyes, t, .15, he, 'cut')) { const p = clamp((t - .15) / (he - .4)); const fl = .85 + .15 * Math.sin(t * 9) * Math.sin(t * 3.7);
    eyes.style.opacity = clamp(eo(p) * 1.15) * fl; eyes.style.transform = `scale(${.72 + .4 * eo(p)})`; eyes.style.filter = `brightness(${.35 + .9 * p}) drop-shadow(0 0 ${20 + 60 * p}px rgba(70,160,255,${.35 + .45 * p}))` }
  if (show(redv, t, 0, T.eyes[1], 'cut')) redv.style.opacity = .6 + .4 * Math.abs(Math.sin(t * 3.2));
  show(nameHide, t, T.eyes[0], T.eyes[1], 'cut');
  if (show(ring, t, CUES.uyari, T.eyes[1], 'pop', .25)) ring.style.transform += ` scale(${1 + .05 * Math.sin(t * 14)})`;
  show(arrow, t, CUES.uyari + .15, T.eyes[1], 'pop', .25);
  show(hookTxt, t, CUES.uyari, T.eyes[1], 'up');
  show(tekStamp, t, CUES.tek, Math.min(CUES.tek + 1.3, T.hook2[0] - .05), 'slam', .3);
  flashW.style.display = (t >= CUES.tek - .02 && t < CUES.tek + .25) ? '' : 'none'; flashW.style.opacity = clamp(1 - (t - CUES.tek) / .25);
  show(title, t, T.hook2[0], W('videonun', 8), 'pop', .35);
  show(promise, t, W('videonun', 8), (M.gel_bakalim || [T.why[0]])[0], 'up');
}

/* ---------- WHY (pros / cons) ---------- */
function listCol(x, ttl, color, rows, t1) {
  const c = h(`<div class="abs" style="left:${x}px;top:140px;width:640px"></div>`);
  const t = h(`<div style="font-family:Ant;font-size:72px;color:${color};text-shadow:0 5px 0 #000;margin-bottom:14px">${ttl}</div>`); c.appendChild(t);
  const rs = rows.map(([txt, t0]) => { const r = h(`<div class="chip ${color === 'var(--green)' ? 'green' : 'red'}" style="font-size:40px">${txt}</div>`); const w = document.createElement('div'); w.className = 'chipwrap'; w.appendChild(r); c.appendChild(w); return [r, t0] });
  return [c, t, rs]
}
const w0 = T.why[0];
const pros = listCol(70, 'ARTILAR', 'var(--green)', [['Arka hattı saniyede siler', W('arka', w0)], ['Güçlendirilmiş yetenekler', W('güçlendirilmiş', w0)], ['Kill aldıkça durdurulamaz', W('birkaç', w0)]]);
const cons = listCol(1170, 'EKSİLER', 'var(--red)', [['Öğrenmesi zor', W('ama', w0)], ['Tanklara karşı zayıf', W('tanklara', w0)]]);
const adc = h(`<div class="abs" style="left:0;right:0;top:820px;text-align:center"><span style="font-family:Ant;font-size:78px;color:#FFF8EC;text-shadow:0 6px 0 #000">ADC'LER İÇİN <span style="color:#FF3B4E">KORKU FİLMİ</span>, TANKLAR İÇİN <span style="color:#FFC23D">SOKAK KEDİSİ</span></span></div>`);

/* ---------- BADGES + CHIPS ---------- */
function badge(key, name, sub, icon, small) { return h(`<div class="abs panel badge"><div class="key ${small ? 'small' : ''}">${key}</div><img src="${A}${icon}"><div class="txt"><div class="sub">${sub}</div><div class="nm">${name}</div></div></div>`) }
const badges = [[badge('P', 'Görünmez Yırtıcı', 'PASİF', 'RengarP.png', true), ...T.passive], [badge('Q', 'Yabani', 'YETENEK · Q', 'RengarQ.png'), ...T.q],
[badge('W', 'Savaş Kükremesi', 'YETENEK · W', 'RengarW.png'), ...T.w], [badge('E', 'Bola Atışı', 'YETENEK · E', 'RengarE.png'), ...T.e], [badge('R', 'Av Heyecanı', 'ULTİ · R', 'RengarR.png'), ...T.r]];
const chipBox = h(`<div class="abs chips"></div>`);
const p0 = T.passive[0], q0 = T.q[0], wq = T.w[0], e0 = T.e[0], r0 = T.r[0], E0 = T.early[0], M0 = T.mid[0], L0 = T.late[0];
const bush = W('ikinci', p0), troph = W('üçüncü', p0);
const chipDefs = [
  ['Yetenek = <b>1 Vahşet</b> yükü', 'gold', W('normal', p0), bush], ['4 yük = <b>güçlü yetenek</b> + hız', 'red', W('4', p0), bush],
  ['Çalıdan <b>sıçrar</b>', 'gold', W('çaladayken', p0, bush + 1.5), troph], ['Çalı = <b>Rengar\'ın evi</b>', 'purple', W('kısacası', p0), troph],
  ['Her yeni kill = <b>ganimet</b>', 'gold', W('her', troph), T.passive[1]], ['Ganimet = <b>+saldırı gücü</b>', 'red', W('katlanarak', troph), T.passive[1]], ['Kafa koleksiyonu. <b>Hobi işte.</b>', 'purple', W('herkesin', troph), T.passive[1]],
  ['Saldırı sıfırlama + <b>hız</b>', 'gold', q0 + .4, T.q[1]], ['2 güçlü saldırı', 'gold', W('sonraki', q0), T.q[1]],
  ['Hasar → <b>gri can</b>', 'gold', W('aldığı', wq), T.w[1]], ['Güçlü W: <b>tüm CC temizlenir</b>', 'purple', W('güçlendirilmiş', wq), T.w[1]], ['Stun mu yedin? <b>KÜKRE.</b>', 'red', W('stan', wq, W('kükre', wq)), T.w[1]],
  ['Bola: <b>yavaşlatır</b>', 'gold', e0 + .5, T.e[1]], ['Güçlü E: <b>KÖKLER</b>', 'red', W('güçlendirilmiş', e0), T.e[1]],
  ['14 sn <b>kamuflaj</b> + hız', 'gold', W('rengar', r0 + 2), (M.avin_kokusu || [T.r[1]])[0]], ['En yakın rakibi <b>görür</b>', 'purple', W('en', r0 + 2), (M.avin_kokusu || [T.r[1]])[0]], ['Sıçrama: <b>dev hasar + zırh kırma</b>', 'red', W('üstüne', r0), T.r[1]],
  ['Ormanı <b>tamamen</b> temizle', 'gold', E0 + .4, W('nehirden', E0)], ['Ulti\'ye kadar altın + tecrübe', 'gold', W('ultine', E0), W('nehirden', E0)],
  ['Nehirden gank = <b>kapı çalmak</b>', 'red', W('nehirden', E0), W('altıncı', E0)], ['Koridor çalısından <b>atla</b>', 'green', W('ama', E0 + 8), W('altıncı', E0)],
  ['Seviye 6: canı azalana <b>atla</b>', 'red', W('altıncı', E0), T.early[1]], ['Ulti → <b>objektif</b> → kartopu', 'gold', W('bu', E0 + 15), T.early[1]],
  ['Farm + pick + <b>objektif</b>', 'gold', M0 + .3, T.mid[1]],
  ['Savaşın başlamasını <b>bekle</b>', 'gold', W('savaşın', L0), T.late[1]], ['Büyük yetenekler gitti mi? <b>DAL</b>', 'red', W('büyük', L0), T.late[1]], ['Kediler gibi: izle, sonra <b>TEK</b>', 'purple', W('hediler', L0, W('gibi', L0 + 9)), T.late[1]]
];
const chips = chipDefs.map(([tx, c, t0, t1]) => { const w = document.createElement('div'); w.className = 'chipwrap'; const e = h(`<div class="chip ${c}">${tx}</div>`); w.appendChild(e); chipBox.appendChild(w); return [w, e, t0, t1] });
// ferocity pips
const fer = h(`<div class="abs panel" style="left:660px;top:36px;width:600px;height:96px;padding:14px 22px;box-sizing:border-box"><div style="font-family:Osw;font-weight:700;font-size:24px;letter-spacing:.14em;color:#FFC23D">VAHŞET</div><div style="display:flex;gap:14px;margin-top:8px" id="pips">${'<div style="flex:1;height:26px;border-radius:8px;background:#2a2238"></div>'.repeat(4)}</div></div>`);
const pips = [...fer.querySelectorAll('#pips div')];
// ult red flash + AVIN letters + age joke + kitty
const ultFlash = h(`<div class="abs" style="inset:0;background:radial-gradient(ellipse at center,rgba(150,0,10,.0) 20%,rgba(150,0,10,.85) 100%)"></div>`);
const avin = h(`<div class="abs" style="left:0;right:0;top:360px;text-align:center;font-family:Ant;font-size:230px;color:#FFC23D;text-shadow:0 12px 0 #000;letter-spacing:.2em"></div>`);
const letters = 'AVIN'.split('').map(c => { const s = document.createElement('span'); s.textContent = c; s.style.display = 'inline-block'; avin.appendChild(s); return s });
const age = h(`<div class="abs" style="left:0;right:0;top:640px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:80px;color:#fff;background:#E62117;padding:6px 34px 14px;border-radius:18px;text-shadow:0 5px 0 #7a0d19">+18 OLMASIN LÜTFEN</span></div>`);
const avT = W('evet', r0 + 6), letT = W('a', avT), harfT = W('bir', avT), ageT = W('bu', avT);
const letTs = [W('a', avT), W('ve', avT), W('I', avT + .3), W('ne', avT)];
const kitty = h(`<div class="abs scene"><div class="abs" style="inset:0;background:url(${A}splash_15.jpg) center/cover"></div><div class="abs" style="inset:0;background:linear-gradient(0deg,rgba(1,10,19,.9) 0,rgba(1,10,19,0) 50%)"></div>
 <div class="abs" style="left:0;right:0;top:700px;text-align:center;font-family:Ant;font-size:110px;color:#FFF8EC;text-shadow:0 7px 0 #000">SEVİMLİ KEDİ <span style="color:#FF8FC8">RENGAR</span></div>
 <div class="abs" id="kst" style="left:0;right:0;top:860px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:96px;color:#FFC23D;text-shadow:0 7px 0 #000;transform:rotate(-4deg)">YİNE DE TEK ATAR.</span></div></div>`);
const kst = kitty.querySelector('#kst'); const kitT = W('arada', r0) - .3, kitT2 = W('ve', kitT + 1);

/* ---------- COMBO BAND ---------- */
const band = h(`<div class="abs band"><div class="ttl" id="bt"></div><div class="row" id="br"></div></div>`);
const bt = band.querySelector('#bt'), br = band.querySelector('#br');
const ic = { Q: 'RengarQ.png', W: 'RengarW.png', E: 'RengarE.png', R: 'RengarR.png' };
function comboRow(steps) {
  br.innerHTML = ''; const els = []; steps.forEach(([k, t0], i) => {
    if (i) br.insertAdjacentHTML('beforeend', '<div class="arrow">›</div>');
    const kk = k.replace('+', ''); const pw = k.endsWith('+');
    const e = ic[kk] ? h(`<div class="step" style="${pw ? 'border-color:#FF3B4E' : ''}"><img src="${A}${ic[kk]}"><div class="k" style="${pw ? 'background:#FF3B4E;color:#fff' : ''}">${pw ? 'GÜÇLÜ ' + kk : kk}</div></div>`) : h(`<div class="step auto">${k}</div>`);
    br.appendChild(e); els.push([e, t0])
  }); return els
}
const c0 = T.combo[0], c2 = W('hasar', c0);
function seqT(a, b, n) { return Array.from({ length: n }, (_, i) => a + (b - a) * i / (n - 1)) }
const s1 = seqT(W('saldırı', c0), W('vurmaya', c0, c2 - .8), 5), s2 = seqT(W('saldırı', c2), W('açmak', c2, T.combo[1] - .8), 4);
const combo1 = ['OTO', 'E', 'W', 'Q', 'E+'].map((k, i) => [k, s1[i]]), combo2 = ['OTO', 'E', 'Q', 'Q+'].map((k, i) => [k, s2[i]]);
let curCombo = 0, comboEls = [];

/* ---------- FULL SCENES ---------- */
const fulls = [];
function scene(bgimg, a, b) { const s = h(`<div class="abs scene"><div class="bg" style="background-image:url(${A}${bgimg})"></div></div>`); fulls.push([s, a, b]); return s }
const m0 = T.match[0], mm = W('rengar', m0 + 4);
// Kha'Zix joke
const kz = scene('splash_1.jpg', m0, mm);
kz.insertAdjacentHTML('beforeend', `<div class="abs" style="left:0;right:0;top:120px;text-align:center"><img src="${A}champ_Khazix.png" style="width:300px;height:300px;border-radius:24px;border:6px solid #FF3B4E;box-shadow:0 0 60px rgba(255,59,78,.6)"></div>
<div class="abs" id="kz1" style="left:0;right:0;top:470px;text-align:center;font-family:Ant;font-size:96px;color:#FFF8EC;text-shadow:0 6px 0 #000">KHA'ZIX: <span style="color:#FF3B4E">BİR GÖZÜNÜ ALDI</span></div>
<div class="abs" id="kz2" style="left:0;right:0;top:620px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:120px;color:#FFC23D;text-shadow:0 8px 0 #000;transform:rotate(-3deg)">SAKIN DİĞERİNİ VERME</span></div>`);
const kz1 = kz.querySelector('#kz1'), kz2 = kz.querySelector('#kz2');
// matchups
const sm = scene('splash_0.jpg', mm, T.match[1]);
sm.insertAdjacentHTML('beforeend', `<div class="title">EŞLEŞMELER</div><div class="abs" style="left:660px;top:200px;width:600px;height:760px;background:url(${A}splash_0.jpg) 62% 30%/auto 125%;border-radius:26px;box-shadow:0 0 0 4px rgba(255,255,255,.25)"></div>`);
const sEasy = h(`<div class="side" style="left:70px;background:linear-gradient(180deg,rgba(30,120,70,.92),rgba(12,50,30,.92))"><h2>KOLAY</h2><div class="icons"><img src="${A}champ_Talon.png"><img src="${A}champ_Graves.png"><img src="${A}champ_Kindred.png"></div><div class="cap">Kırılgan ormancılar.</div><div class="cap" style="color:#d9ffe9">Üstlerine atla, sil.</div></div>`);
const sHard = h(`<div class="side" style="left:1290px;background:linear-gradient(180deg,rgba(150,30,45,.92),rgba(60,10,18,.92))"><h2>ZOR</h2><div class="icons"><img src="${A}champ_Viego.png"><img src="${A}champ_Khazix.png"><img src="${A}champ_JarvanIV.png"></div><div class="cap">Dayanıklı olanlar.</div><div class="cap" style="color:#ffd9dd">Patlamanı boşa çıkaranlar.</div></div>`);
sm.appendChild(sEasy); sm.appendChild(sHard);
const vs = h(`<div class="vs"><div class="ring"></div><div class="t">VS</div></div>`); sm.appendChild(vs);
for (let i = 0; i < 12; i++) { const r = document.createElement('div'); r.className = 'ray'; vs.insertBefore(r, vs.firstChild) }
const vsRing = vs.querySelector('.ring'), vsT = vs.querySelector('.t'), rays = [...vs.querySelectorAll('.ray')];
const easyIc = [W('talon', mm), W('graves', mm), W('kindred', mm)], hardT = W('ama', mm), hardIc = [W('viego', mm), W('kazix', hardT), W('jarvan', hardT)];
// runes
const sr = scene('splash_2.jpg', ...T.runes); const ru0 = T.runes[0];
sr.insertAdjacentHTML('beforeend', `<div class="title">RÜN<span>LER</span></div>
<div class="tag" style="left:250px;top:215px"><img src="${A}rune_7201_Precision.png" style="width:44px;vertical-align:middle;margin-right:12px">İSABET</div>
<div class="tag" style="left:1260px;top:215px"><img src="${A}rune_7200_Domination.png" style="width:44px;vertical-align:middle;margin-right:12px">HÂKİMİYET</div>`);
function rcard(p, x, y, img, name, big) { const c = h(`<div class="card ${big ? 'lg' : ''}" style="left:${x}px;top:${y}px"><img src="${A}${img}" style="border-radius:50%;background:#140d22"><div class="n">${name}</div></div>`); p.appendChild(c); return c }
const runeCards = [[rcard(sr, 140, 300, 'rune_FleetFootwork.png', 'Ayağı Çabuk', 1), W('ayağa', ru0)], [rcard(sr, 430, 320, 'rune_Triumph.png', 'Zafer'), W('zafer', ru0)], [rcard(sr, 680, 320, 'rune_LegendAlacrity.png', 'Efsane: Çeviklik'), W('efsane', ru0)], [rcard(sr, 430, 600, 'rune_CutDown.png', 'Biç Devir'), W('biç', ru0, W('al', ru0 + 3))],
[rcard(sr, 1180, 320, 'rune_SuddenImpact.png', 'Ani Darbe'), W('anidarbe', ru0, W('ikincil', ru0) + 1)], [rcard(sr, 1450, 320, 'rune_UltimateHunter.png', 'Mükemmel Avcı'), W('mükemmel', ru0)]];
// items
const si = scene('splash_23.jpg', ...T.items); const it0 = T.items[0];
si.insertAdjacentHTML('beforeend', `<div class="title">EŞYA<span>LAR</span></div>`);
function rowLabel(p, y, txt) { p.insertAdjacentHTML('beforeend', `<div class="tag" style="left:110px;top:${y}px">${txt}</div>`) }
rowLabel(si, 250, 'BAŞLANGIÇ'); rowLabel(si, 500, 'ÇEKİRDEK'); rowLabel(si, 780, 'DURUMA GÖRE');
function icard(x, y, id, name) { const c = h(`<div class="card" style="left:${x}px;top:${y}px"><img src="${A}item_${id}.png" style="width:130px;height:130px"><div class="n" style="font-size:28px">${name}</div></div>`); si.appendChild(c); return c }
const itemCards = [[icard(420, 200, 1102, 'Yelgezer Yavrusu'), W('yelgezer', it0)], [icard(660, 200, 2003, 'Can İksiri'), W('caniksiri', it0, W('ve', it0 + 1))],
[icard(420, 450, 3179, 'Umbra Mızrağı'), W('umbra', it0)], [icard(700, 450, 3158, 'Ionia Çizmeleri'), W('ionye', it0, W('umbra', it0) + 1)], [icard(980, 450, 6698, 'İtikatsız Hydra'), W('itikatsız', it0)], [icard(1260, 450, 3036, "Dominik Efendi'nin Hürmetleri"), W('dominik', it0)],
[icard(420, 730, 3814, 'Gecenin Kıyısı'), W('gecenin', it0)]];
const allDesc = h(`<div class="abs chip red" style="left:760px;top:790px;font-size:44px">HEPSİ <b>AÇIKLAMADA</b></div>`); si.appendChild(allDesc); const descT = W('hepsi', it0);
// skills
const ss = scene('splash_30.jpg', ...T.skills); const sk0 = T.skills[0];
ss.insertAdjacentHTML('beforeend', `<div class="title">YETENEK <span>SIRASI</span></div>`);
const order = ['Q', 'W', 'E', 'Q', 'Q', 'R', 'Q', 'E', 'Q', 'E', 'R', 'E', 'E', 'W', 'W', 'R', 'W', 'W'];
let gh = '<tr><td class="hd ic"></td>' + order.map((_, i) => `<td class="hd">${i + 1}</td>`).join('') + '</tr>';
['Q', 'W', 'E', 'R'].forEach(k => { gh += `<tr><td class="ic"><img src="${A}${ic[k]}"></td>` + order.map((o, i) => `<td data-k="${k}" data-l="${i}"></td>`).join('') + '</tr>' });
const grid = h(`<table class="grid">${gh}</table>`); ss.appendChild(grid);
const sq = [W('q', sk0), W('w', sk0 + .5), W('e', sk0 + 1)]; const maxT = W('önce', sk0), ultT = W('ultiyi', sk0);
const lvlT = order.map((_, i) => i < 3 ? sq[i] : maxT + (i - 3) * ((T.skills[1] - .5 - maxT) / 15));
const cells = [...grid.querySelectorAll('td[data-k]')].filter(c => order[+c.dataset.l] === c.dataset.k);
const maxChip = h(`<div class="abs chip" style="left:170px;top:760px;font-size:44px">Maks sırası: <b>Q › E › W</b></div>`); ss.appendChild(maxChip);
const ultChip = h(`<div class="abs chip purple" style="left:820px;top:760px;font-size:44px">Ultiyi her fırsatta al: <b>6 · 11 · 16</b></div>`); ss.appendChild(ultChip);
// summoners
const su = scene('splash_40.jpg', ...T.summ);
su.insertAdjacentHTML('beforeend', `<div class="title">SİHİRDAR <span>BÜYÜLERİ</span></div>`);
const sF = h(`<div class="card lg" style="left:600px;top:340px"><img src="${A}SummonerFlash.png" style="width:260px;height:260px"><div class="n" style="font-size:48px">Sıçra</div></div>`);
const sS = h(`<div class="card lg" style="left:1060px;top:340px"><img src="${A}SummonerSmite.png" style="width:260px;height:260px"><div class="n" style="font-size:48px">Çarp</div></div>`);
su.appendChild(sF); su.appendChild(sS);
const flashFx = h(`<div class="abs" style="inset:0;background:radial-gradient(circle at 730px 470px,rgba(240,255,160,.9),rgba(240,255,160,0) 40%)"></div>`); su.appendChild(flashFx);
const smiteFx = h(`<div class="abs" style="inset:0;background:radial-gradient(circle at 1190px 470px,rgba(255,220,120,.9),rgba(255,220,120,0) 40%)"></div>`); su.appendChild(smiteFx);
/* ---------- PHASES ---------- */
const banners = [['EARLY GAME', T.early[0]], ['MID GAME', T.mid[0]], ['LATE GAME', T.late[0]]].map(([tx, t0]) => [h(`<div class="abs banner"><div>${tx}</div></div>`), t0]);
const phase = h(`<div class="abs phase"><div id="ph"></div></div>`); const ph = phase.querySelector('#ph');
/* ---------- CTA ---------- */
const ct0 = T.cta[0];
const odim = h(`<div class="abs dim"></div>`);
const counter = h(`<div class="abs" style="left:0;right:0;top:230px;text-align:center"><div style="font-family:Ant;font-size:84px;color:#FFF8EC;text-shadow:0 6px 0 #000">RENGAR'A KARŞI <span style="color:#FF3B4E">TEK YEMEMENİN</span> YOLU</div>
 <div style="margin-top:30px"><span class="chip gold" style="font-size:50px">Kontrol totemi al</span></div><div><span class="chip red" style="font-size:50px">Çalılara <b>tek başına girme</b></span></div></div>`);
const orPlay = h(`<div class="abs" style="left:0;right:0;top:420px;text-align:center"><span style="display:inline-block;font-family:Ant;font-size:130px;color:#FFC23D;text-shadow:0 8px 0 #000;transform:rotate(-3deg)">YA DA RENGAR'I SEN OYNA</span></div>`);
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
  hookR(t);
  if (inS(t, 'why')) { show(pros[0], t, w0, T.why[1], 'cut'); pros[2].forEach(([r, t0]) => show(r, t, t0, T.why[1], 'slideL')); show(cons[0], t, W('ama', w0), T.why[1], 'slideR'); cons[2].forEach(([r, t0]) => show(r, t, t0, T.why[1], 'slideR')); }
  else { pros[0].style.display = 'none'; cons[0].style.display = 'none' }
  show(adc, t, W('yani', w0), T.why[1], 'up');
  quoteEls.forEach(([e, a, b]) => show(e, t, a, b, 'pop', .2));
  fulls.forEach(([s, a, b]) => show(s, t, a, b, 'fade', .3));
  badges.forEach(([b, a, c]) => { if (show(b, t, a, c, 'slideL', .35)) { const k = b.querySelector('.key'); const p = t - a; k.style.boxShadow = p < 1.2 ? `0 0 ${40 * (1 - p / 1.2)}px rgba(244,185,66,.9)` : '' } });
  chips.forEach(([w, e, t0, t1]) => { const v = t >= t0 && t < t1; w.style.display = v ? '' : 'none'; if (v) show(e, t, t0, t1, 'slideL', .3) });
  if (show(fer, t, p0 + .3, bush, 'drop')) { const a = W('normal', p0), b = W('4', p0); pips.forEach((p, i) => { const on = t >= a + (b - a) * (i + 1) / 4 && t < b + 1.6; p.style.background = on ? 'linear-gradient(90deg,#ff9b3d,#ffd36b)' : '#2a2238'; p.style.boxShadow = on ? '0 0 16px #ffb347' : '' }) }
  if (M.ult_sesi && show(ultFlash, t, M.ult_sesi[0], M.ult_sesi[1] + .6, 'cut')) ultFlash.style.opacity = clamp(1 - (t - M.ult_sesi[0]) / 3) * (.7 + .3 * Math.sin(t * 20));
  if (show(avin, t, letT - .1, ageT + 2.2, 'cut')) letters.forEach((s, i) => {
    const a = letTs[i]; s.style.opacity = t >= a ? 1 : 0; let tf = `scale(${t >= a ? .7 + .3 * eb((t - a) / .2) : 1})`;
    if (i === 1) { // the V: shake, go red, flip into a red question mark
      const h0 = harfT + .15, h1 = h0 + .45, h2 = h1 + .25;
      s.textContent = t >= h1 + .12 ? '?' : 'V'; s.style.color = t >= h0 ? '#FF3B4E' : '';
      if (t >= h0 && t < h1) tf += ` translate(${Math.sin(t * 70) * 10}px,${Math.cos(t * 55) * 4}px) rotate(${Math.sin(t * 40) * 8}deg)`;
      else if (t >= h1 && t < h2) tf += ` scaleX(${Math.abs(Math.cos((t - h1) / (h2 - h1) * Math.PI))})`;
      else if (t >= h2) tf += ` scale(${1 + .25 * clamp(1 - (t - h2) / .3)}) rotate(-8deg)`;
      s.style.textShadow = t >= h2 ? '0 12px 0 #000,0 0 50px rgba(255,59,78,.9)' : '';
    }
    s.style.transform = tf });
  show(age, t, ageT, T.r[1] - 0.01 < ageT + 2.2 ? ageT + 2.2 : ageT + 2.2, 'pop', .25);
  if (show(kitty, t, kitT, T.r[1], 'fade', .25)) { kst.style.opacity = t >= kitT2 ? 1 : 0; kst.style.transform = t >= kitT2 ? `scale(${.6 + .4 * eb((t - kitT2) / .3)})` : '' }
  if (show(band, t, T.combo[0], T.combo[1], 'up')) {
    const want = t < c2 ? 1 : 2; if (want !== curCombo) { curCombo = want; comboEls = comboRow(want === 1 ? combo1 : combo2); bt.textContent = want === 1 ? 'DALIŞ KOMBOSU' : 'HASAR KOMBOSU' }
    comboEls.forEach(([e, t0]) => { const on = t >= t0; e.classList.toggle('on', on); e.style.transform = on ? `scale(${1 + .12 * clamp(1 - (t - t0) / .3)})` : '' })
  }
  if (t >= m0 && t < mm) { kz1.style.opacity = 1; kz2.style.opacity = t >= W('sakın', m0) ? 1 : 0; kz2.style.transform = t >= W('sakın', m0) ? `scale(${.6 + .4 * eb((t - W('sakın', m0)) / .3)}) rotate(-3deg)` : '' }
  if (t >= mm && t < T.match[1]) {
    show(sEasy, t, mm + .2, T.match[1], 'slideL', .4); show(sHard, t, hardT - .2, T.match[1], 'slideR', .4);
    [...sEasy.querySelectorAll('img')].forEach((e, i) => show(e, t, easyIc[i], T.match[1], 'pop')); [...sHard.querySelectorAll('img')].forEach((e, i) => show(e, t, hardIc[i], T.match[1], 'pop'));
    [...sEasy.querySelectorAll('.cap')].forEach((e, i) => e.style.opacity = t >= (i ? W('üstlerine', mm) : W('kırılgan', mm)) ? 1 : 0); [...sHard.querySelectorAll('.cap')].forEach((e, i) => e.style.opacity = t >= (i ? W('patlamasını', mm) : W('dayanıklı', mm)) ? 1 : 0);
    const vt = t - (mm + .4);
    if (show(vs, t, mm + .4, T.match[1], 'pop', .35)) { vsT.style.transform = `scale(${1 + .06 * Math.sin(t * 6)}) rotate(${-6 + 3 * Math.sin(t * 2)}deg)`; vsRing.style.transform = `scale(${1 + .5 * clamp(1 - vt / .5) + .04 * Math.sin(t * 6)})`; vsRing.style.opacity = .5 + .5 * Math.abs(Math.sin(t * 3)); rays.forEach((r, i) => { r.style.opacity = .35 + .35 * Math.sin(t * 5 + i); r.style.transform = `rotate(${i * 30 + t * 25}deg) translateY(150px)` }) }
  }
  if (inS(t, 'runes')) runeCards.forEach(([c, t0]) => show(c, t, t0, T.runes[1], 'pop'));
  if (inS(t, 'items')) { itemCards.forEach(([c, t0]) => show(c, t, t0, T.items[1], 'pop')); show(allDesc, t, descT, T.items[1], 'pop') }
  if (inS(t, 'skills')) { cells.forEach(c => { const l = +c.dataset.l; const on = t >= lvlT[l]; c.classList.toggle('on', on); c.classList.toggle('r', c.dataset.k === 'R'); c.textContent = on ? c.dataset.k : ''; c.style.transform = on ? `scale(${.7 + .3 * eb((t - lvlT[l]) / .25)})` : '' }); show(maxChip, t, maxT, T.skills[1], 'up'); show(ultChip, t, ultT, T.skills[1], 'up') }
  if (inS(t, 'summ')) { const f = CUES.flash, g = CUES.smite; show(sF, t, f - .15, T.summ[1], 'pop'); show(sS, t, g - .15, T.summ[1], 'pop'); flashFx.style.opacity = clamp(1 - Math.abs(t - f) / .35); smiteFx.style.opacity = clamp(1 - Math.abs(t - g) / .4) }
  banners.forEach(([b, t0]) => { if (show(b, t, t0, t0 + 1.8, 'pop', .3)) { b.firstChild.style.clipPath = `inset(0 ${100 - 100 * eo((t - t0) / .35)}% 0 0)` } });
  const pn = inS(t, 'early') ? 'EARLY GAME' : inS(t, 'mid') ? 'MID GAME' : inS(t, 'late') ? 'LATE GAME' : '';
  ph.textContent = pn; phase.style.display = (pn && !banners.some(([b, t0]) => t >= t0 && t < t0 + 1.8)) ? '' : 'none';
  show(odim, t, ct0, 240.5, 'fade', .4);
  show(counter, t, ct0 + .1, W('ya', ct0), 'up'); show(orPlay, t, W('ya', ct0), W('video', ct0), 'pop', .3);
  if (show(likeSub, t, W('video', ct0), finT, 'up')) { const lT = W('beğenmeyi', ct0), sT = W('abone', ct0); lk.style.transform = t >= lT ? `scale(${1 + .15 * clamp(1 - (t - lT) / .4)})` : ''; lk.style.background = t >= lT ? '#FFC23D' : '#1d1530'; lk.style.color = t >= lT ? '#140c22' : '#fff'; sb.style.transform = t >= sT ? `scale(${1 + .15 * clamp(1 - (t - sT) / .4)})` : '' }
  show(fin, t, finT - .2, 240.5, 'fade', .35); fn2.style.opacity = t >= W('yani', finT) ? 1 : 0;
};
window.ready = Promise.all([document.fonts.ready, ...[...document.images].map(i => i.decode().catch(() => { }))]);
window.render(0);
