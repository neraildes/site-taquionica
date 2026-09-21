(function () {
  'use strict';

  // ====== UNICO PONTO A CONFIGURAR ======
  // Cole aqui a Access Key gratuita do https://web3forms.com (chega por e-mail).
  var ACCESS_KEY = '';
  // ======================================

  var ENDPOINT = 'https://api.web3forms.com/submit';
  var WHATS = '5516993668447';
  var UTMS = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'];

  // UTM e GCLID chegam na primeira visita e somem na navegacao seguinte.
  // Guardar na sessao mantem a origem do lead mesmo se a pessoa circular pelo site.
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

  function evento(nome) {
    if (typeof gtag === 'function') gtag('event', nome, { transport_type: 'beacon' });
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

    function mostraErro(msg) {
      if (!erro) return;
      erro.textContent = msg;
      erro.style.display = 'block';
    }

    function valor(n) {
      var el = f.querySelector('[name="' + n + '"]');
      return el && el.value ? el.value.trim() : '';
    }

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (erro) erro.style.display = 'none';

      if (!f.checkValidity()) { f.reportValidity(); return; }

      // Sem chave configurada nao existe envio que possa ser confirmado.
      // Encaminha pelo WhatsApp e NAO redireciona, para nao contar conversao falsa.
      if (!ACCESS_KEY) {
        var linhas = [
          'Ola! Quero uma avaliacao de projeto. Vim da pagina ' + location.pathname + '.',
          '', 'Nome: ' + valor('nome'), 'Empresa: ' + valor('empresa'),
          'E-mail: ' + valor('email'), 'Telefone: ' + valor('telefone'),
          'Investimento: ' + valor('investimento'), 'Prazo: ' + valor('prazo'),
          '', 'Projeto: ' + valor('projeto')
        ];
        var a = document.createElement('a');
        a.href = 'https://wa.me/' + WHATS + '?text=' + encodeURIComponent(linhas.join('\n'));
        a.target = '_blank'; a.rel = 'noopener noreferrer';
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        mostraErro('Formulario ainda sem chave de envio configurada: abrimos o WhatsApp com os dados preenchidos. Nenhuma conversao foi registrada.');
        if (console && console.warn) console.warn('[Taquionica] ACCESS_KEY vazia em /assets/tq-lead.js — o formulario nao envia nem converte.');
        return;
      }

      if (botao) { botao.disabled = true; botao.setAttribute('aria-busy', 'true'); botao.textContent = 'Enviando...'; }

      var dados = new FormData(f);
      dados.append('access_key', ACCESS_KEY);
      dados.append('subject', 'Nova avaliacao de projeto - ' + location.pathname);
      dados.append('from_name', 'Site Taquionica');

      fetch(ENDPOINT, { method: 'POST', body: dados })
        .then(function (r) { return r.json().catch(function () { return { success: false }; }); })
        .then(function (r) {
          // So um sucesso confirmado leva para /obrigado, que e onde a
          // conversao do Google Ads e contada.
          if (r && r.success) {
            evento('Lead_Projeto_Enviado');
            window.location.href = '/obrigado';
            return;
          }
          throw new Error((r && r.message) || 'resposta sem sucesso');
        })
        .catch(function () {
          if (botao) { botao.disabled = false; botao.removeAttribute('aria-busy'); botao.textContent = rotulo; }
          mostraErro('Nao conseguimos enviar agora. Os dados continuam preenchidos: tente novamente em instantes ou chame no WhatsApp (16) 99366-8447.');
        });
    });
  });
})();