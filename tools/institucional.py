"""Páginas institucionais: /sobre/, /contato/, /politica-editorial/ e /termos-de-uso/.

Texto escrito à mão aqui; tools/gerar.py monta as páginas com a moldura comum (cabeçalho, régua e rodapé).
Para mudar um texto, edite a constante e rode python3 tools/gerar.py.
"""

EMAIL = "contato@diasinvestindo.com.br"
INSTAGRAM = "https://www.instagram.com/diasinvestindo/"
ATUALIZADO = "27/11/2026"

SOBRE = f"""<article class="pagina">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>Sobre</span></nav>
  <span class="kicker">Sobre o site</span>
  <h1>Finanças tratadas como gestão de risco</h1>
  <p class="dek">O Dias Investindo explica dinheiro do jeito que se lida com risco: medindo, preparando e corrigindo a rota.</p>
  <div class="corpo">
    <h2>Quem escreve</h2>
    <p>Sou Moisés Dias. Passei a carreira no Corpo de Bombeiros Militar do Distrito Federal, onde aprendi que risco não se ignora: se mede, se prepara e se administra. Minha formação é em Física, e talvez por isso eu goste de fazer as contas antes de acreditar em qualquer promessa. Depois vieram um MBA em Gestão de Projetos e a especialização em gestão de risco e segurança contra incêndio. Nas finanças, tirei a certificação CPA e sigo estudando para a C-Pro I.</p>
    <p>Não escrevo como quem já sabe tudo. Escrevo como quem está fazendo o próprio caminho rumo à liberdade financeira, com números honestos e sem fórmula mágica.</p>
    <h2>O que você encontra aqui</h2>
    <p><strong>Artigos</strong> de finanças pessoais e investimentos que partem de um problema real (organizar o orçamento, montar a reserva de emergência, escolher um título do Tesouro) e chegam a uma solução prática, com as contas abertas.</p>
    <p><strong>Ferramentas gratuitas</strong>, sem cadastro: a Calculadora do Milhão, o Simulador de Aposentadoria e o Conversor de Moedas pela cotação oficial do Banco Central. Elas existem para você fazer as próprias contas antes de decidir.</p>
    <p><strong>Notícias</strong> de economia, mercados, negócios e inteligência artificial, selecionadas em fontes confiáveis e explicadas pelo impacto no seu bolso. Como elas são apuradas e checadas está na <a href="/politica-editorial/">Política Editorial</a>.</p>
    <h2>Princípios</h2>
    <p>Em um site de finanças, um número errado é pior do que nenhum número. Por isso todo dado publicado é conferido antes, e o que não pode ser confirmado não entra. O conteúdo é educativo: não faço recomendação individual de investimentos, e cada leitor deve avaliar a própria situação antes de decidir.</p>
    <h2>Formação</h2>
    <div class="creds"><span>Física</span><span>MBA em Gestão de Projetos</span><span>Gestão de risco</span><span>CPA</span><span>Estudando para a C-Pro I</span></div>
    <p>Dúvidas, sugestões de pauta ou correções: <a href="/contato/">fale comigo</a>.</p>
  </div>
</article>
<div class="capture-slot" data-origem="sobre"></div>"""

CONTATO = f"""<article class="pagina">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>Contato</span></nav>
  <span class="kicker">Contato</span>
  <h1>Fale com o Dias Investindo</h1>
  <p class="dek">Dúvidas sobre os artigos e as ferramentas, sugestões de pauta, correções, parcerias e patrocínio.</p>
  <div class="contact-grid">
    <div class="contact-card"><div><small>E-mail</small><b>{EMAIL}</b></div><a class="btn ghost" href="mailto:{EMAIL}">Escrever</a></div>
    <div class="contact-card"><div><small>Instagram</small><b>@diasinvestindo</b></div><a class="btn ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">Abrir perfil</a></div>
  </div>
  <div class="corpo">
    <h2>Para agilizar a resposta</h2>
    <p>Use um assunto que diga do que se trata:</p>
    <ul>
      <li><strong>Correção</strong>: encontrou um dado errado ou desatualizado? Diga a página e o trecho. Correções são prioridade e ficam registradas na própria página.</li>
      <li><strong>Pauta</strong>: um tema de finanças pessoais ou investimentos que você gostaria de ver explicado.</li>
      <li><strong>Ferramentas</strong>: dúvidas ou problemas com as calculadoras e o conversor.</li>
      <li><strong>Patrocínio</strong> ou <strong>Parceria</strong>: propostas comerciais e de conteúdo.</li>
    </ul>
    <p>Não respondo a pedidos de recomendação individual de investimento: o conteúdo do site é educativo e não substitui a orientação de um profissional certificado que conheça a sua situação.</p>
    <p>Os dados que você enviar por e-mail são usados apenas para responder à sua mensagem, como explica a <a href="/privacidade/">Política de Privacidade</a>.</p>
  </div>
</article>"""

