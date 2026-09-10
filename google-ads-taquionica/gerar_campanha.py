# -*- coding: utf-8 -*-
"""Gera a pasta `import`: a campanha que vai efetivamente ao ar.

O que mudou em relacao a versao anterior, e por que
=====================================================

**1. O teto de lance caiu de R$ 9 para perto do CPC real.**
A conta paga entre R$ 4,28 e R$ 5 por clique. Teto de R$ 9 nao faz o clique
custar 9, mas faz a campanha ganhar leilao em posicao mais alta, e posicao mais
alta custa mais caro por clique. Com o objetivo sendo volume de clique e de
lead, e melhor comprar mais cliques um pouco mais abaixo na pagina. Os tetos
agora ficam entre R$ 3 e R$ 6,50, cada um calibrado pelo valor do lead daquele
grupo, nao por medo de perder o leilao.

**2. Tres campanhas em vez de uma, para proteger o orcamento.**
Os termos de cabeca do nicho ("automação industrial", "indústria 4.0") tem o
maior volume e a pior intencao. Dentro da mesma campanha eles engoliriam a verba
dos termos que trazem comprador. Isolados numa campanha de R$ 15 por dia, eles
entram sem poder passar disso.

**3. Cinco temas novos, que e de onde vem o clique a mais.**
A versao anterior cobria quatro assuntos e nao tinha volume qualificado
suficiente para gastar R$ 100 por dia. A saida nao e afrouxar a correspondencia,
que so compra busca ruim: e ampliar a superficie de busca qualificada. Entraram
retrofit de maquinas, coleta de dados de producao, diagnostico tecnico e
aplicativos para equipamento. Todos sao servicos que a Taquionica ja presta e
agora tem pagina propria.

Um quinto tema, equipamento medico, chegou a ser montado e foi removido: os doze
anos em equipamento oftalmico sao historico do responsavel tecnico, nao linha de
servico da empresa hoje. Biografia no site nao e o mesmo que catalogo.

**4. O comprador que o cliente quer.**
Ele quer projeto grande, industria e empresa de porte. Isso empurra a selecao
para o vocabulario de quem contrata engenharia terceirizada dentro de uma
empresa: "design house", "outsourcing de engenharia", "terceirização de
engenharia eletrônica", "retrofit de máquinas industriais", "coleta de dados de
chão de fábrica". Nenhum deles tem volume de topo, e todos tem comprador real.

O motor de escrita dos CSVs e a funcao `gera` do `gerar_ads.py`, reaproveitada
aqui junto com a lista global de negativas.
"""
import csv, io, os, sys

import gerar_ads as ga

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "import")
SITE = ga.SITE

PAG_PRODUTOS = SITE + "/desenvolvimento-produtos-eletronicos"
PAG_FIRMWARE = SITE + "/desenvolvimento-firmware"
PAG_MONITOR = SITE + "/monitoramento-remoto-iot"
PAG_AUTOMACAO = SITE + "/automacao-industrial"
PAG_RETROFIT = SITE + "/retrofit-de-maquinas"
PAG_COLETA = SITE + "/coleta-de-dados-de-maquinas"
PAG_DIAGNOSTICO = SITE + "/diagnostico-tecnico"
PAG_APP = SITE + "/aplicativo-para-equipamentos"
PAG_TERCEIRIZACAO = SITE + "/terceirizacao-de-engenharia-eletronica"
PAG_CAMPO = SITE + "/telemetria-agricola-e-solar"
PAG_PCB = SITE + "/projeto-de-pcb"

# Os nove titulos que entram em todos os anuncios. Seis titulos especificos do
# grupo mais estes nove fecham os quinze que o anuncio responsivo aceita.
COMUNS = [
    "Engenharia Desde 2001",
    "45 Equipamentos em Campo",
    "6 Anos Sem Interrupção",
    "Um Só Fornecedor Técnico",
    "Do Circuito ao Aplicativo",
    "Escopo e Prazo Fechados",
    "Atendemos Todo o Brasil",
    "Projeto de Grande Porte",
    "Fale com um Especialista",
]

DESCS_COMUNS = [
    "Mais de 45 equipamentos em operação contínua há mais de seis anos. Desde 2001.",
    "Escopo, prazo e valor fechados antes da primeira linha de código. Fale conosco.",
]


def g(nome, url, cpc, p1, p2, kw, titulos, descs, exatas=None, amplas=None):
    return {
        "nome": nome, "url": url, "cpc": cpc, "p1": p1, "p2": p2,
        "kw": kw, "kw_exatas": exatas or [], "kw_amplas": amplas or [],
        "titulos": titulos, "descs": descs,
        "comuns": COMUNS, "descs_comuns": DESCS_COMUNS,
        "fixa_titulo_1": True,
    }


# ============================================================== C1: engenharia
# O nucleo do negocio. Sao os termos em que a pagina de resultados do Google
# devolve fornecedor, nao artigo nem vaga de emprego, e por isso sao os que
# aguentam o teto de lance mais alto sem trazer publico errado.

