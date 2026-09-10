# -*- coding: utf-8 -*-
"""Gera os CSVs de importacao do Google Ads Editor para a Taquionica."""
import csv, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "import")
SITE = "https://taquionica.com.br"
os.makedirs(OUT, exist_ok=True)

erros = []


def lim(valor, maximo, rotulo):
    if len(valor) > maximo:
        erros.append("%s: %d/%d -> %s" % (rotulo, len(valor), maximo, valor))
    return valor


TITULOS_COMUNS = [
    "Engenharia desde 2001",
    "Do circuito ao aplicativo",
    "45+ equipamentos online",
    "Um só time, um só contato",
    "Atendemos todo o Brasil",
    "Escopo e prazo fechados",
    "Fale com um especialista",
    "Projeto sob medida",
    "Primeira conversa sem custo",
]

DESC_COMUNS = [
    "Hardware, firmware, software e aplicativo desenvolvidos pela mesma equipe.",
    "Mais de 45 equipamentos em operação contínua há mais de seis anos. Fale conosco.",
]

NEG_FRASE = [
    # ---------------------------------------------------------- estudo e ensino
    # O maior volume de busca do nicho vem de quem esta estudando, nao contratando.
    "curso", "cursos", "aula", "aulas", "apostila", "apostilas", "tutorial",
    "treinamento", "capacitacao", "capacitação", "workshop", "palestra",
    "ebook", "e-book", "slide", "slides", "aprender", "aprenda", "estudar",
    "exercicios", "exercícios", "simulado", "resumo", "artigo",
    # "prova" fica de fora: bloquearia "prova de conceito", que e busca de comprador.
    "artigos", "tcc", "monografia", "dissertação", "tese", "mestrado",
    "doutorado", "graduação", "pos graduação", "pós graduação", "faculdade",
    "universidade", "senai", "senac", "sesi", "etec", "fatec", "ifsp",
    "curso tecnico", "curso técnico", "tecnico em", "técnico em", "bolsa",
    "matricula", "matrícula", "ead", "certificado", "certificação profissional",
    "livro", "material didatico", "material didático", "trabalho escolar",
    "feira de ciencias", "feira de ciências", "projeto escolar", "escolar",
    "estudante", "aluno", "professor", "sala de aula",

    # ------------------------------------------------------------------ emprego
    "emprego", "empregos", "vaga", "vagas", "salario", "salário",
    "quanto ganha", "piso salarial", "clt", "estagio", "estágio",
    "estagiario", "estagiário", "trainee", "curriculo", "currículo",
    "recrutamento", "contrata-se", "indeed", "catho", "gupy", "infojobs",
    "concurso", "carreira", "profissao", "profissão", "mercado de trabalho",

    # ---------------------------------------------------------- hobby e amador
    "arduino", "raspberry", "hobby", "faça você mesmo", "faca voce mesmo",
    "diy", "como fazer", "como montar", "como criar", "passo a passo",
    "iniciante", "iniciantes", "para iniciantes", "caseiro", "em casa",
    "gambiarra", "maker", "tinkercad", "fritzing", "proteus", "multisim",
    "simulador", "simulação online",

    # ------------------------------------------------------- gratuito e download
    "download", "baixar", "gratis", "grátis", "gratuito", "de graça", "free",
    "torrent", "crack", "pdf", "ppt", "planilha", "template", "modelo pronto",

    # ------------------------------------------------------- busca informacional
    "o que é", "o que sao", "o que são", "significado", "conceito", "definição",
    "para que serve", "tipos de", "exemplos de", "exemplo de", "historia",
    "história", "wikipedia", "quais sao", "quais são", "como funciona",
    "vantagens e desvantagens", "caracteristicas", "características", "pilares",
    "diferença entre", "resumo sobre", "introdução",

    # ------------------------------------------------------------ varejo e peças
    "comprar", "venda de", "loja", "lojas", "mercado livre", "olx", "shopee",
    "aliexpress", "amazon", "usado", "seminovo", "revenda", "atacado",
    "distribuidor", "fornecedor de componentes", "componentes eletronicos preço",
    "kit", "datasheet", "esquema eletrico", "esquema elétrico",
    "manual de instruções", "pinagem", "catalogo", "catálogo",

    # -------------------------------------------- servicos que a empresa nao faz
    "conserto", "consertar", "assistencia tecnica",
    # "reparo" fica de fora: bloquearia "reparo de placa industrial".
    "assistência técnica", "manutencao de celular", "manutenção de celular",
    "conserto de celular", "conserto de notebook", "conserto de computador",
    "conserto de tv", "conserto de geladeira", "maquina de lavar",
    "máquina de lavar", "ar condicionado", "elevador", "eletrodomestico",
    "eletrodoméstico", "residencial", "domestica", "doméstica", "domotica",
    "domótica", "automação residencial", "casa inteligente", "portão eletrônico",
    "portao eletronico", "cerca eletrica", "cerca elétrica", "cftv",
    "camera de seguranca", "câmera de segurança", "alarme residencial",
    "interfone", "instalação elétrica", "eletricista", "energia solar residencial",
    "instalação de painel solar", "placa solar preço",

    # --------------------------------------------- software fora do escopo dele
    "criação de site", "criacao de site", "loja virtual", "e-commerce",
    "aplicativo de delivery", "jogo", "game", "marketing digital",
    "trafego pago", "tráfego pago", "seo", "social media", "erp",
    "sistema de vendas", "software contabil", "software contábil",
    "power bi", "excel",

    # ------------------------------------------------- consultoria fora do nicho
    "consultoria empresarial", "consultoria financeira", "consultoria de rh",
    "consultoria de marketing", "consultoria contabil", "consultoria contábil",

    # -------------------------------------------------- pessoa fisica e freelance
    "freelancer", "freela", "autonomo", "autônomo", "profissional autonomo",
    "pessoa fisica", "pessoa física",

    # ------------------------------------------------------ fora do Brasil e ONGs
    "portugal", "angola", "moçambique", "mocambique",
]

