# Dias Investindo (diasinvestindo.com.br)

Portal publicado pelo GitHub Pages (repositório diasrendas-cyber/diasinvestindo-site, branch `main`, pasta raiz) a cada push. O arquivo `CNAME` mantém o domínio diasinvestindo.com.br; `.nojekyll` faz o Pages servir os arquivos como estão.

## Arquivos

- `noticias.json`: **a base de todas as notícias**, da mais nova para a mais antiga. É o único arquivo de conteúdo que a tarefa diária edita.
- `index.html`: a página inicial (página única com seções). O bloco `site-data` é preenchido pelo gerador; não edite à mão.
- `noticias/<slug>/index.html`, `noticias/index.html`, `artigos/`, páginas de categoria, `privacidade/`, `404.html`, `sitemap.xml`, `robots.txt`, `feed.xml` e `busca.json` (índice da busca da home): **gerados** por `tools/gerar.py`. Não edite à mão.
- `conteudo/artigos/*.md`: os artigos (cabeçalho entre `---` e corpo em Markdown simples). O nome do arquivo é o endereço permanente.
- `assets/estilo.css`, `assets/arte.js` (ilustrações), `assets/comum.js` (formulário de e-mail, anúncios e preço do Bitcoin ao vivo na régua): compartilhados por todas as páginas.
- Cotações ao vivo, consultadas pelo navegador do leitor e sempre com a fonte exibida: Bitcoin na régua (CoinGecko; se não responder, o campo some) e o Conversor de Moedas (PTAX de venda do Banco Central). Nenhuma delas é gravada em `noticias.json`.
- `verificacao/AAAA-MM-DD.md`: registro de checagem de cada edição.
- `diana/index.html`: página de vendas da Diana, **gerada** por `tools/gerar.py` a partir de `conteudo/diana.html` (texto), `tools/diana.py` (CONFIG: preço, plano, destino dos botões, GA4; FAQ e dados estruturados), `assets/diana.css` e `assets/diana.js` (abas, lista de espera e eventos). Página sem anúncios. A lista de espera grava na tabela `lista_espera` do Supabase da Diana (só inserção pela chave pública).
- `diana/politica-de-privacidade/`: Política de Privacidade da Diana, escrita à mão (não gerada), sem anúncios e sem cookies.
- `ads.txt`: autorização do Google AdSense (editor `pub-2224422141615380`).
- Blocos de anúncio fixos (AdSense): faixa do topo = bloco `8353558655` ("Faixa topo 970x90"); coluna lateral = bloco `7385972248` ("Lateral 160x600"). IDs em `assets/comum.js` (constante `ADSENSE`); os espaços são marcados com `data-ad-slot-name="faixa"` e `"lateral"`. O quadro "Apoio/Anuncie" (160 × 160) continua reservado para patrocínio direto.
- `tools/validar.py` (valida `noticias.json`), `tools/gerar.py` (gera as páginas), `tools/preview.py` (prévia autocontida), `tools/teste.js` (testes; `npm install && npm test`).

## Segurança

- O GitHub Pages não aceita cabeçalhos HTTP próprios. Por isso as políticas vão em `<meta>`: `Content-Security-Policy` básica nas páginas com AdSense (`CSP_BASICA` em `tools/gerar.py`, e escrita à mão no `index.html`), CSP rígida com hash dos scripts embutidos na `/diana/` (`tools/diana.py`, calculada sozinha a cada geração) e `referrer` em todas.
- `assets/comum.js` impede que o site publicado seja exibido dentro de moldura (iframe) de outro site (clickjacking).
- Ao incluir um script ou serviço externo novo na `/diana/`, acrescente o domínio em `_csp()` de `tools/diana.py`, ou ele será bloqueado.

## Regra de ouro: nenhum dado sem checagem

O portal trata de finanças: **um número errado é pior do que nenhum número.**