POLITICA_EDITORIAL = f"""<article class="pagina">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>Política Editorial</span></nav>
  <span class="kicker">Política Editorial</span>
  <h1>Como o conteúdo do Dias Investindo é produzido</h1>
  <p class="dek">As regras que valem para cada notícia, artigo, gráfico e ferramenta publicados no site.</p>
  <p class="meta">Atualizada em {ATUALIZADO}</p>
  <div class="corpo">
    <h2>A regra de ouro: nenhum dado sem checagem</h2>
    <p>Este é um site de finanças, e um número errado é pior do que nenhum número. Todo número publicado, no texto, na régua de mercado ou nas ilustrações, precisa estar confirmado em duas fontes independentes ou em uma fonte oficial, como o Banco Central, o IBGE, a B3, o Tesouro Nacional, a CVM ou o comunicado da própria empresa. Quando duas fontes divergem, buscamos uma terceira. Se um dado não pode ser confirmado, ele não é publicado.</p>
    <p>Cada edição de notícias tem um registro de checagem com os números usados e os endereços das fontes que os confirmam.</p>
    <h2>Fontes</h2>
    <p>As notícias partem de agências e veículos reconhecidos, como Reuters, Associated Press, AFP, InfoMoney, Valor Econômico e Yahoo Finanças, de órgãos oficiais e dos comunicados das próprias empresas. Indicadores seguem a fonte oficial: Selic e decisões do Copom pelo Banco Central, inflação pelo IBGE, câmbio pela PTAX do Banco Central e o Ibovespa pela B3 ou pelo fechamento publicado por veículos especializados.</p>
    <h2>Notícias</h2>
    <p>Cada notícia é escrita com palavras próprias, nunca copiando trechos das fontes, e segue a mesma estrutura: o fato, o contexto e as consequências. A partir de novembro de 2026, as notícias trazem também uma análise própria, <em>O que isso muda para você</em>, que relaciona o fato às decisões de quem cuida do próprio dinheiro: orçamento, reserva, dívidas, investimentos e planejamento.</p>
    <h2>Artigos e ferramentas</h2>
    <p>Os artigos partem de um problema real e chegam a uma solução prática, com as contas abertas para o leitor conferir. As simulações dos artigos e das ferramentas usam premissas declaradas na própria página (rentabilidade, inflação, impostos e prazos) e são educativas: mostram o efeito de cada escolha, não prometem resultado.</p>
    <h2>Uso de inteligência artificial</h2>
    <p>O site usa ferramentas de inteligência artificial como apoio na pesquisa, na redação e na produção das ilustrações. As caricaturas que ilustram algumas notícias são geradas por IA e têm caráter editorial e opinativo, não fotográfico. O uso dessas ferramentas não dispensa as regras desta página: os dados passam pela mesma checagem, e a responsabilidade pelo que é publicado é do editor.</p>
    <h2>Correções</h2>
    <p>Se encontrar um erro, escreva para <a href="mailto:{EMAIL}">{EMAIL}</a> com o assunto "Correção". Erros confirmados são corrigidos na própria página.</p>
    <h2>Independência e publicidade</h2>
    <p>O site é mantido por anúncios exibidos pelo Google AdSense, por patrocínios identificados como tais e pelos produtos próprios do Dias Investindo, como a Planilha Liberdade Financeira e a Diana. Anunciantes e parceiros não escolhem pautas nem revisam textos. Quando um conteúdo menciona um produto próprio, isso fica claro no texto.</p>
    <h2>Não é recomendação de investimento</h2>
    <p>Todo o conteúdo é educativo. Nada no site constitui recomendação de compra ou venda de ativos, nem análise de valores mobiliários nos termos da Resolução CVM nº 20/2021. Rentabilidade passada não garante resultados futuros. Antes de investir, avalie seus objetivos, prazos e tolerância a risco, se necessário com um profissional certificado.</p>
  </div>
</article>"""