CAMPANHAS = [
    {
        "nome": "TQ | Pesquisa | Hardware e PCB",
        "orcamento": "30.00",
        "grupos": [
            {
                "nome": "Desenvolvimento de Hardware",
                "url": SITE + "/desenvolvimento-hardware",
                "cpc": "6.00",
                "p1": "hardware", "p2": "sob-medida",
                "kw": [
                    "desenvolvimento de hardware",
                    "empresa de desenvolvimento de hardware",
                    "projeto de hardware eletrônico",
                    "desenvolvimento de hardware sob medida",
                    "projeto de circuito eletrônico",
                    "engenharia eletrônica sob demanda",
                    "desenvolvimento de eletrônica embarcada",
                    "projeto eletrônico industrial",
                ],
                "titulos": [
                    "Desenvolvimento de Hardware",
                    "Hardware Eletrônico Sob Medida",
                    "Projeto de Circuito Completo",
                    "Da Bancada Para o Campo",
                    "Eletrônica Que Aguenta Campo",
                    "Empresa de Hardware no Brasil",
                ],
                "descs": [
                    "Projetamos circuitos, sensores, interfaces e comunicação para operar no mundo real.",
                    "Hardware validado em campo, com vibração, poeira e alimentação oscilando.",
                ],
            },
            {
                "nome": "Projeto de PCB",
                "url": SITE + "/desenvolvimento-pcb",
                "cpc": "6.00",
                "p1": "pcb", "p2": "layout",
                "kw": [
                    "desenvolvimento de pcb",
                    "projeto de pcb",
                    "layout de pcb",
                    "projeto de placa eletrônica",
                    "desenvolvimento de placa de circuito impresso",
                    "revisão de projeto de pcb",
                    "empresa de projeto de pcb",
                    "design de placa eletrônica",
                ],
                "titulos": [
                    "Projeto e Layout de PCB",
                    "Desenvolvimento de PCB",
                    "Revisão da Sua Placa",
                    "PCB Pronta Para Fabricar",
                    "Menos Ruído na Sua Placa",
                    "Placa Eletrônica Sob Medida",
                ],
                "descs": [
                    "Layout, organização de sinais, redução de ruído e preparação para fabricação.",
                    "Revisamos placas que falham em campo e indicamos o caminho para corrigir.",
                ],
            },
            {
                "nome": "Produtos Eletrônicos",
                "url": SITE + "/desenvolvimento-produtos-eletronicos",
                "cpc": "6.00",
                "p1": "produtos", "p2": "eletronicos",
                "kw": [
                    "desenvolvimento de produtos eletrônicos",
                    "empresa de desenvolvimento de produtos eletrônicos",
                    "desenvolvimento de protótipo eletrônico",
                    "protótipo eletrônico funcional",
                    "criar produto eletrônico",
                    "engenharia de produto eletrônico",
                    "transformar ideia em produto eletrônico",
                ],
                "titulos": [
                    "Produtos Eletrônicos",
                    "Da Ideia ao Produto Real",
                    "Protótipo Funcional",
                    "Tire o Projeto do Papel",
                    "Engenharia de Produto",
                    "Hardware, Firmware e PCB",
                ],
                "descs": [
                    "Transformamos a ideia em circuito, protótipo e equipamento pronto para operar.",
                    "Protótipos funcionais para validação técnica e comercial antes da versão final.",
                ],
            },
        ],
    },
    {
        "nome": "TQ | Pesquisa | Firmware e Embarcados",
        "orcamento": "25.00",
        "grupos": [
            {
                "nome": "Firmware Embarcado",
                "url": SITE + "/desenvolvimento-firmware",
                "cpc": "6.00",
                "p1": "firmware", "p2": "embarcado",
                "kw": [
                    "desenvolvimento de firmware",
                    "empresa de desenvolvimento de firmware",
                    "programação de firmware",
                    "desenvolvimento de sistemas embarcados",
                    "firmware para microcontrolador",
                    "desenvolvimento de software embarcado",
                    "empresa de sistemas embarcados",
                ],
                "titulos": [
                    "Desenvolvimento de Firmware",
                    "Firmware Para Embarcados",
                    "Firmware Que Não Trava",
                    "Corrigimos Firmware Instável",
                    "Microcontrolador Sob Medida",
                    "Atualização Remota de Frota",
                ],
                "descs": [
                    "Programação de microcontroladores, sensores, displays, atuadores e comunicação.",
                    "Frota atualizada à distância, com novas versões sem deslocar técnico até o cliente.",
                ],
            },
            {
                "nome": "ESP32 e Protocolos",
                "url": SITE + "/desenvolvimento-firmware",
                "cpc": "5.00",
                "p1": "firmware", "p2": "esp32",
                "kw": [
                    "programação esp32",
                    "desenvolvimento com esp32",
                    "firmware esp32",
                    "desenvolvimento mqtt",
                    "integração modbus",
                    "comunicação modbus industrial",
                    "firmware com wifi e bluetooth",
                ],
                "titulos": [
                    "Firmware em ESP32",
                    "MQTT, Modbus e CAN",
                    "Wi-Fi e Bluetooth no Seu Eqp",
                    "Comunicação Estável",
                    "Integração de Protocolos",
                    "Especialistas em Embarcados",
                ],
                "descs": [
                    "ESP32, Wi-Fi, Bluetooth, MQTT, Modbus e CAN integrados ao seu equipamento.",
                    "Comunicação que se mantém estável no campo, não apenas na bancada.",
                ],
            },
        ],
    },
    {
        "nome": "TQ | Pesquisa | Automação Industrial",
        "orcamento": "35.00",
        "grupos": [
            {
                "nome": "Automação Industrial",
                "url": SITE + "/automacao-industrial",
                "cpc": "8.00",
                "p1": "automacao", "p2": "industrial",
                "kw": [
                    "empresa de automação industrial",
                    "automação industrial sob medida",
                    "projeto de automação industrial",
                    "serviços de automação industrial",
                    "automação industrial personalizada",
                    "integrador de automação industrial",
                    "empresa de automação industrial em ribeirão preto",
                ],
                "titulos": [
                    "Automação Industrial",
                    "Automação Sob Medida",
                    "Empresa de Automação",
                    "Menos Intervenção Manual",
                    "Eletrônica e Firmware Juntos",
                    "Automação Para Sua Operação",
                ],
                "descs": [
                    "Automação desenvolvida sobre o seu processo, não adaptada de um pacote pronto.",
                    "Eletrônica, firmware e comunicação pela mesma equipe. Peça uma avaliação.",
                ],
            },
            {
                "nome": "Automação de Máquinas",
                "url": SITE + "/automacao-e-controle",
                "cpc": "7.00",
                "p1": "automacao", "p2": "controle",
                "kw": [
                    "automação de máquinas",
                    "automação de processos industriais",
                    "sistema de controle de máquinas",
                    "controle de motores e bombas",
                    "automação de equipamentos",
                    "sistema de controle eletrônico",
                ],
                "titulos": [
                    "Automação e Controle",
                    "Controle de Máquinas",
                    "Motores, Bombas e Sensores",
                    "Processos Automatizados",
                    "Mais Previsibilidade",
                    "Controle Eletrônico Sob Medida",
                ],
                "descs": [
                    "Sistemas para controlar motores, bombas, sensores, relés, máquinas e processos.",
                    "Menos tarefa manual e mais previsibilidade na operação. Fale com a Taquionica.",
                ],
            },
            {
                "nome": "Indústria 4.0",
                "url": SITE + "/industria-4-0",
                "cpc": "6.00",
                "p1": "industria4-0", "p2": "projetos",
                "kw": [
                    "soluções indústria 4.0",
                    "indústria 4.0 para empresas",
                    "projeto indústria 4.0",
                    "digitalização da indústria",
                    "transformação digital industrial",
                    "empresa de indústria 4.0",
                ],
                "titulos": [
                    "Soluções Indústria 4.0",
                    "Digitalize Sua Operação",
                    "Dados Que Viram Decisão",
                    "Máquina Conectada à Nuvem",
                    "Indústria 4.0 Sob Medida",
                    "Comece Pelo Diagnóstico",
                ],
                "descs": [
                    "Automação, IoT industrial e sistemas de dados sob medida para a sua indústria.",
                    "Conectamos equipamentos e transformamos dados em decisão. Fale com a Taquionica.",
                ],
            },
        ],
    },
    {
        "nome": "TQ | Pesquisa | IoT e Monitoramento",
        "orcamento": "35.00",
        "grupos": [
            {
                "nome": "IoT Industrial",
                "url": SITE + "/iot-industrial",
                "cpc": "7.00",
                "p1": "iot", "p2": "industrial",
                "kw": [
                    "iot industrial",
                    "soluções iot industrial",
                    "empresa de iot",
                    "desenvolvimento iot",
                    "sensores iot industriais",
                    "gateway iot industrial",
                    "rede de sensores conectados",
                ],
                "titulos": [
                    "IoT Industrial Sob Medida",
                    "Sensores, Gateway e Nuvem",
                    "Conecte Seus Equipamentos",
                    "Uma Só Rede de Dados",
                    "Desenvolvimento IoT",
                    "Da Placa Até o Dashboard",
                ],
                "descs": [
                    "Sensores, gateways, comunicação e nuvem em uma única rede de dados industrial.",
                    "Toda a infraestrutura IoT desenvolvida pela mesma equipe de engenharia.",
                ],
            },
            {
                "nome": "Monitoramento Remoto",
                "url": SITE + "/monitoramento-remoto-iot",
                "cpc": "7.00",
                "p1": "monitoramento", "p2": "remoto",
                "kw": [
                    "monitoramento remoto de equipamentos",
                    "sistema de monitoramento remoto",
                    "telemetria de equipamentos",
                    "monitoramento remoto industrial",
                    "monitoramento de máquinas em tempo real",
                    "alerta de falha em equipamento",
                ],
                "titulos": [
                    "Monitoramento Remoto",
                    "Acompanhe de Onde Estiver",
                    "Alertas em Tempo Real",
                    "Telemetria de Equipamentos",
                    "Menos Visita Técnica",
                    "Sua Operação no Celular",
                ],
                "descs": [
                    "Conectamos equipamentos para enviar dados, gerar alertas e receber comandos.",
                    "Temperatura, tensão, consumo e alarmes em tempo real, de onde você estiver.",
                ],
            },
            {
                "nome": "Manutenção e Preditiva",
                "url": SITE + "/manutencao-industrial",
                "cpc": "6.00",
                "p1": "manutencao", "p2": "industrial",
                "kw": [
                    "manutenção preditiva industrial",
                    "monitoramento de ativos industriais",
                    "manutenção industrial com sensores",
                    "reduzir parada de máquina",
                    "monitoramento de manutenção industrial",
                    "sistema de manutenção preditiva",
                ],
                "titulos": [
                    "Manutenção Preditiva",
                    "Antecipe a Falha",
                    "Menos Parada Não Planejada",
                    "Monitore Seus Ativos",
                    "Falha Vista Antes da Quebra",
                    "Manutenção Com Dados",
                ],
                "descs": [
                    "Monitoramento remoto e diagnóstico para antecipar falhas em equipamentos.",
                    "Reduza paradas não planejadas com dados do equipamento em tempo real.",
                ],
            },
        ],
    },
    {
        "nome": "TQ | Pesquisa | Software Apps e Dashboards",
        "orcamento": "25.00",
        "grupos": [
            {
                "nome": "Aplicativos Conectados",
                "url": SITE + "/aplicativos-conectados",
                "cpc": "6.00",
                "p1": "aplicativos", "p2": "conectados",
                "kw": [
                    "desenvolvimento de aplicativo para equipamento",
                    "aplicativo para controlar equipamento",
                    "aplicativo de monitoramento industrial",
                    "desenvolvimento de aplicativo iot",
                    "app bluetooth para equipamento",
                    "aplicativo para máquina industrial",
                ],
                "titulos": [
                    "Aplicativos Conectados",
                    "Controle Pelo Celular",
                    "App Para Seu Equipamento",
                    "Bluetooth e Wi-Fi no App",
                    "Operação na Palma da Mão",
                    "App Integrado ao Firmware",
                ],
                "descs": [
                    "Aplicativos para monitorar, configurar e controlar equipamentos remotamente.",
                    "App e firmware desenvolvidos juntos, por isso conversam sem improviso.",
                ],
            },
            {
                "nome": "Sistemas e Dashboards",
                "url": SITE + "/sistemas-e-dashboards",
                "cpc": "6.00",
                "p1": "dashboards", "p2": "dados",
                "kw": [
                    "dashboard de monitoramento industrial",
                    "desenvolvimento de dashboard",
                    "sistema de gestão de equipamentos",
                    "painel de dados industriais",
                    "software de telemetria",
                    "dashboard para equipamentos",
                ],
                "titulos": [
                    "Sistemas e Dashboards",
                    "Painéis Claros e Objetivos",
                    "Informação Que Gera Ação",
                    "Dados do Seu Equipamento",
                    "Dashboard Sob Medida",
                    "Decida Com Dado Real",
                ],
                "descs": [
                    "Organizamos os dados dos equipamentos em painéis claros para decidir rápido.",
                    "Sistemas, dashboards e bancos de dados integrados aos seus equipamentos.",
                ],
            },
            {
                "nome": "Software Para Equipamentos",
                "url": SITE + "/desenvolvimento-software",
                "cpc": "6.00",
                "p1": "software", "p2": "industrial",
                "kw": [
                    "desenvolvimento de software industrial",
                    "software para equipamentos",
                    "software sob medida para indústria",
                    "integração de sistemas industriais",
                    "software de controle industrial",
                ],
                "titulos": [
                    "Software Para Equipamentos",
                    "Software Sob Medida",
                    "Integração de Sistemas",
                    "Software Que Fala Com a Placa",
                    "Do Firmware ao Sistema",
                    "Automatize Seus Processos",
                ],
                "descs": [
                    "Software integrado a hardware e firmware, feito para o seu equipamento.",
                    "Sistemas de controle, bancos de dados e automação de processos sob medida.",
                ],
            },
        ],
    },
    {
        "nome": "TQ | Pesquisa | Diagnóstico Técnico",
        "orcamento": "20.00",
        "grupos": [
            {
                "nome": "Diagnóstico de Eletrônica",
                "url": SITE + "/diagnostico-tecnico",
                "cpc": "7.00",
                "p1": "diagnostico", "p2": "tecnico",
                "kw": [
                    "diagnóstico de placa eletrônica",
                    "análise de falha em eletrônica",
                    "falha de comunicação em equipamento",
                    "problema de ruído elétrico em placa",
                    "revisão de projeto eletrônico",
                    "análise de falha em firmware",
                ],
                "titulos": [
                    "Diagnóstico Técnico",
                    "Seu Projeto Está Travando?",
                    "Achamos a Causa da Falha",
                    "Ruído, Falha e Instabilidade",
                    "Análise de Hardware e Firmware",
                    "Hora de Engenharia",
                ],
                "descs": [
                    "Analisamos hardware, firmware, PCB, alimentação e comunicação para achar a causa.",
                    "Você recebe a estimativa de horas e a ordem de correção antes do trabalho começar.",
                ],
            },
            {
                "nome": "Consultoria Técnica",
                "url": SITE + "/diagnostico-tecnico",
                "cpc": "6.00",
                "p1": "consultoria", "p2": "eletronica",
                "kw": [
                    "consultoria em eletrônica",
                    "consultoria em firmware",
                    "consultoria em automação industrial",
                    "consultoria técnica em projeto eletrônico",
                    "consultoria em sistemas embarcados",
                ],
                "titulos": [
                    "Consultoria em Eletrônica",
                    "Revisão de Arquitetura",
                    "Segunda Opinião Técnica",
                    "Consultoria em Firmware",
                    "Mais de 20 Anos na Área",
                    "Orientação Para Evoluir",
                ],
                "descs": [
                    "Diagnóstico, revisão de arquitetura e orientação técnica para o seu projeto.",
                    "Quem já viu a falha antes chega nela em menos horas. É isso que você contrata.",
                ],
            },
        ],
    },
]

