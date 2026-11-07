# Dias Investindo (diasinvestindo.com.br)

Site de página única publicado pela Netlify a cada push na branch `main`.

## Arquivos

- `index.html`: o site inteiro (HTML, CSS, JavaScript e os dados das notícias).
- `ads.txt`: autorização do Google AdSense (editor `pub-2224422141615380`).
- `netlify.toml`: configuração de publicação.
- `tools/validar.py`: valida o bloco de notícias antes de publicar.
- `tools/preview.py`: gera a versão de prévia para o artifact do Claude.

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
5. Registre a checagem no arquivo `verificacao.md` (substituído a cada atualização): cada número usado,
   onde aparece (texto, régua ou ilustração) e as URLs que o confirmam. Esse arquivo vai no mesmo commit.

## Atualização diária das notícias

A tarefa agendada altera **somente** o bloco
`<script type="application/json" id="site-data">` do `index.html`.

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
      "data": "dd/mm/aaaa",
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

Regras: exatamente 3 notícias; `texto` com exatamente 3 parágrafos de pelo menos 200 caracteres cada,
escritos com palavras próprias (nunca copiar trechos das fontes); variações sempre com sinal (`+0,67%`, `-0,82%`).

### Ilustração (`arte`) de cada notícia

A ilustração é desenhada pelo site a partir dos dados da própria notícia. Escolha o tipo que melhor mostra o fato:

| tipo | quando usar | campos |
|---|---|---|
| `linha` | evolução no tempo (juros, inflação, preço) | `titulo`, `pontos: [["rótulo", número], ...]`, `fonte`, opcionais `degraus: true`, `rotular: true`, `sufixo`, `destaque: "texto curto"` |
| `indicador` | um número do dia (índice, cotação, PIB) | `rotulo`, `valor` (texto), `variacao` (`"+1,2%"`), opcional `secundarios: [{rotulo, valor, variacao}]` (até 2) |
| `barras` | comparação de valores | `titulo`, `barras: [{rotulo, valor (número), destaque?: true}]` (1 a 4), opcionais `prefixo`, `sufixo`, `nota` |
| `cena` | notícia sem número central | `titulo` curto (opcional) |

Todos os tipos levam `tema`, o desenho de fundo:
`juros`, `fiscal`, `ia`, `bolsa`, `cambio`, `inflacao`, `energia`, `tecnologia`, `imoveis`, `emprego`.

**Nunca invente dados.** Todo número da ilustração precisa estar na matéria ou em fonte oficial,
e as ilustrações com dados (`linha`, `indicador`, `barras`) levam o campo `fonte`, exibido na imagem
(ex.: `"fonte": "Fonte: InfoMoney, fechamento de 05/11/2026"`).

Séries no tempo usam um ponto por período, sem pular meses: para a Selic, um ponto por mês com a taxa
vigente no fim do mês, `degraus: true` e `rotular: true` (escreve o valor em cada mudança), com `sufixo: "%"`.
Exemplo conferido nas decisões do Copom de 2026: jan 15; fev 15; mar 14,75; abr 14,5; mai 14,5; jun 14,25;
jul 14,25; ago 14; set 13,75; out 13,75; nov 13,75.

### Passos

```
python3 tools/validar.py index.html      # precisa terminar com OK
git diff --stat                           # só index.html e verificacao.md podem mudar
git commit -am "Notícias de dd/mm/aaaa" && git push origin main
python3 tools/preview.py index.html /tmp/preview.html   # para republicar a prévia no Claude
```