TERMOS = f"""<article class="pagina">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>Termos de Uso</span></nav>
  <span class="kicker">Termos de Uso</span>
  <h1>Termos de Uso do Dias Investindo</h1>
  <p class="dek">As condições para usar o site diasinvestindo.com.br, seus conteúdos e suas ferramentas.</p>
  <p class="meta">Atualizados em {ATUALIZADO}</p>
  <div class="corpo">
    <h2>1. Aceitação</h2>
    <p>Ao acessar o diasinvestindo.com.br você concorda com estes Termos de Uso e com a <a href="/privacidade/">Política de Privacidade</a>. Se não concordar, não use o site.</p>
    <h2>2. Conteúdo educativo</h2>
    <p>Os artigos, notícias, gráficos, calculadoras e simuladores têm finalidade exclusivamente educativa e informativa. Nada no site constitui recomendação de investimento, oferta de produto financeiro, consultoria ou análise de valores mobiliários nos termos da Resolução CVM nº 20/2021. As decisões tomadas a partir do conteúdo são de responsabilidade de quem as toma.</p>
    <h2>3. Ferramentas e simulações</h2>
    <p>As calculadoras e simuladores usam as premissas informadas pelo próprio usuário e as descritas em cada ferramenta. Os resultados são estimativas e não consideram todas as variáveis reais, como impostos, taxas, inflação futura e oscilações de mercado. O Conversor de Moedas usa a PTAX do Banco Central como referência; a cotação da sua operação será diferente.</p>
    <h2>4. Exatidão das informações</h2>
    <p>Os dados são conferidos antes da publicação, como descreve a <a href="/politica-editorial/">Política Editorial</a>, mas podem ficar desatualizados com o tempo. Confira a data de cada conteúdo e, para decisões importantes, consulte a fonte oficial.</p>
    <h2>5. Propriedade intelectual</h2>
    <p>Textos, gráficos, ilustrações, ferramentas e a marca Dias Investindo pertencem ao site. É permitido compartilhar o link e citar trechos curtos com crédito e link para a página original. A reprodução integral ou o uso comercial dependem de autorização por escrito.</p>
    <h2>6. Publicidade e links externos</h2>
    <p>O site exibe anúncios do Google AdSense e pode conter patrocínios e links para produtos próprios e sites de terceiros. O Dias Investindo não controla nem se responsabiliza pelo conteúdo, pelas ofertas ou pelas práticas de privacidade de sites externos e anunciantes.</p>
    <h2>7. Newsletter</h2>
    <p>Ao se cadastrar para receber os artigos por e-mail, você pode cancelar a qualquer momento pelo link presente em cada mensagem ou escrevendo para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2>8. Uso adequado</h2>
    <p>Não é permitido usar o site para fins ilegais, tentar comprometer seu funcionamento ou segurança, nem coletar o conteúdo de forma automatizada para republicação.</p>
    <h2>9. Alterações</h2>
    <p>Estes termos podem ser atualizados. A data da versão vigente aparece no topo desta página.</p>
    <h2>10. Lei aplicável e contato</h2>
    <p>Estes termos são regidos pelas leis da República Federativa do Brasil. Dúvidas: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</article>"""

PAGINAS = [
    ("sobre", "Sobre | Dias Investindo", "Quem escreve o Dias Investindo, o que o site oferece e os princípios que guiam o conteúdo.", SOBRE),
    ("contato", "Contato | Dias Investindo", "Fale com o Dias Investindo: dúvidas, pautas, correções, parcerias e patrocínio.", CONTATO),
    ("politica-editorial", "Política Editorial | Dias Investindo", "Como as notícias, artigos e ferramentas do Dias Investindo são produzidos, checados e corrigidos.", POLITICA_EDITORIAL),
    ("termos-de-uso", "Termos de Uso | Dias Investindo", "Condições de uso do site Dias Investindo, de seus conteúdos e de suas ferramentas.", TERMOS),
]
