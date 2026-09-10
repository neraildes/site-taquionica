# -*- coding: utf-8 -*-
"""Reescreve a landing page de Desenvolvimento de Produtos Eletronicos.

Mantem o <head>, o cabecalho e o rodape originais e substitui todo o miolo,
da secao #topo ate o fim de #contato, por um conteudo escrito para converter
o trafego do grupo de anuncios "Hardware e Produtos Eletronicos".
"""
import io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALVO = os.path.join(BASE, "desenvolvimento-produtos-eletronicos", "index.html")

WA = ("https://wa.me/5516993668447?text=Ol%C3%A1!%20Vim%20da%20p%C3%A1gina%20de%20"
      "Desenvolvimento%20de%20Produtos%20Eletr%C3%B4nicos%20da%20Taquionica%20e%20"
      "gostaria%20de%20apresentar%20meu%20projeto.")

SVG_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false" '
          'class="mr-2 h-5 w-5"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"></path></svg>')

CTA_PRIM = ('class="inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium '
            'cursor-pointer transition-colors focus-visible:outline-none focus-visible:ring-1 '
            'focus-visible:ring-ring shadow h-12 rounded-md px-8 text-base bg-black text-white '
            'hover:bg-white focus-visible:bg-white active:bg-white shadow-glow border '
            'border-white/20 [&:hover_*]:!text-black [&:focus-visible_*]:!text-black '
            '[&:active_*]:!text-black lp-cta-wrap"')

CTA_SEC = ('class="inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium '
           'cursor-pointer transition-colors focus-visible:outline-none focus-visible:ring-1 '
           'focus-visible:ring-ring border shadow-sm h-12 rounded-md px-8 text-base bg-black '
           'text-white border-white/30 hover:bg-white focus-visible:bg-white active:bg-white '
           '[&:hover_*]:!text-black [&:focus-visible_*]:!text-black [&:active_*]:!text-black '
           'lp-cta-wrap"')

ICON = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" class="lucide %s" aria-hidden="true">%s</svg>')

P_CPU = ('<rect width="16" height="16" x="4" y="4" rx="2"></rect><rect width="6" height="6" '
         'x="9" y="9" rx="1"></rect><path d="M15 2v2"></path><path d="M15 20v2"></path>'
         '<path d="M2 15h2"></path><path d="M2 9h2"></path><path d="M20 15h2"></path>'
         '<path d="M20 9h2"></path><path d="M9 2v2"></path><path d="M9 20v2"></path>')
P_CIRC = ('<path d="M11 9h4a2 2 0 0 0 2-2V3"></path><circle cx="9" cy="9" r="2"></circle>'
          '<path d="M7 21h10"></path><path d="M13 15h-4a2 2 0 0 1-2-2V7"></path>'
          '<circle cx="15" cy="15" r="2"></circle>')
P_CHECK = '<path d="M20 6 9 17l-5-5"></path>'
P_SHIELD = ('<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 '
            '0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 '
            '1 1z"></path><path d="m9 12 2 2 4-4"></path>')
P_USERS = ('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><path d="M16 3.128a4 4 0 '
           '0 1 0 7.744"></path><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>'
           '<circle cx="9" cy="7" r="4"></circle>')
P_ALERT = ('<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3">'
           '</path><path d="M12 9v4"></path><path d="M12 17h.01"></path>')
P_BULB = ('<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1.3.5 2.6 '
          '1.5 3.5.8.8 1.3 1.5 1.5 2.5"></path><path d="M9 18h6"></path><path d="M10 22h4"></path>')
P_LAYERS = ('<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 '
            '1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"></path><path d="m6.08 10.37-3.5 1.59a1 1 0 0 0 0 '
            '1.83l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9a1 1 0 0 0 0-1.83l-3.5-1.6"></path>'
            '<path d="m6.08 15.37-3.5 1.59a1 1 0 0 0 0 1.83l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9a1 '
            '1 0 0 0 0-1.83l-3.5-1.6"></path>')
P_ARROW = '<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>'

