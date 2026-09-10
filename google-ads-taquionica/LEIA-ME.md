# Taquionica: campanha de pesquisa no Google Ads

Pacote pronto para subir sem digitar nada dentro do Google Ads. Você importa os CSVs da
pasta `import` no Google Ads Editor, revisa e publica.

Site de destino: https://taquionica.com.br
Conversões instaladas: tag `AW-18346942371`, com eventos de clique em WhatsApp, e-mail,
telefone e envio de formulário.

| Item | Valor |
|------|-------|
| Campanhas | 3, todas entram pausadas |
| Grupos | 14 |
| Termos | 180, em 350 critérios |
| Orçamento | R$ 100 por dia no total |
| Lance | Manual, com teto por grupo entre R$ 3 e R$ 5,50 |
| Horário | Segunda a sexta, das 8h às 18h, cadastrado na mão |
| Localização | Brasil |
| Rede | Pesquisa apenas |

---

## O que mudou nesta versão, e por quê

A versão anterior era uma campanha só, com quatro grupos e 86 termos, teto de lance em
R$ 9 e quatro páginas de destino. Ela tinha três problemas que explicam pouco clique e
pouco lead.

### 1. O teto de lance estava muito acima do mercado

O CPC real da conta fica entre R$ 4,28 e R$ 5. Teto de R$ 9 não faz o clique custar 9,
porque o leilão do Google cobra o mínimo necessário para manter a posição. Mas ele faz a
campanha ganhar leilão em posição mais alta, e posição mais alta custa mais caro por
clique. Com R$ 100 por dia, isso é a diferença entre comprar 20 cliques e comprar 28.

Os tetos agora ficam entre R$ 3 e R$ 6,50, cada um calibrado pelo valor do lead daquele
grupo. Os mais altos, R$ 5,50, ficam nos grupos em que a página de resultados do Google
devolve fornecedor e não artigo: produtos eletrônicos, firmware, monitoramento remoto,
retrofit e coleta de dados.

### 2. Não havia volume qualificado para gastar R$ 100 por dia

O caminho errado seria afrouxar a correspondência, porque isso compra busca ruim. O
caminho certo é ampliar a superfície de busca qualificada. Entraram quatro temas novos,
todos serviços que a empresa já presta e que a campanha simplesmente ignorava:

| Tema novo | Por que ele traz lead |
|-----------|----------------------|
| Retrofit e modernização de máquinas | Dor imediata, orçamento fácil de aprovar, porque a alternativa é comprar máquina nova |
| Coleta de dados de máquinas e produção | É a tradução honesta de "indústria 4.0". O gerente industrial não compra conceito, compra o número que hoje não consegue medir |
| Diagnóstico e consultoria técnica | Compra de menor compromisso do catálogo, então converte mais fácil e alimenta o funil dos outros grupos |
| Aplicativos e dashboards | A empresa vende isso desde sempre e a campanha não tinha uma única palavra-chave para o assunto |

### 3. As páginas não tinham formulário

Esta é a mudança de maior impacto em volume de lead do pacote inteiro, e nada tem a ver
com o Google Ads.

Até agora, a única saída das landing pages era um botão de WhatsApp e um link mandando o
visitante de volta para a home preencher o formulário lá. Cada passo desses perde gente,
e quem não usa WhatsApp para tratar de trabalho simplesmente ia embora.

Agora todas as oito páginas têm formulário próprio, com nome, empresa, telefone, e-mail,
porte da operação e a descrição do projeto. Ao enviar, a conversa segue no WhatsApp já com
o cenário escrito, então o contato chega qualificado em vez de chegar como "oi". O evento
de conversão dispara no envio, sem código extra.

---

### Um tema que foi montado e removido

Chegou a existir um grupo de equipamento médico e eletromédico, com página própria, apoiado
na linha do site que fala dos doze anos do responsável técnico em equipamento oftálmico sob
requisitos da Anvisa. O cliente confirmou que isso é histórico dele, não linha de serviço da
empresa hoje, e o tema saiu inteiro: grupo, página, sitelink e palavras-chave.

Fica registrado porque a lição vale para o próximo tema: biografia no site não é o mesmo que
catálogo. Antes de transformar uma credencial em grupo de anúncios, confirmar que a empresa
vende aquilo hoje.

---

## As três campanhas

A separação existe por um motivo só: proteger o orçamento. Os termos de cabeça do nicho
têm o maior volume e a pior intenção. Dentro da mesma campanha eles engoliriam a verba dos
termos que trazem comprador.

### `TQ | Pesquisa | Projetos de Engenharia`, R$ 45 por dia

O núcleo do negócio. São os termos em que a página de resultados do Google devolve
fornecedor, não artigo nem vaga de emprego.

