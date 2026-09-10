# -*- coding: utf-8 -*-
"""Gera as landing pages novas da Taquionica e instala o formulario em todas.

Duas coisas acontecem aqui:

1. Cinco paginas novas sao criadas, cada uma escrita para um grupo de anuncios
   especifico da campanha. Elas reaproveitam o <head>, o cabecalho e o rodape
   da pagina de firmware, entao herdam o mesmo CSS compilado, o mesmo pixel de
   conversao e o mesmo menu, sem depender de build do site.

2. A secao #contato de TODAS as landing pages e substituida por uma versao com
   formulario. Ate agora a unica saida das paginas era um botao de WhatsApp e um
   link mandando o visitante de volta para a home preencher o formulario la.
   Cada passo desses perde gente. O formulario na propria pagina e a mudanca de
   maior impacto em volume de lead do pacote inteiro.

O evento de conversao ja existe no <head> herdado: ele escuta 'submit' na fase
de captura, entao o formulario dispara conversao sozinho, sem codigo extra.
"""
import io, os, re, sys

from paginas_novas import novas

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOADOR = os.path.join(BASE, "desenvolvimento-firmware", "index.html")
SITE = "https://taquionica.com.br"
FONE = "5516993668447"

IMG = {
    "auto1": "/__l5e/assets-v1/eddf785f-6add-4f6f-bb6b-2653af18c093/auto-1.jpeg",
    "auto2": "/__l5e/assets-v1/66984431-7158-4178-81ca-ee4e28e9ed2b/auto-2.jpeg",
    "auto3": "/__l5e/assets-v1/25fa41df-3964-4795-a4fc-36711aa7c78f/auto-3.jpeg",
    "auto4": "/__l5e/assets-v1/96b32edb-4cf0-4a5d-90ec-341f16233d59/auto-4.jpeg",
    "auto5": "/__l5e/assets-v1/d309f2f5-e962-4314-bce6-c628c17223ac/auto-5.jpeg",
    "agro1": "/__l5e/assets-v1/e4198e94-ffe2-440d-996f-faa1dc4041b2/agro-1.jpg",
    "agro2": "/__l5e/assets-v1/329cf150-add6-4625-9322-e473abf10a0d/agro-2.jpg",
    "agro3": "/__l5e/assets-v1/f182d53f-2b42-4a07-944b-137ac707392e/agro-3.jpg",
    "app1": "/__l5e/assets-v1/d9749857-122a-4b78-bd84-9c888177f375/app-monitoramento.jpeg",
    "app2": "/__l5e/assets-v1/7c7d1759-e3c0-47e2-befd-51b74c56fab1/app-monitoramento-2.jpeg",
    "dash": "/assets/tela-dashboard-DrC0Ej63.png",
}

# ---------------------------------------------------------------- icones lucide
P = {
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"></path><path d="M12 9v4"></path><path d="M12 17h.01"></path>',
    "clock": '<circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path>',
    "radio": '<path d="M16.247 7.761a6 6 0 0 1 0 8.478"></path><path d="M19.075 4.933a10 10 0 0 1 0 14.134"></path><path d="M4.925 19.067a10 10 0 0 1 0-14.134"></path><path d="M7.753 16.239a6 6 0 0 1 0-8.478"></path><circle cx="12" cy="12" r="2"></circle>',
    "board": '<rect width="18" height="18" x="3" y="3" rx="2"></rect><path d="M11 9h4a2 2 0 0 0 2-2V3"></path><circle cx="9" cy="9" r="2"></circle><path d="M7 21v-4a2 2 0 0 1 2-2h4"></path><circle cx="15" cy="15" r="2"></circle>',
    "cpu": '<path d="M12 20v2"></path><path d="M12 2v2"></path><path d="M17 20v2"></path><path d="M17 2v2"></path><path d="M2 12h2"></path><path d="M2 17h2"></path><path d="M2 7h2"></path><path d="M20 12h2"></path><path d="M20 17h2"></path><path d="M20 7h2"></path><path d="M7 20v2"></path><path d="M7 2v2"></path><rect x="4" y="4" width="16" height="16" rx="2"></rect><rect x="8" y="8" width="8" height="8" rx="1"></rect>',
    "check": '<path d="M20 6 9 17l-5-5"></path>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path><path d="m9 12 2 2 4-4"></path>',
    "gauge": '<path d="m12 14 4-4"></path><path d="M3.34 19a10 10 0 1 1 17.32 0"></path>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"></path>',
    "chart": '<path d="M3 3v16a2 2 0 0 0 2 2h16"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path>',
    "phone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"></rect><path d="M12 18h.01"></path>',
    "layers": '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"></path><path d="m6.08 10.37-3.5 1.59a1 1 0 0 0 0 1.83l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9a1 1 0 0 0 0-1.83l-3.5-1.6"></path><path d="m6.08 15.37-3.5 1.59a1 1 0 0 0 0 1.83l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9a1 1 0 0 0 0-1.83l-3.5-1.6"></path>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"></path><path d="M17 18h1"></path><path d="M12 18h1"></path><path d="M7 18h1"></path>',
    "search": '<circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path><path d="M14 2v4a2 2 0 0 0 2 2h4"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path>',
    "plug": '<path d="M12 22v-5"></path><path d="M9 8V2"></path><path d="M15 8V2"></path><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"></path>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><path d="M16 3.128a4 4 0 0 1 0 7.744"></path><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><circle cx="9" cy="7" r="4"></circle>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path><path d="M21 3v5h-5"></path><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path><path d="M3 21v-5h5"></path>',
}

# Prints de aplicativo sao verticais (720x1568). Numa coluna de 576px eles
# passam de 1200px de altura, o que estica o hero inteiro e deixa o texto da
# esquerda boiando num vazio enorme. Estas entram com largura de celular.
RETRATO = {IMG["app1"], IMG["app2"]}

SVG = ('<svg xmlns"http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
       'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
       'stroke-linejoin="round" class="lucide %s" aria-hidden="true">%s</svg>')

SVG_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false" '
          'class="mr-2 h-5 w-5"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099'
          '-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255'
          '-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133'
          '.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669'
          '-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074'
          '-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 '
          '3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758'
          '-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 '
          '7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 '
          '9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a'
          '9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 '
          '11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 '
          '24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a'
          '11.821 11.821 0 0 0-3.48-8.413Z"></path></svg>')

CTA_HERO = ('class="inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium '
            'cursor-pointer transition-colors focus-visible:outline-none focus-visible:ring-1 '
            'focus-visible:ring-ring shadow h-12 rounded-md px-8 text-base bg-black text-white '
            'hover:bg-white focus-visible:bg-white active:bg-white shadow-glow border '
            'border-white/20 [&:hover_*]:!text-black [&:focus-visible_*]:!text-black '
            '[&:active_*]:!text-black lp-cta-wrap"')

CTA_FIM = ('class="inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium '
           'cursor-pointer transition-colors focus-visible:outline-none focus-visible:ring-1 '
           'focus-visible:ring-ring text-white shadow-glow bg-[image:var(--gradient-accent)] '
           'hover:brightness-110 border border-white/10 h-12 rounded-md px-8 text-base '
           'lp-cta-wrap"')

CHIP = ('<span class="inline-flex items-center gap-2 rounded-full bg-[oklch(0.66_0.19_250)]/10 '
        'px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[oklch(0.5_0.17_255)]">%s</span>')