CHIP = ('<span class="inline-flex items-center gap-2 rounded-full bg-[oklch(0.66_0.19_250)]/10 '
        'px-3 py-1 text-xs font-semibold uppercase tracking-wide text-[oklch(0.5_0.17_255)]">%s</span>')

BOX_ICON = ('<div class="grid place-items-center h-11 w-11 shrink-0 rounded-xl '
            'bg-[oklch(0.66_0.19_250)]/10 text-[oklch(0.5_0.17_255)]">%s</div>')


def item(icone, titulo, texto):
    return ('<div class="flex items-start gap-4">' + BOX_ICON % (ICON % (icone[0] + ' h-5 w-5', icone[1])) +
            '<div><h3 class="text-lg font-semibold">' + titulo + '</h3>'
            '<p class="mt-2 text-sm text-muted-foreground leading-relaxed">' + texto + '</p></div></div>')


def card(icone, titulo, texto, marcadores):
    # O CSS compilado não traz a variante bg- dessa cor arbitrária, só a text-.
    # Um ícone de check resolve o visual e ainda lê melhor numa lista de entregas.
    tick = ICON % ('lucide-check h-4 w-4 shrink-0 mt-0.5 text-[oklch(0.5_0.17_255)]', P_CHECK)
    lis = "".join('<li class="flex items-start gap-2">' + tick + '<span>' + m + '</span></li>'
                  for m in marcadores)
    return ('<div class="card-surface p-6 sm:p-8 flex flex-col gap-4">' +
            BOX_ICON % (ICON % (icone[0] + ' h-5 w-5', icone[1])) +
            '<h3 class="text-xl font-bold tracking-tight">' + titulo + '</h3>'
            '<p class="text-sm text-muted-foreground leading-relaxed">' + texto + '</p>'
            '<ul class="mt-1 flex flex-col gap-2 text-sm text-muted-foreground">' + lis + '</ul></div>')


def numero(valor, rotulo):
    return ('<div class="card-surface p-6 text-center"><div class="text-3xl sm:text-4xl font-extrabold '
            'tracking-tight text-gradient">' + valor + '</div>'
            '<p class="mt-2 text-sm text-muted-foreground leading-relaxed">' + rotulo + '</p></div>')


def etapa(n, titulo, texto):
    return ('<div class="card-surface p-6 flex flex-col gap-3"><span class="text-xs font-bold '
            'tracking-widest text-[oklch(0.5_0.17_255)]">' + n + '</span>'
            '<h3 class="text-lg font-semibold leading-snug">' + titulo + '</h3>'
            '<p class="text-sm text-muted-foreground leading-relaxed">' + texto + '</p></div>')


def faq(pergunta, resposta):
    return ('<details class="lp-faq-item card-surface p-6"><summary class="flex cursor-pointer '
            'items-center justify-between gap-4 text-left"><span class="text-base font-semibold">' +
            pergunta + '</span>' + ICON % ('lucide-chevron-down lp-faq-chevron h-5 w-5 shrink-0 '
            'text-muted-foreground', '<path d="m6 9 6 6 6-6"></path>') + '</summary>'
            '<p class="mt-4 text-sm text-muted-foreground leading-relaxed">' + resposta + '</p></details>')


