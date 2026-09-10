# -*- coding: utf-8 -*-
"""Conteudo das tres landing pages da segunda rodada.

Ficam num arquivo separado so por tamanho: o `build_lps.py` ja passava de
setecentas linhas e o conteudo editorial nao tem por que disputar espaco com o
motor de montagem. A funcao recebe o dicionario de imagens em vez de importar,
para nao criar import circular com o modulo que a chama.

As tres foram escolhidas por um criterio unico: sao grupos de anuncios que ja
existem na campanha e hoje dividem pagina com outro assunto. Terceirizacao esta
dentro do grupo de produtos eletronicos, telemetria agricola aponta para a
pagina de monitoramento e PCB aponta para a de produtos. Dar pagina propria a
cada um sobe o Indice de Qualidade e a conversao dos dois lados, porque a
pagina passa a dizer exatamente o que a pessoa buscou.
"""


def novas(IMG):
    return [

        # ==================================== 1. terceirizacao de engenharia
        # A pagina do gerente de engenharia de indústria grande. Volume de busca
        # baixo, ticket alto, e e o vocabulario que o comprador certo usa.
        {
            "slug": "terceirizacao-de-engenharia-eletronica",
            "titulo": "Terceirização de Engenharia Eletrônica | Taquionica",
            "descricao": ("Braço técnico de engenharia eletrônica para empresas com projeto "
                          "na fila e time interno ocupado. Hardware, firmware e PCB pela "
                          "mesma equipe."),
            "hero": (
                "Terceirização de engenharia",
                "O projeto está na fila esperando um ",
                "engenheiro que você não tem",
                "",
                "Abrir vaga leva meses e vira custo fixo para sempre. A Taquionica entra "
                "como braço técnico de engenharia eletrônica, com time dimensionado pelo "
                "escopo do seu projeto, e devolve o produto pronto para operar. Você trata "
                "com o responsável técnico, não com um gerente de conta.",
                "Apresentar meu projeto",
                "Olá! Vim da página de Terceirização de Engenharia Eletrônica da Taquionica "
                "e gostaria de apresentar um projeto.",
                IMG["auto5"],
                "Placa de aquisição e condicionamento de sinais desenvolvida pela Taquionica",
                "Placa de aquisição e condicionamento de sinais",
                "Instrumentação",
            ),
            "problema": (
                "A engenharia que falta não é a que você demitiu, é a que você nunca teve tempo de contratar",
                "O time interno raramente está parado. Ele está sustentando o produto que já "
                "vende, e é justamente por isso que o produto novo não sai do papel.",
                [
                    ("clock", "Vaga aberta há meses, e o projeto parado esperando alguém aceitar"),
                    ("users", "O time atual consumido mantendo o que já existe, sem folga para o novo"),
                    ("alert", "Um único especialista concentra o conhecimento, e ele pode sair amanhã"),
                    ("layers", "Fornecedores diferentes para placa, firmware e aplicativo, culpando uns aos outros"),
                    ("refresh", "Freelancer que entrega e some quando chega a primeira revisão"),
                ],
            ),
            "oferta": (
                "Você contrata a engenharia que o escopo exige, não a folha de um time parado",
                "A Taquionica assume o desenvolvimento eletrônico do seu projeto, parcial ou "
                "completo. Hardware, firmware, PCB, aplicativo e integração saem da mesma "
                "equipe, coordenados por um responsável técnico que acompanha do diagnóstico "
                "à entrega. O time cresce e reduz junto com o projeto, sem estrutura ociosa "
                "embutida no preço.",
            ),
            "entregas": (
                "Como um projeto terceirizado acontece aqui",
                "Nada começa antes de escopo, prazo e valor estarem fechados. Você aprova "
                "cada etapa sabendo exatamente o que entra nela.",
                [
                    ("Diagnóstico técnico",
                     "Entendemos o produto, o problema e as restrições reais de custo, prazo "
                     "e volume. É onde aparecem os riscos que ninguém tinha mapeado."),
                    ("Arquitetura e escopo fechado",
                     "Definimos a arquitetura, as etapas e as entregas. Você recebe escopo, "
                     "prazo e valor antes da primeira linha de código."),
                    ("Desenvolvimento com time por escopo",
                     "Especialistas de eletrônica de potência, layout de PCB, firmware, "
                     "aplicativo e integração entram conforme a etapa exige."),
                    ("Entrega, documentação e evolução",
                     "O projeto é entregue funcionando, com a documentação técnica, e o "
                     "caminho de evolução fica planejado para as próximas versões."),
                ],
            ),
            "prova": (
                "Engenharia que já sustenta parque instalado, não portfólio de apresentação",
                "O que a Taquionica entrega continua rodando anos depois da entrega, e "
                "continua recebendo versão nova sem ninguém sair do escritório.",
                [
                    ("Desde 2001", "O responsável técnico desenvolve eletrônica, firmware e "
                                   "comunicação industrial."),
                    ("45+", "Equipamentos em operação contínua há mais de seis anos, com "
                            "atualização remota de frota."),
                    ("Um interlocutor", "Você trata com quem responde tecnicamente pelo "
                                        "projeto, do diagnóstico à entrega."),
                ],
            ),
            "tecnologias": (
                "A disciplina vem antes da ferramenta",
                "A arquitetura é escolhida pelo que o produto precisa suportar em campo, não "
                "pelo que era mais rápido de montar.",
                ["Hardware", "Firmware", "Layout de PCB", "Aplicativos", "MQTT", "Modbus",
                 "ESP32", "Integração"],
            ),
            "projetos": (
                "Projetos desenvolvidos como braço técnico de outras empresas",
                [
                    (IMG["auto1"], "Automação industrial",
                     "Placa de controle para acionamento de motores",
                     "Projeto completo de hardware dedicado, com estágio de potência para "
                     "dois motores, proteções e firmware de controle.",
                     ["Eletrônica", "Placa dedicada (PCB)", "Microcontrolador", "Firmware"]),
                    (IMG["auto4"], "Energia",
                     "Placa de acionamento e conversão de energia",
                     "Hardware com estágio de conversão, filtragem, proteções e interface de "
                     "comando para o inversor.",
                     ["Eletrônica", "Conversão DC/DC", "PCB de potência"]),
                    (IMG["app1"], "Eletrônica embarcada",
                     "Aplicativo para configuração de equipamento",
                     "App conectado por Bluetooth ao firmware, com perfis de operação, "
                     "gráficos em tempo real e histórico.",
                     ["Android", "BLE", "Firmware"]),
                ],
            ),
            "faq": (
                "Dúvidas sobre terceirizar engenharia eletrônica",
                [
                    ("De quem é a propriedade do que for desenvolvido?",
                     "Do cliente. O projeto é desenvolvido para a sua empresa e a titularidade "
                     "do resultado é sua. As condições são formalizadas em contrato antes do "
                     "início dos trabalhos."),
                    ("Vocês assinam acordo de confidencialidade?",
                     "Sim. Tratamos as informações compartilhadas com confidencialidade e "
                     "formalizamos acordos específicos de sigilo antes do começo do projeto "
                     "sempre que necessário."),
                    ("Dá para contratar só uma parte do desenvolvimento?",
                     "Dá. É possível contratar apenas hardware, apenas firmware, apenas o "
                     "layout de PCB, apenas o aplicativo, ou o desenvolvimento completo com "
                     "todas as camadas integradas."),
                    ("Como o trabalho é cobrado?",
                     "Por escopo fechado, definido depois do diagnóstico técnico. Você recebe "
                     "escopo, prazo e valor antes de qualquer desenvolvimento começar, e não "
                     "existe tabela de prateleira porque cada projeto é dimensionado sobre o "
                     "problema real."),
                    ("Vocês têm capacidade para um projeto de grande porte?",
                     "Sim. O time é montado conforme o escopo: o responsável técnico coordena "
                     "os especialistas de cada disciplina, que entram de acordo com a etapa. A "
                     "capacidade acompanha o tamanho do projeto."),
                    ("O que acontece depois da entrega?",
                     "O projeto é entregue funcionando e documentado. A partir daí é possível "
                     "contratar evolução, novas funcionalidades ou suporte técnico, mas você "
                     "não fica preso a isso para continuar operando."),
                ],
            ),
            "contato": (
                "Tire o projeto da fila",
                "Conte o que a sua empresa precisa desenvolver e qual prazo está pressionando. "
                "A Taquionica avalia a viabilidade técnica, aponta os riscos e devolve o "
                "caminho até o produto pronto.",
                "Apresentar meu projeto",
                "Olá! Vim da página de Terceirização de Engenharia Eletrônica da Taquionica e "
                "gostaria de avaliar um projeto.",
                "Terceirização de Engenharia Eletrônica",
            ),
        },

        # ======================================= 2. telemetria agricola e solar
        # A unica pagina da conta com prova visual propria: o trator e o
        # implemento de escovas em usina fotovoltaica sao projeto da casa.
        {
            "slug": "telemetria-agricola-e-solar",
            "titulo": "Eletrônica Embarcada Agrícola e Solar | Taquionica",
            "descricao": ("Eletrônica embarcada e telemetria para máquinas agrícolas, "
                          "implementos e usinas fotovoltaicas, projetadas para vibração, "
                          "poeira e alimentação oscilando."),
            "hero": (
                "Eletrônica embarcada em campo",
                "O que se prova na bancada precisa ",
                "aguentar o campo",
                "",
                "Na bancada a tensão é estável, a temperatura é constante e ninguém encosta "
                "na placa. No campo o implemento vibra o dia inteiro, a alimentação oscila "
                "com o motor e poeira entra onde não devia. A Taquionica projeta a eletrônica "
                "e o firmware que continuam funcionando nessa condição.",
                "Falar sobre meu equipamento",
                "Olá! Vim da página de Eletrônica Embarcada Agrícola e Solar da Taquionica e "
                "gostaria de falar sobre um equipamento de campo.",
                IMG["agro2"],
                "Implemento automatizado de escovas rotativas operando em usina fotovoltaica",
                "Implemento automatizado de escovas rotativas",
                "Energia solar",
            ),
            "problema": (
                "Máquina em campo sem informação é máquina que só avisa depois que parou",
                "Quando o equipamento está a quilômetros e não reporta nada, cada problema "
                "vira deslocamento, e cada deslocamento vira hora parada.",
                [
                    ("radio", "Equipamento no campo sem nenhum dado até alguém ir até ele"),
                    ("alert", "A máquina só informa que quebrou depois de parar no meio da operação"),
                    ("plug", "Eletrônica de prateleira que não aguenta vibração, poeira e tensão oscilando"),
                    ("clock", "Atualizar firmware da frota significa mandar técnico a cada unidade"),
                    ("factory", "Nenhum registro do que a máquina fez, para provar operação e planejar manutenção"),
                ],
            ),
            "oferta": (
                "Do sensor no implemento ao painel que a operação acompanha",
                "A Taquionica desenvolve a placa que vai dentro do equipamento, o firmware de "
                "controle, a comunicação com a nuvem e o painel onde o dado vira decisão. É a "
                "mesma engenharia da bancada ao campo, o que significa que não existe "
                "fornecedor culpando o outro quando a máquina para na fileira.",
            ),
            "entregas": (
                "O que entra em um projeto de eletrônica embarcada para o campo",
                "O escopo é dimensionado sobre a sua máquina e sobre a condição real de "
                "operação, não sobre um kit fechado.",
                [
                    ("Controle embarcado",
                     "Leitura de sensores de posição, acionamento de atuadores hidráulicos, "
                     "ajuste de velocidade e proteção contra sobrecarga."),
                    ("Eletrônica que aguenta campo",
                     "Alimentação, proteções e layout dimensionados para vibração contínua, "
                     "poeira, umidade e tensão que oscila com o motor."),
                    ("Telemetria e alerta",
                     "O equipamento reporta operação, leitura e alarme por 4G ou Wi-Fi, com "
                     "buffer local para o dado não se perder quando não há sinal."),
                    ("Frota atualizada à distância",
                     "Novas versões de firmware distribuídas remotamente, sem deslocar "
                     "técnico até cada unidade."),
                ],
            ),
            "prova": (
                "Equipamento que trabalha sobre milhões em ativo instalado",
                "O implemento desenvolvido pela Taquionica se desloca todos os dias sobre as "
                "fileiras de uma usina fotovoltaica, encostando em vidro que gera receita. É "
                "esse contexto que define o que significa funcionar.",
                [
                    ("Dezenas de milhares", "De módulos fotovoltaicos na usina em que o "
                                            "equipamento opera."),
                    ("45+", "Equipamentos em operação contínua há mais de seis anos, com "
                            "atualização remota."),
                    ("Desde 2001", "O responsável técnico projeta eletrônica de controle e "
                                   "potência para equipamento que trabalha em campo."),
                ],
            ),
            "tecnologias": (
                "Comunicação escolhida pela condição do campo",
                "O protocolo é definido pela distância, pelo sinal disponível e pelo consumo "
                "que a máquina pode bancar, não pelo que estava na moda.",
                ["4G", "Wi-Fi", "MQTT", "Modbus", "CAN", "Sensores de posição",
                 "Controle hidráulico", "Atualização remota"],
            ),
            "projetos": (
                "Eletrônica embarcada em operação no campo",
                [
                    (IMG["agro2"], "Energia solar / Usinas fotovoltaicas",
                     "Implemento automatizado de escovas rotativas",
                     "Controle eletrônico do braço e das escovas, com ajuste de velocidade, "
                     "sensores de posição e proteção contra sobrecarga.",
                     ["Eletrônica", "Controle hidráulico", "Sensores de posição", "Firmware"]),
                    (IMG["agro3"], "Energia solar / Usinas fotovoltaicas",
                     "Operação em larga escala em usinas fotovoltaicas",
                     "Padronização do processo com equipamentos automatizados e registro "
                     "operacional para gestão da manutenção.",
                     ["Eletrônica", "Telemetria", "Gestão operacional"]),
                    (IMG["dash"], "Monitoramento",
                     "Painel de acompanhamento do parque instalado",
                     "Equipamentos no mapa, estado de conexão e leituras em tempo real, com "
                     "histórico por período.",
                     ["Dashboard", "MQTT", "Tempo real"]),
                ],
            ),
            "faq": (
                "Dúvidas sobre eletrônica embarcada para campo",
                [
                    ("A eletrônica aguenta vibração, poeira e umidade?",
                     "É para isso que ela é projetada. Alimentação, proteções, escolha de "
                     "componentes e layout são dimensionados para a condição real de operação, "
                     "que é justamente onde a eletrônica genérica falha."),
                    ("Funciona onde não tem sinal de celular?",
                     "O controle embarcado funciona independente de sinal, porque a lógica "
                     "roda dentro do equipamento. A telemetria guarda as leituras localmente e "
                     "envia quando a conexão volta, então o histórico não se perde."),
                    ("Dá para atualizar o firmware da frota à distância?",
                     "Quando o hardware e a arquitetura de comunicação permitem, sim. A "
                     "Taquionica já mantém mais de 45 equipamentos recebendo novas versões "
                     "remotamente, sem deslocar técnico até o cliente."),
                    ("Vocês desenvolvem para o fabricante embarcar em série?",
                     "Sim. O projeto pode ser desenvolvido para produção, com a documentação "
                     "e os arquivos preparados para fabricação, e não apenas como unidade "
                     "única de protótipo."),
                    ("A telemetria integra com o sistema que já usamos?",
                     "Integra. Os dados podem ser entregues no painel próprio ou enviados por "
                     "MQTT ou API para o sistema que a sua equipe já mantém."),
                    ("Vocês atendem projeto de grande porte?",
                     "Sim. O time é montado conforme o escopo, e a experiência vem de "
                     "equipamentos que operam sobre parques avaliados em milhões de reais, "
                     "onde falha de controle não é defeito, é prejuízo no mesmo dia."),
                ],
            ),
            "contato": (
                "Leve a sua máquina para o campo sabendo o que ela está fazendo",
                "Conte qual é o equipamento, onde ele opera e o que a sua equipe precisa "
                "controlar ou acompanhar à distância. A Taquionica avalia a viabilidade e "
                "indica o caminho de eletrônica e comunicação.",
                "Falar sobre meu equipamento",
                "Olá! Vim da página de Eletrônica Embarcada Agrícola e Solar da Taquionica e "
                "gostaria de avaliar um equipamento de campo.",
                "Eletrônica Embarcada Agrícola e Solar",
            ),
        },

        # ================================================== 3. projeto de PCB
        # Grupo proprio na campanha desde o inicio, mas apontando para a pagina
        # de produtos eletronicos. A pagina propria e o que casa termo e destino.
        {
            "slug": "projeto-de-pcb",
            "titulo": "Projeto e Layout de PCB Sob Medida | Taquionica",
            "descricao": ("Projeto e layout de placa de circuito impresso, com organização de "
                          "sinais, redução de ruído e arquivos prontos para fabricação. "
                          "Também revisamos placas que falham em campo."),
            "hero": (
                "Projeto e layout de PCB",
                "Layout de placa não é desenho. É ",
                "engenharia",
                ", e é onde a falha nasce",
                "A placa funciona na bancada e falha no cliente. Quase sempre a causa está no "
                "retorno de corrente, no aterramento, na separação de sinais ou no "
                "posicionamento dos componentes. A Taquionica projeta a placa e entrega os "
                "arquivos prontos para o fabricante que você escolher.",
                "Falar sobre minha placa",
                "Olá! Vim da página de Projeto de PCB da Taquionica e gostaria de falar sobre "
                "o projeto de uma placa.",
                IMG["auto4"],
                "Placa de acionamento e conversão de energia com filtragem e proteções",
                "Placa de acionamento e conversão de energia",
                "Eletrônica de potência",
            ),
            "problema": (
                "Sinais de que o problema está no layout, e não no componente",
                "Trocar componente resolve o sintoma até a próxima unidade. Quando a falha "
                "acompanha o projeto, ela está desenhada na placa.",
                [
                    ("alert", "A placa funciona na bancada e falha depois de montada no equipamento"),
                    ("board", "Ruído que só aparece com o equipamento inteiro em operação"),
                    ("radio", "Comunicação instável sem causa aparente no firmware"),
                    ("plug", "Aquecimento e componente que queima sempre no mesmo ponto"),
                    ("clock", "Revisão atrás de revisão sem convergir para uma explicação"),
                ],
            ),
            "oferta": (
                "Projetamos a placa. Quem fabrica é o seu fornecedor",
                "A Taquionica desenvolve esquemático, layout e roteamento, organiza os sinais, "
                "trata as fontes de ruído e prepara os arquivos para fabricação. Ela não "
                "fabrica nem monta placa: você recebe o pacote pronto e leva ao fabricante da "
                "sua escolha, sem ficar amarrado a nenhum fornecedor.",
            ),
            "entregas": (
                "O que entra em um projeto de PCB",
                "Cada etapa é aprovada antes da seguinte, e o escopo é fechado antes do "
                "trabalho começar.",
                [
                    ("Esquemático e escolha de componentes",
                     "Definição do circuito, dimensionamento e seleção de componentes com "
                     "olho em disponibilidade e custo de produção."),
                    ("Layout e roteamento",
                     "Empilhamento de camadas, plano de terra, retorno de corrente, separação "
                     "de sinal analógico e digital, e posicionamento térmico."),
                    ("Redução de ruído e proteções",
                     "Filtragem, desacoplamento, proteção de entradas e tratamento das fontes "
                     "de interferência que derrubam a placa em campo."),
                    ("Arquivos prontos para fabricar",
                     "Gerber, furação, lista de materiais e desenho de montagem, no formato "
                     "que o seu fabricante precisa receber."),
                ],
            ),
            "prova": (
                "Placas que continuam em operação anos depois de entregues",
                "A Taquionica desenvolve hardware e firmware com a mesma equipe, então layout "
                "e código são decididos juntos. É isso que evita a placa e o firmware "
                "discordarem em campo.",
                [
                    ("Desde 2001", "O responsável técnico projeta eletrônica de potência, "
                                   "instrumentação e comunicação."),
                    ("45+", "Equipamentos em operação contínua há mais de seis anos, com as "
                            "placas desenvolvidas aqui."),
                    ("Setores regulados", "Formação em medição e em ambiente onde erro de "
                                          "leitura vira perda de receita no mesmo dia."),
                ],
            ),
            "tecnologias": (
                "Os pontos que decidem se a placa funciona em campo",
                "Não existe layout bonito e errado. O que define a placa é como ela se "
                "comporta com o equipamento montado e ligado.",
                ["Retorno de corrente", "Plano de terra", "Separação de sinais",
                 "Eletrônica de potência", "Instrumentação", "Multicamadas",
                 "Redução de EMI", "Arquivos Gerber"],
            ),
            "projetos": (
                "Placas projetadas pela Taquionica",
                [
                    (IMG["auto4"], "Energia",
                     "Placa de acionamento e conversão de energia",
                     "Hardware com estágio de conversão, filtragem, proteções e interface de "
                     "comando para o inversor.",
                     ["Conversão DC/DC", "PCB de potência", "Filtragem", "Proteções"]),
                    (IMG["auto5"], "Instrumentação",
                     "Placa de aquisição e condicionamento de sinais",
                     "Amplificação configurável, ajuste de ganho e offset, sinalização por "
                     "LEDs e barramento de integração.",
                     ["Instrumentação", "Ganho e offset", "PCB"]),
                    (IMG["auto1"], "Automação industrial",
                     "Placa de controle para acionamento de motores",
                     "Hardware dedicado com estágio de potência para dois motores, proteções "
                     "e firmware de controle.",
                     ["Estágio de potência", "PCB", "Firmware"]),
                ],
            ),
            "faq": (
                "Dúvidas sobre projeto de PCB",
                [
                    ("Vocês fabricam ou montam a placa?",
                     "Não. A Taquionica projeta: esquemático, layout, roteamento e preparação "
                     "dos arquivos. Você recebe o pacote de fabricação pronto e leva ao "
                     "fabricante que preferir, o que mantém você livre para negociar preço e "
                     "prazo de produção."),
                    ("O que exatamente eu recebo no fim?",
                     "Esquemático, arquivos Gerber, arquivo de furação, lista de materiais e "
                     "desenho de montagem, no formato que o fabricante precisa. É o pacote "
                     "completo para produzir sem depender de nós."),
                    ("Vocês revisam uma placa projetada por outra equipe?",
                     "Sim, e é um dos pedidos mais comuns. Avaliamos o esquemático e o layout "
                     "existentes, identificamos as causas prováveis da falha e apresentamos as "
                     "correções na ordem em que devem ser feitas."),
                    ("Dá para contratar só o layout?",
                     "Dá. É possível contratar apenas o layout a partir de um esquemático que "
                     "você já tem, apenas a revisão de uma placa existente, ou o projeto "
                     "completo do circuito à preparação para fabricação."),
                    ("Fazem placa de potência e multicamadas?",
                     "Fazem. O projeto é dimensionado pelo que o circuito exige, incluindo "
                     "estágio de potência, conversão de energia e empilhamento de múltiplas "
                     "camadas quando a densidade ou a integridade de sinal pedem."),
                    ("Como funciona o prazo e o orçamento?",
                     "Os dois são definidos depois de entender o circuito e os requisitos, "
                     "porque o escopo muda muito de uma placa para outra. Você recebe prazo e "
                     "valor fechados antes de qualquer trabalho começar."),
                ],
            ),
            "contato": (
                "Traga a sua placa para uma avaliação",
                "Conte o que o circuito precisa fazer, ou o que está falhando na placa atual. "
                "A Taquionica avalia e indica o caminho, seja projetar do zero ou corrigir o "
                "que já existe.",
                "Falar sobre minha placa",
                "Olá! Vim da página de Projeto de PCB da Taquionica e gostaria de uma "
                "avaliação da minha placa.",
                "Projeto de PCB",
            ),
        },
    ]