G_PRODUTOS = g(
    "Produtos Eletrônicos e Hardware", PAG_PRODUTOS, "5.50", "produtos", "eletronicos",
    [
        "desenvolvimento de produtos eletrônicos",
        "empresa de desenvolvimento de produtos eletrônicos",
        "desenvolvimento de projetos eletrônicos",
        "empresa de projetos eletrônicos",
        "desenvolvimento de protótipos eletrônicos",
        "desenvolvimento de protótipo eletrônico",
        "protótipo eletrônico funcional",
        "criar produto eletrônico",
        "engenharia de produto eletrônico",
        "transformar ideia em produto eletrônico",
        "desenvolvimento de hardware",
        "empresa de desenvolvimento de hardware",
        "projeto de hardware eletrônico",
        "desenvolvimento de hardware sob medida",
        "projeto de circuito eletrônico",
        "engenharia eletrônica sob demanda",
        "desenvolvimento de eletrônica embarcada",
        "projeto eletrônico industrial",
        # O vocabulario de design house saiu daqui e virou grupo proprio, com
        # pagina propria, porque a busca por "terceirizacao de engenharia" quer
        # ler sobre terceirizacao, nao sobre produto eletronico.
        "desenvolvimento de equipamento eletrônico industrial",
        "desenvolvimento de equipamento sob encomenda",
        "fabricante de equipamento eletrônico sob medida",
    ],
    [
        "Produtos Eletrônicos",
        "Desenvolvimento de Hardware",
        "Engenharia Eletrônica",
        "Da Ideia ao Produto Real",
        "Design House de Eletrônica",
        "Braço Técnico de Engenharia",
    ],
    [
        "Transformamos a ideia em circuito, protótipo e equipamento pronto para operar.",
        "Hardware, firmware e PCB integrados pela mesma equipe, sem depender de terceiros.",
    ],
)

G_PCB = g(
    "Projeto de PCB", PAG_PCB, "5.00", "pcb", "layout",
    [
        "desenvolvimento de pcb",
        "projeto de pcb",
        "layout de pcb",
        "projeto de placa eletrônica",
        "desenvolvimento de placa de circuito impresso",
        "projeto de placa de circuito impresso",
        "revisão de projeto de pcb",
        "empresa de projeto de pcb",
        "design de placa eletrônica",
        "layout de placa eletrônica",
        "roteamento de pcb",
        "projeto de pcb multicamadas",
        "empresa de layout de pcb",
    ],
    [
        "Projeto e Layout de PCB",
        "Desenvolvimento de PCB",
        "Revisão do Layout da Placa",
        "PCB Pronta Para Fabricar",
        "Menos Ruído na Sua Placa",
        "Placa Eletrônica Sob Medida",
    ],
    [
        "Layout, organização de sinais, redução de ruído e preparação para fabricação.",
        "Revisamos placas que falham em campo e indicamos o caminho para corrigir.",
    ],
)

G_FIRMWARE = g(
    "Firmware e Embarcados", PAG_FIRMWARE, "5.50", "firmware", "embarcado",
    [
        "desenvolvimento de firmware",
        "empresa de desenvolvimento de firmware",
        "empresa de firmware",
        "programação de firmware",
        "desenvolvimento de firmware embarcado",
        "firmware sob medida",
        "desenvolvimento de sistemas embarcados",
        "empresa de sistemas embarcados",
        "firmware para microcontrolador",
        "programação de microcontrolador",
        "desenvolvimento de software embarcado",
        "terceirização de desenvolvimento de firmware",
        "desenvolvimento embarcado para indústria",
        "atualização remota de firmware",
        "programação esp32",
        "desenvolvimento com esp32",
        "firmware esp32",
        "desenvolvimento mqtt",
        "integração modbus",
        "comunicação modbus industrial",
        "firmware com wifi e bluetooth",
        "integração can bus industrial",
    ],
    [
        "Desenvolvimento de Firmware",
        "Firmware Para Embarcados",
        "Firmware Que Não Trava",
        "Corrigimos Firmware Instável",
        "Microcontrolador Sob Medida",
        "Atualização Remota de Frota",
    ],
    [
        "Programação de microcontroladores, sensores, displays, atuadores e comunicação.",
        "Frota atualizada à distância, com novas versões sem deslocar técnico até o cliente.",
    ],
)

# O grupo de entrada. Diagnostico e a compra de menor compromisso do catalogo,
# entao converte mais facil e alimenta o funil dos outros grupos.
G_DIAGNOSTICO = g(
    "Diagnóstico e Consultoria Técnica", PAG_DIAGNOSTICO, "4.50", "diagnostico", "tecnico",
    [
        "diagnóstico técnico de equipamento eletrônico",
        "análise de falha em placa eletrônica",
        "análise de falha em equipamento eletrônico",
        "consultoria em eletrônica",
        "consultoria em hardware eletrônico",
        "consultoria em sistemas embarcados",
        "revisão de projeto eletrônico",
        "análise de projeto eletrônico",
        "laudo técnico de equipamento eletrônico",
        "problema de ruído em placa eletrônica",
        "falha intermitente em equipamento eletrônico",
        "empresa de consultoria em eletrônica",
    ],
    [
        "Diagnóstico Técnico",
        "Análise de Falha em Placa",
        "Seu Equipamento Falha?",
        "Achamos a Causa da Falha",
        "Revisão de Projeto Eletrônico",
        "Consultoria em Eletrônica",
    ],
    [
        "Analisamos hardware, firmware, comunicação e layout para achar a causa da falha.",
        "Você recebe a estimativa de horas e as causas prováveis antes de contratar.",
    ],
)