# ------------------------------------------------------------------ secoes
HERO = (
    '<section id="topo" class="relative overflow-hidden gradient-hero text-white pt-24 pb-20 md:pt-28 md:pb-28">'
    '<div class="container-x relative grid gap-12 lg:grid-cols-2 lg:items-center"><div class="min-w-0">'
    '<span class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-3 py-1 '
    'text-xs font-medium text-white/80 backdrop-blur">' +
    ICON % ('lucide-cpu h-3.5 w-3.5 text-[oklch(0.82_0.13_220)]', P_CPU) +
    'Design house de eletrônica desde 2001</span>'
    '<h1 class="mt-5 text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl leading-[1.05]">'
    'Desenvolvimento de produtos eletrônicos <span class="text-gradient">do circuito ao equipamento em campo</span></h1>'
    '<p class="mt-6 text-lg text-white/70 max-w-xl leading-relaxed">Hardware, firmware e PCB projetados pela '
    'mesma equipe de engenharia. Sua empresa trata com um único responsável técnico, do diagnóstico à entrega, '
    'com escopo, prazo e valor fechados antes da primeira linha de código.</p>'
    '<div class="mt-8 flex flex-wrap gap-3">'
    '<a href="' + WA + '" target="_blank" rel="noopener noreferrer" ' + CTA_PRIM + '>' + SVG_WA +
    'Apresentar meu projeto</a>'
    '<a href="#entrega" ' + CTA_SEC + '>Ver o que entregamos ' +
    ICON % ('lucide-arrow-right ml-2 h-4 w-4', P_ARROW) + '</a></div>'
    '<p class="mt-5 text-sm text-white/60">Primeira conversa sem custo e sem compromisso. Informações '
    'tratadas com confidencialidade, com acordo de sigilo quando necessário.</p></div>'
    '<div class="relative"><div class="relative mx-auto w-full max-w-xl">'
    '<div class="absolute inset-0 -z-10 rounded-3xl bg-gradient-to-br from-white/5 to-white/0 blur-2xl"></div>'
    '<div class="relative rounded-3xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur-sm shadow-elegant">'
    '<img src="/__l5e/assets-v1/e4198e94-ffe2-440d-996f-faa1dc4041b2/agro-1.jpg" alt="Automação embarcada '
    'desenvolvida pela Taquionica operando em campo" loading="eager" decoding="async" '
    'class="w-full h-auto rounded-2xl border border-white/10"/>'
    '<div class="mt-4 flex items-center justify-between text-xs text-white/60">'
    '<span class="inline-flex items-center gap-2"><span class="h-1.5 w-1.5 rounded-full '
    'bg-[oklch(0.72_0.17_155)] animate-pulse-dot"></span>Projeto nosso, em operação há mais de seis anos</span>'
    '<span>Hardware • Firmware • PCB</span></div></div></div></div></div></section>'
)

PROVA = (
    '<section id="prova" class="py-14 md:py-16 bg-background"><div class="container-x">'
    '<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">' +
    numero("2001", "Ano em que o responsável técnico começou a desenvolver equipamentos eletrônicos.") +
    numero("12 anos", "Em equipamentos médicos, sob requisitos da Anvisa, onde não existe improviso.") +
    numero("45+", "Equipamentos nossos em operação contínua, com atualização remota de frota.") +
    numero("6 anos", "É há quanto tempo esse parque roda sem interrupção de serviço.") +
    '</div></div></section>'
)

PROBLEMA = (
    '<section id="problema" class="py-20 md:py-28 bg-secondary/40"><div class="container-x">'
    '<div class="text-center mx-auto max-w-3xl">' + CHIP % "O que trava um projeto eletrônico" +
    '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight leading-[1.1]">'
    'O projeto não para por falta de ideia. Para por falta de engenharia.</h2>'
    '<p class="mt-5 text-base text-muted-foreground leading-relaxed">Se algum destes pontos descreve o seu '
    'momento, a conversa técnica costuma resolver mais rápido do que mais uma rodada de tentativa.</p></div>'
    '<div class="mt-12 mx-auto max-w-3xl card-surface p-6 sm:p-10 flex flex-col gap-6">' +
    item(('lucide-lightbulb', P_BULB), "A ideia existe, o caminho técnico não",
         "Sua empresa enxerga a oportunidade, mas falta quem transforme o requisito comercial em arquitetura "
         "eletrônica, escolha de componentes e plano de desenvolvimento.") +
    item(('lucide-alert', P_ALERT), "O protótipo de bancada não vira produto",
         "Montado com módulos genéricos, funciona na mesa e falha no campo. Sem projeto de hardware e de placa "
         "pensado para produção, não há como escalar nem certificar.") +
    item(('lucide-users', P_USERS), "Fornecedores que não conversam entre si",
         "Um faz a placa, outro o firmware, outro o aplicativo. Quando algo falha, cada um aponta para o "
         "próximo, e o prazo do seu produto é quem paga a conta.") +
    item(('lucide-alert', P_ALERT), "A placa que funciona na bancada falha em campo",
         "Vibração, poeira, temperatura e alimentação oscilando derrubam projeto que não foi feito para o "
         "ambiente real de operação.") +
    '</div></div></section>'
)

