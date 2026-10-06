(function () {
  'use strict';
  // Acrescenta a origem da visita ao texto pre-preenchido do WhatsApp, para a
  // equipe saber que o contato veio do Google Ads (e de qual campanha, quando
  // houver UTM). Nao envia nada a lugar nenhum: so altera o texto do link no
  // momento do clique. A identificacao do servico ja esta no texto de cada pagina.
  if (window.__tqWa) return;
  window.__tqWa = true;

  var CHAVES = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'];

  function origem() {
    var o = {};
    try { o = JSON.parse(sessionStorage.getItem('tq_origem') || '{}') || {}; } catch (e) { o = {}; }
    var busca = new URLSearchParams(location.search);
    var mudou = false;
    CHAVES.forEach(function (k) {
      var v = busca.get(k);
      if (v) { o[k] = v; mudou = true; }
    });
    if (mudou) { try { sessionStorage.setItem('tq_origem', JSON.stringify(o)); } catch (e) {} }
    return o;
  }

  function sufixo(o) {
    var partes = [];
    if (o.gclid) partes.push('Google Ads');
    else if (o.utm_source) partes.push(o.utm_source);
    if (o.utm_campaign) partes.push(o.utm_campaign);
    if (o.utm_term) partes.push('termo: ' + o.utm_term);
    if (o.gclid) partes.push('ref ' + String(o.gclid).slice(-8));
    return partes.length ? ' [Origem: ' + partes.join(' | ').slice(0, 160) + ']' : '';
  }

  var dados = origem();

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="wa.me/"]') : null;
    if (!a || a.getAttribute('data-tq-origem')) return;
    var s = sufixo(dados);
    if (!s) return;
    try {
      var url = new URL(a.href);
      var texto = url.searchParams.get('text') || '';
      // encodeURIComponent (espaco vira %20), em vez de searchParams.set,
      // que trocaria espaco por "+" no texto do WhatsApp.
      a.href = url.origin + url.pathname + '?text=' + encodeURIComponent(texto + s);
      a.setAttribute('data-tq-origem', '1');
    } catch (err) {}
  }, true);
})();