# ===================================================== C2: industria conectada
# O que a industria de porte procura quando quer enxergar ou modernizar o que ja
# tem instalado. E o bloco com maior potencial de lead, porque a dor e imediata:
# maquina parada, dado que nao existe, peca que saiu de linha.

G_MONITOR = g(
    "Monitoramento Remoto e Telemetria", PAG_MONITOR, "5.50", "monitoramento", "remoto",
    [
        "monitoramento remoto de equipamentos",
        "sistema de monitoramento remoto",
        "monitoramento remoto industrial",
        "telemetria de equipamentos",
        "telemetria industrial",
        "empresa de telemetria industrial",
        "sistema de telemetria sob medida",
        "monitoramento de máquinas em tempo real",
        "monitoramento de ativos industriais",
        "alerta de falha em equipamento",
        "monitoramento remoto de motores",
        "monitoramento de temperatura remoto industrial",
        "reduzir parada de máquina",
    ],
    [
        "Monitoramento Remoto",
        "Telemetria de Equipamentos",
        "Alertas em Tempo Real",
        "Menos Visita Técnica",
        "Do Sensor ao Dashboard",
        "Acompanhe de Onde Estiver",
    ],
    [
        "Conectamos equipamentos para enviar dados, gerar alertas e receber comandos.",
        "Temperatura, tensão, consumo e alarmes em tempo real, de onde você estiver.",
    ],
)

G_IOT = g(
    "IoT Industrial", PAG_MONITOR, "4.50", "iot", "industrial",
    [
        "soluções iot industrial",
        "empresa de iot",
        "empresa de iot industrial",
        "desenvolvimento iot",
        "desenvolvimento de solução iot",
        "projeto de iot para indústria",
        "sensores iot industriais",
        "gateway iot industrial",
        "rede de sensores conectados",
    ],
    [
        "IoT Industrial Sob Medida",
        "Soluções de IoT Industrial",
        "Empresa de IoT no Brasil",
        "Sensores e Gateway IoT",
        "Do Sensor à Nuvem",
        "Projeto de IoT Sob Medida",
    ],
    [
        "Rede de sensores, gateway e nuvem desenvolvidos para a sua operação industrial.",
        "MQTT, Modbus, Wi-Fi e 4G integrados pela mesma equipe que faz a eletrônica.",
    ],
    exatas=["iot industrial"],
)

# Grupo novo, e provavelmente o melhor da conta. E a traducao honesta de
# "indústria 4.0": o gerente industrial nao compra conceito, compra o numero que
# ele hoje nao consegue medir. As negativas deste grupo sao criticas, porque
# "coleta de dados" tambem e o termo da metodologia de pesquisa academica.
G_COLETA = g(
    "Coleta de Dados e Produção", PAG_COLETA, "5.50", "coleta", "dados",
    [
        "coleta de dados de máquinas",
        "coleta de dados chão de fábrica",
        "coleta automática de dados de produção",
        "sistema de coleta de dados industrial",
        "monitoramento de produção industrial",
        "sistema de monitoramento de produção",
        "monitoramento de chão de fábrica",
        "apontamento de produção automático",
        "sistema de apontamento de produção",
        "sistema de oee",
        "monitoramento de oee",
        "indicador de oee industrial",
        "monitoramento de parada de máquina",
        "conectar máquina antiga à rede",
        "integração de máquinas com sistema",
        "digitalização do chão de fábrica",
    ],
    [
        "Coleta de Dados de Máquina",
        "Monitorar a Produção",
        "OEE e Parada de Máquina",
        "Conecte a Máquina Antiga",
        "Dados do Chão de Fábrica",
        "Apontamento Automático",
    ],
    [
        "Contagem de peças, tempo e motivo de parada e OEE em painel de tempo real.",
        "Conectamos até a máquina antiga, sem CLP e sem saída de dados na origem.",
    ],
)

G_PREDITIVA = g(
    "Manutenção Preditiva", PAG_MONITOR, "4.50", "manutencao", "preditiva",
    [
        "manutenção preditiva industrial",
        "sistema de manutenção preditiva",
        "manutenção preditiva com iot",
        "manutenção industrial com sensores",
        "monitoramento de manutenção industrial",
        "sensor de vibração para manutenção preditiva",
        "monitoramento de vibração de motores",
    ],
    [
        "Manutenção Preditiva",
        "Preveja a Parada de Máquina",
        "Sensores Para Preditiva",
        "Reduza Parada Não Prevista",
        "Monitoramento de Ativos",
        "Alerta Antes da Quebra",
    ],
    [
        "Sensores e telemetria que avisam antes de a máquina parar no meio do turno.",
        "Monitoramento de ativos industriais com alerta no celular de quem precisa agir.",
    ],
)

