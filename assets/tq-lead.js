(function () {
  'use strict';

  // =====================================================================
  // CONFIGURACAO DO ENVIO  -  preencha UMA das duas opcoes
  // ---------------------------------------------------------------------
  // 1) Web3Forms: pegue a access key em https://web3forms.com (ela chega
  //    por e-mail em segundos) e cole em WEB3FORMS_KEY. Nao exige nenhum
  //    outro passo depois disso.
  //
  // 2) FormSubmit: o primeiro envio dispara um e-mail de ativacao para o
  //    endereco de FORMSUBMIT_ALVO. ENQUANTO NINGUEM CLICAR em "Activate
  //    Form" nesse e-mail, a API responde HTTP 200 com success:"false" e
  //    NADA e entregue. Depois de ativar, o FormSubmit mostra um token
  //    aleatorio; usar o token aqui no lugar do e-mail evita expor o
  //    endereco no codigo-fonte da pagina para robos de spam.
  //
  // Com as duas vazias, o formulario nao envia e explica no console qual
  // passo esta faltando.
  // =====================================================================
  var WEB3FORMS_KEY = '11f35ae5-a62c-438f-a1b3-439035127c00';
  var FORMSUBMIT_ALVO = 'taquionica.oficial@gmail.com';

  var SERVICO = WEB3FORMS_KEY ? 'web3forms' : (FORMSUBMIT_ALVO ? 'formsubmit' : '');
  var ENDPOINT = SERVICO === 'web3forms'
    ? 'https://api.web3forms.com/submit'
    : (SERVICO === 'formsubmit' ? 'https://formsubmit.co/ajax/' + FORMSUBMIT_ALVO : '');

  var DESTINO_SUCESSO = '/obrigado/';
  var TIMEOUT_MS = 20000;

  var UTMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'];

  var GENERICA = 'Nao conseguimos enviar seu projeto agora. Seus dados continuam preenchidos: tente novamente em instantes. Se preferir, fale com a gente pelo WhatsApp usando o botao acima.';

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

  // Conversao do Google Ads "Formulario_Enviado_Sucesso" (acao por evento,
  // categoria Enviar formulario de lead), criada em 06/10/2026.
  var CONVERSAO_FORMULARIO = 'AW-18346942371/fZ7zCOir3ZIdEKO_wKxE';

  // Dispara a conversao UMA vez, aqui, somente depois que o servico de
  // formulario confirmou o envio no corpo da resposta. A pagina /obrigado nao
  // dispara nada: abrir /obrigado direto, recarregar ou voltar pelo navegador
  // nao gera evento. O transaction_id unico por envio faz o Google Ads
  // descartar qualquer repeticao do mesmo envio.
  function novoIdEnvio() {
    var r = '';
    try {
      var b = new Uint8Array(6);
      crypto.getRandomValues(b);
      for (var i = 0; i < b.length; i++) r += ('0' + b[i].toString(16)).slice(-2);
    } catch (e) { r = Math.random().toString(16).slice(2, 14); }
    return 'tq-' + Date.now().toString(36) + '-' + r;
  }

  function registraConversaoESegue(idEnvio, destino) {
    var foi = false;
    function segue() {
      if (foi) return;
      foi = true;
      window.location.href = destino;
    }
    if (typeof window.gtag !== 'function') { segue(); return; }
    try {
      window.gtag('event', 'conversion', {
        send_to: CONVERSAO_FORMULARIO,
        transaction_id: idEnvio,
        transport_type: 'beacon',
        event_callback: segue
      });
    } catch (e) { segue(); return; }
    // Se o gtag estiver bloqueado ou lento, o visitante nao fica preso.
    setTimeout(segue, 1500);
  }

  // Marca local, usada so para a /obrigado saber que veio de um envio
  // (exibicao). Nao gera conversao.
  function marcaEnvioConfirmado(idEnvio) {
    try { sessionStorage.setItem('tq_lead_ok', idEnvio); } catch (e) {}
  }

  // O diagnostico completo vai SEMPRE para o console, mesmo quando a pessoa
  // ve apenas a mensagem amigavel. Sem isto, uma falha de configuracao do
  // servico (que responde HTTP 200 dizendo success:"false") fica
  // indistinguivel de uma queda de rede.
  function diagnostico(info) {
    if (typeof console === 'undefined') return;
    try {
      var titulo = '[tq-lead] envio ' + (info.ok ? 'CONFIRMADO' : 'FALHOU') +
        ' - ' + (SERVICO || 'sem servico configurado');
      if (console.groupCollapsed) { console.groupCollapsed(titulo); } else { console.log(titulo); }
      console.log('URL.......:', info.url || '(nenhuma)');
      console.log('Metodo....: POST (multipart/form-data)');
      console.log('Status....:', info.status === undefined ? '(sem resposta)' : info.status + ' ' + (info.statusText || ''));
      console.log('Enviado...:', info.enviado);
      console.log('Resposta..:', info.resposta === undefined ? '(corpo nao lido)' : info.resposta);
      if (info.causa) console.warn('Causa.....:', info.causa);
      if (info.erro) console.error('Erro......:', info.erro);
      if (console.groupEnd) console.groupEnd();
    } catch (e) {}
  }

  // Traduz a falha real em algo acionavel. Cada caso descreve o que houve de
  // fato; o texto mostrado ao visitante continua sendo o amigavel.
  function explica(status, resposta) {
    var msg = ((resposta && (resposta.message || resposta.error)) || '') + '';
    var m = msg.toLowerCase();

    if (m.indexOf('activation') !== -1 || m.indexOf('activate') !== -1) {
      return 'FormSubmit ainda nao foi ativado. Um e-mail com o link "Activate Form" foi enviado para ' +
        FORMSUBMIT_ALVO + '. Enquanto ninguem clicar nesse link, todo envio falha e nada e entregue.';
    }
    if (m.indexOf('web server') !== -1) {
      return 'A pagina foi aberta como arquivo local (file://). O FormSubmit exige que a pagina venha de um servidor HTTP.';
    }
    if (status === 401 || status === 403) {
      return 'Chave ou origem recusada pelo servico (HTTP ' + status + '). Confira a access key e o dominio autorizado.';
    }
    if (status === 404) {
      return 'Endpoint inexistente (HTTP 404). Confira a URL do servico e o identificador do formulario.';
    }
    if (status === 422 || status === 400) {
      return 'O servico recusou os campos enviados (HTTP ' + status + '): ' + (msg || 'sem detalhe');
    }
    if (status === 429) {
      return 'Limite de envios atingido (HTTP 429). Aguarde antes de tentar de novo.';
    }
    if (status >= 500) {
      return 'Falha no servidor do servico (HTTP ' + status + '). O problema esta do lado dele.';
    }
    return msg || 'O servico respondeu sem confirmar o envio.';
  }

  // Os dois servicos confirmam de formas diferentes: Web3Forms devolve
  // success booleano, FormSubmit devolve a string "true". Qualquer outra
  // coisa (inclusive HTTP 200 com success:"false") conta como falha.
  function deuCerto(r) {
    if (!r) return false;
    return r.success === true || r.success === 'true';
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

    function falhou(info) {
      diagnostico(info);
      liberaBotao();
      mostraErro(GENERICA);
    }

    // Envio ja confirmado nesta pagina. Se a pessoa voltar pelo navegador
    // (pagina restaurada do cache), o formulario continua travado e avisa,
    // em vez de permitir reenviar o mesmo projeto por engano.
    var enviadoId = null;
    window.addEventListener('pageshow', function (ev) {
      if (!ev.persisted || !enviadoId || !botao) return;
      botao.disabled = true;
      botao.textContent = 'Projeto enviado';
      if (erro) {
        erro.textContent = 'Este projeto já foi enviado. Se quiser complementar, fale com a gente pelo WhatsApp.';
        erro.style.display = 'block';
      }
    });

    if (!SERVICO) {
      diagnostico({
        ok: false,
        causa: 'Nenhum servico de envio configurado: WEB3FORMS_KEY e FORMSUBMIT_ALVO estao vazios em assets/tq-lead.js.'
      });
    }

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (enviando) return;
      if (erro) erro.style.display = 'none';
      if (!f.checkValidity()) { f.reportValidity(); return; }

      if (!SERVICO) {
        falhou({
          ok: false,
          causa: 'Envio bloqueado: assets/tq-lead.js nao tem servico configurado. Preencha WEB3FORMS_KEY ou FORMSUBMIT_ALVO.'
        });
        return;
      }

      enviando = true;
      if (botao) { botao.disabled = true; botao.setAttribute('aria-busy', 'true'); botao.textContent = 'Enviando...'; }

      // Campos do formulario: nome, empresa, email, telefone, projeto,
      // investimento, prazo, os seis utm_/gclid e landing_page.
      var dados = new FormData(f);
      var assunto = 'Nova avaliacao de projeto - ' + location.pathname;
      // Identificador deste envio: vai no e-mail e e o transaction_id da
      // conversao, para cruzar lead recebido com conversao no Google Ads.
      var idEnvio = novoIdEnvio();
      dados.append('id_envio', idEnvio);

      if (SERVICO === 'web3forms') {
        dados.append('access_key', WEB3FORMS_KEY);
        dados.append('subject', assunto);
        dados.append('from_name', 'Site Taquionica');
      } else {
        dados.append('_subject', assunto);
        dados.append('_template', 'table');
        dados.append('_captcha', 'false');
        dados.append('_honey', '');       // honeypot do FormSubmit
        dados.delete('botcheck');         // honeypot do Web3Forms, inutil aqui
      }

      // Copia legivel do corpo, so para o diagnostico no console.
      var enviado = {};
      dados.forEach(function (v, k) { enviado[k] = typeof v === 'string' ? v : '(arquivo)'; });

      var corta = null;
      var controle = null;
      if (typeof AbortController !== 'undefined') {
        controle = new AbortController();
        corta = setTimeout(function () { controle.abort(); }, TIMEOUT_MS);
      }

      var opcoes = { method: 'POST', headers: { Accept: 'application/json' }, body: dados };
      if (controle) opcoes.signal = controle.signal;

      var status, statusText;

      fetch(ENDPOINT, opcoes)
        .then(function (r) {
          status = r.status;
          statusText = r.statusText;
          return r.text().then(function (texto) {
            try { return JSON.parse(texto); } catch (e) { return texto || null; }
          });
        })
        .then(function (resposta) {
          if (corta) clearTimeout(corta);

          // Redireciona SOMENTE com sucesso confirmado no corpo da resposta.
          // HTTP 200 sozinho nao basta: os dois servicos devolvem 200 com
          // success:"false" quando a configuracao esta pendente.
          if (status >= 400 || !deuCerto(resposta)) {
            falhou({
              ok: false,
              url: ENDPOINT,
              status: status,
              statusText: statusText,
              enviado: enviado,
              resposta: resposta,
              causa: explica(status, resposta)
            });
            return;
          }

          diagnostico({
            ok: true, url: ENDPOINT, status: status, statusText: statusText,
            enviado: enviado, resposta: resposta
          });
          enviadoId = idEnvio;
          marcaEnvioConfirmado(idEnvio);
          registraConversaoESegue(idEnvio, DESTINO_SUCESSO);
        })
        .catch(function (err) {
          if (corta) clearTimeout(corta);
          var abortou = err && err.name === 'AbortError';
          falhou({
            ok: false,
            url: ENDPOINT,
            status: status,
            statusText: statusText,
            enviado: enviado,
            causa: abortou
              ? 'A requisicao passou de ' + (TIMEOUT_MS / 1000) + 's e foi cancelada.'
              : 'A requisicao nao chegou a receber resposta (rede, CORS ou bloqueio do navegador).',
            erro: err
          });
        });
    });
  });
})();