| Grupo | Página | Teto |
|-------|--------|------|
| Produtos Eletrônicos e Hardware | `/desenvolvimento-produtos-eletronicos` | R$ 5,50 |
| Projeto de PCB | `/desenvolvimento-produtos-eletronicos` | R$ 5,00 |
| Firmware e Embarcados | `/desenvolvimento-firmware` | R$ 5,50 |
| Diagnóstico e Consultoria Técnica | `/diagnostico-tecnico` | R$ 4,50 |

### `TQ | Pesquisa | Indústria Conectada`, R$ 40 por dia

O que a indústria de porte procura quando quer enxergar ou modernizar o que já tem
instalado.

| Grupo | Página | Teto |
|-------|--------|------|
| Monitoramento Remoto e Telemetria | `/monitoramento-remoto-iot` | R$ 5,50 |
| IoT Industrial | `/monitoramento-remoto-iot` | R$ 4,50 |
| Coleta de Dados e Produção | `/coleta-de-dados-de-maquinas` | R$ 5,50 |
| Manutenção Preditiva | `/monitoramento-remoto-iot` | R$ 4,50 |
| Retrofit e Modernização de Máquinas | `/retrofit-de-maquinas` | R$ 5,50 |
| Aplicativos e Dashboards | `/aplicativo-para-equipamentos` | R$ 4,50 |
| Telemetria Agrícola e Solar | `/monitoramento-remoto-iot` | R$ 4,50 |

### `TQ | Pesquisa | Termos Amplos`, R$ 15 por dia

Volume alto, intenção pior, leilão disputado por integrador de CLP e por consultoria de
gestão. Ficam isolados aqui para poderem ser pausados sozinhos.

| Grupo | Página | Teto |
|-------|--------|------|
| Automação Industrial | `/automacao-industrial` | R$ 3,50 |
| Indústria 4.0 | `/coleta-de-dados-de-maquinas` | R$ 3,00 |
| Descoberta Ampla | `/` | R$ 3,00 |

Repare que o grupo de Indústria 4.0 aponta para a página de coleta de dados, e não para a
de automação. Quem procura "indústria 4.0" e vai comprar alguma coisa quer o dado da
máquina. Mandar essa busca para uma página de automação genérica era parte do motivo de o
termo não converter.

---

## A correspondência ampla, e por que ela existe em um grupo só

Quase todos os 180 termos entram em frase e em exata. Correspondência ampla aparece em um
único lugar: o grupo `Descoberta Ampla`, com sete termos centrais, teto de R$ 3 e dentro
da campanha de R$ 15 por dia. O pior caso possível é perder R$ 15 num dia.

Ele não existe para vender. Existe para descobrir, no relatório de termos de pesquisa, que
buscas reais o mercado faz e que ninguém previu. O que aparecer de bom vira palavra-chave
em frase num dos grupos qualificados, o que aparecer de ruim vira negativa.

Ampla em toda a conta, com lance manual e sem histórico de conversão, gastaria os R$ 100
num dia em busca desqualificada. É por isso que ela está contida.

---

## As duas camadas de negativas

A **lista global**, com 275 termos, corta o que não serve para nada: curso, emprego,
download, uso residencial, conserto de eletrodoméstico, pesquisa acadêmica.

As **negativas por grupo**, 903 no total, fazem duas coisas. Cortam o lixo específico do
tema e, além disso, cada grupo recebe como negativa exata os termos dos grupos irmãos, o
que força cada busca a cair no grupo certo, com o anúncio e a página certos. É isso que
torna o relatório legível no fim da semana.

Três grupos têm negativas que decidem se eles funcionam ou queimam verba:

- **Retrofit.** No Brasil, "retrofit" sozinho quase sempre significa reforma de fachada de
  prédio. Sem bloquear fachada, predial, elevador, edifício, imóvel, iluminação e LED, o
  grupo traria construtora.
- **Coleta de dados.** É também o termo da metodologia de pesquisa acadêmica. Sem bloquear
  coleta qualitativa, instrumento de coleta, TCC e afins, o grupo traria estudante.
- **Aplicativos.** "Desenvolvimento de aplicativo" sozinho é o termo mais disputado do
  Brasil em software. Sem bloquear delivery, app de banco, "criar app grátis" e "quanto
  custa um aplicativo", o grupo traria quem quer um app de celular qualquer.

---

## Como os anúncios foram montados

Cada grupo tem um anúncio responsivo com 15 títulos e 4 descrições, em três camadas.

**Relevância.** Os seis primeiros títulos carregam o termo do grupo e o benefício dele. O
título 1 está fixado na posição 1, então o anúncio sempre abre com o termo buscado.
Fixamos só ele: fixar vários faz o Google parar de testar combinações e derruba a Eficácia
do anúncio.