# Os sitelinks cobrem exatamente as quatro páginas que existem no site, mais
# duas âncoras da home. Sitelink apontando para página inexistente é reprovado
# pelo Google e joga o clique pago num erro 404.
SITELINKS = [
    ("Produtos eletrônicos", "Da ideia ao produto real", "Hardware, firmware e PCB", SITE + "/desenvolvimento-produtos-eletronicos"),
    ("Firmware e embarcados", "ESP32, MQTT, Modbus e CAN", "Firmware que aguenta o campo", SITE + "/desenvolvimento-firmware"),
    ("Monitoramento e IoT", "Dados e alertas em tempo real", "Acompanhe de onde estiver", SITE + "/monitoramento-remoto-iot"),
    ("Automação industrial", "Automação sob medida", "Eletrônica, firmware e app", SITE + "/automacao-industrial"),
    ("Projetos realizados", "Casos reais de engenharia", "Da placa à usina solar", SITE + "/#projetos"),
    ("Falar com especialista", "Primeira conversa sem custo", "Retorno pela sua preferência", SITE + "/#contato"),
]

CALLOUTS = [
    "Engenharia desde 2001",
    "45+ equipamentos online",
    "Do circuito ao aplicativo",
    "Atendemos todo o Brasil",
    "Escopo e prazo fechados",
    "Um só interlocutor",
    "Projetos sob medida",
    "Conversa inicial gratuita",
]