ENTREGA = (
    '<section id="entrega" class="py-20 md:py-28 bg-background"><div class="container-x">'
    '<div class="text-center mx-auto max-w-3xl">' + CHIP % "O que entregamos" +
    '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight leading-[1.1]">'
    'Engenharia eletrônica completa, ou só a camada que falta no seu time</h2>'
    '<p class="mt-5 text-base text-muted-foreground leading-relaxed">É possível contratar o produto inteiro '
    'ou apenas uma disciplina, como braço técnico complementar da sua engenharia.</p></div>'
    '<div class="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">' +
    card(('lucide-circuit', P_CIRC), "Projeto de hardware",
         "Arquitetura eletrônica, circuitos, sensores, interfaces e comunicação, com escolha de componentes "
         "pensada para disponibilidade e para o custo do produto final.",
         ["Eletrônica analógica e digital", "Estágios de potência e proteções",
          "Instrumentação e condicionamento de sinais", "Seleção de componentes e BOM"]) +
    card(('lucide-layers', P_LAYERS), "Projeto e revisão de PCB",
         "Layout de placa preparado para fabricar e para operar, não apenas para passar no software de "
         "desenho. Também revisamos placas existentes que falham em campo.",
         ["Layout multicamada e organização de sinais", "Redução de ruído e integridade de sinal",
          "Preparação de arquivos para fabricação", "Revisão de projeto de terceiros"]) +
    card(('lucide-cpu', P_CPU), "Firmware embarcado",
         "Programação de microcontroladores com a comunicação que o seu equipamento precisa falar, do "
         "primeiro protótipo à versão que roda no campo.",
         ["ESP32 e microcontroladores em geral", "Wi-Fi, Bluetooth, MQTT, Modbus e CAN",
          "Leitura de sensores e acionamento de atuadores", "Atualização remota de frota"]) +
    card(('lucide-check', P_CHECK), "Protótipo funcional",
         "Uma versão que a sua empresa pode testar, mostrar para cliente e levar para validação técnica "
         "antes de comprometer verba com produção.",
         ["Prova de conceito rápida", "Protótipo de validação técnica",
          "Testes em condição real de uso", "Caminho claro até a versão final"]) +
    card(('lucide-shield', P_SHIELD), "Produto preparado para operar",
         "A diferença entre um projeto que funciona e um produto que aguenta. Vinte e quatro anos de "
         "eletrônica aplicados ao que costuma quebrar.",
         ["Robustez elétrica e proteções", "Operação sob vibração, poeira e variação térmica",
          "Disciplina vinda de setor regulado", "Documentação técnica do projeto"]) +
    card(('lucide-users', P_USERS), "Terceirização de engenharia",
         "Sua engenharia continua no comando e nós entramos na disciplina que falta, com um interlocutor "
         "único e capacidade dimensionada pelo escopo.",
         ["Um só responsável técnico do início ao fim", "Time montado conforme a etapa do projeto",
          "Sem estrutura ociosa embutida no preço", "Acordo de sigilo quando necessário"]) +
    '</div></div></section>'
)

JORNADA = (
    '<section id="jornada" class="py-20 md:py-28 bg-secondary/40"><div class="container-x">'
    '<div class="text-center mx-auto max-w-3xl">' + CHIP % "Como trabalhamos" +
    '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight leading-[1.1]">'
    'Você sabe o escopo, o prazo e o valor antes do desenvolvimento começar</h2>'
    '<p class="mt-5 text-base text-muted-foreground leading-relaxed">Cada projeto é dimensionado sobre o '
    'problema real. Por isso o investimento é definido na conversa técnica, e não em tabela de prateleira.</p></div>'
    '<div class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">' +
    etapa("01", "Entendimento", "Sua empresa apresenta a ideia, o equipamento ou o problema que precisa ser resolvido.") +
    etapa("02", "Diagnóstico", "Avaliamos necessidades, riscos, limitações e possibilidades técnicas.") +
    etapa("03", "Planejamento", "Definimos arquitetura, escopo, etapas, entregas e requisitos, com prazo e valor fechados.") +
    etapa("04", "Desenvolvimento", "Criamos e integramos hardware, firmware, placa, software e comunicação.") +
    etapa("05", "Testes", "Validamos funcionamento, comunicação, estabilidade e resposta em condição real.") +
    etapa("06", "Entrega e evolução", "Entregamos o projeto e planejamos melhorias e novas funcionalidades.") +
    '</div></div></section>'
)