# Grupo novo. Dor imediata e orcamento aprovado com facilidade, porque a
# alternativa e comprar maquina nova. Atencao total as negativas: no Brasil,
# "retrofit" sozinho significa reforma de fachada de predio na maioria das buscas.
G_RETROFIT = g(
    "Retrofit e Modernização de Máquinas", PAG_RETROFIT, "5.50", "retrofit", "maquinas",
    [
        "retrofit de máquinas",
        "retrofit de máquinas industriais",
        "retrofit de equipamento industrial",
        "retrofit industrial",
        "empresa de retrofit de máquinas",
        "modernização de máquinas industriais",
        "modernização de equipamentos industriais",
        "modernização de linha de produção",
        "automatizar máquina antiga",
        "atualizar máquina antiga",
        "troca de comando de máquina",
        "eletrônica nova para máquina antiga",
    ],
    [
        "Retrofit de Máquinas",
        "Modernização de Máquinas",
        "Comando Novo, Máquina Sua",
        "Peça de Reposição Acabou?",
        "Automatize a Máquina Antiga",
        "Eletrônica e Firmware Novos",
    ],
    [
        "Trocamos a eletrônica de comando e o firmware, mantendo a mecânica que funciona.",
        "A máquina volta a produzir e passa a conversar com a rede da sua fábrica.",
    ],
)

# Grupo novo. A empresa vende aplicativo e dashboard desde sempre e a campanha
# anterior nao tinha uma unica palavra-chave para isso.
G_APP = g(
    "Aplicativos e Dashboards", PAG_APP, "4.50", "aplicativo", "equipamento",
    [
        "aplicativo para controlar equipamento",
        "aplicativo para monitorar equipamento",
        "desenvolvimento de aplicativo para equipamento",
        "aplicativo conectado a equipamento",
        "app para equipamento industrial",
        "aplicativo bluetooth para equipamento",
        "dashboard industrial",
        "dashboard de monitoramento industrial",
        "desenvolvimento de dashboard industrial",
        "software de monitoramento de equipamentos",
        "sistema de monitoramento de equipamentos",
    ],
    [
        "Aplicativo Para Equipamento",
        "Controle Pelo Celular",
        "Dashboard de Equipamentos",
        "App Conectado ao Firmware",
        "Configure Sem Ir Até Lá",
        "Gráficos em Tempo Real",
    ],
    [
        "Aplicativo e painel desenvolvidos junto com o firmware que roda no equipamento.",
        "Configure, acompanhe e controle o equipamento pelo celular, de qualquer lugar.",
    ],
)

# Grupo novo, e o unico da conta com prova visual pronta: o trator e o implemento
# de escovas em usina fotovoltaica sao projeto da casa.
G_CAMPO = g(
    "Telemetria Agrícola e Solar", PAG_CAMPO, "5.00", "telemetria", "campo",
    [
        "telemetria de máquinas agrícolas",
        "telemetria agrícola",
        "monitoramento de máquinas agrícolas",
        "automação de implementos agrícolas",
        "eletrônica embarcada agrícola",
        "monitoramento de usina fotovoltaica",
        "telemetria de usina solar",
        "automação para usina fotovoltaica",
    ],
    [
        "Telemetria Para o Campo",
        "Máquinas Agrícolas Online",
        "Automação de Implementos",
        "Monitorar Usina Solar",
        "Eletrônica Que Aguenta",
        "Vibração, Poeira e Sol",
    ],
    [
        "Automação embarcada em trator e implemento, validada em usina fotovoltaica.",
        "Eletrônica projetada para vibração, poeira e alimentação oscilando no campo.",
    ],
)

# ================================================================ C3: amplos
# Volume alto, intencao pior, leilao disputado por integrador de CLP e por
# consultoria de gestao. Ficam aqui com orcamento e teto proprios, para poderem
# ser pausados sozinhos sem mexer no resto da conta.

G_AUTOMACAO = g(
    "Automação Industrial", PAG_AUTOMACAO, "3.50", "automacao", "industrial",
    [
        "empresa de automação industrial",
        "automação industrial sob medida",
        "automação industrial personalizada",
        "projeto de automação industrial",
        "serviços de automação industrial",
        "integrador de automação industrial",
        "empresa de automação industrial em ribeirão preto",
        "automação de máquinas",
        "automação de processos industriais",
        "automação de equipamentos",
        "sistema de controle de máquinas",
        "sistema de controle eletrônico",
        "controle de motores e bombas",
    ],
    [
        "Automação Industrial",
        "Automação Sob Medida",
        "Empresa de Automação",
        "Menos Intervenção Manual",
        "Eletrônica e Firmware Juntos",
        "Automação Para Sua Operação",
    ],
    [
        "Automação desenvolvida sobre o seu processo, não adaptada de um pacote pronto.",
        "Eletrônica, firmware e comunicação pela mesma equipe. Peça uma avaliação.",
    ],
    exatas=["automação industrial"],
)

