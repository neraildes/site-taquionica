# Conectar o Planejador de Palavras-Chave direto no Claude

O servidor MCP já está baixado e configurado. Falta só preencher as credenciais, que só
você consegue gerar, porque elas saem da sua conta do Google.

Arquivos já criados:

- `mcp-keyword-planner\kwp-mcp-win-x64.exe`: o servidor, versão v0.1.1 do projeto
  [google-keyword-planner-mcp](https://github.com/ncosentino/google-keyword-planner-mcp).
  É um binário de terceiros, código aberto. Ele não roda até ter credencial válida.
- `.mcp.json` na raiz do workspace: a configuração, com seis campos marcados como
  `PREENCHER_`.

## O que preencher, e onde pegar cada coisa

### 1. GOOGLE_ADS_DEVELOPER_TOKEN

É o campo que demora, então comece por ele.

1. Você precisa de uma **conta de administrador (MCC)**. Se ainda não tem, crie em
   https://ads.google.com/home/tools/manager-accounts/ e vincule a conta da Taquionica
   a ela.
2. Dentro da MCC, vá em `Ferramentas > Configuração > Central de API`, ou direto em
   https://ads.google.com/aw/apicenter
3. Solicite o token. Ele nasce em **modo de teste**, que só acessa contas de teste e não
   serve para o que queremos.
4. Clique em solicitar **acesso básico**. O Google faz uma análise e pede uma descrição
   do uso. Descreva algo honesto e simples: uso interno para pesquisa de palavras-chave
   e gestão de campanhas dos clientes da agência.

A aprovação costuma levar de um a alguns dias úteis. É o único passo que não depende de
nós dois.

### 2. GOOGLE_ADS_CLIENT_ID e GOOGLE_ADS_CLIENT_SECRET

1. Acesse https://console.cloud.google.com/ e crie um projeto, ou use um existente.
2. Em `APIs e serviços > Biblioteca`, busque **Google Ads API** e clique em ativar.
3. Em `APIs e serviços > Credenciais`, clique em `Criar credenciais > ID do cliente
   OAuth`, tipo **App para computador**.
4. Copie o ID do cliente e a chave secreta.

### 3. GOOGLE_ADS_REFRESH_TOKEN

O repositório do servidor traz um script de autorização em PowerShell. Ele abre o
navegador, você entra com a conta Google que administra o Ads, autoriza, e o script
devolve o refresh token. Rode uma vez só, e guarde o valor.

### 4. GOOGLE_ADS_CUSTOMER_ID e GOOGLE_ADS_LOGIN_CUSTOMER_ID

Os dois são os números de dez dígitos que aparecem no canto superior da tela do Google
Ads, sem os hifens.

- `GOOGLE_ADS_CUSTOMER_ID`: a conta da Taquionica.
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID`: a conta administradora (MCC).

## Depois de preencher

1. Salve o `.mcp.json`.
2. Reinicie o Claude Code para ele carregar o servidor.
3. Me peça o volume. Eu consulto direto e devolvo a lista ordenada por busca mensal, com
   concorrência e faixa de lance de topo de página, e já reorganizo os quatro grupos da
   campanha em cima desse número.

## Um aviso que muda a expectativa

Conta do Google Ads **sem gasto ativo recebe faixa, não número**. Em vez de "2.400 buscas
por mês", vem "1 mil a 10 mil". Isso vale tanto pela API quanto pela tela do Planejador,
porque é a mesma fonte. O número fechado aparece depois que a conta começa a investir.

Ou seja: subir a campanha de teste não é só o objetivo final, é também o que destrava a
precisão do dado para a segunda rodada.

## O caminho de dois minutos, enquanto o token não sai

Não precisa esperar a aprovação para decidir as palavras-chave:

1. Google Ads, `Ferramentas > Planejamento > Planejador de palavras-chave`.
2. `Descobrir novas palavras-chave`.
3. Local **Brasil**, idioma **português**.
4. Cole os quatro termos de uma vez: automação industrial, iot industrial,
   indústria 4.0, manutenção industrial.
5. Botão de download, formato CSV.
6. Salve o arquivo dentro da pasta do projeto e me avise.

Eu leio o CSV aqui, ordeno por volume real, comparo com a intenção de compra de cada
termo e refaço a priorização dos quatro grupos. Mesmo resultado, sem esperar o Google
aprovar nada.
