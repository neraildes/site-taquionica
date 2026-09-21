(function () {
  'use strict';

  var EMAIL = 'taquionica.oficial@gmail.com';
  var WEB3FORMS_KEY = '';

  var ENDPOINT = WEB3FORMS_KEY
    ? 'https://api.web3forms.com/submit'
    : 'https://formsubmit.co/ajax/' + EMAIL;

  var UTMS = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'];

  // UTM e GCLID chegam na primeira visita e somem na navegacao seguinte.
  // Guardar na sessao mantem a origem do lead mesmo se a pessoa circular
  // pelo site antes de preencher.
  function memoriaOrigem() {
    var guardado = {};
    try { guardado = JSON.parse(sessionStorage.getItem('tq_origem') || '{}'); } catch (e) { guardado = {}; }
    var busca = new URLSearchParams(location.search);
    var mudou = false;
    UTMS.forEach(function (k) {
      var v = busca.get(k);
      if (v) { guardado[k] = v; mudou = true; }
    });
    if (mudou) { try { sessionStorage.setItem('tq_origem', JSON.stringify(guardado)); } catch (e) {} }
    return guardado;
  }

  // Marca que UM envio foi confirmado. A pagina /obrigado so conta conversao
  // se encontrar esta marca, e a apaga em seguida. Assim, abrir /obrigado
  // direto pela URL nao gera conversao, e recarregar a pagina nao conta duas.
  function marcaEnvioConfirmado() {
    try { sessionStorage.setItem('tq_lead_ok', String(Date.now())); } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    var f = document.getElementById('tq-form');
    if (!f) return;

    var origem = memoriaOrigem();
    UTMS.forEach(function (k) {
      var campo = f.querySelector('[name="' + k + '"]');
      if (campo) campo.value = origem[k] || '';
    });
    var lp = f.querySelector('[name="landing_page"]');
    if (lp) lp.value = location.pathname;

    var botao = f.querySelector('.tq-send');
    var erro = f.querySelector('.tq-err');
    var rotulo = botao ? botao.textContent : '';
    var enviando = false;

    function mostraErro(msg) {
      if (!erro) return;
      erro.textContent = msg;
      erro.style.display = 'block';
    }

    function liberaBotao() {
      enviando = false;
      if (!botao) return;
      botao.disabled = false;
      botao.removeAttribute('aria-busy');
      botao.textContent = rotulo;
    }

    // O servico responde de formas diferentes: Web3Forms devolve success
    // booleano, FormSubmit devolve a string "true".
    function deuCerto(r) {
      if (!r) return false;
      return r.success === true || r.success === 'true';
    }

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (enviando) return;
      if (erro) erro.style.display = 'none';
      if (!f.checkValidity()) { f.reportValidity(); return; }

      enviando = true;
      if (botao) { botao.disabled = true; botao.setAttribute('aria-busy', 'true'); botao.textContent = 'Enviando...'; }

      var dados = new FormData(f);
      dados.append('_subject', 'Nova avaliacao de projeto - ' + location.pathname);
      if (WEB3FORMS_KEY) {
        dados.append('access_key', WEB3FORMS_KEY);
        dados.append('subject', 'Nova avaliacao de projeto - ' + location.pathname);
        dados.append('from_name', 'Site Taquionica');
      } else {
        dados.append('_template', 'table');
        dados.append('_captcha', 'false');
      }

      fetch(ENDPOINT, { method: 'POST', headers: { Accept: 'application/json' }, body: dados })
        .then(function (r) { return r.json().catch(function () { return null; }); })
        .then(function (r) {
          if (!deuCerto(r)) throw new Error((r && (r.message || r.error)) || 'envio nao confirmado');
          // So aqui o envio esta confirmado de verdade.
          marcaEnvioConfirmado();
          window.location.href = '/obrigado/';
        })
        .catch(function () {
          liberaBotao();
          mostraErro('Nao conseguimos enviar seu projeto agora. Seus dados continuam preenchidos: tente novamente em instantes. Se preferir, fale com a gente pelo WhatsApp usando o botao acima.');
        });
    });
  });
})();