# Aponta para a pagina de coleta de dados, nao para a de automacao. Quem procura
# "indústria 4.0" e vai comprar alguma coisa quer o dado da maquina. Mandar essa
# busca para uma pagina de automacao generica e o que fazia o termo nao converter.
G_INDUSTRIA40 = g(
    "Indústria 4.0", PAG_COLETA, "3.00", "industria", "4-0",
    [
        "soluções indústria 4.0",
        "indústria 4.0 para empresas",
        "projeto indústria 4.0",
        "empresa de indústria 4.0",
        "digitalização da indústria",
        "transformação digital industrial",
    ],
    [
        "Indústria 4.0 na Prática",
        "Digitalize o Chão de Fábrica",
        "Indústria 4.0 Sob Medida",
        "Comece Pelo Dado da Máquina",
        "Transformação Digital",
        "Projeto de Indústria 4.0",
    ],
    [
        "Indústria 4.0 começa quando a máquina passa a informar o que está fazendo.",
        "Coleta de dados, painel e alerta implantados sobre as máquinas que você já tem.",
    ],
    exatas=["indústria 4.0"],
)

# A unica valvula de volume da conta. Correspondencia ampla em oito termos
# centrais, teto baixo e dentro da campanha de R$ 15, entao o pior caso e perder
# R$ 15 num dia. Existe para descobrir, no relatorio de termos de pesquisa, que
# buscas reais o mercado faz e que ninguem previu. O que aparecer de bom vira
# palavra-chave em frase num dos grupos qualificados; o resto vira negativa.
G_AMPLA = g(
    "Descoberta Ampla", SITE + "/", "3.00", "engenharia", "sob-medida",
    [],
    [
        "Engenharia Sob Medida",
        "Hardware, Firmware e App",
        "Projeto Técnico Sob Medida",
        "Um Só Time de Engenharia",
        "Empresa de Engenharia",
        "Tecnologia Para Indústria",
    ],
    [
        "Hardware, firmware, software e aplicativo desenvolvidos pela mesma equipe.",
        "Projetos empresariais e industriais sob medida, atendidos em todo o Brasil.",
    ],
    amplas=[
        "desenvolvimento de produtos eletrônicos",
        "desenvolvimento de firmware",
        "empresa de engenharia eletrônica",
        "monitoramento remoto de equipamentos",
        "coleta de dados de máquinas",
        "retrofit de máquinas industriais",
        "telemetria industrial",
    ],
)


# Grupo novo, e o de melhor encaixe com o pedido de projeto grande. E o
# vocabulario que o gerente de engenharia de uma industria usa quando precisa de
# time e nao tem. Volume baixo, ticket alto, quase nenhum concorrente disputando.
G_TERCEIRIZACAO = g(
    "Terceirização de Engenharia", PAG_TERCEIRIZACAO, "5.50", "engenharia", "terceirizada",
    [
        "terceirização de engenharia eletrônica",
        "terceirização de engenharia",
        "engenharia eletrônica terceirizada",
        "empresa de engenharia terceirizada",
        "outsourcing de engenharia eletrônica",
        "outsourcing de engenharia",
        "empresa de engenharia eletrônica",
        "design house eletrônica",
        "design house de eletrônica",
        "parceiro de engenharia eletrônica",
        "braço de engenharia eletrônica",
        "empresa de p&d eletrônica",
        "terceirização de p&d",
        "desenvolvimento eletrônico terceirizado",
        "terceirização de desenvolvimento eletrônico",
    ],
    [
        "Engenharia Terceirizada",
        "Design House de Eletrônica",
        "Braço Técnico de Engenharia",
        "Time de Engenharia Sob Escopo",
        "Seu Projeto Sai da Fila",
        "Sem Custo Fixo de Equipe",
    ],
    [
        "Você contrata a engenharia que o escopo exige, não a folha de um time parado.",
        "Hardware, firmware, PCB e aplicativo pela mesma equipe, com um só responsável.",
    ],
)


CAMPANHAS = [
    {
        "nome": "TQ | Pesquisa | Projetos de Engenharia",
        "orcamento": "45.00",
        "grupos": [G_PRODUTOS, G_PCB, G_FIRMWARE, G_TERCEIRIZACAO, G_DIAGNOSTICO],
    },
    {
        "nome": "TQ | Pesquisa | Indústria Conectada",
        "orcamento": "40.00",
        "grupos": [G_MONITOR, G_IOT, G_COLETA, G_PREDITIVA, G_RETROFIT, G_APP, G_CAMPO],
    },
    {
        "nome": "TQ | Pesquisa | Termos Amplos",
        "orcamento": "15.00",
        "grupos": [G_AUTOMACAO, G_INDUSTRIA40, G_AMPLA],
    },
]


