(function () {
  const css = `
    #mlgBanana {
      position: fixed;
      width: 72px; height: 72px;
      image-rendering: pixelated;
      z-index: 9998;
      pointer-events: auto;
      cursor: pointer;
      filter: drop-shadow(0 0 8px #ffd700) drop-shadow(0 0 16px #ff00ff);
      transition: filter 0.2s;
    }
    #mlgBanana:hover {
      filter: drop-shadow(0 0 14px #ff00ff) drop-shadow(0 0 28px #00f0ff);
    }
    #mlgBanana.flip { transform: scaleX(-1); }

    .mlg-postit {
      position: fixed;
      z-index: 9997;
      background: rgba(0, 0, 0, 0.88);
      color: #fff;
      font-family: 'Orbitron', 'Press Start 2P', monospace;
      font-size: 10px;
      font-weight: 700;
      padding: 10px 13px;
      max-width: 200px;
      box-shadow:
        0 0 12px rgba(127,0,255,0.8),
        0 0 24px rgba(255,0,255,0.4),
        inset 0 0 8px rgba(127,0,255,0.1);
      border: 1px solid #7f00ff;
      border-left: 4px solid #ff00ff;
      line-height: 1.7;
      letter-spacing: 1px;
      cursor: pointer;
      animation: mlgPostitPop 0.25s ease;
      text-shadow: 0 0 6px #ff00ff;
    }
    @keyframes mlgPostitPop {
      from { transform: scale(0.4) rotate(-12deg); opacity: 0; }
      to   { transform: scale(1)   rotate(-1deg);  opacity: 1; }
    }

    #mlgHonkText {
      position: fixed;
      font-family: 'Press Start 2P', 'Orbitron', monospace;
      font-size: 14px;
      font-weight: 900;
      color: #ff00ff;
      text-shadow:
        1px 1px 0 #7f00ff,
        0 0 10px #ff00ff,
        0 0 20px #7f00ff;
      z-index: 9999;
      pointer-events: none;
      opacity: 0;
      transform: translateY(0) scale(0.5);
      transition: opacity 0.1s, transform 0.18s cubic-bezier(0.34,1.56,0.64,1);
      white-space: nowrap;
      letter-spacing: 2px;
    }
    #mlgHonkText.show {
      opacity: 1;
      transform: translateY(-10px) scale(1);
    }

    /* Scanline overlay en los post-its */
    .mlg-postit::after {
      content: '';
      position: absolute; inset: 0;
      background: repeating-linear-gradient(
        to bottom,
        transparent 0px, transparent 2px,
        rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 3px
      );
      pointer-events: none;
    }
  `;

  const styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  const banana = document.createElement('img');
  banana.id  = 'mlgBanana';
  banana.src = '/static/banana-dance.gif';
  banana.alt = '🍌';
  document.body.appendChild(banana);

  const honkEl = document.createElement('div');
  honkEl.id = 'mlgHonkText';
  document.body.appendChild(honkEl);

  // ── Sonido MLG airhorn sintético ─────────────────────────────────────────
  function playMLGHonk() {
    try {
      const actx = new (window.AudioContext || window.webkitAudioContext)();

      // Onda 1: tono grave de airhorn
      const osc1  = actx.createOscillator();
      const gain1 = actx.createGain();
      osc1.connect(gain1); gain1.connect(actx.destination);
      osc1.type = 'sawtooth';
      osc1.frequency.setValueAtTime(110, actx.currentTime);
      osc1.frequency.exponentialRampToValueAtTime(85, actx.currentTime + 0.6);
      gain1.gain.setValueAtTime(0.3, actx.currentTime);
      gain1.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + 0.65);
      osc1.start(actx.currentTime);
      osc1.stop(actx.currentTime + 0.65);

      // Onda 2: armónico agudo
      const osc2  = actx.createOscillator();
      const gain2 = actx.createGain();
      osc2.connect(gain2); gain2.connect(actx.destination);
      osc2.type = 'square';
      osc2.frequency.setValueAtTime(220, actx.currentTime);
      osc2.frequency.exponentialRampToValueAtTime(160, actx.currentTime + 0.5);
      gain2.gain.setValueAtTime(0.12, actx.currentTime);
      gain2.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + 0.55);
      osc2.start(actx.currentTime);
      osc2.stop(actx.currentTime + 0.55);
    } catch(e) {}
  }

  // ── Frases MLG 420 ───────────────────────────────────────────────────────
  const MSGS = [
    '360 NO SCOPE 💥',
    'MLG PRO GAMER 2016 🎮',
    'DORITOS & MTN DEW 🔺🥤',
    'GET REKT SON 💀',
    'IT\'S HIGH NOON 🕛',
    'ILLUMINATI CONFIRMED 🔺👁️',
    'SMOKE WEED EVERY DAY 🌿',
    'PRESS F TO PAY RESPECTS 🙏',
    'DANK MEMES ONLY 🐸',
    'YOLO SWAG 420 😎',
    'DOGE MUCH WOW VERY MLG 🐕',
    'QUICKSCOPE OR NEVER 🎯',
    'NYAN CAT IS ETERNAL 🌈',
    'REKT BY THE ILLUMINATI 👁️',
    '420 BLAZE IT 🔥',
    'REKT INTENSIFIES 💯',
    'SANIC GOTTA GO FAST ⚡',
    'JOHN CENA!!!! 💪',
    'ALLAHU AKBAR AIRHORN 🎺',
    'U WOT M8 🤙',
  ];

  // ── Textos del honk aleatorios ────────────────────────────────────────────
  const HONKS = [
    'MLG!', '420!', 'REKT!', 'HONK!', 'DANK!',
    'NO SCOPE!', 'YOLO!', 'WOW!', 'EZ!', 'GG!'
  ];

  const NAV_H = 64;
  let px = 150, py = window.innerHeight / 2;
  let vx = 0.5,  vy = 0.35;
  let mouseX = 0, mouseY = 0;
  let frame     = 0;
  let fleeing   = false;
  let honkTimer = null;

  let lastPostit = Date.now() - 15000;
  let lastHonk   = Date.now() - 18000;

  document.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });

  function doHonk() {
    playMLGHonk();
    const txt = HONKS[Math.floor(Math.random() * HONKS.length)];
    honkEl.textContent = txt;
    honkEl.style.left  = (px + 36) + 'px';
    honkEl.style.top   = (py - 26) + 'px';
    honkEl.classList.add('show');
    clearTimeout(honkTimer);
    honkTimer = setTimeout(() => honkEl.classList.remove('show'), 1100);
  }

  function spawnPostit() {
    const msg = MSGS[Math.floor(Math.random() * MSGS.length)];
    const p   = document.createElement('div');
    p.className   = 'mlg-postit';
    p.textContent = msg;
    p.style.left  = Math.max(10, Math.min(window.innerWidth - 220, px)) + 'px';
    p.style.top   = Math.max(NAV_H + 10, py - 100) + 'px';
    p.style.position = 'fixed';
    document.body.appendChild(p);
    p.addEventListener('click', () => p.remove());
    setTimeout(() => {
      p.style.transition = 'opacity 0.6s';
      p.style.opacity    = '0';
      setTimeout(() => p.remove(), 600);
    }, 7000);
  }

  banana.addEventListener('click', () => {
    doHonk();
    // spawn pequeño glitch visual al hacer click
    spawnGlitch();
  });

  function spawnGlitch() {
    const g = document.createElement('div');
    g.style.cssText = `
      position:fixed;
      left:${(px - 10)|0}px; top:${(py - 10)|0}px;
      width:92px; height:92px;
      border:2px solid #ff00ff;
      box-shadow:0 0 20px #ff00ff,0 0 40px #7f00ff;
      pointer-events:none; z-index:9996;
      border-radius:2px;
      animation: glitchOut 0.4s ease-out forwards;
    `;
    const kf = document.createElement('style');
    kf.textContent = `@keyframes glitchOut {
      0%  { opacity:1; transform:scale(1); }
      100%{ opacity:0; transform:scale(1.8); }
    }`;
    document.head.appendChild(kf);
    document.body.appendChild(g);
    setTimeout(() => { g.remove(); kf.remove(); }, 420);
  }

  function update() {
    frame++;
    const W = window.innerWidth;
    const H = window.innerHeight;

    const dx   = mouseX - px;
    const dy   = mouseY - py;
    const dist = Math.sqrt(dx * dx + dy * dy);

    // Huir del cursor
    if (dist < 130) {
      fleeing = true;
      const angle = Math.atan2(dy, dx);
      vx = -Math.cos(angle) * 1.8;
      vy = -Math.sin(angle) * 1.8;
    } else if (fleeing && dist > 220) {
      fleeing = false;
      const angle = Math.random() * Math.PI * 2;
      const spd   = 0.35 + Math.random() * 0.45;
      vx = Math.cos(angle) * spd;
      vy = Math.sin(angle) * spd;
    }

    px += vx; py += vy;

    // Rebotar en bordes
    if (px < 0)       { px = 0;       vx =  Math.abs(vx); }
    if (px > W - 72)  { px = W - 72;  vx = -Math.abs(vx); }
    if (py < NAV_H)   { py = NAV_H;   vy =  Math.abs(vy); }
    if (py > H - 72)  { py = H - 72;  vy = -Math.abs(vy); }

    // Cambio de dirección aleatorio cada ~4 segundos
    if (frame % 260 === 0 && !fleeing) {
      const angle = Math.random() * Math.PI * 2;
      const spd   = 0.35 + Math.random() * 0.45;
      vx = Math.cos(angle) * spd;
      vy = Math.sin(angle) * spd;
    }

    // Flip horizontal según dirección
    if (vx < -0.15)      banana.classList.add('flip');
    else if (vx > 0.15)  banana.classList.remove('flip');

    banana.style.left = (px | 0) + 'px';
    banana.style.top  = (py | 0) + 'px';

    // Mantener el honk text pegado a la banana
    if (honkEl.classList.contains('show')) {
      honkEl.style.left = (px + 36) + 'px';
      honkEl.style.top  = (py - 26) + 'px';
    }

    // Post-it cada ~18s
    const now = Date.now();
    if (now - lastPostit > 18000) { lastPostit = now; spawnPostit(); }
    // Honk automático cada ~22s
    if (now - lastHonk   > 22000) { lastHonk   = now; doHonk();     }

    requestAnimationFrame(update);
  }

  banana.style.left = px + 'px';
  banana.style.top  = py + 'px';
  update();
})();
