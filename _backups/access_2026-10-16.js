/* French Wine — free member access (DEMO of "option B": sign-up + e-mail magic link).
   Loaded on every page by theme.js. Nothing leaves the browser in demo mode: sign-ups are kept in
   localStorage ("fw_demo_db") so the flow can be tried before the site is online. To go live, replace
   the DEMO backend below with a real one (e.g. Supabase signInWithOtp) — the rest stays the same.

   What is locked for visitors is set in RULES (edit freely):
     page   : the whole page is covered (cadastral plans, except SAMPLES)
     lock   : CSS selectors blurred with an "unlock" card (IGP details, calculators 2-5)
     clicks : CSS selectors whose clicks open the sign-up form instead (vintage-chart periods)
   NOTE: this is a client-side lock — real protection needs the server (see Infos/Confidentialite.html). */
(function () {
  if (window.__fwAccess) return; window.__fwAccess = true;
  var root = document.documentElement;

  /* ------------------------------------------------------------------ settings */
  // MASTER SWITCH — false = no popup and no locks anywhere (everything below is kept for going live).
  var ENABLED = false;
  // Owner bypass: SHA-256 of "fw-owner:" + your passphrase, written by assets/set_owner_key.py (never the passphrase itself).
  // Unlock a browser: open any page with  #cle=<passphrase>  — remove it again with  #cle=off
  var OWNER_HASH = '';
  var POLICY_VERSION = '2026-10-07';
  var POPUP_DELAY_MS = 8000;          // first visit: popup after 8 s on a page…
  var POPUP_ON_PAGEVIEW = 2;          // …or as soon as the 2nd page is opened
  var SNOOZE_DAYS = 3;                // "Continue as a visitor" → no automatic popup for 3 days
  var SAMPLES = ['Plan Cadastraux/Bordeaux_RightBank/Pomerol.html',
                 'Plan Cadastraux/Champagne_Grands_Crus/Champagne-Grands-Crus.html'];
  var RULES = [
    { id: 'plans', page: true,
      test: function (p) { return p.indexOf('Plan Cadastraux/') === 0 && SAMPLES.indexOf(p) < 0; },
      why: ['Les 355 plans cadastraux sont réservés aux membres.', 'The 355 cadastral plans are for members.'] },
    { id: 'igp', lock: ['#info .ibody'],
      test: function (p) { return /Carte des IGP\.html$/.test(p); },
      why: ['Le détail complet de chaque IGP et son cahier des charges sont réservés aux membres.',
            'The full detail of each IGP and its cahier des charges are for members.'] },
    { id: 'tools', lock: ['.tools > .tool:nth-child(n+2)'],
      test: function (p) { return /^Infos\/French_Wine_in_Numbers\.html$/.test(p); },
      why: ['Tous les calculateurs sont accessibles aux membres.', 'All calculators are available to members.'] },
    { id: 'vintage', clicks: ['.periods [data-period]:not([data-period="0"])'],
      test: function (p) { return /^Infos\/Vintages\/Vintage_Chart\.html$/.test(p); },
      why: ['Les millésimes antérieurs à 2000 sont réservés aux membres.', 'Vintages before 2000 are for members.'] }
  ];

  /* ------------------------------------------------------------------ paths */
  var me = document.currentScript && document.currentScript.src;
  var SITE = me ? me.replace(/assets\/access\.js(\?.*)?$/, '') : '';
  function rel(href) {
    try {
      var a = decodeURIComponent(String(href).split('#')[0].split('?')[0]);
      var s = decodeURIComponent(SITE);
      return a.indexOf(s) === 0 ? a.slice(s.length) : null;
    } catch (e) { return null; }
  }
  var HERE = rel(location.href) || '';
  var PRIVACY = SITE + 'Infos/Confidentialite.html';

  /* ------------------------------------------------------------------ storage */
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function getJ(k, d) { try { var v = JSON.parse(get(k)); return v == null ? d : v; } catch (e) { return d; } }
  function setJ(k, v) { set(k, JSON.stringify(v)); }
  function sget(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function sset(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  /* ------------------------------------------------------------------ DEMO backend
     Same promise-based interface a real backend would expose. */
  var Backend = {
    name: 'demo',
    signUp: function (profile) {           // real: supabase.auth.signInWithOtp({email, options:{data:profile}})
      return new Promise(function (ok) {
        var db = getJ('fw_demo_db', []);
        var rec = db.filter(function (r) { return r.email === profile.email; })[0];
        if (!rec) { rec = { id: 'm' + Date.now().toString(36), createdAt: new Date().toISOString() }; db.push(rec); }
        for (var k in profile) rec[k] = profile[k];
        rec.status = rec.verifiedAt ? 'member' : 'pending';
        setJ('fw_demo_db', db); setJ('fw_pending', rec);
        setTimeout(function () { ok({ sent: true }); }, 700);
      });
    },
    verify: function () {                  // real: the user clicks the link in the e-mail
      return new Promise(function (ok) {
        var p = getJ('fw_pending', null); if (!p) return ok(null);
        var db = getJ('fw_demo_db', []);
        db.forEach(function (r) { if (r.email === p.email) { r.verifiedAt = r.verifiedAt || new Date().toISOString(); r.status = 'member'; p = r; } });
        setJ('fw_demo_db', db); setJ('fw_member', p); del('fw_pending');
        ok(p);
      });
    },
    signOut: function () { del('fw_member'); del('fw_pending'); return Promise.resolve(); },
    deleteMe: function () {                // right to erasure
      var m = getJ('fw_member', null) || getJ('fw_pending', null);
      if (m) setJ('fw_demo_db', getJ('fw_demo_db', []).filter(function (r) { return r.email !== m.email; }));
      del('fw_member'); del('fw_pending');
      return Promise.resolve();
    }
  };

  function member() { return getJ('fw_member', null); }
  function isOwner() { return !!OWNER_HASH && get('fw_owner') === OWNER_HASH; }
  function isMember() { return !!member() || isOwner(); }
  function syncClass() {
    if (!ENABLED) { root.classList.remove('fw-member', 'fw-guest'); return; }
    root.classList.toggle('fw-member', isMember());
    root.classList.toggle('fw-guest', !isMember());
  }
  syncClass();

  /* ------------------------------------------------------------------ i18n */
  function L() {
    var l = get('fw_lang') || root.lang || 'fr';
    return l.slice(0, 2) === 'en' ? 'en' : 'fr';
  }
  function T(fr, en) { return L() === 'en' ? en : fr; }
  function setLang(l) {
    if (window.fwNav && window.fwNav.setLang) window.fwNav.setLang(l);      // whole page + menu, remembered site-wide
    else {
      set('fw_lang', l); root.lang = l;
      try { document.dispatchEvent(new CustomEvent('fw:lang', { detail: { lang: l } })); } catch (e) {}
    }
    tr();                                                                    // popup, lock cards, page cover
  }
  function tr(scope) {
    var en = L() === 'en';
    if (ov) ov.querySelectorAll('.fa-lang [data-lang]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === L())); });
    var dl = ov && ov.querySelector('#fa-countries');
    if (dl) dl.innerHTML = COUNTRIES.map(function (c) { return '<option value="' + esc(c[en ? 1 : 0]) + '">'; }).join('');
    (scope || document).querySelectorAll('[data-tfr]').forEach(function (n) {
      n.innerHTML = n.getAttribute(en ? 'data-ten' : 'data-tfr');
    });
    (scope || document).querySelectorAll('[data-pfr]').forEach(function (n) {
      n.setAttribute('placeholder', n.getAttribute(en ? 'data-pen' : 'data-pfr'));
    });
  }
  function t2(fr, en, tag, cls) {
    tag = tag || 'span';
    return '<' + tag + (cls ? ' class="' + cls + '"' : '') + ' data-tfr="' + esc(fr) + '" data-ten="' + esc(en) + '">' + fr + '</' + tag + '>';
  }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  /* ------------------------------------------------------------------ styles */
  var LOCK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4.5" y="10.5" width="15" height="10" rx="2.2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.3" fill="currentColor"/></svg>';
  var LOCK_URI = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23b48a3c' stroke-width='2' stroke-linecap='round'%3E%3Crect x='4.5' y='10.5' width='15' height='10' rx='2.2'/%3E%3Cpath d='M8 10.5V7.5a4 4 0 0 1 8 0v3'/%3E%3C/svg%3E\")";
  var CSS = [
    ':root{--fa-bg:#2a0910;--fa-panel:#34101a;--fa-ink:#f5efe3;--fa-mute:rgba(245,239,227,.68);--fa-gold:#d9b36b;--fa-gold2:#e7cf9c;',
    '--fa-hair:rgba(217,179,107,.22);--fa-hair2:rgba(217,179,107,.55);--fa-field:rgba(0,0,0,.28);--fa-btn:#9b2235;--fa-btnink:#fff;--fa-err:#ff9b8f;}',
    'html[data-theme="cream"]{--fa-bg:#fffdf8;--fa-panel:#f7f0e2;--fa-ink:#2e1419;--fa-mute:rgba(46,20,25,.7);--fa-gold:#9a6a1f;--fa-gold2:#7b1e2b;',
    '--fa-hair:rgba(142,31,51,.18);--fa-hair2:rgba(142,31,51,.45);--fa-field:#fff;--fa-btn:#7b1e2b;--fa-err:#b3261e;}',
    '.fa-ov{position:fixed;inset:0;z-index:2147483600;display:flex;align-items:center;justify-content:center;padding:18px;',
    'background:rgba(20,3,8,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);animation:faIn .25s ease;}',
    'html[data-theme="cream"] .fa-ov{background:rgba(60,30,20,.35);}',
    '@keyframes faIn{from{opacity:0}to{opacity:1}} @keyframes faUp{from{transform:translateY(14px);opacity:0}to{transform:none;opacity:1}}',
    '.fa-box{position:relative;width:min(640px,100%);max-height:calc(100vh - 36px);overflow:auto;background:var(--fa-bg);color:var(--fa-ink);',
    'border:1px solid var(--fa-hair2);border-radius:20px;box-shadow:0 30px 80px rgba(0,0,0,.45);padding:30px clamp(18px,4vw,34px) 24px;',
    'font:400 14px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI","Helvetica Neue",Arial,sans-serif;animation:faUp .3s ease;}',
    '.fa-box *{box-sizing:border-box;}',
    '.fa-x{position:absolute;top:12px;right:12px;width:34px;height:34px;border-radius:50%;border:1px solid var(--fa-hair);background:transparent;color:var(--fa-mute);cursor:pointer;font-size:16px;}',
    '.fa-x:hover{border-color:var(--fa-hair2);color:var(--fa-ink);}',
    '.fa-lang{position:absolute;top:12px;right:56px;display:flex;border:1px solid var(--fa-hair2);border-radius:999px;overflow:hidden;}',
    '.fa-lang button{all:unset;cursor:pointer;padding:0 11px;height:32px;display:inline-flex;align-items:center;font:700 11px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.12em;color:var(--fa-mute);}',
    '.fa-lang button+button{border-left:1px solid var(--fa-hair);}',
    '.fa-lang button{gap:6px;padding:0 12px 0 9px;}',
    '.fa-flag{width:15px;height:15px;flex:none;border-radius:50%;box-shadow:0 0 0 1px rgba(0,0,0,.18);}',
    '.fa-lang button[aria-pressed="true"] .fa-flag{box-shadow:0 0 0 1.5px #fff;}',
    '.fa-lang button[aria-pressed="true"]{background:var(--fa-btn);color:var(--fa-btnink);}',
    '.fa-lang button:focus-visible{outline:2px solid var(--fa-gold);outline-offset:-2px;}',
    '.fa-box .fa-kick{padding-right:150px;}',
    '.fa-kick{margin:0 0 6px;font-size:10.5px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:var(--fa-gold);}',
    '.fa-h{margin:0 0 8px;font:500 clamp(24px,4vw,31px)/1.12 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;color:var(--fa-ink);}',
    '.fa-lead{margin:0 0 14px;color:var(--fa-mute);}',
    '.fa-why{margin:0 0 14px;padding:9px 12px;border-radius:10px;border:1px solid var(--fa-hair);background:var(--fa-panel);font-size:13px;display:flex;gap:9px;align-items:center;}',
    '.fa-why svg{width:18px;height:18px;flex:none;color:var(--fa-gold);}',
    '.fa-perks{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin:0 0 18px;padding:0;list-style:none;font-size:13px;}',
    '.fa-perks li{display:flex;gap:7px;align-items:flex-start;} .fa-perks li::before{content:"✓";color:var(--fa-gold);font-weight:700;}',
    '.fa-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px 12px;}',
    '.fa-f{display:flex;flex-direction:column;gap:4px;grid-column:span 2;} .fa-f.w3{grid-column:span 3;} .fa-f.w6{grid-column:1/-1;}',
    '.fa-f label{font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--fa-gold);}',
    '.fa-f label i{font-style:normal;font-weight:500;letter-spacing:.04em;text-transform:none;color:var(--fa-mute);}',
    '.fa-f input{font:500 15px/1.2 inherit;font-family:inherit;color:var(--fa-ink);background:var(--fa-field);border:1px solid var(--fa-hair2);border-radius:10px;padding:10px 12px;outline:none;width:100%;}',
    '.fa-f input:focus{border-color:var(--fa-gold);box-shadow:0 0 0 3px rgba(217,179,107,.18);}',
    '.fa-f.bad input{border-color:var(--fa-err);} .fa-f .fa-e{display:none;font-size:11.5px;color:var(--fa-err);} .fa-f.bad .fa-e{display:block;}',
    '.fa-consent{grid-column:1/-1;display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.5;margin-top:4px;padding:10px 12px;border-radius:10px;border:1px solid var(--fa-hair);}',
    '.fa-consent.bad{border-color:var(--fa-err);} .fa-consent input{margin-top:3px;width:17px;height:17px;flex:none;accent-color:var(--fa-btn);}',
    '.fa-consent a,.fa-small a{color:var(--fa-gold);}',
    '.fa-small{font-size:11.5px;line-height:1.5;color:var(--fa-mute);margin:12px 0 0;}',
    '.fa-act{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:18px;}',
    '.fa-btn{cursor:pointer;border-radius:999px;padding:12px 22px;font:700 12px/1 inherit;font-family:inherit;letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--fa-btn);background:var(--fa-btn);color:var(--fa-btnink);}',
    '.fa-btn:hover{filter:brightness(1.1);} .fa-btn[disabled]{opacity:.6;cursor:wait;}',
    '.fa-btn.ghost{background:transparent;color:var(--fa-gold);border-color:var(--fa-hair2);}',
    '.fa-link{background:none;border:0;padding:4px 2px;cursor:pointer;color:var(--fa-mute);font:500 13px inherit;font-family:inherit;text-decoration:underline;text-underline-offset:3px;}',
    '.fa-demo{margin:16px 0 0;padding:8px 12px;border-radius:10px;font-size:11.5px;line-height:1.45;background:rgba(217,179,107,.12);border:1px dashed var(--fa-hair2);color:var(--fa-mute);}',
    '.fa-demo b{color:var(--fa-gold);}',
    '.fa-mail{display:flex;gap:14px;align-items:center;margin:6px 0 14px;padding:14px;border-radius:14px;background:var(--fa-panel);border:1px solid var(--fa-hair);}',
    '.fa-mail svg{width:42px;height:42px;flex:none;color:var(--fa-gold);} .fa-mail b{color:var(--fa-ink);word-break:break-all;}',
    '.fa-toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:2147483646;padding:10px 18px;border-radius:999px;background:var(--fa-bg);color:var(--fa-ink);border:1px solid var(--fa-hair2);font:600 13px ui-sans-serif,system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.3);}',
    '@media (max-width:560px){.fa-grid{grid-template-columns:1fr 1fr;} .fa-f,.fa-f.w3{grid-column:1/-1;} .fa-f.half{grid-column:span 1;} .fa-perks{grid-template-columns:1fr;} .fa-box{padding-top:24px;}}',
    /* locks */
    'html.fw-guest .fa-lockbox{position:relative;min-height:150px;}',
    'html.fw-guest .fa-lockbox > :not(.fa-card){filter:blur(5px);opacity:.55;pointer-events:none;user-select:none;}',
    '.fa-card{display:none;}',
    'html.fw-guest .fa-card{display:flex;position:absolute;inset:0;z-index:6;flex-direction:column;align-items:center;justify-content:center;gap:8px;text-align:center;padding:16px;',
    'font:500 13.5px/1.45 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;color:var(--fa-ink);}',
    '.fa-card .fa-cin{max-width:320px;padding:16px 18px;border-radius:16px;background:var(--fa-bg);border:1px solid var(--fa-hair2);box-shadow:0 12px 30px rgba(0,0,0,.25);display:flex;flex-direction:column;align-items:center;gap:8px;}',
    '.fa-card svg{width:26px;height:26px;color:var(--fa-gold);} .fa-card .fa-btn{padding:10px 16px;font-size:11px;}',
    'html.fw-guest .fa-clicklock{position:relative;}',
    'html.fw-guest .fa-clicklock::after{content:"";display:inline-block;width:11px;height:11px;margin-left:5px;vertical-align:-1px;background:' + LOCK_URI + ' center/contain no-repeat;}',
    'html.fw-guest a.fa-locklink::after{content:"";display:inline-block;width:10px;height:10px;margin-left:5px;vertical-align:-1px;opacity:.85;background:' + LOCK_URI + ' center/contain no-repeat;}',
    '.fa-page{position:fixed;inset:0;z-index:2147483500;display:flex;align-items:center;justify-content:center;padding:18px;',
    'background:rgba(25,4,10,.42);-webkit-backdrop-filter:blur(9px) saturate(.8);backdrop-filter:blur(9px) saturate(.8);}',
    'html[data-theme="cream"] .fa-page{background:rgba(245,238,224,.55);}',
    'html.fw-member .fa-page{display:none;}',
    '.fa-page .fa-box{animation:none;text-align:center;width:min(520px,100%);}',
    '.fa-page .fa-act{justify-content:center;} .fa-page .fa-lock{width:46px;height:46px;color:var(--fa-gold);margin:0 auto 6px;display:block;}',
    '@media print{.fa-ov,.fa-page,.fa-card,.fa-toast{display:none!important;}}'
  ].join('');

  function addCSS() {
    if (document.getElementById('fa-css')) return;
    var s = document.createElement('style'); s.id = 'fa-css'; s.textContent = CSS; document.head.appendChild(s);
  }

  /* ------------------------------------------------------------------ popup */
  var ov = null, lastFocus = null;
  var COUNTRIES = [['France', 'France'], ['Belgique', 'Belgium'], ['Suisse', 'Switzerland'], ['Luxembourg', 'Luxembourg'],
    ['Canada', 'Canada'], ['États-Unis', 'United States'], ['Royaume-Uni', 'United Kingdom'], ['Irlande', 'Ireland'],
    ['Allemagne', 'Germany'], ['Italie', 'Italy'], ['Espagne', 'Spain'], ['Portugal', 'Portugal'], ['Pays-Bas', 'Netherlands'],
    ['Danemark', 'Denmark'], ['Suède', 'Sweden'], ['Norvège', 'Norway'], ['Autriche', 'Austria'], ['Pologne', 'Poland'],
    ['Japon', 'Japan'], ['Chine', 'China'], ['Hong Kong', 'Hong Kong'], ['Singapour', 'Singapore'], ['Corée du Sud', 'South Korea'],
    ['Australie', 'Australia'], ['Nouvelle-Zélande', 'New Zealand'], ['Afrique du Sud', 'South Africa'], ['Brésil', 'Brazil'],
    ['Argentine', 'Argentina'], ['Chili', 'Chile'], ['Mexique', 'Mexico'], ['Émirats arabes unis', 'United Arab Emirates'], ['Israël', 'Israel']];

  function field(id, fr, en, opts) {
    opts = opts || {};
    var opt = opts.optional ? ' <i data-tfr="(facultatif)" data-ten="(optional)">(facultatif)</i>' : '';
    return '<div class="fa-f ' + (opts.cls || '') + '"><label for="fa-' + id + '">' + t2(fr, en) + opt + '</label>' +
      '<input id="fa-' + id + '" name="' + id + '" type="' + (opts.type || 'text') + '"' +
      (opts.ac ? ' autocomplete="' + opts.ac + '"' : '') + (opts.list ? ' list="' + opts.list + '"' : '') +
      (opts.optional ? '' : ' required') + ' maxlength="120">' +
      '<span class="fa-e">' + t2(opts.efr || 'Champ requis', opts.een || 'Required') + '</span></div>';
  }

  function formHTML(why) {
    var p = getJ('fw_pending', null) || {};
    var dl = '<datalist id="fa-countries">' + COUNTRIES.map(function (c) { return '<option value="' + esc(c[L() === 'en' ? 1 : 0]) + '">'; }).join('') + '</datalist>';
    return '' +
      t2('Accès membre gratuit', 'Free member access', 'p', 'fa-kick') +
      t2('Profitez de tout le site', 'Get full use of the site', 'h2', 'fa-h') +
      t2('Laissez-nous vos coordonnées : vous recevrez un lien de connexion par e-mail, sans mot de passe.',
         'Leave us your details: you’ll receive a sign-in link by e-mail — no password needed.', 'p', 'fa-lead') +
      (why ? '<div class="fa-why">' + LOCK_SVG + t2(why[0], why[1]) + '</div>' : '') +
      '<ul class="fa-perks">' +
        t2('Les 355 plans cadastraux', 'All 355 cadastral plans', 'li') +
        t2('La carte des IGP en détail', 'The IGP map in full detail', 'li') +
        t2('Tous les calculateurs', 'All the calculators', 'li') +
        t2('Le tableau des millésimes complet', 'The complete vintage chart', 'li') +
      '</ul>' +
      '<form class="fa-grid" novalidate>' +
        field('first', 'Prénom', 'First name', { ac: 'given-name' }) +
        field('middle', 'Second prénom', 'Middle name', { ac: 'additional-name', optional: true }) +
        field('last', 'Nom', 'Last name', { ac: 'family-name' }) +
        field('email', 'E-mail', 'E-mail', { type: 'email', ac: 'email', cls: 'w3', efr: 'Adresse e-mail valide requise', een: 'A valid e-mail address is required' }) +
        field('phone', 'Téléphone', 'Phone', { type: 'tel', ac: 'tel', cls: 'w3', optional: true, efr: 'Numéro non valide', een: 'Invalid number' }) +
        field('city', 'Ville', 'City', { ac: 'address-level2', cls: 'w3' }) +
        field('country', 'Pays', 'Country', { ac: 'country-name', cls: 'w3', list: 'fa-countries' }) + dl +
        '<label class="fa-consent"><input type="checkbox" id="fa-consent">' +
          t2('J’accepte que ces informations soient utilisées pour créer et gérer mon accès membre, conformément à la <a href="' + PRIVACY + '" target="_blank">politique de confidentialité</a>. Je peux retirer mon consentement et demander la suppression de mes données à tout moment.',
             'I agree that this information is used to create and manage my member access, as described in the <a href="' + PRIVACY + '" target="_blank">privacy policy</a>. I can withdraw my consent and ask for my data to be deleted at any time.') +
        '</label>' +
      '</form>' +
      '<div class="fa-act">' +
        '<button class="fa-btn" type="button" data-act="submit">' + t2('Recevoir mon lien d’accès', 'Send my access link') + '</button>' +
        '<button class="fa-link" type="button" data-act="guest">' + t2('Continuer en visiteur', 'Continue as a visitor') + '</button>' +
      '</div>' +
      t2('Les champs sans mention sont obligatoires. Vos données ne sont ni vendues ni partagées ; elles sont conservées 3 ans après votre dernière connexion. <a href="' + PRIVACY + '" target="_blank">En savoir plus</a>.',
         'Fields not marked optional are required. Your data is never sold or shared; it is kept for 3 years after your last sign-in. <a href="' + PRIVACY + '" target="_blank">Learn more</a>.', 'p', 'fa-small') +
      demoNote() +
      (p.email ? '<script type="text/plain" data-prefill="' + esc(JSON.stringify(p)) + '"></script>' : '');
  }
  function demoNote() {
    return '<p class="fa-demo">' + t2('<b>Démo</b> — le site n’est pas encore en ligne : aucune donnée n’est envoyée, tout reste dans ce navigateur.',
      '<b>Demo</b> — the site isn’t online yet: nothing is sent, everything stays in this browser.') + '</p>';
  }
  /* small round language markers in flag colours (SVG: emoji flags don't render on Windows) */
  var FLAG_FR = '<svg class="fa-flag" viewBox="0 0 12 12" aria-hidden="true"><defs><clipPath id="faCf"><circle cx="6" cy="6" r="6"/></clipPath></defs>' +
    '<g clip-path="url(#faCf)"><rect width="4" height="12" fill="#0055a4"/><rect x="4" width="4" height="12" fill="#fff"/><rect x="8" width="4" height="12" fill="#ef4135"/></g></svg>';
  var FLAG_EN = '<svg class="fa-flag" viewBox="0 0 12 12" aria-hidden="true"><defs><clipPath id="faCe"><circle cx="6" cy="6" r="6"/></clipPath></defs>' +
    '<g clip-path="url(#faCe)"><rect width="12" height="12" fill="#012169"/><path d="M0 0L12 12M12 0L0 12" stroke="#fff" stroke-width="2.4"/>' +
    '<path d="M0 0L12 12M12 0L0 12" stroke="#c8102e" stroke-width=".9"/><path d="M6 0V12M0 6H12" stroke="#fff" stroke-width="3.4"/>' +
    '<path d="M6 0V12M0 6H12" stroke="#c8102e" stroke-width="1.9"/></g></svg>';
  var MAIL_SVG = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="5" y="11" width="38" height="27" rx="4"/><path d="m6 13 18 14 18-14"/></svg>';
  function sentHTML(email) {
    return t2('Presque terminé', 'Almost there', 'p', 'fa-kick') +
      t2('Vérifiez votre boîte e-mail', 'Check your inbox', 'h2', 'fa-h') +
      '<div class="fa-mail">' + MAIL_SVG + '<div>' + t2('Nous avons envoyé un lien de connexion à', 'We sent a sign-in link to') + '<br><b>' + esc(email) + '</b></div></div>' +
      t2('Cliquez sur le lien dans l’e-mail pour activer votre accès. Il est valable 1 heure. Pensez à regarder dans vos courriers indésirables.',
         'Click the link in the e-mail to activate your access. It is valid for 1 hour. Remember to check your spam folder.', 'p', 'fa-lead') +
      '<div class="fa-act">' +
        '<button class="fa-btn" type="button" data-act="verify">' + t2('Démo : ouvrir le lien reçu', 'Demo: open the link') + '</button>' +
        '<button class="fa-btn ghost" type="button" data-act="resend">' + t2('Renvoyer le lien', 'Resend the link') + '</button>' +
        '<button class="fa-link" type="button" data-act="edit">' + t2('Modifier mes informations', 'Edit my details') + '</button>' +
      '</div>' +
      '<p class="fa-demo">' + t2('<b>Démo</b> — en ligne, ce bouton n’existera pas : l’accès s’activera quand vous cliquerez sur le lien dans l’e-mail.',
        '<b>Demo</b> — once online this button won’t exist: access activates when you click the link in the e-mail.') + '</p>';
  }
  function welcomeHTML(m) {
    return t2('Bienvenue', 'Welcome', 'p', 'fa-kick') +
      '<h2 class="fa-h">' + t2('Merci, ', 'Thank you, ') + esc(m.first) + ' !</h2>' +
      t2('Votre accès membre est actif : plans cadastraux, carte des IGP, calculateurs et millésimes sont maintenant entièrement débloqués.',
         'Your member access is active: cadastral plans, the IGP map, calculators and vintages are now fully unlocked.', 'p', 'fa-lead') +
      t2('Vous pouvez consulter, modifier ou supprimer vos données à tout moment depuis la page <a href="' + PRIVACY + '#compte">Confidentialité &amp; mon compte</a>.',
         'You can view, change or delete your data at any time on the <a href="' + PRIVACY + '#compte">Privacy &amp; my account</a> page.', 'p', 'fa-small') +
      '<div class="fa-act"><button class="fa-btn" type="button" data-act="close">' + t2('Continuer la visite', 'Continue browsing') + '</button></div>';
  }

  function open(why, step) {
    addCSS();
    if (ov) close(true);
    lastFocus = document.activeElement;
    ov = document.createElement('div');
    ov.className = 'fa-ov';
    ov.innerHTML = '<div class="fa-box" role="dialog" aria-modal="true" aria-labelledby="fa-title">' +
      '<button class="fa-x" type="button" data-act="guest" aria-label="Fermer / Close">✕</button>' +
      '<div class="fa-lang" role="group" aria-label="Langue / Language"><button type="button" data-lang="fr" lang="fr" aria-label="Français">' + FLAG_FR + 'FR</button><button type="button" data-lang="en" lang="en" aria-label="English">' + FLAG_EN + 'EN</button></div>' +
      '<div class="fa-body"></div></div>';
    document.body.appendChild(ov);
    ov.__why = why || null;
    var pending = getJ('fw_pending', null);
    render(step || (pending && pending.email ? 'sent' : 'form'));
    ov.addEventListener('click', onClick);
    ov.addEventListener('keydown', onKey);
    ov.addEventListener('mousedown', function (e) { if (e.target === ov) ov.__down = true; });
  }
  function render(step) {
    var body = ov.querySelector('.fa-body');
    ov.__step = step;
    if (step === 'form') {
      body.innerHTML = formHTML(ov.__why);
      var pf = body.querySelector('[data-prefill]');
      if (pf) { var p = JSON.parse(pf.getAttribute('data-prefill')); ['first', 'middle', 'last', 'email', 'phone', 'city', 'country'].forEach(function (k) { var i = body.querySelector('#fa-' + k); if (i && p[k]) i.value = p[k]; }); }
    } else if (step === 'sent') body.innerHTML = sentHTML((getJ('fw_pending', {}) || {}).email || '');
    else if (step === 'welcome') body.innerHTML = welcomeHTML(member() || {});
    var h = body.querySelector('.fa-h'); if (h) h.id = 'fa-title';
    tr(ov);
    var f = body.querySelector('input,.fa-btn'); if (f) setTimeout(function () { try { f.focus({ preventScroll: true }); } catch (e) {} }, 30);
  }
  function close(silent) {
    if (!ov) return;
    ov.remove(); ov = null;
    if (!silent && lastFocus && lastFocus.focus) try { lastFocus.focus(); } catch (e) {}
  }
  function snooze() {
    sset('fw_dismissed', '1');
    set('fw_snooze_until', String(Date.now() + SNOOZE_DAYS * 864e5));
  }
  function onKey(e) {
    if (e.key === 'Escape') { snooze(); close(); }
    if (e.key === 'Tab') {                       // keep focus inside the dialog
      var f = [].slice.call(ov.querySelectorAll('button,input,a[href]')).filter(function (n) { return n.offsetParent; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  }
  function onClick(e) {
    if (e.target === ov && ov.__down) { ov.__down = false; snooze(); close(); return; }
    ov.__down = false;
    var lb = e.target.closest('[data-lang]'); if (lb) { setLang(lb.getAttribute('data-lang')); return; }
    var b = e.target.closest('[data-act]'); if (!b) return;
    var a = b.getAttribute('data-act');
    if (a === 'guest') { snooze(); close(); }
    else if (a === 'close') close();
    else if (a === 'submit') submit(b);
    else if (a === 'edit') render('form');
    else if (a === 'resend') toast(T('Démo : lien renvoyé à ', 'Demo: link resent to ') + ((getJ('fw_pending', {}) || {}).email || ''));
    else if (a === 'verify') Backend.verify().then(function (m) { if (m) { syncClass(); applyLocks(); render('welcome'); } });
  }

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^\+?[0-9 ().\-]{6,22}$/;
  function submit(btn) {
    var form = ov.querySelector('form'), ok = true, d = {};
    ['first', 'middle', 'last', 'email', 'phone', 'city', 'country'].forEach(function (k) {
      var i = form.querySelector('#fa-' + k), v = i.value.trim().replace(/\s+/g, ' '), wrap = i.closest('.fa-f');
      var bad = (i.required && !v) || (k === 'email' && v && !EMAIL_RE.test(v)) || (k === 'phone' && v && !PHONE_RE.test(v));
      wrap.classList.toggle('bad', !!bad); if (bad) ok = false;
      d[k] = k === 'email' ? v.toLowerCase() : v;
    });
    var c = ov.querySelector('#fa-consent'), cl = c.closest('.fa-consent');
    cl.classList.toggle('bad', !c.checked); if (!c.checked) ok = false;
    if (!ok) { var first = ov.querySelector('.bad input'); if (first) first.focus(); return; }
    d.consent = { access: true, at: new Date().toISOString(), policy: POLICY_VERSION, lang: L() };
    d.page = HERE;
    btn.disabled = true;
    Backend.signUp(d).then(function () { render('sent'); });
  }
  function toast(msg) {
    addCSS();
    var t = document.createElement('div'); t.className = 'fa-toast'; t.textContent = msg; document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 2600);
  }

  /* ------------------------------------------------------------------ locks */
  var RULE = null;
  RULES.forEach(function (r) { if (!RULE && r.test(HERE)) RULE = r; });

  function card(why) {
    var c = document.createElement('div'); c.className = 'fa-card';
    c.innerHTML = '<div class="fa-cin">' + LOCK_SVG + t2(why[0], why[1]) +
      '<button class="fa-btn" type="button">' + t2('Débloquer gratuitement', 'Unlock for free') + '</button></div>';
    c.querySelector('button').addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); open(why); });
    tr(c);
    return c;
  }
  var pageCover = null;
  function applyLocks() {
    syncClass();
    if (!ENABLED || !RULE) return;
    if (RULE.lock) RULE.lock.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        if (isMember()) { el.classList.remove('fa-lockbox'); var k = el.querySelector(':scope > .fa-card'); if (k) k.remove(); return; }
        el.classList.add('fa-lockbox');
        if (!el.querySelector(':scope > .fa-card')) el.appendChild(card(RULE.why));
      });
    });
    if (RULE.clicks) RULE.clicks.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) { el.classList.add('fa-clicklock'); });
    });
    if (RULE.page && !isMember() && !pageCover) {
      pageCover = document.createElement('div'); pageCover.className = 'fa-page';
      pageCover.innerHTML = '<div class="fa-box" role="dialog" aria-modal="true">' + LOCK_SVG.replace('<svg ', '<svg class="fa-lock" ') +
        t2('Réservé aux membres', 'Members only', 'p', 'fa-kick') +
        t2('Plans cadastraux', 'Cadastral plans', 'h2', 'fa-h') +
        t2('Les plans parcellaires de toutes les appellations sont accessibles gratuitement aux membres. L’inscription prend une minute.',
           'The parcel plans of every appellation are free for members. Signing up takes a minute.', 'p', 'fa-lead') +
        '<div class="fa-act"><button class="fa-btn" type="button" data-go="join">' + t2('Créer mon accès gratuit', 'Get free access') + '</button>' +
        '<a class="fa-btn ghost" style="text-decoration:none" href="' + SITE + encodeURI(SAMPLES[0]) + '">' + t2('Voir un plan d’exemple', 'See a sample plan') + '</a></div>' +
        '<p class="fa-small"><a href="' + SITE + 'index.html">' + t2('← Retour à l’accueil', '← Back to the home page') + '</a></p>' +
        demoNote() + '</div>';
      pageCover.querySelector('[data-go="join"]').addEventListener('click', function () { open(RULE.why); });
      document.body.appendChild(pageCover);
      tr(pageCover);
    }
    if (pageCover && isMember()) { pageCover.remove(); pageCover = null; }
  }
  // clicks on locked controls open the form instead (capture phase: runs before the page's own handlers)
  document.addEventListener('click', function (e) {
    if (!ENABLED || isMember() || !RULE || !RULE.clicks) return;
    for (var i = 0; i < RULE.clicks.length; i++) {
      if (e.target.closest && e.target.closest(RULE.clicks[i])) {
        e.preventDefault(); e.stopImmediatePropagation(); open(RULE.why); return;
      }
    }
  }, true);

  // small padlock on links that lead to a fully locked page (menu, home page, lists)
  function markLinks(scope) {
    if (!ENABLED || isMember()) { document.querySelectorAll('a.fa-locklink').forEach(function (a) { a.classList.remove('fa-locklink'); }); return; }
    (scope || document).querySelectorAll('a[href]').forEach(function (a) {
      if (a.__faChecked) return; a.__faChecked = true;
      var p = rel(a.href); if (!p) return;
      for (var i = 0; i < RULES.length; i++) if (RULES[i].page && RULES[i].test(p)) { a.classList.add('fa-locklink'); return; }
    });
  }

  /* ------------------------------------------------------------------ automatic popup */
  function maybeAuto() {
    if (!ENABLED || isMember()) return;
    if (/^Infos\/(Confidentialite|_admin_members)\.html$/.test(HERE)) return;
    var pv = (+get('fw_pv') || 0) + 1; set('fw_pv', String(pv));
    if (sget('fw_dismissed')) return;
    if (+get('fw_snooze_until') > Date.now()) return;
    var go = function () { if (!ov && !isMember()) open(RULE && RULE.page ? RULE.why : null); };
    if (pv >= POPUP_ON_PAGEVIEW) setTimeout(go, 1200); else setTimeout(go, POPUP_DELAY_MS);
  }

  /* ------------------------------------------------------------------ owner bypass (#cle=…) */
  function sha256(str) {                       // small pure-JS SHA-256 (works on file:// too)
    var K = [], H = [], i, j, n = 0, isP = function (x) { for (var d = 2; d * d <= x; d++) if (x % d === 0) return false; return true; };
    for (i = 2; n < 64; i++) if (isP(i)) { if (n < 8) H[n] = (Math.pow(i, 1 / 2) * 4294967296) | 0; K[n++] = (Math.pow(i, 1 / 3) * 4294967296) | 0; }
    var b = unescape(encodeURIComponent(str)), l = b.length, w = [];
    for (i = 0; i < l; i++) w[i >> 2] |= b.charCodeAt(i) << ((3 - i % 4) * 8);
    w[l >> 2] |= 0x80 << ((3 - l % 4) * 8); w[(((l + 8) >> 6) << 4) + 15] = l * 8;
    for (i = 0; i < w.length; i++) w[i] = w[i] | 0;                        // fill holes (undefined → NaN in sums)
    var R = function (x, c) { return (x >>> c) | (x << (32 - c)); };
    for (j = 0; j < w.length; j += 16) {
      var W = w.slice(j, j + 16), a = H.slice(0);
      for (i = 0; i < 64; i++) {
        if (i >= 16) { var x = W[i - 15], y = W[i - 2]; W[i] = (W[i - 16] + (R(x, 7) ^ R(x, 18) ^ (x >>> 3)) + W[i - 7] + (R(y, 17) ^ R(y, 19) ^ (y >>> 10))) | 0; }
        var t1 = a[7] + (R(a[4], 6) ^ R(a[4], 11) ^ R(a[4], 25)) + ((a[4] & a[5]) ^ (~a[4] & a[6])) + K[i] + (W[i] | 0);
        var t2 = (R(a[0], 2) ^ R(a[0], 13) ^ R(a[0], 22)) + ((a[0] & a[1]) ^ (a[0] & a[2]) ^ (a[1] & a[2]));
        a = [(t1 + t2) | 0].concat(a); a[4] = (a[4] + t1) | 0; a.length = 8;
      }
      for (i = 0; i < 8; i++) H[i] = (H[i] + a[i]) | 0;
    }
    return H.map(function (h) { return ('00000000' + (h >>> 0).toString(16)).slice(-8); }).join('');
  }
  function ownerKey() {
    var m = /[#&]cle=([^&]*)/.exec(location.hash); if (!m) return;
    var v = ''; try { v = decodeURIComponent(m[1]); } catch (e) { v = m[1]; }
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}   // wipe the passphrase from the address bar
    if (v === 'off') { del('fw_owner'); syncClass(); applyLocks(); toast(T('Mode propriétaire désactivé sur ce navigateur.', 'Owner mode switched off in this browser.')); return; }
    if (OWNER_HASH && sha256('fw-owner:' + v) === OWNER_HASH) {
      set('fw_owner', OWNER_HASH); syncClass(); applyLocks(); markLinks(); close(true);
      toast(T('Mode propriétaire activé sur ce navigateur.', 'Owner mode switched on in this browser.'));
    }
  }

  /* ------------------------------------------------------------------ boot */
  var moT = null;
  function boot() {
    ownerKey();
    window.addEventListener('hashchange', ownerKey);   // typing #cle=… after the current address doesn't reload the page
    if (!ENABLED) { syncClass(); return; }
    addCSS(); applyLocks(); markLinks(); maybeAuto();
    new MutationObserver(function () {
      clearTimeout(moT); moT = setTimeout(function () { applyLocks(); markLinks(); }, 120);
    }).observe(document.body, { childList: true, subtree: true });
    new MutationObserver(function () { tr(); }).observe(root, { attributes: true, attributeFilter: ['lang'] });
    window.addEventListener('storage', function (e) { if (e.key === 'fw_member') { syncClass(); applyLocks(); markLinks(); } });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();

  /* ------------------------------------------------------------------ public API (privacy / admin pages) */
  window.FWAccess = {
    open: function (step) { open(null, step); },
    member: member,
    pending: function () { return getJ('fw_pending', null); },
    signOut: function () { return Backend.signOut().then(function () { syncClass(); applyLocks(); markLinks(); }); },
    deleteMe: function () { return Backend.deleteMe().then(function () { syncClass(); applyLocks(); markLinks(); }); },
    update: function (patch) {
      var m = member(); if (!m) return;
      for (var k in patch) m[k] = patch[k];
      setJ('fw_member', m);
      setJ('fw_demo_db', getJ('fw_demo_db', []).map(function (r) { return r.email === m.email ? m : r; }));
    },
    db: function () { return getJ('fw_demo_db', []); },
    clearDb: function () { del('fw_demo_db'); },
    resetDemo: function () { ['fw_member', 'fw_pending', 'fw_pv', 'fw_snooze_until'].forEach(del); try { sessionStorage.removeItem('fw_dismissed'); } catch (e) {} syncClass(); },
    isOwner: isOwner, enabled: ENABLED,
    rules: RULES, samples: SAMPLES, backend: Backend.name, policyVersion: POLICY_VERSION
  };
})();