# ------------------------------------------------------- negativas por grupo
# Lixo especifico de cada tema. As negativas cruzadas entre grupos irmaos o
# `gera` monta sozinho, para uma busca nao cair no grupo do vizinho.
NEGATIVAS = {
    "Produtos Eletrônicos e Hardware": [
        "loja de eletrônicos", "conserto de eletrônicos", "revenda de eletrônicos",
        "importar eletrônicos", "hardware de computador", "loja de hardware",
        "hardware gamer", "manutenção de computador", "placa mãe", "montagem de pc",
        "hardware de servidor", "peças de computador",
    ],
    "Projeto de PCB": [
        "comprar pcb", "fábrica de pcb", "fabricação de pcb", "montagem de pcb",
        "pcb china", "placa universal", "pcb way", "jlcpcb", "pcb preço",
        "placa de fenolite", "placa perfurada",
    ],
    "Firmware e Embarcados": [
        "atualizar firmware", "firmware do celular", "firmware da tv",
        "firmware da impressora", "baixar firmware", "flash firmware",
        "firmware box android", "firmware original", "firmware do roteador",
        "firmware receptor", "comprar esp32", "esp32 preço", "esp32 datasheet",
        "esp32 pinagem", "esp32 pinout",
    ],
    # Terceirizacao atrai quem procura emprego e quem vende mao de obra. As
    # negativas globais ja cortam vaga e salario, aqui vai o resto.
    "Terceirização de Engenharia": [
        "terceirização de mão de obra", "empresa de terceirização de serviços",
        "terceirização de limpeza", "terceirização de rh", "terceirização de ti",
        "terceirização de folha", "cooperativa de trabalho", "pj ou clt",
        "body shop", "alocação de profissionais", "engenharia civil",
        "engenharia de segurança", "art engenheiro", "crea",
    ],
    "Diagnóstico e Consultoria Técnica": [
        "diagnóstico automotivo", "scanner automotivo", "conserto de placa de tv",
        "conserto de fonte", "conserto de placa de máquina de lavar",
        "consultoria empresarial", "consultoria financeira", "consultoria de marketing",
        "consultoria de rh", "consultoria contábil", "laudo de instalação elétrica",
        "laudo spda", "art de instalação", "diagnóstico organizacional",
    ],
    "Monitoramento Remoto e Telemetria": [
        "rastreador veicular", "rastreamento de veículos", "rastreamento de frota",
        "monitoramento de veículos", "monitoramento de rede",
        "câmera de monitoramento", "monitoramento de alarme residencial",
        "monitoramento de servidores", "monitoramento de redes sociais",
        "monitoramento de ponto eletrônico",
    ],
    "IoT Industrial": [
        "módulo iot preço", "comprar sensor", "chip iot operadora",
        "plano de dados iot", "iot barato", "kit iot",
    ],
    # "coleta de dados" e, no Google, principalmente termo de metodologia de
    # pesquisa academica. Sem esta lista o grupo traria estudante de TCC.
    "Coleta de Dados e Produção": [
        "coleta seletiva", "coleta de lixo", "coleta de dados pesquisa",
        "coleta de dados qualitativa", "coleta de dados quantitativa",
        "metodologia de coleta de dados", "instrumento de coleta de dados",
        "técnicas de coleta de dados", "coleta de dados tcc", "formulário de coleta",
        "coleta de dados no excel", "planilha de oee", "oee excel",
        "como calcular oee", "fórmula do oee", "oee o que é",
        "coleta de dados lgpd", "web scraping",
    ],
    "Manutenção Preditiva": [
        "manutenção predial", "manutenção mecânica terceirizada",
        "empresa de manutenção elétrica predial", "plano de manutenção modelo",
        "tipos de manutenção", "manutenção corretiva e preventiva",
        "manutenção autônoma", "tpm manutenção",
    ],
    # No Brasil, "retrofit" sem qualificador e quase sempre reforma de predio.
    # Esta e a lista que decide se o grupo funciona ou queima verba.
    "Retrofit e Modernização de Máquinas": [
        "retrofit de fachada", "retrofit predial", "retrofit de edifício",
        "retrofit de elevador", "retrofit arquitetura", "retrofit de imóvel",
        "retrofit residencial", "retrofit hoteleiro", "retrofit automotivo",
        "retrofit de ar condicionado", "retrofit de iluminação",
        "retrofit led", "retrofit o que é", "máquina usada", "aluguel de máquina",
        "peças de máquina",
    ],
    "Aplicativos e Dashboards": [
        "aplicativo de delivery", "criar app grátis", "loja de aplicativos",
        "aplicativo de banco", "app de mensagens", "quanto custa um aplicativo",
        "aplicativo de vendas", "criar aplicativo sem programar",
        "fábrica de software", "dashboard excel", "power bi",
        "template de dashboard", "looker studio", "aplicativo de namoro",
        "aplicativo de treino",
    ],
    "Telemetria Agrícola e Solar": [
        "rastreador agrícola", "energia solar residencial",
        "instalação de placa solar", "kit de energia solar",
        "orçamento de energia solar", "financiamento de energia solar",
        "placa solar preço", "gerador solar", "limpeza de placa solar preço",
        "curso de energia solar", "telemetria f1", "telemetria de corrida",
        "máquina agrícola usada", "trator preço",
    ],
    "Automação Industrial": [
        "automação residencial", "automação predial", "automação comercial pdv",
        "comprar clp", "clp preço", "curso de clp", "programação de clp",
        "montagem de painel elétrico", "quadro de comando preço",
        "robô industrial preço", "célula robotizada", "esteira transportadora",
        "supervisório scada", "siemens", "rockwell", "allen bradley",
        "schneider", "weg", "delta clp",
    ],
    "Indústria 4.0": [
        "artigo indústria 4.0", "livro indústria 4.0", "história da indústria",
        "quarta revolução industrial", "pilares da indústria 4.0",
        "indústria 4.0 resumo", "indústria 5.0", "indústria 4.0 o que é",
    ],
    "Descoberta Ampla": [
        "loja", "conserto", "aluguel", "revenda", "usado", "preço de",
        "quanto custa", "onde comprar",
    ],
}