PROJETO = (
    '<section id="projeto" class="py-20 md:py-28 bg-background"><div class="container-x">'
    '<div class="grid gap-12 lg:grid-cols-2 lg:items-center"><div class="min-w-0">' +
    CHIP % "Projeto real" +
    '<h2 class="mt-4 text-3xl sm:text-4xl font-extrabold tracking-tight leading-[1.1]">'
    'Eletrônica que trabalha sobre milhões em ativo instalado</h2>'
    '<p class="mt-5 text-base text-muted-foreground leading-relaxed">Uma usina fotovoltaica reúne dezenas de '
    'milhares de módulos, e o parque instalado é avaliado na casa dos milhões de reais. O equipamento '
    'automatizado que desenvolvemos se desloca sobre essas fileiras todos os dias, encostando em vidro que '
    'gera receita.</p>'
    '<p class="mt-4 text-base text-muted-foreground leading-relaxed">Isso muda o que significa funcionar. Um '
    'erro de leitura de posição, um atuador que não recua ou um firmware que trava no meio da fileira deixa '
    'de ser defeito de equipamento e vira módulo danificado e geração perdida. É por isso que a proteção '
    'contra sobrecarga e o controle de posição não são opcionais nesse projeto.</p>'
    '<p class="mt-4 text-base text-muted-foreground leading-relaxed">Quem confia um equipamento automatizado a '
    'um parque desse valor não está comprando uma placa. Está comprando o julgamento de engenharia que decide '
    'onde colocar a proteção, quanta margem deixar e o que o firmware faz quando algo sai do previsto.</p>'
    '<div class="mt-8 flex flex-wrap gap-2 text-xs text-muted-foreground">'
    '<span class="rounded-full border px-3 py-1">Hardware embarcado</span>'
    '<span class="rounded-full border px-3 py-1">Sensores de posição</span>'
    '<span class="rounded-full border px-3 py-1">Controle de atuadores</span>'
    '<span class="rounded-full border px-3 py-1">Firmware</span></div></div>'
    '<div class="relative"><div class="card-surface p-4">'
    '<img src="/__l5e/assets-v1/e4198e94-ffe2-440d-996f-faa1dc4041b2/agro-1.jpg" alt="Implemento automatizado '
    'desenvolvido pela Taquionica em operação numa usina fotovoltaica" loading="lazy" decoding="async" '
    'class="w-full h-auto rounded-2xl"/>'
    '<p class="mt-4 text-sm text-muted-foreground">Automação embarcada em trator para manutenção de usinas '
    'fotovoltaicas, com sensores, controle de atuadores e proteção contra sobrecarga.</p></div></div>'
    '</div></div></section>'
)