# O Editor em portugues espera o cabecalho e o idioma no idioma da conta.
# Com "Services" ele importa o snippet como frances e reprova a extensao.
SNIPPET_HEADER = "Serviços"
SNIPPET_VALORES = ["Hardware", "Firmware", "Software", "Aplicativos", "PCB", "Consultoria"]

# Um segundo snippet com outro cabecalho da lista fixa do Google. Dois snippets
# dao ao anuncio mais uma linha possivel de texto, o que amplia o espaco ocupado
# na tela de resultados e ajuda a taxa de clique.
SNIPPET2_HEADER = "Tipos"
SNIPPET2_VALORES = ["Monitoramento remoto", "Automação industrial", "IoT industrial",
                    "Telemetria", "Sistemas embarcados", "Produtos eletrônicos"]
TELEFONE = "16993668447"



# ------------------------------------------------------ negativas por grupo
# Lixo específico de cada tema. As negativas cruzadas entre grupos irmãos
# são geradas automaticamente mais abaixo, para um grupo não roubar o termo
# do outro dentro da mesma campanha.
NEG_POR_GRUPO = {
    "Desenvolvimento de Hardware": [
        "hardware de computador", "loja de hardware", "hardware gamer",
        "manutenção de computador", "placa mãe",
    ],
    "Projeto de PCB": [
        "comprar pcb", "fábrica de pcb", "fabricação de pcb", "pcb china",
        "placa universal", "pcb way",
    ],
    "Produtos Eletrônicos": [
        "loja de eletrônicos", "conserto de eletrônicos", "revenda de eletrônicos",
        "importar eletrônicos",
    ],
    "Firmware Embarcado": [
        "atualizar firmware", "firmware do celular", "firmware da tv",
        "firmware da impressora", "baixar firmware", "flash firmware",
        "firmware box android", "firmware original",
    ],
    "ESP32 e Protocolos": [
        "comprar esp32", "esp32 preço", "esp32 datasheet", "esp32 pinagem",
    ],
    "Automação Industrial": [
        "automação residencial", "automação predial", "comprar clp",
        "clp preço", "automação comercial pdv",
    ],
    "Automação de Máquinas": [
        "máquina de costura", "peças de máquina", "máquina usada",
        "aluguel de máquina",
    ],
    "Indústria 4.0": [
        "artigo indústria 4.0", "livro indústria 4.0", "história da indústria",
        "quarta revolução industrial resumo",
    ],
    "IoT Industrial": [
        "módulo iot preço", "comprar sensor", "chip iot operadora",
    ],
    "Monitoramento Remoto": [
        "rastreador veicular", "monitoramento de veículos", "monitoramento de rede",
        "câmera de monitoramento", "monitoramento de alarme residencial",
    ],
    "Manutenção e Preditiva": [
        "manutenção predial", "manutenção mecânica terceirizada",
        "empresa de manutenção elétrica predial", "plano de manutenção modelo",
    ],
    "Aplicativos Conectados": [
        "aplicativo de delivery", "criar app grátis", "loja de aplicativos",
        "aplicativo de banco", "app de mensagens",
    ],
    "Sistemas e Dashboards": [
        "dashboard excel", "power bi", "template de dashboard", "looker studio grátis",
    ],
    "Software Para Equipamentos": [
        "erp", "software de gestão empresarial", "sistema de vendas",
        "software contábil", "sistema para loja",
    ],
    "Diagnóstico de Eletrônica": [
        "diagnóstico automotivo", "scanner automotivo", "conserto de placa de tv",
        "conserto de fonte", "conserto de placa de máquina de lavar",
    ],
    "Consultoria Técnica": [
        "consultoria empresarial", "consultoria financeira", "consultoria de marketing",
        "consultoria de rh", "consultoria contábil",
    ],
}