def wa(texto):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (FONE, quote(texto, safe=""))


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------- CSS proprio
# O CSS do site e compilado por Tailwind, entao so contem as classes que ja
# existiam no build. Escrever o formulario com utilitarios novos correria o risco
# de cair numa classe que nao foi gerada e nao existe no arquivo. Por isso o
# formulario tem CSS proprio, escrito a mao, usando as mesmas variaveis de cor do
# tema. Assim ele funciona independente do que o Tailwind compilou.
CSS_EXTRA = """
.tq-cta-grid{display:grid;gap:2.5rem;align-items:start}
@media (min-width:1024px){.tq-cta-grid{grid-template-columns:1fr 1fr;gap:3.5rem}}
.tq-cta-list{margin-top:1.75rem;display:grid;gap:.75rem}
.tq-hero-retrato{max-width:330px}
.tq-hero-retrato img{max-height:560px;width:auto;margin-inline:auto;display:block}
@media (max-width:1023px){.tq-hero-retrato{max-width:270px}.tq-hero-retrato img{max-height:440px}}
.tq-hero-retrato .mt-4{flex-direction:column;align-items:center;gap:.15rem;text-align:center}
.tq-cta-list li{display:flex;align-items:flex-start;gap:.65rem;font-size:.9rem;line-height:1.6;color:#ffffffb3}
.tq-cta-list svg{height:1.15rem;width:1.15rem;flex-shrink:0;margin-top:.15rem;color:oklch(0.82 0.13 220)}
.tq-form{background:#fff;border-radius:var(--radius-xl);padding:1.5rem;box-shadow:0 24px 60px #0006;color:var(--foreground);text-align:left}
@media (min-width:640px){.tq-form{padding:2rem}}
.tq-form h3{font-size:1.15rem;font-weight:700;line-height:1.3}
.tq-form .tq-sub{margin-top:.4rem;font-size:.85rem;line-height:1.55;color:var(--muted-foreground)}
.tq-grid{margin-top:1.25rem;display:grid;gap:.9rem}
@media (min-width:640px){.tq-grid{grid-template-columns:1fr 1fr}.tq-full{grid-column:1 / -1}}
.tq-field label{display:block;font-size:.8rem;font-weight:600;margin-bottom:.35rem}
.tq-field input,.tq-field select,.tq-field textarea{width:100%;box-sizing:border-box;font:inherit;font-size:.9rem;color:var(--foreground);background:#fff;border:1px solid var(--color-border);border-radius:var(--radius);padding:.6rem .75rem;transition:border-color .15s,box-shadow .15s}
.tq-field textarea{min-height:5.5rem;resize:vertical}
.tq-field input:focus,.tq-field select:focus,.tq-field textarea:focus{outline:none;border-color:oklch(0.66 0.19 250);box-shadow:0 0 0 3px oklch(0.66 0.19 250 / .18)}
.tq-send{margin-top:1.25rem;width:100%;display:inline-flex;align-items:center;justify-content:center;gap:.5rem;border:none;cursor:pointer;font:inherit;font-weight:600;font-size:.95rem;color:#fff;background:var(--gradient-accent);border-radius:var(--radius);padding:.85rem 1rem;transition:filter .15s}
.tq-send:hover{filter:brightness(1.1)}
.tq-ok a{color:inherit;font-weight:700;text-decoration:underline}
.tq-note{margin-top:.8rem;font-size:.72rem;line-height:1.5;color:var(--muted-foreground)}
.tq-ok{margin-top:1rem;display:none;border-radius:var(--radius);background:oklch(0.66 0.19 250 / .1);color:oklch(0.42 0.15 255);padding:.8rem .9rem;font-size:.85rem;line-height:1.5}
.tq-steps{display:grid;gap:1rem}
@media (min-width:768px){.tq-steps{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1024px){.tq-steps{grid-template-columns:repeat(4,1fr)}}
.tq-step{background:var(--color-card);border:1px solid var(--color-border);border-radius:var(--radius-xl);padding:1.35rem}
.tq-step .n{font-size:.72rem;font-weight:700;letter-spacing:.08em;color:oklch(0.5 0.17 255)}
.tq-step h3{margin-top:.5rem;font-size:1rem;font-weight:650}
.tq-step p{margin-top:.5rem;font-size:.85rem;line-height:1.6;color:var(--muted-foreground)}
.tq-prova{display:grid;gap:1rem}
@media (min-width:768px){.tq-prova{grid-template-columns:repeat(3,1fr)}}
.tq-prova div{background:var(--color-card);border:1px solid var(--color-border);border-radius:var(--radius-xl);padding:1.35rem}
.tq-prova strong{display:block;font-size:1.6rem;font-weight:800;letter-spacing:-.02em}
.tq-prova span{display:block;margin-top:.35rem;font-size:.85rem;line-height:1.55;color:var(--muted-foreground)}
"""

# --------------------------------------------------------------- JS do formulario
JS_FORM = """
(function(){
  var f = document.getElementById('tq-form');
  if (!f) return;
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) {
      var el = f.querySelector('[name="' + n + '"]');
      return el && el.value ? el.value.trim() : '';
    };
    var linhas = [
      'Ol\\u00e1! Vim da p\\u00e1gina ' + (f.getAttribute('data-pagina') || '') +
        ' do site da Taquionica.',
      '',
      'Nome: ' + v('nome'),
      'Empresa: ' + v('empresa'),
      'Telefone: ' + v('telefone')
    ];
    if (v('email')) linhas.push('E-mail: ' + v('email'));
    if (v('porte')) linhas.push('Porte da empresa: ' + v('porte'));
    if (v('projeto')) { linhas.push(''); linhas.push('O que preciso: ' + v('projeto')); }
    var url = 'https://wa.me/FONE?text=' + encodeURIComponent(linhas.join('\\n'));
    var ok = f.querySelector('.tq-ok');
    if (ok) {
      var link = ok.querySelector('a');
      if (link) link.href = url;
      ok.style.display = 'block';
    }
    // window.open com 'noopener' devolve null no Chrome mesmo quando abre a aba.
    // Usar esse retorno como teste de sucesso fazia o fallback disparar sempre, e
    // a propria aba do visitante ia embora para o WhatsApp: ele perdia a pagina e
    // nunca via a confirmacao. Um link temporario abre a aba nova sem esse efeito,
    // e se o navegador bloquear, a confirmacao ja traz o link para clicar.
    var a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });
})();
""".replace("FONE", FONE)


# ----------------------------------------------------------------------- blocos
def hero(chip, h1_pre, h1_forte, h1_pos, sub, cta_txt, cta_wa, img, img_alt,
         img_cap, img_tag):
    h1 = esc(h1_pre) + '<span class="text-gradient">' + esc(h1_forte) + '</span>' + esc(h1_pos)
    return (
        '<section id="topo" class="relative overflow-hidden gradient-hero text-white pt-24 pb-20 '
        'md:pt-28 md:pb-28"><div class="container-x relative grid gap-12 lg:grid-cols-2 '
        'lg:items-center"><div class="min-w-0"><span class="inline-flex items-center gap-2 '
        'rounded-full border border-white/15 bg-white/5 px-3 py-1 text-xs font-medium '
        'text-white/80 backdrop-blur">' + SVG % ('lucide-circuit-board h-3.5 w-3.5 '
        'text-[oklch(0.82_0.13_220)]', P["board"]) + esc(chip) + '</span>'
        '<h1 class="mt-5 text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl '
        'leading-[1.05] break-words">' + h1 + '</h1>'
        '<p class="mt-6 text-lg text-white/70 max-w-xl leading-relaxed">' + esc(sub) + '</p>'
        '<div class="mt-8 flex flex-wrap gap-3"><a href="' + wa(cta_wa) + '" target="_blank" '
        'rel="noopener noreferrer" ' + CTA_HERO + '>' + SVG_WA + esc(cta_txt) + '</a>'
        '<a href="#contato" class="inline-flex items-center justify-center gap-2 '
        'whitespace-nowrap font-medium cursor-pointer transition-colors border shadow-sm h-12 '
        'rounded-md px-8 text-base border-white/30 bg-white/5 text-white hover:bg-white/10 '
        'lp-cta-wrap">Enviar detalhes do projeto</a></div></div>'
        '<div class="relative"><div class="relative mx-auto w-full max-w-xl' +
        (' tq-hero-retrato' if img in RETRATO else '') + '">'
        '<div class="absolute inset-0 -z-10 rounded-3xl bg-gradient-to-br from-white/5 to-white/0 '
        'blur-2xl"></div><div class="relative rounded-3xl border border-white/10 '
        'bg-white/[0.03] p-6 backdrop-blur-sm shadow-elegant"><img src="' + img + '" alt="' +
        esc(img_alt) + '" loading="eager" decoding="async" class="w-full h-auto rounded-2xl '
        'border border-white/10"/><div class="mt-4 flex items-center justify-between text-xs '
        'text-white/60"><span>' + esc(img_cap) + '</span><span>' + esc(img_tag) + '</span>'
        '</div></div></div></div></div></section>')


