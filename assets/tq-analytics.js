(function () {
  'use strict';
  // Audiencia para o painel /admin, igual ao que o aplicativo React compilado
  // gravava: uma linha 'pageview' ao abrir, uma 'permanencia' ao sair e um
  // registro por clique em WhatsApp. Mesmas tabelas, mesmas colunas e as
  // mesmas chaves de sessao/geolocalizacao, entao o historico continua.
  if (window.__tqAnalytics) return;
  window.__tqAnalytics = true;

  var BASE = 'https://iqsprnneeogeugmwomgz.supabase.co/rest/v1/';
  // Chave publica (anon) do projeto, a mesma que ja viajava dentro do bundle.
  var CHAVE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlxc3Bybm5lZW9nZXVnbXdvbWd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQxOTYxODQsImV4cCI6MjA5OTc3MjE4NH0.j_uvWAOV0PBx_1fJ-cFMTZ4bax9BCdUEOb3yRNrHRGY';
  var SESSAO = 'tq_session_id', SESSAO_INICIO = 'tq_session_start';
  var GEO = 'tq_geo_v2', GEO_PERSISTE = 'tq_geo_v2_persist';

  function grava(tabela, linha) {
    try {
      fetch(BASE + tabela, {
        method: 'POST',
        headers: { apikey: CHAVE, Authorization: 'Bearer ' + CHAVE, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify(linha),
        keepalive: true
      }).catch(function () {});
    } catch (e) {}
  }

  function novoId() {
    return (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID()
      : 'sid_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
  }
  function sessao() {
    try {
      var id = sessionStorage.getItem(SESSAO);
      if (!id) { id = novoId(); sessionStorage.setItem(SESSAO, id); sessionStorage.setItem(SESSAO_INICIO, String(Date.now())); }
      return id;
    } catch (e) { return 'sem-sessao'; }
  }

  function dispositivo() {
    var ua = navigator.userAgent || '';
    var nav = /Edg\//.test(ua) ? 'Edge' : /OPR\/|Opera/.test(ua) ? 'Opera' : /Chrome\//.test(ua) ? 'Chrome' : /Firefox\//.test(ua) ? 'Firefox' : /Safari\//.test(ua) ? 'Safari' : 'Other';
    var ipad = /iPad/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var so = /iPhone|iPod/.test(ua) ? 'iOS' : ipad ? 'iPadOS' : /Android/i.test(ua) ? 'Android' : /Windows/i.test(ua) ? 'Windows' : /CrOS/i.test(ua) ? 'ChromeOS' : /Mac OS X|Macintosh/i.test(ua) ? 'macOS' : /Linux/i.test(ua) ? 'Linux' : 'Outros';
    var tipo = so === 'iOS' ? 'mobile' : so === 'iPadOS' ? 'tablet' : /Android/i.test(ua) ? (/Mobile/.test(ua) ? 'mobile' : 'tablet') : /Mobi|Tablet/i.test(ua) ? (/Tablet/i.test(ua) ? 'tablet' : 'mobile') : 'desktop';
    return { device: tipo, browser: nav, os: so };
  }

  function utms() {
    var q = new URLSearchParams(location.search), o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach(function (k) { var v = q.get(k); if (v) o[k] = v; });
    return o;
  }

  // Geolocalizacao aproximada por IP, com cache de 24h (mesmas chaves do bundle).
  var FONTES = [
    function () { return fetch('https://ipwho.is/?fields=ip,success,country,country_code,region,city,postal,latitude,longitude,timezone,connection').then(function (r) { return r.json(); }).then(function (t) {
      if (t.success === false) throw 0;
      return { ip_address: t.ip || null, country: t.country || null, country_code: t.country_code || null, region: t.region || null, city: t.city || null, postal_code: t.postal || null, latitude: typeof t.latitude === 'number' ? t.latitude : null, longitude: typeof t.longitude === 'number' ? t.longitude : null, timezone: (t.timezone && t.timezone.id) || t.timezone || null, isp: (t.connection && (t.connection.isp || t.connection.org)) || null }; }); },
    function () { return fetch('https://ipapi.co/json/').then(function (r) { return r.json(); }).then(function (t) {
      if (t.error) throw 0;
      return { ip_address: t.ip || null, country: t.country_name || null, country_code: t.country_code || null, region: t.region || null, city: t.city || null, postal_code: t.postal || null, latitude: typeof t.latitude === 'number' ? t.latitude : null, longitude: typeof t.longitude === 'number' ? t.longitude : null, timezone: t.timezone || null, isp: t.org || t.asn || null }; }); },
    function () { return fetch('https://get.geojs.io/v1/ip/geo.json').then(function (r) { return r.json(); }).then(function (t) {
      return { ip_address: t.ip || null, country: t.country || null, country_code: t.country_code || null, region: t.region || null, city: t.city || null, postal_code: null, latitude: t.latitude ? Number(t.latitude) : null, longitude: t.longitude ? Number(t.longitude) : null, timezone: t.timezone || null, isp: t.organization_name || t.organization || null }; }); }
  ];
  function geoCache() {
    try {
      var s = sessionStorage.getItem(GEO); if (s) return JSON.parse(s);
      var p = localStorage.getItem(GEO_PERSISTE);
      if (p) { var o = JSON.parse(p); if (Date.now() - o.t < 864e5) return o.g; }
    } catch (e) {}
    return null;
  }
  function geoGuarda(g) {
    try { sessionStorage.setItem(GEO, JSON.stringify(g)); localStorage.setItem(GEO_PERSISTE, JSON.stringify({ t: Date.now(), g: g })); } catch (e) {}
  }
  function fuso() { try { return Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return null; } }
  function geo() {
    var c = geoCache();
    if (c && c.country) return Promise.resolve(c);
    var i = 0;
    function tenta() {
      if (i >= FONTES.length) return Promise.resolve({ timezone: fuso() });
      return FONTES[i++]().then(function (g) {
        if (!g.country && !g.country_code) throw 0;
        if (!g.timezone) g.timezone = fuso();
        geoGuarda(g); return g;
      }).catch(tenta);
    }
    return tenta();
  }

  // ------------------------------------------------------------ pageview
  var caminho = location.pathname, inicio = Date.now(), maxScroll = 0, enviouPermanencia = false;
  var d = dispositivo();
  geo().then(function (g) {
    var linha = {
      session_id: sessao(), event_type: 'pageview', page_path: caminho, page_title: document.title,
      referrer: document.referrer || null, user_agent: navigator.userAgent, language: navigator.language || null,
      browser: d.browser, os: d.os, device: d.device,
      country: g.country || null, country_code: g.country_code || null, region: g.region || null, city: g.city || null,
      postal_code: g.postal_code || null, latitude: g.latitude || null, longitude: g.longitude || null,
      timezone: g.timezone || null, isp: g.isp || null, ip_address: g.ip_address || null
    };
    var u = utms(); for (var k in u) linha[k] = u[k];
    grava('analytics_events', linha);
  });

  // ------------------------------------------------------------ permanencia
  function secaoVisivel() {
    var alvo = window.scrollY + window.innerHeight * 0.5, atual = null;
    document.querySelectorAll('section[id]').forEach(function (s) { if (s.offsetTop <= alvo) atual = s.id; });
    return atual;
  }
  window.addEventListener('scroll', function () {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (h > 0) maxScroll = Math.max(maxScroll, Math.round(100 * window.scrollY / h));
  }, { passive: true });
  function permanencia() {
    if (enviouPermanencia) return;
    var dur = Date.now() - inicio;
    if (dur < 1000) return;
    enviouPermanencia = true;
    var partes = [];
    var sec = secaoVisivel(); if (sec) partes.push('secao=' + sec.replace(/[;=]/g, ''));
    partes.push('scroll=' + maxScroll);
    grava('analytics_events', { session_id: sessao(), event_type: 'permanencia', page_path: caminho, duration_ms: dur, page_title: partes.join(';') });
  }
  window.addEventListener('pagehide', permanencia);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') permanencia(); });

  // ------------------------------------------------------------ cliques em WhatsApp
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (!/wa\.me|api\.whatsapp\.com|whatsapp:\/\//.test(href)) return;
    var sec = a.closest('section[id]');
    var local = /fixed/.test(a.className) ? 'flutuante' : sec ? sec.id : a.closest('footer') ? 'rodape' : a.closest('header') ? 'cabecalho' : 'pagina';
    var u = utms();
    grava('whatsapp_clicks', { session_id: sessao(), page_path: caminho, button_location: local, service: null, source: 'site', device: d.device, utm_source: u.utm_source, utm_medium: u.utm_medium, utm_campaign: u.utm_campaign });
  }, true);
})();