1. **Pesquise antes de escrever ou ilustrar.** Leia a matéria completa (não só o trecho da busca).
2. **Todo número** (texto, régua e ilustração) precisa estar confirmado em **duas fontes independentes**
   ou em **uma fonte oficial** (Banco Central, IBGE, B3, Tesouro, CVM, comunicado da própria empresa).
   - Selic e decisões do Copom: bcb.gov.br (comunicados do Copom).
   - Quando duas fontes divergirem, busque uma terceira; publique o valor confirmado por pelo menos duas e registre a divergência.
   - Inflação (IPCA): IBGE. Câmbio Ptax: Banco Central. Ibovespa: B3 ou fechamento publicado por InfoMoney/Valor.
3. **Séries no tempo** (ex.: a Selic mês a mês) são montadas a partir das decisões oficiais, ponto a ponto.
   Não preencha meses por estimativa; o valor de cada mês é o vigente no fim do mês.
4. Se um número não puder ser confirmado, **não o use**: troque a ilustração por `cena` (sem números)
   e escreva o texto sem esse dado.
5. Registre a checagem em `verificacao/AAAA-MM-DD.md` (um arquivo por edição, no formato dos anteriores): cada número usado,
   onde aparece (texto, régua ou ilustração) e as URLs que o confirmam. Esse arquivo vai no mesmo commit.

## Atualização diária das notícias

As notícias **se acumulam**: cada edição diária acrescenta **4 notícias** (mínimo 3, se não houver 4 com dados confirmados) **no topo** da lista `noticias`
de `noticias.json`, sem apagar as anteriores. Também atualiza `atualizado` e `ticker` (Selic, Ibovespa, dólar e data do pregão; o Bitcoin é ao vivo e não entra aqui).
O gerador cria a página própria de cada notícia (`/noticias/<slug>/`), o arquivo `/noticias/` (por mês, com filtro por editoria),
a home (4 destaques, o bloco "Mais notícias" com as 4 seguintes e a lista com as 10 mais recentes), o índice da busca, o sitemap e o RSS.

```json
{
  "atualizado": "dd/mm/aaaa",
  "ticker": {
    "selic": "13,75%",
    "ibov": "166.191", "ibovVar": "-0,82%",
    "dolar": "R$ 5,489", "dolarVar": "+0,67%",
    "data": "dd/mm/aaaa"
  },
  "noticias": [
    {
      "editoria": "Juros | Mercados | Economia | Inteligência Artificial | Produtividade | Negócios",
      "data": "dd/mm/aaaa (dia do fato)",
      "publicado": "dd/mm/aaaa (dia da edição; igual a atualizado)",
      "titulo": "Manchete com verbo e fato principal",
      "resumo": "Uma frase que explica a notícia.",
      "texto": ["Parágrafo 1: o fato.", "Parágrafo 2: causas e contexto.", "Parágrafo 3: próximos passos e consequências."],
      "bolso": "Opcional: uma frase sobre o impacto no bolso do leitor, sem recomendação de investimento.",
      "arte": { "...": "ver abaixo" },
      "fontes": [{ "nome": "Veículo", "url": "https://endereço-da-matéria" }]
    }
  ]
}
```

Regras: 4 notícias novas por edição (mínimo 3), inseridas no topo; não altere nem remova notícias antigas
(o campo `slug` é criado pelo gerador e nunca deve mudar, porque é o endereço permanente da página); `texto` com exatamente 3 parágrafos de pelo menos 200 caracteres cada,
escritos com palavras próprias (nunca copiar trechos das fontes); variações sempre com sinal (`+0,67%`, `-0,82%`).

### Ilustração (`arte`) de cada notícia

A ilustração é desenhada pelo site a partir dos dados da própria notícia. Escolha o tipo que melhor mostra o fato:

| tipo | quando usar | campos |
|---|---|---|
| `linha` | evolução no tempo (juros, inflação, preço) | `titulo`, `pontos: [["rótulo", número], ...]`, `fonte`, opcionais `degraus: true`, `rotular: true`, `sufixo`, `decimais` (casas nos rótulos; 0 para pontos do Ibovespa), `destaque: "texto curto"` |
| `indicador` | um número do dia (índice, cotação, PIB) | `rotulo`, `valor` (texto), `variacao` (`"+1,2%"`), opcional `secundarios: [{rotulo, valor, variacao}]` (até 2) |
| `barras` | comparação de valores | `titulo`, `barras: [{rotulo, valor (número), destaque?: true}]` (1 a 4), opcionais `prefixo`, `sufixo`, `nota`, `subtitulo` (premissas em letra legível), `decimais` (ex.: 2 para R$ 26.250,85) |
| `comparacao` | dois valores lado a lado: esperado x realizado, antes x depois | `titulo`, `a: {rotulo, valor (texto), nota?}`, `b: {rotulo, valor, nota?}` (b fica em destaque), opcionais `variacao`, `nota` |
| `faixa` | um valor dentro de uma faixa de referência (ex.: inflação e o intervalo da meta) | `titulo`, `valor` (número), `min`, `max`, opcionais `faixa_min`, `faixa_max`, `alvo`, `rotulo_alvo`, `rotulo_faixa`, `rotulo`, `sufixo`, `decimais`, `nota` |
| `rosca` | partes de um todo (até 4) | `titulo`, `partes: [{rotulo, valor (número)}]` (2 a 4), opcionais `sufixo`, `centro` |
| `cena` | notícia sem número central | `titulo` curto (opcional) |
| `planilha` | só em artigos: planilha de receitas e despesas; a última linha (saldo) é calculada automaticamente | `titulo`, `linhas: [{item, grupo (Receita, Essencial, Escolha, Futuro), valor (número), tipo: receita ou despesa}]` (até 7), opcionais `colunas`, `saldo` (rótulo da última linha) |
| `imagem` | só em artigos: imagem pronta em 16:9 salva em `assets/img/` (ex.: logomarca do Tesouro Direto no artigo de Tesouro Direto) | `src` (`/assets/img/arquivo.png`), `alt`, `tema` (usado se a imagem falhar) |

Todos os tipos levam `tema`, o desenho de fundo:
`juros`, `fiscal`, `ia`, `bolsa`, `cambio`, `inflacao`, `energia`, `tecnologia`, `imoveis`, `emprego`, `cripto`, `tesouro` (título público: certificado, cupons e moedas), `planilha` (planilha com setas de entrada e saída de dinheiro).

**Varie as ilustrações** (o validador confere): na mesma edição, cada notícia usa um tipo diferente;
a notícia de abertura não repete o tipo da abertura da edição anterior; e no máximo 2 tipos se repetem de um dia para o outro.
Exemplo: se ontem houve `barras`, hoje prefira `comparacao`, `faixa` ou `rosca` para dados equivalentes.

**Nunca invente dados.** Todo número da ilustração precisa estar na matéria ou em fonte oficial,
e as ilustrações com dados (todos os tipos, exceto `cena`) levam o campo `fonte`, exibido na imagem
(ex.: `"fonte": "Fonte: InfoMoney, fechamento de 05/11/2026"`).

Séries no tempo usam um ponto por período, sem pular meses: para a Selic, um ponto por mês com a taxa
vigente no fim do mês, `degraus: true` e `rotular: true` (escreve o valor em cada mudança), com `sufixo: "%"`.
Exemplo conferido nas decisões do Copom de 2026: jan 15; fev 15; mar 14,75; abr 14,5; mai 14,5; jun 14,25;
jul 14,25; ago 14; set 13,75; out 13,75; nov 13,75.

### Gráfico da notícia (`grafico`, recomendado)

Além da `arte` (que continua obrigatória e serve de reserva), cada notícia com
número confirmado ganha um gráfico pronto em PNG, feito com o método Storytelling with Data
(skill "graficos-noticias-swd"). Quando existe, ele substitui a `arte` em todos os lugares onde a notícia aparece (página da notícia, destaques, "Mais notícias", lista e leitor da home) e vira a
imagem de compartilhamento (og:image).