def problema(titulo, intro, itens):
    lis = ""
    for icone, texto in itens:
        lis += ('<li class="flex items-start gap-3">' +
                SVG % ('lucide-' + icone + ' h-5 w-5 shrink-0 text-[oklch(0.5_0.17_255)]', P[icone]) +
                '<span class="text-sm leading-relaxed text-foreground">' + esc(texto) +
                '</span></li>')
    return (
        '<section id="problema" class="py-20 md:py-28 bg-secondary/40"><div class="container-x">'
        '<div class="card-surface p-6 sm:p-10 grid gap-8 lg:grid-cols-2 lg:items-center"><div>' +
        CHIP % "O problema" +
        '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight '
        'leading-[1.1]">' + esc(titulo) + '</h2>'
        '<p class="mt-4 text-muted-foreground leading-relaxed">' + esc(intro) + '</p></div>'
        '<ul class="space-y-3">' + lis + '</ul></div></div></section>')


def oferta(titulo, texto):
    return (
        '<section id="oferta" class="py-14 md:py-20 bg-background"><div class="container-x">'
        '<div class="mx-auto max-w-3xl text-center"><span class="text-xs font-semibold uppercase '
        'tracking-wider text-[oklch(0.5_0.17_255)]">O que fazemos</span>'
        '<h2 class="mt-3 text-2xl font-bold leading-tight sm:text-3xl">' + esc(titulo) + '</h2>'
        '<p class="mt-4 text-muted-foreground leading-relaxed">' + esc(texto) +
        '</p></div></div></section>')


def entregas(titulo, intro, passos):
    cards = ""
    for i, (t, d) in enumerate(passos, 1):
        cards += ('<div class="tq-step"><div class="n">%02d</div><h3>%s</h3><p>%s</p></div>'
                  % (i, esc(t), esc(d)))
    return (
        '<section id="entregas" class="py-20 md:py-28 bg-background"><div class="container-x">'
        '<div class="text-center mx-auto max-w-3xl">' + CHIP % "O que entra no projeto" +
        '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight '
        'leading-[1.1]">' + esc(titulo) + '</h2>'
        '<p class="mt-4 text-muted-foreground leading-relaxed">' + esc(intro) + '</p></div>'
        '<div class="tq-steps mt-12">' + cards + '</div></div></section>')


def prova(titulo, intro, numeros):
    cards = ""
    for n, d in numeros:
        cards += '<div><strong>%s</strong><span>%s</span></div>' % (esc(n), esc(d))
    return (
        '<section id="prova" class="py-14 md:py-20 bg-secondary/40"><div class="container-x">'
        '<div class="text-center mx-auto max-w-2xl"><span class="text-xs font-semibold uppercase '
        'tracking-wider text-[oklch(0.5_0.17_255)]">Quem está do outro lado</span>'
        '<h2 class="mt-3 text-2xl font-bold leading-tight sm:text-3xl">' + esc(titulo) + '</h2>'
        '<p class="mt-3 text-muted-foreground leading-relaxed">' + esc(intro) + '</p></div>'
        '<div class="tq-prova mt-8">' + cards + '</div></div></section>')


def tecnologias(titulo, texto, chips):
    tags = "".join('<span class="rounded-full bg-secondary px-3 py-1.5 text-sm">%s</span>' % esc(c)
                   for c in chips)
    return (
        '<section id="tecnologias" class="py-14 md:py-20 bg-background"><div class="container-x">'
        '<div class="text-center mx-auto max-w-2xl"><span class="text-xs font-semibold uppercase '
        'tracking-wider text-[oklch(0.5_0.17_255)]">Tecnologias</span>'
        '<h2 class="mt-3 text-2xl font-bold leading-tight sm:text-3xl">' + esc(titulo) + '</h2>'
        '<p class="mt-3 text-muted-foreground">' + esc(texto) + '</p></div>'
        '<div class="mt-8 flex flex-wrap items-center justify-center gap-2">' + tags +
        '</div></div></section>')


def projetos(titulo, cards):
    arts = ""
    for img, cat, nome, desc, tags in cards:
        chips = "".join('<span class="rounded-full bg-secondary px-2 py-0.5 text-xs">%s</span>'
                        % esc(t) for t in tags)
        arts += ('<article class="card-surface overflow-hidden"><div class="relative w-full '
                 'overflow-hidden bg-secondary aspect-[4/3]"><img src="' + img + '" alt="' +
                 esc(nome) + '" loading="lazy" decoding="async" class="absolute inset-0 h-full '
                 'w-full object-cover object-center"/></div><div class="p-6">'
                 '<div class="text-xs font-medium text-muted-foreground">' + esc(cat) + '</div>'
                 '<h3 class="mt-2 text-base font-semibold">' + esc(nome) + '</h3>'
                 '<p class="mt-2 text-sm text-muted-foreground leading-relaxed">' + esc(desc) +
                 '</p><div class="mt-4 flex flex-wrap gap-1.5">' + chips +
                 '</div></div></article>')
    return (
        '<section id="projetos" class="py-20 md:py-28 bg-secondary/40"><div class="container-x">'
        '<div class="text-center mx-auto max-w-3xl">' + CHIP % "Projetos reais" +
        '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight '
        'leading-[1.1]">' + esc(titulo) + '</h2></div>'
        '<div class="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">' + arts +
        '</div></div></section>')


def faq(titulo, itens):
    chev = SVG % ('lp-faq-chevron lucide-chevron-down h-4 w-4 shrink-0 text-muted-foreground',
                  '<path d="m6 9 6 6 6-6"></path>')
    blocos = ""
    for p, r in itens:
        blocos += ('<details class="lp-faq-item card-surface px-5"><summary class="flex flex-1 '
                   'items-center justify-between py-4 cursor-pointer text-left text-base '
                   'font-semibold"><span>' + esc(p) + '</span>' + chev + '</summary>'
                   '<div class="pb-4 text-sm text-muted-foreground leading-relaxed">' + esc(r) +
                   '</div></details>')
    return (
        '<section id="faq" class="py-20 md:py-28 bg-background"><div class="container-x">'
        '<div class="text-center mx-auto max-w-3xl">' + CHIP % "Perguntas frequentes" +
        '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight '
        'leading-[1.1]">' + esc(titulo) + '</h2></div>'
        '<div class="mt-12 mx-auto max-w-3xl space-y-3">' + blocos + '</div></div></section>')


GARANTIAS = [
    ("check", "Primeira conversa sem custo e sem compromisso."),
    ("shield", "Informações do projeto tratadas com confidencialidade."),
    ("clock", "Retorno em até um dia útil, pelo canal que você preferir."),
    ("factory", "Projetos empresariais e industriais em todo o Brasil."),
]


