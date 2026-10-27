(function () {
  'use strict';
  // Interacoes da home estatica. Substitui o que o aplicativo React compilado
  // fazia na pagina: menu, abas, FAQ, filtro de projetos, som dos videos,
  // aviso de cookies e destaque do item de menu conforme a rolagem.
  if (window.__tqHome) return;
  window.__tqHome = true;

  var header = document.getElementById('tq-header');

  // ------------------------------------------------------------ cabecalho
  function aoRolar() {
    if (header) header.classList.toggle('tq-scrolled', window.scrollY > 24);
  }
  aoRolar();
  window.addEventListener('scroll', aoRolar, { passive: true });

  (function menuMobile() {
    var btn = document.getElementById('lp-menu-btn');
    var menu = document.getElementById('lp-mobile-menu');
    var iconMenu = document.getElementById('lp-icon-menu');
    var iconClose = document.getElementById('lp-icon-close');
    if (!btn || !menu) return;
    function define(aberto) {
      menu.classList.toggle('hidden', !aberto);
      if (iconMenu) iconMenu.classList.toggle('hidden', aberto);
      if (iconClose) iconClose.classList.toggle('hidden', !aberto);
      btn.setAttribute('aria-expanded', String(aberto));
      if (header) header.classList.toggle('tq-menu-open', aberto);
    }
    btn.addEventListener('click', function () { define(menu.classList.contains('hidden')); });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { define(false); });
    });
  })();

  (function destaqueMenu() {
    var links = [].slice.call(document.querySelectorAll('.tq-nav a[href^="#"]'));
    var secoes = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
    if (!secoes.length) return;
    var agendado = false;
    function marca() {
      agendado = false;
      var y = window.scrollY + window.innerHeight * 0.35;
      // A ordem do menu nao e a da pagina (Projetos vem antes de "Como trabalhamos"),
      // entao compara pela posicao real de cada secao.
      var atual = secoes[0];
      secoes.slice().sort(function (a, b) { return a.offsetTop - b.offsetTop; })
        .forEach(function (s) { if (s.offsetTop <= y) atual = s; });
      links.forEach(function (a) {
        if (a.getAttribute('href') === '#' + atual.id) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }
    window.addEventListener('scroll', function () {
      if (!agendado) { agendado = true; requestAnimationFrame(marca); }
    }, { passive: true });
    marca();
  })();

  // ------------------------------------------------------------ abas (Solucoes)
  document.querySelectorAll('[role="tablist"]').forEach(function (lista) {
    var abas = [].slice.call(lista.querySelectorAll('[role="tab"]'));
    function ativa(aba) {
      abas.forEach(function (a) {
        var ligada = a === aba;
        a.setAttribute('aria-selected', String(ligada));
        a.setAttribute('data-state', ligada ? 'active' : 'inactive');
        a.tabIndex = ligada ? 0 : -1;
        var painel = document.getElementById(a.getAttribute('aria-controls'));
        if (painel) { painel.setAttribute('data-state', ligada ? 'active' : 'inactive'); painel.hidden = !ligada; }
      });
    }
    abas.forEach(function (aba, i) {
      aba.addEventListener('click', function () { ativa(aba); });
      aba.addEventListener('keydown', function (e) {
        var passo = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!passo) return;
        e.preventDefault();
        var prox = abas[(i + passo + abas.length) % abas.length];
        ativa(prox); prox.focus();
      });
    });
  });

  // ------------------------------------------------------------ FAQ (acordeao)
  document.querySelectorAll('button[aria-expanded][data-orientation="vertical"]').forEach(function (btn) {
    var regiao = document.querySelector('[role="region"][aria-labelledby="' + btn.id + '"]');
    if (!regiao) return;
    var item = btn.closest('div[data-state]');
    btn.addEventListener('click', function () {
      var abrir = btn.getAttribute('data-state') !== 'open';
      var estado = abrir ? 'open' : 'closed';
      btn.setAttribute('data-state', estado);
      btn.setAttribute('aria-expanded', String(abrir));
      regiao.setAttribute('data-state', estado);
      regiao.hidden = !abrir;
      if (item) item.setAttribute('data-state', estado);
    });
  });

  // ------------------------------------------------------------ filtro de projetos
  (function filtroProjetos() {
    var sec = document.getElementById('projetos');
    if (!sec) return;
    var botoes = [].slice.call(sec.querySelectorAll('button')).filter(function (b) { return /rounded-full/.test(b.className); });
    var cards = [].slice.call(sec.querySelectorAll('article'));
    if (!botoes.length || !cards.length) return;
    var LIGADO = ['bg-[oklch(0.14_0.03_258)]', 'text-white', 'border-transparent'];
    var DESLIGADO = ['bg-background', 'text-foreground', 'border-border', 'hover:bg-accent'];
    function norm(s) { return (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim(); }
    function categoria(card) {
      // data-categoria vem do gerador (refazer-home.mjs); o rotulo visivel e so reserva.
      var el = card.querySelector('.text-xs.font-medium');
      return norm(card.getAttribute('data-categoria') || (el && el.textContent));
    }
    function aplica(rotulo) {
      var k = norm(rotulo);
      botoes.forEach(function (b) {
        var on = norm(b.textContent) === k;
        LIGADO.forEach(function (c) { b.classList.toggle(c, on); });
        DESLIGADO.forEach(function (c) { b.classList.toggle(c, !on); });
        b.setAttribute('aria-pressed', String(on));
      });
      cards.forEach(function (c) {
        var cat = categoria(c);
        var mostra = k === 'todos' ||
          (k === 'automacao' && cat.indexOf('automa') > -1) ||
          (k === 'agronegocio' && cat.indexOf('agro') > -1) ||
          (k === 'aplicativos' && (cat.indexOf('aplicativo') > -1 || cat.indexOf('app') > -1 || cat.indexOf('software') > -1));
        c.hidden = !mostra;
      });
    }
    botoes.forEach(function (b) { b.addEventListener('click', function () { aplica(b.textContent); }); });
  })();

  // ------------------------------------------------------------ videos
  var ICONE_SOM = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-volume-2 h-5 w-5" aria-hidden="true"><path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"/><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.364 18.364a9 9 0 0 0 0-12.728"/></svg>';
  document.querySelectorAll('button[aria-label*="som do v"]').forEach(function (btn) {
    var video = btn.parentElement && btn.parentElement.querySelector('video');
    if (!video) return;
    var iconeMudo = btn.innerHTML;
    btn.addEventListener('click', function () {
      video.muted = !video.muted;
      if (!video.muted && video.paused && video.play) video.play().catch(function () {});
      btn.innerHTML = video.muted ? iconeMudo : ICONE_SOM;
      btn.setAttribute('aria-label', video.muted ? 'Ativar som do vídeo' : 'Desativar som do vídeo');
    });
  });
  // preload="none" + autoplay: o navegador so comeca quando mandamos. Toca ao entrar na tela.
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) { if (v.paused && v.play) v.play().catch(function () {}); }
        else if (!v.paused) v.pause();
      });
    }, { threshold: 0.25 });
    document.querySelectorAll('video[autoplay], video[autoPlay]').forEach(function (v) { v.muted = true; obs.observe(v); });
  }

  // ------------------------------------------------------------ contadores do hero
  (function contadores() {
    var els = [].slice.call(document.querySelectorAll('[data-count]'));
    if (!els.length || !('IntersectionObserver' in window)) return;
    var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var el = en.target, fim = parseInt(el.getAttribute('data-count'), 10), pre = el.getAttribute('data-prefix') || '';
        if (reduz || isNaN(fim)) { el.textContent = pre + fim; return; }
        var t0 = null;
        function passo(t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 900), e = 1 - Math.pow(1 - p, 3);
          el.textContent = pre + Math.round(fim * e);
          if (p < 1) requestAnimationFrame(passo);
        }
        requestAnimationFrame(passo);
      });
    }, { threshold: 0.6 });
    els.forEach(function (el) { io.observe(el); });
  })();

  // ------------------------------------------------------------ aviso de cookies
  (function cookies() {
    var CHAVE = 'tq_cookie_consent_v1';
    try { if (localStorage.getItem(CHAVE)) return; } catch (e) { return; }
    setTimeout(function () {
      var caixa = document.createElement('div');
      caixa.className = 'fixed bottom-4 left-4 right-4 md:left-6 md:right-auto md:max-w-md z-[60] animate-in fade-in slide-in-from-bottom-4 duration-500';
      caixa.innerHTML =
        '<div class="rounded-2xl border border-white/10 bg-[oklch(0.14_0.03_258)]/95 backdrop-blur-xl shadow-2xl p-4 md:p-5"><div class="flex items-start gap-3">' +
        '<div class="shrink-0 rounded-lg bg-[oklch(0.69_0.17_54)]/15 p-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 text-[oklch(0.84_0.13_75)]" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg></div>' +
        '<div class="flex-1 min-w-0"><h4 class="text-sm font-semibold text-white">Cookies e privacidade</h4>' +
        '<p class="mt-1 text-xs leading-relaxed text-white/60">Utilizamos cookies e dados técnicos (navegador, dispositivo, idioma e localização aproximada por IP) para análise de audiência e melhoria contínua. Nenhuma informação pessoal é vendida. Ao continuar, você concorda com nossa <a href="/politica-de-privacidade" class="text-[oklch(0.84_0.13_75)] hover:underline">Política de Privacidade</a>.</p>' +
        '<div class="mt-3 flex flex-wrap gap-2"><button type="button" data-consent="accepted" class="inline-flex items-center justify-center rounded-md bg-[oklch(0.69_0.17_54)] px-3 py-1.5 text-xs font-medium text-white hover:bg-[oklch(0.69_0.17_54)]/90 transition">Entendi</button>' +
        '<button type="button" data-consent="dismissed" class="inline-flex items-center justify-center rounded-md border border-white/15 px-3 py-1.5 text-xs font-medium text-white/80 hover:bg-white/10 transition">Saber mais depois</button></div></div></div></div>';
      document.body.appendChild(caixa);
      caixa.querySelectorAll('button[data-consent]').forEach(function (b) {
        b.addEventListener('click', function () {
          try { localStorage.setItem(CHAVE, b.getAttribute('data-consent')); } catch (e) {}
          caixa.remove();
        });
      });
    }, 800);
  })();
})();