# Negativas globais adicionais, para valer na conta inteira. Elas nao existiam
# na lista anterior e cobrem buracos que os temas novos abriram.
NOVAS_GLOBAIS = [
    "coleta seletiva", "coleta de lixo", "reclame aqui", "cnpj", "razão social",
    "telefone da", "endereço da", "horário de funcionamento", "franquia",
    "abrir empresa", "norma", "nbr", "abnt", "iso 9001",
    "importar da china", "alibaba", "sindicato", "cbo", "modelo de contrato",
    "modelo de proposta", "modelo de laudo", "github", "open source",
    "código fonte", "quem inventou", "linha do tempo", "trabalho pronto",
]


def keywords_amplas(campanhas):
    """Anexa a correspondencia ampla ao arquivo de palavras-chave.

    A funcao `gera` do `gerar_ads.py` so escreve frase e exata, de proposito.
    A ampla entra so aqui, no unico grupo que a usa, para ficar evidente no
    codigo que ela e excecao e nao regra.
    """
    linhas = []
    for c in campanhas:
        for grupo in c["grupos"]:
            for k in grupo.get("kw_amplas", []):
                linhas.append([c["nome"], grupo["nome"], k, "Broad", grupo["cpc"], "Enabled"])
    if not linhas:
        return 0
    caminho = os.path.join(OUT, "3-keywords.csv")
    with io.open(caminho, "a", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL).writerows(linhas)
    return len(linhas)


def horarios(campanhas):
    """Troca o CSV de programacao de anuncios por uma instrucao escrita.

    Duas tentativas de importar a programacao pelo Editor em portugues falharam.
    Com as cinco colunas (`Campaign, Day of Week, Start Time, End Time, Bid
    Adjustment`) ele tratou cada linha como linha de campanha e recusou o `0%` no
    campo de ajuste de lance de dispositivos moveis. Sem a coluna de ajuste, ele
    parou de acusar erro mas ignorou as 15 linhas do mesmo jeito: reconheceu so a
    coluna `Campaign` e nao encontrou nada para alterar.

    Ou seja, esta versao do Editor nao aceita programacao de anuncios por CSV.
    Manter um arquivo que nunca importa so faz a proxima pessoa perder tempo,
    entao o passo vira instrucao. Sao tres campanhas, um cadastro em cada.
    """
    for velho in ("10-horarios.csv", "10-horarios-FAZER-NA-MAO.txt"):
        caminho_velho = os.path.join(OUT, velho)
        if os.path.exists(caminho_velho):
            os.remove(caminho_velho)

    texto = [
        "PROGRAMACAO DE ANUNCIOS: cadastrar na mao, nao existe CSV que funcione",
        "=" * 70,
        "",
        "O Google Ads Editor em portugues ignora a programacao de anuncios vinda",
        "de CSV. Foram duas tentativas, as duas recusadas. Faca pela interface.",
        "",
        "No Google Ads Editor, para cada uma das tres campanhas:",
        "",
        "  1. Selecione a campanha na arvore da esquerda.",
        "  2. Painel de tipos > Palavras-chave e segmentacao > Programacao de anuncios.",
        "  3. Adicionar programacao de anuncios.",
        "  4. Segunda a sexta, das 08:00 as 18:00, ajuste de lance em branco.",
        "",
        "As campanhas:",
        "",
    ]
    for c in campanhas:
        texto.append("  - " + c["nome"])
    texto += [
        "",
        "POR QUE 8h AS 18h, DE SEGUNDA A SEXTA",
        "",
        "Gerente de engenharia e de manutencao pesquisa fornecedor no expediente.",
        "Fora dele sobra curioso, e o clique custa igual. Concentrar a verba em 50",
        "horas por semana em vez de 168 multiplica a presenca nos leiloes que",
        "importam, sem aumentar o orcamento.",
        "",
        "Nao e obrigatorio para subir a campanha. Sem programacao ela roda 24 por 7,",
        "o que nao quebra nada, so espalha a verba por horario pior. Da para deixar",
        "para depois da primeira semana e decidir com o relatorio de horario na mao.",
        "",
    ]
    caminho = os.path.join(BASE, "PASSO-EXTRA-programacao-de-horario.txt")
    io.open(caminho, "w", encoding="utf-8", newline="").write("\n".join(texto))
    print("  PASSO-EXTRA-programacao-de-horario.txt: fora da pasta import")