FAQ = (
    '<section id="faq" class="py-20 md:py-28 bg-secondary/40"><div class="container-x">'
    '<div class="text-center mx-auto max-w-3xl">' + CHIP % "Perguntas frequentes" +
    '<h2 class="mt-4 text-3xl sm:text-4xl lg:text-[2.75rem] font-extrabold tracking-tight leading-[1.1]">'
    'O que as empresas costumam perguntar antes de contratar</h2></div>'
    '<div class="mt-12 mx-auto max-w-3xl flex flex-col gap-4">' +
    faq("Quanto custa desenvolver um produto eletrônico?",
        "Depende do escopo, e por isso o valor é definido depois da conversa técnica. O que garantimos é que "
        "escopo, prazo e valor ficam fechados antes de qualquer desenvolvimento começar. Não existe orçamento "
        "aberto que cresce no meio do projeto.") +
    faq("Dá para contratar só uma parte, como a placa ou o firmware?",
        "Sim. É possível contratar apenas hardware, firmware, software, aplicativo, PCB ou consultoria, como "
        "braço técnico complementar da sua engenharia, ou o desenvolvimento completo com todas as camadas "
        "integradas.") +
    faq("Vocês têm capacidade para um projeto de grande porte?",
        "Sim. O time é montado conforme o escopo. Nell atua como gerente de projeto e responsável técnico, "
        "coordenando os especialistas de cada disciplina, eletrônica de potência, layout de PCB, firmware, "
        "aplicativo e integração, que entram de acordo com a etapa. A capacidade acompanha o tamanho do "
        "projeto, sem estrutura ociosa embutida no preço.") +
    faq("É possível melhorar um equipamento que já existe?",
        "Sim. Analisamos o equipamento atual e propomos evoluções em eletrônica, firmware, comunicação ou "
        "integração com sistemas e aplicativos. Também revisamos placas de terceiros que falham em campo.") +
    faq("Como as informações do meu projeto são protegidas?",
        "Tratamos tudo com confidencialidade e formalizamos acordo de sigilo antes do início dos trabalhos "
        "sempre que necessário.") +
    faq("Vocês atendem empresas fora de Ribeirão Preto?",
        "Atendemos projetos em todo o Brasil, com reuniões remotas e envio de amostras, protótipos ou "
        "equipamentos conforme a necessidade.") +
    '</div></div></section>'
)

CONTATO = (
    '<section id="contato" class="relative overflow-hidden bg-[oklch(0.14_0.03_258)] text-white py-20 md:py-24">'
    '<div class="container-x text-center mx-auto max-w-3xl">'
    '<h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-[1.1]">'
    'Conte o que sua empresa precisa. A avaliação inicial é sem custo.</h2>'
    '<p class="mt-6 text-lg text-white/70 leading-relaxed">Em uma conversa técnica curta já é possível dizer '
    'se o projeto é viável, por onde começar e qual o caminho mais curto até um protótipo funcional.</p>'
    '<div class="mt-8 flex flex-wrap justify-center gap-3">'
    '<a href="' + WA + '" target="_blank" rel="noopener noreferrer" ' + CTA_PRIM + '>' + SVG_WA +
    'Falar com um especialista</a>'
    '<a href="mailto:taquionica.oficial@gmail.com" ' + CTA_SEC + '>Enviar por e-mail</a></div>'
    '<p class="mt-6 text-sm text-white/60">Ribeirão Preto, São Paulo. Atendimento a projetos em todo o Brasil.</p>'
    '</div></section>'
)

NOVO = HERO + PROVA + PROBLEMA + ENTREGA + JORNADA + PROJETO + FAQ + CONTATO

# ------------------------------------------------------------------ splice
html = io.open(ALVO, encoding="utf-8").read().replace("\x00", "")
ini = html.index('<section id="topo"')
fim = html.index('<footer')
html = html[:ini] + NOVO + html[fim:]

TITULO = "Desenvolvimento de Produtos Eletrônicos e Hardware | Taquionica"
DESC = ("A Taquionica desenvolve produtos eletrônicos sob medida para empresas: projeto de hardware, "
        "PCB e firmware pela mesma equipe, do conceito ao equipamento operando em campo.")
html = re.sub(r"<title>.*?</title>", "<title>" + TITULO + "</title>", html, count=1)
html = re.sub(r'(<meta name="description" content=")[^"]*(")', r"\g<1>" + DESC + r"\g<2>", html, count=1)
html = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r"\g<1>" + TITULO + r"\g<2>", html, count=1)
html = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r"\g<1>" + DESC + r"\g<2>", html, count=1)
html = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', r"\g<1>" + TITULO + r"\g<2>", html, count=1)
html = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', r"\g<1>" + DESC + r"\g<2>", html, count=1)

io.open(ALVO, "w", encoding="utf-8").write(html)
print("ok:", len(html), "bytes")