- Script da edição: `graficos/AAAA-MM-DD.py`, usando `tools/grafico.py` (`quadro`, `limpar`, `salvar`, `br` e as cores).
  Rodar da raiz: `python3 graficos/AAAA-MM-DD.py`. Gera `assets/img/noticias/AAAA-MM-DD-N.png` (1600x900), N = ordem da notícia.
- Campo: `"grafico": {"src": "/assets/img/noticias/AAAA-MM-DD-N.png", "alt": "o que o gráfico mostra e a conclusão", "fonte": "Fonte: ..."}`.
- O validador exige arquivo existente, `alt` com 30+ caracteres e `fonte` começando com "Fonte".
- Só números já conferidos em `verificacao/AAAA-MM-DD.md`. Notícia sem número confirmado fica sem `grafico` (usa `cena`).

**Conte uma história, não só compare barras** (regra de 26/11/2026, a pedido do editor). Antes de desenhar, defina o enredo
(antes → virada → agora → o que vem) e escolha o formato que o conta:
- linha com fases anotadas: blocos curtos de texto sobre cada trecho ("Set–Nov: dólar sobe 8%", "23/11: toca R$ 6"), só os pontos de virada rotulados;
- linha atravessando uma faixa de referência sombreada (meta, teto, faixa recomendada), destaque só no trecho fora dela;
- inclinação com várias categorias, rótulo e valor dos dois lados, texto explicativo colorido com a cor da linha (sem legenda);
- colunas 100% empilhadas no tempo, só a parte que importa colorida e rotulada;
- área ou linha com eventos anotados (linha-guia + "quando" em negrito + "por quê");
- pequenos múltiplos; linha do tempo de próximos passos com o "hoje" marcado; grade de quadrados para proporções ("1 em cada 9").

**Inflação e meta** (regra de 27/11/2026, a pedido do editor):
- Valor x meta de inflação: use `banda_meta()` de `tools/grafico.py`. Três linhas horizontais: **teto em cima, meta no meio, piso embaixo** (hoje 4,5%, 3% e 1,5%).
  Valor **dentro** da faixa: faixa sombreada e ponto em **verde**. Valor **fora** (acima do teto ou abaixo do piso): só a região de fora sombreada e o ponto em **vermelho**.
- Tendência mensal (IPCA, IPCA-15, IGP-M etc.): **no mínimo 3 meses, de preferência 6**, cada mês conferido (publicação do IBGE ou duas fontes). Dois pontos (antes x depois) não mostram tendência.

Composição: título de ação alinhado à esquerda com subtítulo, rótulos e fonte; rótulo direto no dado e texto colorido no lugar de legenda;
1 a 3 blocos de texto explicativo dentro do gráfico; nada redundante (categoria "Todos", decimais à toa, eixo quando os valores já estão rotulados).

Variedade obrigatória por edição: **no máximo 1 gráfico de barras** (qualquer tipo); **pelo menos 2 com eixo de tempo ou antes/depois**;
**pelo menos 1 com texto de fases ou eventos dentro do gráfico**. Para séries, reaproveite os fechamentos já conferidos em `graficos/*.py`
e `verificacao/*.md`; sem série confirmada, prefira inclinação, faixa, linha do tempo ou grade de quadrados a uma barra.

### Passos

```
python3 graficos/AAAA-MM-DD.py            # gráficos da edição (antes de validar)
python3 tools/validar.py                  # precisa terminar com OK
python3 tools/gerar.py                    # gera páginas, arquivo, home, sitemap e RSS
npm install && npm test                   # testes (se o npm estiver disponível)
git add -A && git status --short          # devem aparecer: noticias.json, index.html, páginas geradas e o novo verificacao/AAAA-MM-DD.md
git commit -m "Notícias de dd/mm/aaaa" && git push origin main
python3 tools/preview.py index.html /tmp/preview.html   # para republicar a prévia no Claude
```