def contato(titulo, texto, cta_txt, cta_wa, pagina):
    itens = "".join('<li>%s<span>%s</span></li>'
                    % (SVG % ('lucide-' + i, P[i]), esc(t)) for i, t in GARANTIAS)
    return (
        '<section id="contato" class="relative overflow-hidden bg-[oklch(0.14_0.03_258)] '
        'text-white py-20 md:py-24"><div class="container-x"><div class="tq-cta-grid">'
        '<div><h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold leading-tight">' +
        esc(titulo) + '</h2>'
        '<p class="mt-5 max-w-xl text-white/70 leading-relaxed">' + esc(texto) + '</p>'
        '<ul class="tq-cta-list">' + itens + '</ul>'
        '<div class="mt-8"><a href="' + wa(cta_wa) + '" target="_blank" rel="noopener noreferrer" '
        + CTA_FIM + '>' + SVG_WA + esc(cta_txt) + '</a></div></div>'
        '<form class="tq-form" id="tq-form" data-pagina="' + esc(pagina) + '">'
        '<h3>Envie os detalhes do seu projeto</h3>'
        '<p class="tq-sub">Preencha os campos abaixo. Ao enviar, a conversa segue no WhatsApp já '
        'com o seu cenário escrito, então você não precisa repetir nada.</p>'
        '<div class="tq-grid">'
        '<div class="tq-field"><label for="tq-nome">Nome</label>'
        '<input id="tq-nome" name="nome" type="text" autocomplete="name" required/></div>'
        '<div class="tq-field"><label for="tq-empresa">Empresa</label>'
        '<input id="tq-empresa" name="empresa" type="text" autocomplete="organization" required/>'
        '</div>'
        '<div class="tq-field"><label for="tq-telefone">Telefone ou WhatsApp</label>'
        '<input id="tq-telefone" name="telefone" type="tel" inputmode="tel" autocomplete="tel" '
        'required/></div>'
        '<div class="tq-field"><label for="tq-email">E-mail</label>'
        '<input id="tq-email" name="email" type="email" autocomplete="email"/></div>'
        '<div class="tq-field tq-full"><label for="tq-porte">Porte da operação</label>'
        '<select id="tq-porte" name="porte"><option value="">Selecione</option>'
        '<option>Indústria de grande porte</option><option>Indústria de médio porte</option>'
        '<option>Fabricante de equipamentos</option><option>Empresa de serviços</option>'
        '<option>Startup ou novo produto</option><option>Outro</option></select></div>'
        '<div class="tq-field tq-full"><label for="tq-projeto">O que sua empresa precisa</label>'
        '<textarea id="tq-projeto" name="projeto" placeholder="Descreva o equipamento, o processo '
        'ou o problema técnico em poucas linhas."></textarea></div></div>'
        '<button class="tq-send" type="submit">' + SVG_WA + 'Enviar e continuar no WhatsApp'
        '</button>'
        '<div class="tq-ok">Pronto, a sua mensagem está montada e o WhatsApp foi aberto numa '
        'aba nova. Se a aba não abrir, <a href="' + wa("Olá! Vim do site da Taquionica.") +
        '" target="_blank" rel="noopener noreferrer">clique aqui</a> ou chame no '
        '(16) 99366-8447.</div>'
        '<p class="tq-note">Ao enviar, você concorda que a Taquionica use estes dados apenas para '
        'responder ao seu contato.</p>'
        '</form></div></div></section>')


# --------------------------------------------------------------------- montagem
def le_doador():
    h = io.open(DOADOR, encoding="utf-8").read()
    i = h.index("<main>")
    j = h.index("<footer")
    return h[:i], h[j:]


def cabeca(prefixo, slug, titulo, descricao, img_hero):
    """Ajusta o <head> herdado para a pagina nova."""
    h = prefixo
    h = h.replace("https://taquionica.com.br/desenvolvimento-firmware", SITE + "/" + slug)
    h = re.sub(r"<title>.*?</title>", "<title>" + esc(titulo) + "</title>", h, flags=re.S)
    h = h.replace(
        'content="A Taquionica desenvolve, corrige e evolui firmware para microcontroladores e '
        'sistemas embarcados, incluindo ESP32 e protocolos industriais."',
        'content="' + esc(descricao) + '"')
    h = re.sub(r"<title>[^<]*</title>", "<title>" + esc(titulo) + "</title>", h)
    h = h.replace('property="og:title" content="Desenvolvimento de Firmware para Sistemas '
                  'Embarcados | Taquionica"',
                  'property="og:title" content="' + esc(titulo) + '"')
    h = h.replace('name="twitter:title" content="Desenvolvimento de Firmware para Sistemas '
                  'Embarcados | Taquionica"',
                  'name="twitter:title" content="' + esc(titulo) + '"')
    h = h.replace('<link rel="preload" as="image" href="' + IMG["agro2"] + '"/>',
                  '<link rel="preload" as="image" href="' + img_hero + '"/>')
    h = h.replace("</style></head>", CSS_EXTRA + "</style></head>")
    return h


def monta(pag, prefixo, sufixo):
    corpo = "".join([
        hero(*pag["hero"]),
        problema(*pag["problema"]),
        oferta(*pag["oferta"]),
        entregas(*pag["entregas"]),
        prova(*pag["prova"]),
        tecnologias(*pag["tecnologias"]),
        projetos(*pag["projetos"]),
        faq(*pag["faq"]),
        contato(*pag["contato"]),
    ])
    h = cabeca(prefixo, pag["slug"], pag["titulo"], pag["descricao"], pag["hero"][7])
    return h + "<main>" + corpo + "</main>" + sufixo.replace(
        "</body></html>", "<script>" + JS_FORM + "</script></body></html>")