# ------------------------------------------------------------ campanha teste
# Orçamento de teste: R$ 100 por semana. Concentrar tudo em uma campanha só,
# com quatro grupos, é o que dá volume suficiente para o Google aprender e
# para a gente ler o resultado. Seis campanhas dividiriam a verba em migalhas.
ORCAMENTO_TESTE = "14.00"   # R$ 14 por dia, cerca de R$ 98 por semana
CPC_TESTE = "4.00"          # teto menor para comprar mais cliques com a mesma verba


def grupo(nome):
    for c in CAMPANHAS:
        for g in c["grupos"]:
            if g["nome"] == nome:
                return dict(g)
    raise KeyError(nome)


def monta_teste():
    """Os quatro grupos escolhidos por retorno, não por volume de busca.

    Critério, nesta ordem: encaixe entre o que a pessoa busca e o que a
    Taquionica realmente vende, depois intenção de compra, e só então volume.
    Três grupos compram exatamente o serviço da casa, onde quase não existe
    concorrente pagando. O quarto compra o termo de maior volume do nicho,
    para garantir clique, mas filtrado contra o público de integrador de CLP,
    que busca outro tipo de fornecedor.
    """
    # 1. O que ele vende de maior ticket: produto eletrônico do zero.
    g1 = grupo("Produtos Eletrônicos")
    g1["nome"] = "Hardware e Produtos Eletrônicos"
    g1["cpc"] = "6.00"
    # O vocabulário aqui é o que empresa grande usa quando procura parceiro de
    # desenvolvimento: "design house", "engenharia eletrônica", "terceirização".
    # São termos exclusivamente B2B, sem estudante nem curioso disputando, por
    # isso custam bem menos que "automação industrial" e puxam o CPC médio para
    # baixo. Confirmado na SERP: Ideen House, Prime Brasil, ECK, E2Pro e Victum
    # mantêm página dedicada para cada um deles.
    g1["kw"] = [
        "desenvolvimento de produtos eletrônicos",
        "empresa de desenvolvimento de produtos eletrônicos",
        "desenvolvimento de projetos eletrônicos",
        "empresa de projetos eletrônicos",
        "desenvolvimento de protótipos eletrônicos",
        "design house eletrônica",
        "empresa de engenharia eletrônica",
        "terceirização de engenharia eletrônica",
        "desenvolvimento de hardware",
        "empresa de desenvolvimento de hardware",
        "projeto de hardware eletrônico",
        "projeto de placa eletrônica",
        "desenvolvimento de pcb",
    ]
    g1["titulos"] = [
        "Produtos Eletrônicos",
        "Desenvolvimento de Hardware",
        "Da Ideia ao Produto Real",
        "Placa, Firmware e App",
        "Protótipo Funcional",
        "Engenharia de Produto",
    ]
    g1["descs"] = [
        "Transformamos a ideia em circuito, protótipo e equipamento pronto para operar.",
        "Hardware, firmware e PCB integrados pela mesma equipe, sem depender de terceiros.",
    ]

    # 2. Nicho onde quase não existe concorrente comprando no Brasil.
    g2 = grupo("Firmware Embarcado")
    g2["nome"] = "Firmware e Embarcados"
    g2["cpc"] = "6.00"
    g2["kw"] = [
        "desenvolvimento de firmware",
        "empresa de desenvolvimento de firmware",
        "programação de firmware",
        "desenvolvimento de sistemas embarcados",
        "empresa de sistemas embarcados",
        "firmware para microcontrolador",
        "desenvolvimento de software embarcado",
        "terceirização de desenvolvimento de firmware",
        "programação esp32",
        "firmware esp32",
    ]

    # 3. Onde a prova da casa é mais forte: 45 equipamentos, 6 anos online.
    g3 = grupo("Monitoramento Remoto")
    g3["nome"] = "Monitoramento Remoto e Telemetria"
    g3["cpc"] = "6.00"
    g3["kw"] = [
        "monitoramento remoto de equipamentos",
        "sistema de monitoramento remoto",
        "monitoramento remoto industrial",
        "telemetria de equipamentos",
        "telemetria industrial",
        "monitoramento de máquinas em tempo real",
        "monitoramento de ativos industriais",
        "soluções iot industrial",
        "desenvolvimento iot",
    ]
    g3["kw_exatas"] = ["iot industrial"]
    g3["titulos"] = [
        "Monitoramento Remoto",
        "Telemetria de Equipamentos",
        "Acompanhe de Onde Estiver",
        "Alertas em Tempo Real",
        "Menos Visita Técnica",
        "Do Sensor ao Dashboard",
    ]

    # 4. O grupo de volume. Traz clique, mas precisa filtrar quem procura
    # integrador de CLP, painel e robótica, que não é o serviço da casa.
    g4 = grupo("Automação Industrial")
    g4["cpc"] = "3.00"
    g4["kw"] = [
        "empresa de automação industrial",
        "projeto de automação industrial",
        "automação industrial sob medida",
        "serviços de automação industrial",
        "automação de máquinas",
        "automação de equipamentos",
    ]
    g4["kw_exatas"] = ["automação industrial"]

    grupos = [g1, g2, g3, g4]
    for g in grupos:
        g["comuns"] = [
            "Engenharia Desde 2001",
            "45 Equipamentos em Campo",
            "6 Anos Sem Interrupção",
            "Um Só Fornecedor",
            "Do Circuito ao Aplicativo",
            "Escopo e Prazo Fechados",
            "Atendemos Todo o Brasil",
            "Fale com um Especialista",
            "Peça uma Avaliação",
        ]
        g["descs_comuns"] = [
            "Mais de 45 equipamentos em operação contínua há mais de seis anos. Desde 2001.",
            "Escopo, prazo e valor fechados antes da primeira linha de código. Fale conosco.",
        ]
        g["fixa_titulo_1"] = True
    return [{
        "nome": "TQ | Pesquisa | Teste",
        "orcamento": ORCAMENTO_TESTE,
        "grupos": grupos,
    }]