**Prova.** "Engenharia Desde 2001", "45 Equipamentos em Campo", "6 Anos Sem Interrupção".
Número específico convence mais que adjetivo, e esses vêm do histórico real da empresa.

**Objeção.** "Um Só Fornecedor Técnico", "Escopo e Prazo Fechados", "Projeto de Grande
Porte". São as dúvidas que travam quem contrata engenharia sob medida, e a última responde
diretamente a quem tem projeto grande e desconfia do tamanho do fornecedor.

Se o Editor não reconhecer a coluna `Headline 1 position`, ela é ignorada e a fixação se
faz em quatro cliques: selecione o anúncio, clique no alfinete ao lado do título 1 e
escolha posição 1.

---

## Arquivos, na ordem de importação

| # | Arquivo | O que cria |
|---|---------|-----------|
| 1 | `1-campanhas.csv` | 3 campanhas, pausadas, com orçamento e idioma |
| 2 | `11-locais.csv` | Brasil como localização das três |
| 3 | `2-grupos.csv` | 14 grupos com CPC máximo por grupo |
| 4 | `3-keywords.csv` | 350 critérios: frase, exata e 7 em ampla |
| 5 | `4-negativas-por-grupo.csv` | 903 negativas no nível do grupo |
| 6 | `5-anuncios.csv` | 14 anúncios responsivos |
| 7 | `6-extensoes-sitelinks.csv` | 7 sitelinks por campanha |
| 8 | `7-extensoes-chamadas.csv` | Extensão de chamada com o (16) 99366-8447 |
| 9 | `8-extensoes-destaques.csv` | 8 frases de destaque |
| 10 | `9-extensoes-snippets.csv` | Dois snippets estruturados |

### A programação de anúncios não vai por arquivo

O Google Ads Editor em português ignora programação de anúncios vinda de CSV. Foram duas
tentativas, as duas recusadas: com a coluna `Bid Adjustment` ele tratou cada linha como
linha de campanha e reprovou o `0%` no ajuste de lance de dispositivos móveis; sem essa
coluna, parou de acusar erro mas ignorou as 15 linhas do mesmo jeito.

Cadastre na mão, é rápido. Para cada uma das três campanhas, no Editor: selecione a
campanha, `Palavras-chave e segmentação` > `Programação de anúncios` > `Adicionar`,
`Segunda a sexta`, `08:00` às `18:00`, ajuste de lance em branco. O passo a passo também
está em `PASSO-EXTRA-programacao-de-horario.txt`.

Não é obrigatório para subir a campanha. Sem programação ela roda 24 horas por dia, sete
dias por semana, o que não quebra nada, só espalha a verba por horário pior.

Fora da numeração, a lista global de negativas:

- `negativas-lista-global.csv`: os 275 termos como negativa de campanha, para o Editor.
- `PASSO-EXTRA-negativas-para-colar-na-web.txt` (fora da pasta `import`): os mesmos 275, um
  por linha e já entre aspas, para colar em
  `Ferramentas > Biblioteca compartilhada > Listas de palavras-chave negativas`. Melhor no
  longo prazo, porque a lista passa a valer para campanhas futuras.

Tudo que está na pasta `import` se importa, na ordem do número. Os dois arquivos
`PASSO-EXTRA-*.txt` ficam um nível acima justamente porque não são importação: são passos
que se fazem na interface. Se você tentar importar um `.txt`, o Editor devolve "Cabeçalho
CSV não informado" e desabilita o botão.

### Passo a passo no Editor

1. Abra o Google Ads Editor e baixe a conta em `Obter dados recentes`.
2. Menu `Conta` > `Importar` > `Importar de arquivo`.
3. Selecione o CSV da vez e confira a prévia.
4. Se alguma coluna não for reconhecida, use o mapeamento manual. Os cabeçalhos estão em
   inglês porque é o formato que o Editor reconhece automaticamente na maioria das
   instalações.
5. Repita para os dez arquivos, sempre na ordem.
6. Clique em `Verificar alterações`, corrija o que aparecer e só então em `Publicar`.

---

## Duas configurações que o Editor liga sozinho e precisam ser desligadas

Estas não vêm em nenhum CSV. O Editor as ativa por padrão em toda campanha nova, e as
duas prejudicam uma campanha de Pesquisa com orçamento pequeno. Selecione as três
campanhas juntas com `Ctrl+clique` e mude no painel da direita, de uma vez só.

**`Incluir Rede de Display` para Desativado.** É a que mais queima verba. Com ela ligada, a
campanha de Pesquisa também exibe anúncio em sites, blogs e apps da Rede de Display. É
clique barato em volume alto, de quem não estava procurando nada. Com R$ 15 por dia, a
Display sozinha consome a campanha de Termos Amplos inteira, e o relatório de termos de
pesquisa fica ilegível.