# ------------------------------------------------------------- conteudo das LPs
PAGINAS = [
    # ------------------------------------------------------ 1. retrofit de maquinas
    {
        "slug": "retrofit-de-maquinas",
        "titulo": "Retrofit e Modernização de Máquinas Industriais | Taquionica",
        "descricao": ("A Taquionica moderniza a eletrônica, o comando e a comunicação de máquinas "
                      "industriais que ainda produzem bem, mas dependem de peça que saiu de linha."),
        "hero": (
            "Retrofit e modernização",
            "A máquina ainda produz. O ",
            "comando dela",
            " é que virou risco",
            "Quando o painel depende de uma peça que saiu de linha, a máquina inteira fica refém "
            "de um componente. A Taquionica projeta a eletrônica nova, escreve o firmware de "
            "controle e conecta o equipamento à rede da fábrica, mantendo a mecânica que já "
            "funciona.",
            "Falar sobre o retrofit",
            "Olá! Vim da página de Retrofit de Máquinas da Taquionica e gostaria de falar sobre a "
            "modernização de um equipamento.",
            IMG["auto1"],
            "Placa de controle para acionamento de motores, com estágio de potência e proteções",
            "Placa de controle para acionamento de motores",
            "Automação industrial",
        ),
        "problema": (
            "Sinais de que a máquina precisa de retrofit, não de conserto",
            "Consertar recoloca a máquina em operação até a próxima falha. O retrofit tira a "
            "operação da dependência que causou a falha.",
            [
                ("alert", "A peça de reposição do comando saiu de linha e só existe em usado"),
                ("clock", "Cada parada espera dias por um componente que ninguém mais fabrica"),
                ("radio", "A máquina não conversa com nenhum sistema da fábrica"),
                ("cpu", "O painel foi remendado tantas vezes que ninguém sabe mais o esquema"),
                ("factory", "Um único técnico entende a máquina, e a operação depende dele"),
            ],
        ),
        "oferta": (
            "Mecânica preservada, eletrônica e controle refeitos",
            "A Taquionica avalia a máquina em operação, define o que vale manter e o que precisa "
            "ser refeito, e desenvolve a eletrônica de comando, o firmware de controle e a "
            "comunicação. O investimento fica em cima do que muda, não da máquina inteira.",
        ),
        "entregas": (
            "O retrofit acontece em quatro etapas, com escopo fechado antes de começar",
            "Você aprova cada etapa sabendo o que entra nela. Nenhuma linha de código começa antes "
            "de escopo, prazo e valor estarem definidos.",
            [
                ("Levantamento na máquina",
                 "Mapeamos entradas, saídas, sensores, atuadores e a sequência de operação real, "
                 "que quase sempre é diferente do manual."),
                ("Projeto da eletrônica",
                 "Placa de comando dedicada, estágio de potência dimensionado para os motores e "
                 "atuadores existentes, proteções e interface de operação."),
                ("Firmware de controle",
                 "A lógica da máquina escrita do zero, com intertravamentos, tratamento de falha "
                 "e o comportamento definido para quando algo sai do previsto."),
                ("Conexão com a fábrica",
                 "Modbus, Wi-Fi ou Ethernet para a máquina reportar produção, parada e alarme "
                 "para o painel ou o sistema que a sua equipe já usa."),
            ],
        ),
        "prova": (
            "Retrofit em máquina que não pode errar",
            "A Taquionica desenvolve automação embarcada para equipamentos que operam sobre "
            "ativos de alto valor, onde uma falha de controle não é defeito de máquina, é "
            "prejuízo no mesmo dia.",
            [
                ("Desde 2001", "O responsável técnico desenvolve eletrônica de controle e "
                               "potência para equipamento industrial."),
                ("45+", "Equipamentos em operação contínua há mais de seis anos, com atualização "
                        "remota de frota."),
                ("Todo o Brasil", "Projetos atendidos de Ribeirão Preto, com reuniões remotas e "
                                  "visita técnica quando o escopo exige."),
            ],
        ),
        "tecnologias": (
            "A tecnologia é escolhida pela máquina, não pelo catálogo",
            "O comando novo usa o protocolo que a sua fábrica já fala, para o retrofit não criar "
            "mais uma ilha isolada dentro da operação.",
            ["Modbus", "CAN", "Ethernet", "Wi-Fi", "MQTT", "ESP32", "Relés de potência",
             "Sensores de posição"],
        ),
        "projetos": (
            "Eletrônica de comando desenvolvida para máquina em operação",
            [
                (IMG["auto1"], "Automação industrial", "Placa de controle para acionamento de motores",
                 "Projeto completo de hardware dedicado, com estágio de potência para dois "
                 "motores, proteções e firmware de controle.",
                 ["Eletrônica", "Placa dedicada (PCB)", "Microcontrolador", "Firmware"]),
                (IMG["auto3"], "Automação", "Central de automação para equipamento comercial",
                 "Central com entradas sensoriais, relés de potência, interface de configuração e "
                 "conectividade para telemetria.",
                 ["Eletrônica", "Relés 127V a 220V", "IoT", "Firmware"]),
                (IMG["agro2"], "Energia solar / Usinas fotovoltaicas",
                 "Implemento automatizado de escovas rotativas",
                 "Controle eletrônico do braço e das escovas, com ajuste de velocidade e proteção "
                 "contra sobrecarga.",
                 ["Eletrônica", "Controle hidráulico", "Sensores de posição", "Firmware"]),
            ],
        ),
        "faq": (
            "Dúvidas sobre retrofit de máquinas industriais",
            [
                ("Vocês fazem retrofit de máquina de qualquer fabricante?",
                 "Sim. O retrofit trabalha sobre a máquina que está na sua fábrica, "
                 "independentemente do fabricante. Quando não existe documentação, o levantamento "
                 "é feito na própria máquina, mapeando entradas, saídas e a sequência real de "
                 "operação."),
                ("A máquina precisa ficar parada durante o projeto?",
                 "Não durante todo o projeto. O levantamento e boa parte do desenvolvimento "
                 "acontecem com a máquina produzindo. A parada fica concentrada na instalação e "
                 "nos testes, e o período é combinado com a sua produção antes de começar."),
                ("Vale mais a pena o retrofit ou comprar uma máquina nova?",
                 "Depende do estado da mecânica. Quando a estrutura, os motores e a parte "
                 "hidráulica ainda estão bons e o problema é o comando, o retrofit custa uma "
                 "fração da máquina nova. O levantamento inicial serve exatamente para responder "
                 "isso com números, antes de qualquer compromisso."),
                ("O retrofit inclui a integração com o nosso sistema?",
                 "Sim, quando esse é o escopo. A máquina pode passar a reportar contagem de peças, "
                 "tempo e motivo de parada e alarmes por Modbus, Ethernet ou MQTT para o painel "
                 "ou o sistema que a sua equipe já utiliza."),
                ("Quem responde pelo projeto do começo ao fim?",
                 "Nell, gerente de projeto e responsável técnico. Você trata com ele do "
                 "levantamento à entrega, e é ele quem coordena os especialistas de eletrônica de "
                 "potência, layout de PCB, firmware e integração conforme a etapa."),
                ("Vocês atendem indústria de grande porte?",
                 "Sim. O time é montado conforme o escopo, então a capacidade acompanha o tamanho "
                 "do projeto sem estrutura ociosa embutida no preço."),
            ],
        ),
        "contato": (
            "Descubra se a sua máquina vale um retrofit",
            "Conte qual é o equipamento e o que está travando. A Taquionica avalia o cenário e "
            "indica se o caminho é modernizar o comando, integrar à rede da fábrica ou corrigir "
            "um ponto específico.",
            "Falar sobre o retrofit",
            "Olá! Vim da página de Retrofit de Máquinas da Taquionica e gostaria de avaliar a "
            "modernização de um equipamento.",
            "Retrofit de Máquinas",
        ),
    },

    # --------------------------------------------- 2. coleta de dados de maquinas
    {
        "slug": "coleta-de-dados-de-maquinas",
        "titulo": "Coleta de Dados de Máquinas e Monitoramento de Produção | Taquionica",
        "descricao": ("A Taquionica instala eletrônica e software para coletar dados de máquinas, "
                      "inclusive as antigas, e transformar produção, parada e OEE em painel."),
        "hero": (
            "Coleta de dados de máquinas",
            "A sua produção gera dado todo dia. ",
            "Ninguém consegue ler",
            "",
            "Contagem de peças no papel, motivo de parada anotado de memória no fim do turno, "
            "planilha fechada no dia seguinte. A Taquionica coloca eletrônica na máquina, "
            "inclusive na que não tem saída de dados, e leva produção, parada e disponibilidade "
            "para um painel em tempo real.",
            "Falar sobre coleta de dados",
            "Olá! Vim da página de Coleta de Dados de Máquinas da Taquionica e gostaria de falar "
            "sobre monitorar a produção da minha fábrica.",
            IMG["dash"],
            "Painel de monitoramento com equipamentos conectados e leituras em tempo real",
            "Painel de acompanhamento de equipamentos",
            "Monitoramento em tempo real",
        ),
        "problema": (
            "O chão de fábrica sabe. O relatório chega tarde",
            "Quando o dado é anotado à mão e consolidado depois, ele serve para explicar o mês "
            "passado. Não serve para agir no turno em que o problema aconteceu.",
            [
                ("clock", "Motivo de parada preenchido de memória, horas depois da parada"),
                ("chart", "Indicador de produção que só fecha no dia seguinte, ou na semana"),
                ("factory", "Máquina antiga sem nenhuma saída de dado para a rede"),
                ("radio", "Equipamentos de fabricantes diferentes que não falam a mesma língua"),
                ("alert", "Ninguém sabe dizer, no momento, qual máquina está parada e por quê"),
            ],
        ),
        "oferta": (
            "Do sensor na máquina ao painel que a diretoria abre",
            "A Taquionica desenvolve a eletrônica que lê a máquina, o firmware que envia o dado, "
            "a comunicação com a nuvem e o painel onde a informação vira decisão. Tudo pela mesma "
            "equipe, então não existe fornecedor culpando o outro quando o dado não chega.",
        ),
        "entregas": (
            "O que a Taquionica entrega em um projeto de coleta de dados",
            "O escopo é dimensionado sobre as suas máquinas, não sobre um pacote fechado. Máquina "
            "nova com CLP e máquina antiga sem saída nenhuma exigem caminhos diferentes.",
            [
                ("Leitura da máquina",
                 "Sensor dedicado, leitura direta do CLP por Modbus ou captação do sinal de "
                 "acionamento, conforme o que a máquina permite."),
                ("Gateway e comunicação",
                 "Eletrônica embarcada com Wi-Fi, Ethernet ou 4G enviando por MQTT, com buffer "
                 "para o dado não se perder quando a rede cai."),
                ("Produção, parada e OEE",
                 "Contagem de peças, tempo de ciclo, tempo e motivo de parada, disponibilidade e "
                 "os indicadores que a sua operação usa para decidir."),
                ("Painel e alerta",
                 "Dashboard em tempo real, histórico por turno e alerta quando a máquina para ou "
                 "sai da faixa esperada, no celular de quem precisa agir."),
            ],
        ),
        "prova": (
            "Infraestrutura que já roda em campo, não protótipo de apresentação",
            "A Taquionica mantém um parque instalado enviando dado continuamente há anos, com "
            "atualização de firmware à distância, sem deslocar técnico até o cliente.",
            [
                ("45+", "Equipamentos em operação contínua há mais de seis anos, enviando "
                        "leituras e recebendo comando."),
                ("6 anos", "Sem interrupção do serviço de monitoramento do parque instalado."),
                ("Desde 2001", "Experiência do responsável técnico em medição, onde erro de "
                               "leitura vira perda de receita no mesmo dia."),
            ],
        ),
        "tecnologias": (
            "Protocolo industrial de verdade, não integração improvisada",
            "A coleta usa o que a máquina já fala. Quando ela não fala nada, a Taquionica "
            "desenvolve a eletrônica que passa a falar.",
            ["Modbus RTU", "Modbus TCP", "MQTT", "Ethernet", "Wi-Fi", "4G", "ESP32",
             "Sensores industriais"],
        ),
        "projetos": (
            "Equipamentos conectados e dados chegando ao painel",
            [
                (IMG["auto3"], "Automação / Indústria",
                 "Controlador conectado para monitoramento remoto",
                 "Placa com módulo Wi-Fi integrado, múltiplas saídas de acionamento e envio de "
                 "dados para dashboard em nuvem.",
                 ["Eletrônica", "IoT", "ESP32", "Wi-Fi / MQTT"]),
                (IMG["dash"], "Monitoramento", "Painel de acompanhamento do parque instalado",
                 "Equipamentos no mapa, estado de conexão e leituras de temperatura, tensão, "
                 "corrente, potência e consumo em tempo real.",
                 ["Dashboard", "MQTT", "Tempo real", "Histórico"]),
                (IMG["agro3"], "Energia solar / Usinas fotovoltaicas",
                 "Operação em larga escala com registro operacional",
                 "Padronização do processo com equipamentos automatizados e registro operacional "
                 "para gestão da manutenção.",
                 ["Eletrônica", "Telemetria", "Gestão operacional"]),
            ],
        ),
        "faq": (
            "Dúvidas sobre coleta de dados de máquinas",
            [
                ("Dá para coletar dado de máquina antiga, sem CLP?",
                 "Dá. É o caso mais comum. Quando a máquina não tem saída de dados, a Taquionica "
                 "desenvolve a eletrônica que capta o sinal disponível, seja o acionamento do "
                 "motor, um sensor de presença na saída de peças ou a corrente consumida, e "
                 "transforma isso em contagem e tempo de parada confiáveis."),
                ("Vocês integram máquinas de fabricantes diferentes?",
                 "Sim. Cada máquina entra pelo caminho que ela permite, e todas passam a reportar "
                 "no mesmo formato para o painel. É justamente esse trabalho de padronização que "
                 "faz o indicador do parque inteiro fechar."),
                ("O dado se perde se a internet cair?",
                 "Não. A eletrônica embarcada guarda as leituras localmente e envia quando a "
                 "conexão volta, então o histórico do turno fica completo mesmo com queda de rede."),
                ("Vocês entregam o painel ou integram com o sistema que já usamos?",
                 "Os dois caminhos são possíveis. A Taquionica entrega o dashboard próprio ou "
                 "envia os dados por MQTT ou API para o ERP, o MES ou o painel que a sua equipe "
                 "já mantém."),
                ("Quanto tempo até o primeiro indicador aparecer?",
                 "Depende do número de máquinas e do estado delas. O projeto é dimensionado para "
                 "começar por um conjunto piloto, que valida a leitura e o indicador antes de "
                 "escalar para o restante da fábrica."),
                ("O projeto atende indústria de grande porte?",
                 "Sim. A arquitetura é a mesma que sustenta um parque de dezenas de equipamentos "
                 "em operação contínua, e o time é montado conforme o escopo do projeto."),
            ],
        ),
        "contato": (
            "Comece pelo indicador que hoje ninguém consegue medir",
            "Conte quais máquinas você precisa acompanhar e o que a sua equipe gostaria de ver em "
            "tempo real. A Taquionica avalia o cenário e indica o caminho de leitura para cada "
            "tipo de equipamento.",
            "Falar sobre coleta de dados",
            "Olá! Vim da página de Coleta de Dados de Máquinas da Taquionica e gostaria de avaliar "
            "o monitoramento da minha produção.",
            "Coleta de Dados de Máquinas",
        ),
    },

    # ------------------------------------------------------ 4. diagnostico tecnico
    {
        "slug": "diagnostico-tecnico",
        "titulo": "Diagnóstico Técnico de Hardware, Firmware e Placas Eletrônicas | Taquionica",
        "descricao": ("A Taquionica analisa hardware, firmware, comunicação e layout de placa "
                      "para encontrar a causa da falha e apresentar o caminho de correção."),
        "hero": (
            "Diagnóstico técnico",
            "O equipamento falha em campo e ",
            "ninguém sabe dizer por quê",
            "",
            "Ruído elétrico, alimentação subdimensionada, comunicação instável, firmware que "
            "bloqueia, layout que acopla sinal. A Taquionica analisa o projeto, identifica as "
            "causas prováveis e entrega a ordem em que elas devem ser resolvidas.",
            "Solicitar diagnóstico",
            "Olá! Vim da página de Diagnóstico Técnico da Taquionica e gostaria de solicitar uma "
            "análise do meu equipamento.",
            IMG["auto4"],
            "Placa de acionamento e conversão de energia, com filtragem e proteções",
            "Placa de acionamento e conversão de energia",
            "Eletrônica de potência",
        ),
        "problema": (
            "A falha que só acontece no cliente",
            "Bancada não reproduz o problema, campo reproduz toda semana. Esse padrão quase sempre "
            "aponta para uma causa que não está onde a equipe procurou.",
            [
                ("alert", "Falha intermitente que não se reproduz em bancada"),
                ("plug", "Reset aleatório que ninguém consegue associar a uma causa"),
                ("radio", "Comunicação que cai sob condição específica de campo"),
                ("board", "Placa que aquece, queima componente ou apresenta ruído"),
                ("clock", "Meses de tentativa e erro sem convergir para uma explicação"),
            ],
        ),
        "oferta": (
            "Hora de engenharia, não mais uma rodada de tentativa",
            "O que você contrata é a bagagem que a equipe leva para dentro do problema: mais de "
            "duas décadas em eletrônica, firmware e comunicação industrial. Quem já viu a falha "
            "antes chega nela em menos horas.",
        ),
        "entregas": (
            "O que o diagnóstico cobre",
            "O escopo e o valor são definidos depois de entender o equipamento e a falha. Não "
            "existe diagnóstico de prateleira, e você recebe a estimativa de horas antes de "
            "qualquer trabalho começar.",
            [
                ("Revisão de hardware",
                 "Alimentação, aterramento, proteções, dimensionamento de componentes e pontos de "
                 "acoplamento de ruído no circuito."),
                ("Análise de firmware",
                 "Estrutura do código, bloqueios, tratamento de exceção, watchdog e o que o "
                 "equipamento faz quando um sensor devolve valor inesperado."),
                ("Avaliação de comunicação",
                 "Estabilidade de Wi-Fi, Bluetooth, Modbus, CAN ou MQTT sob a condição real de "
                 "operação, não sob a condição da bancada."),
                ("Revisão de PCB e laudo",
                 "Layout, retorno de corrente, separação de sinais e um relatório com as causas "
                 "prováveis na ordem em que devem ser atacadas."),
            ],
        ),
        "prova": (
            "Diagnóstico feito por quem projeta, não por quem só testa",
            "A Taquionica desenvolve hardware, firmware e comunicação. É por isso que a análise "
            "atravessa as camadas em vez de parar na fronteira entre elas, que é justamente onde "
            "a maioria das falhas mora.",
            [
                ("Desde 2001", "O responsável técnico projeta eletrônica, firmware e comunicação "
                               "industrial."),
                ("45+", "Equipamentos em operação contínua há mais de seis anos, mantidos e "
                        "atualizados à distância."),
                ("Estimativa antes", "Você recebe a estimativa de horas e as causas prováveis "
                                     "antes de autorizar qualquer trabalho."),
            ],
        ),
        "tecnologias": (
            "As camadas onde a falha costuma se esconder",
            "A análise não escolhe uma camada de antemão. Ela segue a evidência até onde a causa "
            "estiver.",
            ["Alimentação", "Aterramento", "Ruído e EMI", "Layout de PCB", "Firmware",
             "Modbus", "CAN", "Wi-Fi e BLE"],
        ),
        "projetos": (
            "Eletrônica desenvolvida e mantida pela Taquionica",
            [
                (IMG["auto4"], "Energia", "Placa de acionamento e conversão de energia",
                 "Hardware com estágio de conversão, filtragem, proteções e interface de comando "
                 "para o inversor.",
                 ["Eletrônica", "Conversão DC/DC", "PCB de potência"]),
                (IMG["auto1"], "Automação industrial", "Placa de controle para acionamento de motores",
                 "Hardware dedicado com estágio de potência para dois motores, proteções e "
                 "firmware de controle.",
                 ["Eletrônica", "PCB", "Microcontrolador", "Firmware"]),
                (IMG["auto5"], "Instrumentação", "Placa de aquisição e condicionamento de sinais",
                 "Amplificação configurável, ajuste de ganho e offset, sinalização por LEDs e "
                 "barramento de integração.",
                 ["Eletrônica", "Instrumentação", "PCB"]),
            ],
        ),
        "faq": (
            "Dúvidas sobre diagnóstico técnico",
            [
                ("Vocês analisam projeto desenvolvido por outra equipe?",
                 "Sim. É o caso mais comum. Avaliamos hardware, firmware e comunicação "
                 "independentemente de quem desenvolveu, e o relatório aponta as causas prováveis "
                 "sem depender de acesso ao fornecedor anterior."),
                ("Preciso enviar o equipamento?",
                 "Nem sempre. Boa parte da análise começa por esquemático, layout, código e pela "
                 "descrição precisa de quando a falha acontece. O envio de amostra é combinado "
                 "quando a investigação exige medição no equipamento montado."),
                ("Quanto custa o diagnóstico?",
                 "O valor é definido depois de entender o equipamento e a falha, porque o escopo "
                 "muda muito de um caso para outro. Você recebe a estimativa de horas antes de "
                 "qualquer trabalho começar."),
                ("O que eu recebo no fim?",
                 "Um relatório com as causas prováveis da falha, a ordem em que devem ser "
                 "resolvidas e a orientação técnica para corrigir e evoluir a solução."),
                ("A Taquionica executa a correção depois do diagnóstico?",
                 "Pode executar, se você quiser. Também é possível levar o relatório para a sua "
                 "equipe interna executar. O diagnóstico é contratável isoladamente."),
                ("Vocês assinam acordo de sigilo antes da análise?",
                 "Sim. Tratamos as informações com confidencialidade e formalizamos acordos "
                 "específicos de sigilo antes do início dos trabalhos quando necessário."),
            ],
        ),
        "contato": (
            "Descreva a falha e receba a estimativa antes de contratar",
            "Conte qual é o equipamento, o que acontece e em que condição a falha aparece. A "
            "Taquionica avalia o cenário e devolve as causas prováveis e a estimativa de horas.",
            "Solicitar diagnóstico",
            "Olá! Vim da página de Diagnóstico Técnico da Taquionica e gostaria de solicitar uma "
            "análise do meu equipamento.",
            "Diagnóstico Técnico",
        ),
    },

    # -------------------------------------------------- 5. aplicativo e dashboard
    {
        "slug": "aplicativo-para-equipamentos",
        "titulo": "Aplicativo e Dashboard para Controlar Equipamentos | Taquionica",
        "descricao": ("A Taquionica desenvolve aplicativo e dashboard conectados ao firmware do "
                      "equipamento, para configurar, acompanhar e controlar de qualquer lugar."),
        "hero": (
            "Aplicativo e dashboard",
            "O aplicativo que ",
            "configura e controla",
            " o seu equipamento",
            "Não é um app genérico ligado a uma API pronta. A Taquionica desenvolve o aplicativo "
            "junto com o firmware que roda dentro do equipamento, então o que aparece na tela é "
            "exatamente o que a placa está fazendo naquele instante.",
            "Falar sobre meu aplicativo",
            "Olá! Vim da página de Aplicativo para Equipamentos da Taquionica e gostaria de falar "
            "sobre um aplicativo conectado ao meu equipamento.",
            IMG["app2"],
            "Aplicativo mostrando gráficos de temperatura, tensão e potência em tempo real",
            "App com gráficos de temperatura, tensão e potência",
            "Eletrônica embarcada",
        ),
        "problema": (
            "O equipamento é bom. A experiência de usar não é",
            "Quando a única interface é um display de duas linhas e três botões, o valor do "
            "equipamento fica escondido de quem opera e de quem compra.",
            [
                ("phone", "Configuração que só é possível com técnico na frente do equipamento"),
                ("chart", "Dado que o equipamento gera e ninguém consegue visualizar"),
                ("radio", "App feito por terceiro que não conversa direito com o firmware"),
                ("clock", "Cada ajuste de parâmetro vira um deslocamento técnico"),
                ("layers", "Fabricante de app e fabricante da placa culpando um ao outro"),
            ],
        ),
        "oferta": (
            "App, dashboard e firmware desenvolvidos pela mesma equipe",
            "A Taquionica desenvolve o aplicativo para configurar, acompanhar e controlar o "
            "equipamento, o painel web para a gestão do parque instalado e o firmware que conversa "
            "com os dois. Um só fornecedor responde pela cadeia inteira.",
        ),
        "entregas": (
            "O que o aplicativo entrega para a sua operação",
            "O escopo é definido sobre o equipamento real e sobre quem vai usar o app, o operador "
            "em campo, o técnico de assistência ou o gestor do parque instalado.",
            [
                ("Configuração no lugar",
                 "Perfis de operação, ajuste de parâmetros e calibração pelo celular, por "
                 "Bluetooth, sem precisar de notebook e cabo."),
                ("Acompanhamento em tempo real",
                 "Gráficos de temperatura, tensão, corrente, potência e consumo, com histórico "
                 "para investigar o que aconteceu."),
                ("Controle e alerta",
                 "Comando enviado ao equipamento e alerta no celular quando a leitura sai da "
                 "faixa esperada ou o equipamento para."),
                ("Painel do parque instalado",
                 "Dashboard web com todos os equipamentos, estado de conexão, localização e "
                 "atualização de firmware da frota à distância."),
            ],
        ),
        "prova": (
            "App que já está no bolso de quem opera",
            "A Taquionica mantém aplicativo e painel em operação sobre um parque instalado real, "
            "com atualização remota de firmware, sem deslocar técnico até o cliente.",
            [
                ("45+", "Equipamentos acompanhados por app e painel, em operação contínua há "
                        "mais de seis anos."),
                ("Frota remota", "Novas versões de firmware distribuídas à distância, sem visita "
                                 "técnica."),
                ("Um só time", "Firmware, comunicação, app e painel desenvolvidos pela mesma "
                               "equipe, sem fronteira entre fornecedores."),
            ],
        ),
        "tecnologias": (
            "A conexão certa para cada situação de uso",
            "Bluetooth para o operador que está ao lado do equipamento, nuvem para o gestor que "
            "está a quilômetros dele. O projeto usa as duas quando faz sentido.",
            ["Android", "BLE", "Wi-Fi", "MQTT", "4G", "Dashboard web", "Histórico",
             "Atualização remota"],
        ),
        "projetos": (
            "Aplicativo e painel em equipamentos reais",
            [
                (IMG["app1"], "Eletrônica embarcada", "Aplicativo para configuração de equipamento",
                 "App conectado por Bluetooth ao firmware, com perfis de operação, gráficos em "
                 "tempo real de temperatura, tensão e potência, e histórico.",
                 ["Android", "BLE", "Firmware", "App"]),
                (IMG["dash"], "Monitoramento", "Painel de acompanhamento do parque instalado",
                 "Equipamentos no mapa, estado de conexão e leituras em tempo real, com "
                 "atualização contínua.",
                 ["Dashboard", "MQTT", "Tempo real", "Mapa"]),
                (IMG["auto3"], "Automação / Indústria",
                 "Controlador conectado para monitoramento remoto",
                 "Placa com módulo Wi-Fi integrado, múltiplas saídas de acionamento e envio de "
                 "dados para dashboard em nuvem.",
                 ["Eletrônica", "IoT", "ESP32", "Wi-Fi / MQTT"]),
            ],
        ),
        "faq": (
            "Dúvidas sobre aplicativo para equipamentos",
            [
                ("Vocês desenvolvem o app para um equipamento que já existe?",
                 "Sim. Avaliamos o firmware atual e a capacidade de comunicação do equipamento, e "
                 "definimos o que precisa ser ajustado no embarcado para o aplicativo conversar "
                 "com ele de forma estável."),
                ("O aplicativo funciona sem internet?",
                 "Funciona, quando a conexão é por Bluetooth. Nesse modo o operador configura e "
                 "acompanha o equipamento estando ao lado dele, sem depender de rede. O painel "
                 "web e o alerta remoto dependem de conexão."),
                ("Dá para atualizar o firmware da frota pelo aplicativo?",
                 "Quando o hardware e a arquitetura de comunicação permitem, sim. A Taquionica já "
                 "mantém um parque instalado recebendo novas versões à distância, sem deslocar "
                 "técnico até o cliente."),
                ("Vocês fazem app para iPhone também?",
                 "A plataforma é definida no início do projeto, conforme quem vai usar o "
                 "aplicativo e o tipo de conexão com o equipamento. Isso entra na conversa "
                 "técnica antes do escopo fechar."),
                ("O app pode ficar com a marca da nossa empresa?",
                 "Pode. O aplicativo é desenvolvido para o seu equipamento e leva a identidade da "
                 "sua empresa, publicado na conta da sua empresa."),
                ("Vocês desenvolvem o hardware junto com o aplicativo?",
                 "Sim. Hardware, firmware, comunicação, aplicativo e painel são desenvolvidos e "
                 "integrados pela mesma equipe, que é o que evita o app e a placa discordarem em "
                 "campo."),
            ],
        ),
        "contato": (
            "Coloque o seu equipamento na palma da mão de quem opera",
            "Conte qual é o equipamento e o que a sua equipe precisa ver ou ajustar à distância. A "
            "Taquionica avalia a viabilidade e indica o caminho de comunicação mais adequado.",
            "Falar sobre meu aplicativo",
            "Olá! Vim da página de Aplicativo para Equipamentos da Taquionica e gostaria de avaliar "
            "um aplicativo conectado ao meu equipamento.",
            "Aplicativo para Equipamentos",
        ),
    },
]