# Quem busca "automação industrial" quase sempre procura integrador de CLP,
# painel elétrico e robótica, que a Taquionica não faz. Sem este filtro, o
# grupo de maior volume traz o lead errado e gasta a verba da semana.
NEG_POR_GRUPO["Automação Industrial"] += [
    "clp", "painel elétrico", "quadro de comando", "robótica", "robô industrial",
    "célula robotizada", "linha de montagem", "esteira transportadora",
    "siemens", "rockwell", "allen bradley", "schneider", "weg",
    "instalação elétrica", "montagem de painel", "supervisório scada",
]
NEG_POR_GRUPO["Hardware e Produtos Eletrônicos"] = NEG_POR_GRUPO["Produtos Eletrônicos"] + \
    NEG_POR_GRUPO["Desenvolvimento de Hardware"] + NEG_POR_GRUPO["Projeto de PCB"]
NEG_POR_GRUPO["Firmware e Embarcados"] = NEG_POR_GRUPO["Firmware Embarcado"] + \
    NEG_POR_GRUPO["ESP32 e Protocolos"]
NEG_POR_GRUPO["Monitoramento Remoto e Telemetria"] = NEG_POR_GRUPO["Monitoramento Remoto"] + \
    NEG_POR_GRUPO["IoT Industrial"]
def escreve(pasta, nome, cabecalho, linhas):
    caminho = os.path.join(pasta, nome)
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        w.writerow(cabecalho)
        w.writerows(linhas)
    print("  %s: %d linhas" % (nome, len(linhas)))


def gera(campanhas, pasta):
    os.makedirs(pasta, exist_ok=True)
    print(os.path.basename(pasta) + ":")

    escreve(pasta, "1-campanhas.csv",
            ["Campaign", "Campaign Type", "Campaign Status", "Campaign Daily Budget",
             "Bid Strategy Type", "Languages"],
            [[c["nome"], "Search", "Paused", c["orcamento"], "Manual CPC", "Portuguese"]
             for c in campanhas])

    # Local em arquivo proprio. Dentro do arquivo de campanhas o Editor ignora a
    # coluna, e a campanha sobe sem segmentacao, exibindo o anuncio no mundo todo.
    escreve(pasta, "11-locais.csv", ["Campaign", "Location"],
            [[c["nome"], "Brasil"] for c in campanhas])

    linhas = []
    for c in campanhas:
        for g in c["grupos"]:
            linhas.append([c["nome"], g["nome"], "Enabled", g["cpc"]])
    escreve(pasta, "2-grupos.csv", ["Campaign", "Ad Group", "Ad Group Status", "Max CPC"], linhas)

    linhas = []
    for c in campanhas:
        for g in c["grupos"]:
            for k in g["kw"]:
                linhas.append([c["nome"], g["nome"], k, "Phrase", g["cpc"], "Enabled"])
                linhas.append([c["nome"], g["nome"], k, "Exact", g["cpc"], "Enabled"])
            # termos raiz: só exata, para não abrir a torneira da busca genérica
            for k in g.get("kw_exatas", []):
                linhas.append([c["nome"], g["nome"], k, "Exact", g["cpc"], "Enabled"])
    escreve(pasta, "3-keywords.csv",
            ["Campaign", "Ad Group", "Keyword", "Criterion Type", "Max CPC", "Status"], linhas)

    linhas = []
    for c in campanhas:
        for g in c["grupos"]:
            proprias = set(g["kw"]) | set(g.get("kw_exatas", []))
            for n in NEG_POR_GRUPO.get(g["nome"], []):
                linhas.append([c["nome"], g["nome"], n, "Negative Phrase"])
            irmaos = []
            for outro in c["grupos"]:
                if outro["nome"] == g["nome"]:
                    continue
                for k in outro["kw"] + outro.get("kw_exatas", []):
                    if k not in proprias and k not in irmaos:
                        irmaos.append(k)
            for k in irmaos:
                linhas.append([c["nome"], g["nome"], k, "Negative Exact"])
    escreve(pasta, "4-negativas-por-grupo.csv",
            ["Campaign", "Ad Group", "Keyword", "Criterion Type"], linhas)

    cab = ["Campaign", "Ad Group", "Ad Type", "Headline 1", "Headline 1 position"] + \
          ["Headline %d" % i for i in range(2, 16)] + \
          ["Description %d" % i for i in range(1, 5)] + ["Path 1", "Path 2", "Final URL", "Status"]
    linhas = []
    for c in campanhas:
        for g in c["grupos"]:
            titulos = g["titulos"] + g.get("comuns", TITULOS_COMUNS)
            assert len(titulos) == 15, "%s: %d titulos" % (g["nome"], len(titulos))
            assert len(set(titulos)) == 15, "%s: titulo repetido" % g["nome"]
            for t in titulos:
                lim(t, 30, "TITULO " + g["nome"])
            descs = g["descs"] + g.get("descs_comuns", DESC_COMUNS)
            for d in descs:
                lim(d, 90, "DESC " + g["nome"])
            lim(g["p1"], 15, "PATH1 " + g["nome"])
            lim(g["p2"], 15, "PATH2 " + g["nome"])
            posicao = "1" if g.get("fixa_titulo_1") else ""
            linhas.append([c["nome"], g["nome"], "Responsive search ad",
                           titulos[0], posicao] + titulos[1:] + descs +
                          [g["p1"], g["p2"], g["url"], "Enabled"])
    escreve(pasta, "5-anuncios.csv", cab, linhas)

    linhas = []
    for c in campanhas:
        for texto, d1, d2, url in SITELINKS:
            lim(texto, 25, "SITELINK")
            lim(d1, 35, "SITELINK D1")
            lim(d2, 35, "SITELINK D2")
            linhas.append([c["nome"], texto, d1, d2, url])
    escreve(pasta, "6-extensoes-sitelinks.csv",
            ["Campaign", "Link Text", "Description Line 1", "Description Line 2", "Final URL"], linhas)

    escreve(pasta, "7-extensoes-chamadas.csv", ["Campaign", "Phone Number", "Country Code"],
            [[c["nome"], TELEFONE, "BR"] for c in campanhas])

    linhas = []
    for c in campanhas:
        for t in CALLOUTS:
            lim(t, 25, "CALLOUT")
            linhas.append([c["nome"], t])
    escreve(pasta, "8-extensoes-destaques.csv", ["Campaign", "Callout text"], linhas)

    for v in SNIPPET_VALORES + SNIPPET2_VALORES:
        lim(v, 25, "SNIPPET")
    escreve(pasta, "9-extensoes-snippets.csv",
            ["Campaign", "Language", "Header"] + ["Value %d" % i for i in range(1, 7)],
            [[c["nome"], "Portuguese", SNIPPET_HEADER] + SNIPPET_VALORES for c in campanhas] +
            [[c["nome"], "Portuguese", SNIPPET2_HEADER] + SNIPPET2_VALORES for c in campanhas])

    # Gerente de engenharia e de manutenção pesquisa fornecedor no expediente.
    # Fora dele sobra curioso, e o clique custa igual. Concentrar os R$ 14 em
    # 50 horas por semana em vez de 168 multiplica a presença nos leilões que
    # importam, sem aumentar a verba.
    dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    escreve(pasta, "10-horarios.csv",
            ["Campaign", "Day of Week", "Start Time", "End Time", "Bid Adjustment"],
            [[c["nome"], d, "08:00", "18:00", "0%"] for c in campanhas for d in dias])

    escreve(pasta, "negativas-lista-global.csv",
            ["Campaign", "Ad Group", "Keyword", "Criterion Type"],
            [[c["nome"], "", n, "Campaign Negative Phrase"] for c in campanhas for n in NEG_FRASE])

    with open(os.path.join(pasta, "negativas-lista-global.txt"), "w", encoding="utf-8") as f:
        for n in NEG_FRASE:
            f.write('"%s"\n' % n)
    print("  negativas-lista-global.txt: %d termos" % len(NEG_FRASE))