**`Incluir parceiros de pesquisa` para Desativado.** Não é lixo como a Display, são sites
que usam a busca do Google, mas a intenção é mais fraca e o dado fica misturado. Nas
primeiras semanas o objetivo é saber o que a busca do Google entrega, limpo. Depois de três
ou quatro semanas dá para ligar e comparar.

---

## Antes de ativar

1. **Pause ou remova a campanha antiga `TQ | Pesquisa | Teste`.** As campanhas novas têm
   nomes diferentes, então a importação não sobrescreve a antiga, ela cria as três ao lado.
   Se as duas rodarem juntas, elas disputam o mesmo leilão e o custo sobe.
2. Publique o site com as páginas novas antes de ativar. Quatro dos catorze grupos apontam
   para páginas que só existem depois do deploy, e anúncio com URL quebrada é reprovado.
3. Confirme que a ação de conversão da tag `AW-18346942371` está marcada como conversão
   principal. Sem isso o teste não mede nada.
4. Revise a lista global de negativas e remova o que não fizer sentido para a operação.
5. As campanhas entram pausadas. Ative só depois de conferir.

---

## O que esperar, sem otimismo

Com R$ 100 por dia e CPC entre R$ 4,28 e R$ 5, a conta compra algo entre 600 e 700 cliques
por mês. Esse número sobe conforme o Índice de Qualidade melhora, porque agora cada grupo
tem uma página que fala exatamente o mesmo que o termo, e é razoável esperar o CPC médio
cair para a faixa de R$ 3 a R$ 4 nos grupos qualificados depois de duas ou três semanas.

O que **não** dá para prometer é que os R$ 100 sejam gastos por inteiro desde o primeiro
dia. Esse vocabulário é B2B e de volume baixo por natureza. Se ao fim da primeira semana a
campanha estiver entregando menos que a verba, o ajuste certo não é abrir a
correspondência: é subir o orçamento da campanha de Termos Amplos e promover a frase os
termos que o grupo `Descoberta Ampla` tiver revelado.

Também vale dizer o que a estrutura assume: que o cliente quer projeto grande, de indústria
e de empresa de porte. Isso empurra a seleção para termos de volume menor e intenção
melhor. Um conjunto montado para volume puro traria mais clique e menos reunião.

---

## Como ler o resultado

Olhe o **relatório de termos de pesquisa** antes de qualquer outra métrica. Com verba de
teste o objetivo não é vender, é descobrir quais buscas reais chegaram e qual dos serviços
gera contato. Termo ruim que apareceu vira negativa nova. O grupo que trouxe contato ganha
a verba da próxima rodada.

Dois pontos merecem atenção:

- **"programação esp32" e "firmware esp32"** têm bom volume, mas parte vem de maker e
  estudante. As negativas globais cortam curso, tutorial e faça você mesmo. Se ainda assim
  vierem sujos no relatório, pause os dois.
- **O grupo `Descoberta Ampla`** vai trazer lixo por definição. Isso não é defeito, é a
  função dele. Leia o relatório dele toda semana e mova o que for bom para os grupos
  qualificados.

Não espere conversão suficiente para lance automático nessa fase. CPC manual continua
sendo o certo até acumular algo entre 15 e 30 conversões. Depois disso, o caminho é
Maximizar conversões com CPA alvo, começando pela campanha de Projetos de Engenharia.

---

## Regenerar os arquivos

| Script | O que faz |
|--------|-----------|
| `gerar_campanha.py` | Gera a pasta `import`, as três campanhas que vão ao ar |
| `conferir.py` | Confere `import` antes de importar: negativa que anula palavra-chave, URL inexistente, termo repetido entre grupos |
| `build_lps.py` | Gera as cinco páginas novas, instala o formulário nas nove e atualiza o `sitemap.xml` |
| `gerar_ads.py` | Só a estrutura ampla de reserva, em `import-completo`. Serve de biblioteca para o `gerar_campanha.py` |
| `build_lp1.py` | Reescreve a página de produtos eletrônicos. Legado, mantido por referência |

A ordem quando algo mudar:

```
python gerar_campanha.py
python conferir.py
python build_lps.py
```

Para mudar orçamento ou teto de lance, edite os valores em `gerar_campanha.py`: o
orçamento fica na lista `CAMPANHAS`, o teto no terceiro argumento de cada `g(...)`.

A pasta `import-completo` guarda uma estrutura ampla de reserva, com 6 campanhas e 16
grupos. Ela não deve ser importada agora. Existe para o caso de a verba crescer muito e a
conta precisar de uma separação ainda mais granular.