PAGINAS += novas(IMG)

# ------------------------------------------- formulario nas paginas que ja existem
EXISTENTES = {
    "desenvolvimento-produtos-eletronicos": (
        "Transforme a sua ideia em um produto que funciona em campo",
        "Conte o que a sua empresa precisa desenvolver. A Taquionica avalia a viabilidade "
        "técnica, aponta os pontos críticos do projeto e indica o caminho até o produto pronto "
        "para operar.",
        "Apresentar meu projeto",
        "Olá! Vim da página de Desenvolvimento de Produtos Eletrônicos da Taquionica e gostaria de "
        "apresentar meu projeto.",
        "Desenvolvimento de Produtos Eletrônicos",
    ),
    "desenvolvimento-firmware": (
        "Chega de travamentos: evolua o firmware do seu equipamento",
        "A Taquionica avalia o firmware atual do seu equipamento e define o caminho para corrigir "
        "problemas, adicionar funcionalidades ou desenvolver um firmware novo, do zero.",
        "Falar sobre meu firmware",
        "Olá! Vim da página de Desenvolvimento de Firmware da Taquionica e gostaria de falar sobre "
        "o firmware do meu equipamento.",
        "Desenvolvimento de Firmware",
    ),
    "monitoramento-remoto-iot": (
        "Enxergue a sua operação em tempo real, de onde você estiver",
        "Conte quais equipamentos você precisa acompanhar e o que a sua equipe gostaria de "
        "receber em alerta. A Taquionica avalia o cenário e indica o caminho de conexão para "
        "cada tipo de equipamento.",
        "Falar sobre monitoramento",
        "Olá! Vim da página de Monitoramento Remoto e IoT da Taquionica e gostaria de falar sobre "
        "monitorar meus equipamentos.",
        "Monitoramento Remoto e IoT",
    ),
    "automacao-industrial": (
        "Automatize o processo que hoje depende de intervenção manual",
        "Conte qual processo ou equipamento precisa ser automatizado. A Taquionica avalia o "
        "cenário e indica o caminho de eletrônica, firmware e comunicação para a sua operação.",
        "Falar sobre automação",
        "Olá! Vim da página de Automação Industrial da Taquionica e gostaria de falar sobre "
        "automatizar um processo da minha operação.",
        "Automação Industrial",
    ),
}