# O que se importa agora: uma campanha, quatro grupos, R$ 14 por dia.

# ==================================================================== R$ 100/dia
# Com R$ 100 por dia a restricao deixa de ser orcamento e passa a ser volume de
# busca. Os 40 termos do teste de R$ 14 rendem no maximo algo entre 400 e 800
# cliques por mes, enquanto R$ 100 por dia compraria 1.200. Sem ampliar o
# conjunto, a campanha ficaria limitada por volume e devolveria verba.
#
# A ampliacao respeita uma restricao real: o site tem apenas quatro paginas.
# Cada grupo aponta para a pagina que de fato cobre o assunto dele.
PAG_PRODUTOS = SITE + "/desenvolvimento-produtos-eletronicos"
PAG_FIRMWARE = SITE + "/desenvolvimento-firmware"
PAG_MONITOR = SITE + "/monitoramento-remoto-iot"
PAG_AUTOMACAO = SITE + "/automacao-industrial"

COMUNS_100 = [
    "Engenharia Desde 2001",
    "45 Equipamentos em Campo",
    "6 Anos Sem Interrupção",
    "Um Só Fornecedor",
    "Do Circuito ao Aplicativo",
    "Escopo e Prazo Fechados",
    "Atendemos Todo o Brasil",
    "Fale com um Especialista",
    "Peça uma Avaliação",
]
DESCS_COMUNS_100 = [
    "Mais de 45 equipamentos em operação contínua há mais de seis anos. Desde 2001.",
    "Escopo, prazo e valor fechados antes da primeira linha de código. Fale conosco.",
]


def prep(nome, url, cpc, extras=None, exatas=None, novo_nome=None):
    g = grupo(nome)
    if novo_nome:
        g["nome"] = novo_nome
        NEG_POR_GRUPO[novo_nome] = NEG_POR_GRUPO.get(nome, [])
    g["url"] = url
    g["cpc"] = cpc
    if extras:
        g["kw"] = g["kw"] + [k for k in extras if k not in g["kw"]]
    if exatas:
        g["kw_exatas"] = exatas
        g["kw"] = [k for k in g["kw"] if k not in exatas]
    g["comuns"] = COMUNS_100
    g["descs_comuns"] = DESCS_COMUNS_100
    g["fixa_titulo_1"] = True
    return g


def monta_100():
    """Tres campanhas, R$ 100 por dia no total.

    A separacao em campanhas so existe porque agora cada uma sustenta o proprio
    orcamento. E ela serve a um proposito concreto: conter a campanha de termos
    amplos em R$ 20 por dia, para que ela nunca consuma a verba das duas que
    trazem o comprador certo.
    """
    engenharia = {
        "nome": "TQ | Pesquisa | Engenharia Eletrônica",
        "orcamento": "45.00",
        "grupos": [
            prep("Produtos Eletrônicos", PAG_PRODUTOS, "7.00", extras=[
                "empresa de engenharia eletrônica",
                "design house eletrônica",
                "terceirização de engenharia eletrônica",
                "desenvolvimento de projetos eletrônicos",
                "empresa de projetos eletrônicos",
                "desenvolvimento de protótipos eletrônicos",
            ], novo_nome="Produtos Eletrônicos e Engenharia"),
            prep("Desenvolvimento de Hardware", PAG_PRODUTOS, "7.00"),
            prep("Projeto de PCB", PAG_PRODUTOS, "7.00"),
            prep("Firmware Embarcado", PAG_FIRMWARE, "7.00", extras=[
                "terceirização de desenvolvimento de firmware",
            ]),
            prep("ESP32 e Protocolos", PAG_FIRMWARE, "6.00"),
        ],
    }

    iot = {
        "nome": "TQ | Pesquisa | IoT e Monitoramento",
        "orcamento": "35.00",
        "grupos": [
            prep("Monitoramento Remoto", PAG_MONITOR, "7.00", extras=[
                "telemetria industrial",
            ]),
            prep("IoT Industrial", PAG_MONITOR, "6.00", exatas=["iot industrial"]),
            prep("Manutenção e Preditiva", PAG_MONITOR, "6.00",
                 novo_nome="Manutenção Preditiva"),
        ],
    }

    # Termos de cabeca: muito volume, intencao pior. Ficam isolados aqui com
    # orcamento e lance proprios, para poderem ser pausados sozinhos se o
    # relatorio de termos de pesquisa mostrar que trazem o publico errado.
    amplos = {
        "nome": "TQ | Pesquisa | Automação e Indústria 4.0",
        "orcamento": "20.00",
        "grupos": [
            prep("Automação Industrial", PAG_AUTOMACAO, "4.00",
                 exatas=["automação industrial"]),
            prep("Automação de Máquinas", PAG_AUTOMACAO, "4.00"),
            prep("Indústria 4.0", PAG_AUTOMACAO, "3.00",
                 exatas=["indústria 4.0"]),
        ],
    }
    return [engenharia, iot, amplos]