def limpa_pasta_import():
    """Deixa na pasta `import` somente arquivo que o Editor aceita importar.

    O `negativas-lista-global.txt` nao e um CSV: sao os termos entre aspas para
    colar na interface web. Dentro de uma pasta chamada `import`, ao lado de onze
    CSVs, ele parece a decima segunda importacao. Quem selecionar ele leva um erro
    de "Cabecalho CSV nao informado" e perde tempo procurando defeito onde nao ha.

    A regra passa a ser simples: tudo que esta em `import` se importa, na ordem do
    numero. O que precisa de outro tratamento fica um nivel acima, com nome que diz
    o que fazer.
    """
    origem = os.path.join(OUT, "negativas-lista-global.txt")
    destino = os.path.join(BASE, "PASSO-EXTRA-negativas-para-colar-na-web.txt")
    if os.path.exists(origem):
        conteudo = io.open(origem, encoding="utf-8").read()
        io.open(destino, "w", encoding="utf-8", newline="").write(conteudo)
        os.remove(origem)
        print("  PASSO-EXTRA-negativas-para-colar-na-web.txt: fora da pasta import")


def main():
    ga.NEG_POR_GRUPO.update(NEGATIVAS)
    for n in NOVAS_GLOBAIS:
        if n not in ga.NEG_FRASE:
            ga.NEG_FRASE.append(n)

    # Sitelinks e destaques atualizados: as paginas novas precisam aparecer.
    ga.SITELINKS[:] = [
        ("Produtos eletrônicos", "Da ideia ao produto real", "Hardware, firmware e PCB",
         PAG_PRODUTOS),
        ("Firmware e embarcados", "ESP32, MQTT, Modbus e CAN", "Firmware que aguenta o campo",
         PAG_FIRMWARE),
        ("Monitoramento e IoT", "Dados e alertas em tempo real", "Acompanhe de onde estiver",
         PAG_MONITOR),
        ("Coleta de dados", "Produção, parada e OEE", "Do sensor ao painel", PAG_COLETA),
        ("Retrofit de máquinas", "Comando novo na máquina sua", "Sem trocar a mecânica",
         PAG_RETROFIT),
        ("Diagnóstico técnico", "Achamos a causa da falha", "Estimativa antes de contratar",
         PAG_DIAGNOSTICO),
        ("Engenharia terceirizada", "Time dimensionado por escopo", "Sem custo fixo de equipe",
         PAG_TERCEIRIZACAO),
        ("Projeto de PCB", "Layout, ruído e fabricação", "Também revisamos a sua placa",
         PAG_PCB),
        ("Agrícola e usinas solares", "Eletrônica que aguenta campo", "Vibração, poeira e sol",
         PAG_CAMPO),
        ("Falar com especialista", "Primeira conversa sem custo", "Retorno pela sua preferência",
         SITE + "/#contato"),
    ]
    ga.CALLOUTS[:] = [
        "Engenharia desde 2001",
        "45+ equipamentos online",
        "Do circuito ao aplicativo",
        "Atendemos todo o Brasil",
        "Escopo e prazo fechados",
        "Um só interlocutor",
        "Projetos de grande porte",
        "Conversa inicial gratuita",
    ]
    ga.SNIPPET2_VALORES[:] = [
        "Monitoramento remoto", "Retrofit de máquinas", "Coleta de dados",
        "IoT industrial", "Aplicativos", "Produtos eletrônicos",
    ]

    ga.gera(CAMPANHAS, OUT)
    n = keywords_amplas(CAMPANHAS)
    horarios(CAMPANHAS)
    limpa_pasta_import()
    print("  3-keywords.csv: +%d em correspondência ampla" % n)

    termos = sum(len(g["kw"]) + len(g["kw_exatas"]) + len(g["kw_amplas"])
                 for c in CAMPANHAS for g in c["grupos"])
    grupos = sum(len(c["grupos"]) for c in CAMPANHAS)
    verba = sum(float(c["orcamento"]) for c in CAMPANHAS)
    print("\n%d campanhas, %d grupos, %d termos, R$ %.2f por dia"
          % (len(CAMPANHAS), grupos, termos, verba))

    if ga.erros:
        print("\n*** LIMITES ESTOURADOS ***")
        for e in ga.erros:
            print("  " + e)
        sys.exit(1)
    print("OK: nenhum limite de caracteres estourado.")


if __name__ == "__main__":
    main()