def instala_form(slug, dados):
    caminho = os.path.join(BASE, slug, "index.html")
    h = io.open(caminho, encoding="utf-8").read()
    i = h.index('<section id="contato"')
    j = h.index("</section>", i) + len("</section>")
    novo = h[:i] + contato(*dados) + h[j:]
    # A pagina de produtos eletronicos abria <main> e nunca fechava, defeito
    # herdado do build_lp1.py. Sem o fechamento o navegador encerra o <main>
    # sozinho, mas a marcacao fica invalida. Fecha aqui, antes do rodape.
    if "</main>" not in novo:
        novo = novo.replace("<footer", "</main>\n\n<footer", 1)
    if "tq-cta-grid" not in novo.split("</head>")[0]:
        novo = novo.replace("</style></head>", CSS_EXTRA + "</style></head>", 1)
    if "id='tq-form'" not in novo and "tq-form" in novo and JS_FORM.strip() not in novo:
        novo = novo.replace("</body></html>", "<script>" + JS_FORM + "</script></body></html>")
    io.open(caminho, "w", encoding="utf-8", newline="").write(novo)
    return caminho


def main():
    prefixo, sufixo = le_doador()
    escritos = []

    for pag in PAGINAS:
        html = monta(pag, prefixo, sufixo)
        pasta = os.path.join(BASE, pag["slug"])
        if not os.path.isdir(pasta):
            os.makedirs(pasta)
        alvo = os.path.join(pasta, "index.html")
        io.open(alvo, "w", encoding="utf-8", newline="").write(html)
        escritos.append(alvo)
        print("nova    %-42s %6d bytes" % (pag["slug"], len(html)))

    for slug, dados in EXISTENTES.items():
        escritos.append(instala_form(slug, dados))
        print("form em %-42s" % slug)

    # ------------------------------------------------------------------ sitemap
    urls = [("", "weekly", "1.0")]
    for slug in ["desenvolvimento-produtos-eletronicos", "desenvolvimento-firmware",
                 "monitoramento-remoto-iot", "automacao-industrial"]:
        urls.append((slug, "monthly", "0.9"))
    for pag in PAGINAS:
        urls.append((pag["slug"], "monthly", "0.9"))
    urls.append(("politica-de-privacidade", "yearly", "0.3"))
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, freq, pri in urls:
        loc = SITE + "/" if slug == "" else SITE + "/" + slug
        linhas += ["  <url>", "    <loc>%s</loc>" % loc,
                   "    <changefreq>%s</changefreq>" % freq,
                   "    <priority>%s</priority>" % pri, "  </url>"]
    linhas.append("</urlset>")
    sm = os.path.join(BASE, "sitemap.xml")
    io.open(sm, "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
    print("sitemap com %d URLs" % len(urls))

    # -------------------------------------------------------------- verificacoes
    problemas = []
    for caminho in escritos:
        txt = io.open(caminho, encoding="utf-8").read()
        nome = os.path.relpath(caminho, BASE)
        # Regra permanente do cliente: nada de travessao dentro das frases.
        for tracinho in ["—", "–"]:
            if tracinho in txt:
                problemas.append("%s: travessao encontrado" % nome)
        # Tipografia vazada e proibida no projeto inteiro.
        if "text-stroke" in txt:
            problemas.append("%s: texto com contorno" % nome)
        if txt.count("<main>") != 1 or txt.count("</main>") != 1:
            problemas.append("%s: <main> desbalanceado" % nome)
        if 'id="tq-form"' not in txt:
            problemas.append("%s: sem formulario" % nome)
        if "tq-cta-grid" not in txt.split("</head>")[0]:
            problemas.append("%s: CSS do formulario ausente" % nome)
        if "var f = document.getElementById('tq-form')" not in txt:
            problemas.append("%s: JS do formulario ausente" % nome)

    if problemas:
        print("\n*** PROBLEMAS ***")
        for p in problemas:
            print("  " + p)
        sys.exit(1)
    print("\nOK: %d paginas verificadas." % len(escritos))


if __name__ == "__main__":
    main()