def monta_uma_campanha():
    """Uma campanha, quatro grupos, R$ 100 por dia.

    Mantem exatamente a estrutura que ja esta montada no Google Ads Editor,
    inclusive os nomes da campanha e dos grupos, para que a importacao dos
    arquivos ADICIONE palavras-chave aos grupos existentes em vez de criar
    grupos novos e duplicados.

    O volume necessario para gastar R$ 100 por dia vem de dentro: cada grupo
    absorve os termos dos temas vizinhos que apontam para a mesma pagina. Sao
    86 termos no lugar dos 40 anteriores, sem criar campanha nova.
    """
    def junta(*nomes):
        termos, exatas = [], []
        for n in nomes:
            g = grupo(n)
            for k in g["kw"]:
                if k not in termos:
                    termos.append(k)
            for k in g.get("kw_exatas", []):
                if k not in exatas:
                    exatas.append(k)
        return termos, exatas

    def negs(*nomes):
        saida = []
        for n in nomes:
            for x in NEG_POR_GRUPO.get(n, []):
                if x not in saida:
                    saida.append(x)
        return saida

    # G1: a pagina de produtos eletronicos cobre hardware, PCB e produto.
    g1 = grupo("Produtos Eletrônicos")
    g1["nome"] = "Hardware e Produtos Eletrônicos"
    g1["url"] = SITE + "/desenvolvimento-produtos-eletronicos"
    g1["cpc"] = "9.00"
    g1["kw"], _ = junta("Produtos Eletrônicos", "Desenvolvimento de Hardware", "Projeto de PCB")
    g1["kw"] += [k for k in [
        "empresa de engenharia eletrônica",
        "design house eletrônica",
        "terceirização de engenharia eletrônica",
        "desenvolvimento de projetos eletrônicos",
        "empresa de projetos eletrônicos",
        "desenvolvimento de protótipos eletrônicos",
    ] if k not in g1["kw"]]
    NEG_POR_GRUPO[g1["nome"]] = negs("Produtos Eletrônicos", "Desenvolvimento de Hardware",
                                     "Projeto de PCB")
    g1["titulos"] = [
        "Produtos Eletrônicos",
        "Desenvolvimento de Hardware",
        "Projeto e Layout de PCB",
        "Da Ideia ao Produto Real",
        "Placa, Firmware e App",
        "Engenharia de Produto",
    ]
    g1["descs"] = [
        "Transformamos a ideia em circuito, protótipo e equipamento pronto para operar.",
        "Hardware, firmware e PCB integrados pela mesma equipe, sem depender de terceiros.",
    ]

    # G2: firmware e ESP32 apontam para a mesma pagina.
    g2 = grupo("Firmware Embarcado")
    g2["nome"] = "Firmware e Embarcados"
    g2["url"] = SITE + "/desenvolvimento-firmware"
    g2["cpc"] = "9.00"
    g2["kw"], _ = junta("Firmware Embarcado", "ESP32 e Protocolos")
    g2["kw"] += ["terceirização de desenvolvimento de firmware"]
    NEG_POR_GRUPO[g2["nome"]] = negs("Firmware Embarcado", "ESP32 e Protocolos")

    # G3: monitoramento, IoT e manutencao preditiva vendem a mesma solucao.
    g3 = grupo("Monitoramento Remoto")
    g3["nome"] = "Monitoramento Remoto e Telemetria"
    g3["url"] = SITE + "/monitoramento-remoto-iot"
    g3["cpc"] = "9.00"
    g3["kw"], g3["kw_exatas"] = junta("Monitoramento Remoto", "IoT Industrial",
                                      "Manutenção e Preditiva")
    g3["kw"] += [k for k in ["telemetria industrial"] if k not in g3["kw"]]
    g3["kw_exatas"] = ["iot industrial"]
    g3["kw"] = [k for k in g3["kw"] if k not in g3["kw_exatas"]]
    NEG_POR_GRUPO[g3["nome"]] = negs("Monitoramento Remoto", "IoT Industrial",
                                     "Manutenção e Preditiva")
    g3["titulos"] = [
        "Monitoramento Remoto",
        "Telemetria de Equipamentos",
        "IoT Industrial Sob Medida",
        "Alertas em Tempo Real",
        "Menos Visita Técnica",
        "Do Sensor ao Dashboard",
    ]

    # G4: o grupo de volume. Teto de lance menor porque a intencao e pior e o
    # leilao e disputado por integrador de CLP, que vende outra coisa.
    g4 = grupo("Automação Industrial")
    g4["url"] = SITE + "/automacao-industrial"
    # Teto abaixo dos outros tres de proposito. Ele tem o maior volume do
    # nicho, entao com teto igual ganharia os leiloes e levaria a maior parte
    # da verba para o trafego de menor intencao. Em R$ 6 ele absorve a sobra
    # que os grupos qualificados nao conseguem gastar, sem competir com eles.
    g4["cpc"] = "6.00"
    g4["kw"], _ = junta("Automação Industrial", "Automação de Máquinas", "Indústria 4.0")
    g4["kw_exatas"] = ["automação industrial", "indústria 4.0"]
    g4["kw"] = [k for k in g4["kw"] if k not in g4["kw_exatas"]]
    NEG_POR_GRUPO["Automação Industrial"] = negs("Automação Industrial",
                                                 "Automação de Máquinas", "Indústria 4.0")

    grupos = [g1, g2, g3, g4]
    for g in grupos:
        g["comuns"] = [
            "Engenharia Desde 2001",
            "45 Equipamentos em Campo",
            "6 Anos Sem Interrupção",
            "Um Só Fornecedor",
            "Do Circuito ao Aplicativo",
            "Escopo e Prazo Fechados",
            "Atendemos Todo o Brasil",
            "Fale com um Especialista",
            "Peça uma Avaliação",
        ]
        g["descs_comuns"] = [
            "Mais de 45 equipamentos em operação contínua há mais de seis anos. Desde 2001.",
            "Escopo, prazo e valor fechados antes da primeira linha de código. Fale conosco.",
        ]
        g["fixa_titulo_1"] = True
    return [{
        "nome": "TQ | Pesquisa | Teste",
        "orcamento": "100.00",
        "grupos": grupos,
    }]


# A pasta `import` passou a ser gerada por `gerar_campanha.py`, que monta a
# estrutura de tres campanhas e reaproveita a funcao `gera` daqui. Este arquivo
# ficou responsavel so pela estrutura ampla de reserva, em `import-completo`, e
# por servir de biblioteca: negativas globais, sitelinks, destaques e o motor de
# escrita dos CSVs. A geracao fica atras do guard porque, sem ele, importar este
# modulo sobrescreveria os arquivos.

if __name__ == "__main__":
    gera(CAMPANHAS, os.path.join(BASE, "import-completo"))

    if erros:
        print("\n*** LIMITES ESTOURADOS ***")
        for e in erros:
            print("  " + e)
        sys.exit(1)
    print("\nOK: nenhum limite de caracteres estourado.")
