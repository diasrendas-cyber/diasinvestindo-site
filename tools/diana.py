"""Página de vendas da Diana (/diana/), gerada por tools/gerar.py a partir de conteudo/diana.html.

TUDO O QUE VOCÊ PRECISA PREENCHER OU TROCAR ESTÁ NO DICIONÁRIO CONFIG ABAIXO.
Depois de editar, rode: python3 tools/gerar.py  (e faça o commit/push).
"""
import html, json, re

esc = lambda t: html.escape(str(t if t is not None else ""), quote=True)

CONFIG = {
    # Destino dos botões "Quero a Diana" (troque em um só lugar):
    #   "lista"    -> formulário da lista de espera do piloto (nesta página)
    #   "whatsapp" -> link wa.me do número da Diana (preencha "whatsapp")
    #   "checkout" -> página de pagamento (preencha "checkout")
    "cta_modo": "lista",
    "whatsapp": "",   # ex.: "https://wa.me/5561999999999?text=Oi%20Diana"
    "checkout": "",   # ex.: "https://pay.hotmart.com/XXXX"

    # Planos e preço (os marcadores aparecem na página até você trocar)
    "plano": "[PLANO]",
    "preco": "[PREÇO]",
    "periodo_teste": "[PERÍODO DE TESTE]",
    "garantia": "[GARANTIA]",
    "como_cancelar": "[COMO CANCELAR]",
    # Preço só em número, para os dados estruturados (ex.: 49.90). Enquanto for None, o bloco
    # "offers" fica fora do JSON-LD, porque um preço em texto invalidaria os dados estruturados.
    "preco_numero": None,

    # Google Analytics 4 (ex.: "G-XXXXXXX"). Vazio = sem GA; os eventos continuam indo para window.dataLayer.
    "ga4": "",
}

TITULO = "Diana: secretária financeira no WhatsApp | DiasInvestindo"
DESCRICAO = "Mande foto do comprovante ou o extrato no WhatsApp e a Diana organiza gastos, recebimentos e contas. Separa empresa e pessoal. Conheça."
URL = "/diana/"
OG = "/assets/img/diana-og.png"


def faq():
    c = CONFIG
    return [
        ("Preciso instalar algo?",
         "Não. A Diana funciona no WhatsApp que você já usa. Você salva o número dela e manda mensagem, foto ou PDF, como faria com uma pessoa."),
        ("Ela acessa minha conta do banco?",
         "Não. A Diana não se conecta ao banco e não pede senha de banco nem número de cartão. Ela registra só o que você manda: texto, foto do comprovante ou o extrato em PDF."),
        ("Funciona para empresa e pessoal ao mesmo tempo?",
         "Sim. A Diana separa Empresa e Pessoal, mesmo quando você usa as mesmas contas para tudo. Quando não dá para saber de qual lado é um lançamento, ela pergunta."),
        ("E se eu mandar um dado errado?",
         "É só avisar e ela corrige. Extrato e fatura em PDF passam por você antes: a Diana mostra um resumo e só grava depois da sua confirmação. Ela nunca inventa dado: o que falta vira pendência, e ela lembra você depois."),
        ("A Diana recomenda investimentos?",
         "Não. Ela registra aportes, resgates e proventos e acompanha o seu caminho rumo à independência financeira. A Diana organiza e calcula; ela não recomenda compra ou venda de ativos."),
        ("Como cancelo?",
         f"{c['como_cancelar']} Se também quiser apagar os seus dados, mande \"apagar meus dados\" para a Diana ou escreva para diasrendas@gmail.com. A exclusão é concluída em até 30 dias."),
        ("Meus dados estão seguros?",
         "Cada cliente só vê os próprios dados. O banco de dados fica no Brasil, em servidor em São Paulo, com acesso restrito; os arquivos ficam em armazenamento privado e as comunicações são criptografadas. Para entender textos, fotos e PDFs, a Diana usa inteligência artificial de parceiros listados na Política de Privacidade."),
    ]


def _faq_html():
    itens = []
    for i, (p, r) in enumerate(faq(), 1):
        r_html = esc(r).replace("Política de Privacidade", '<a href="/diana/politica-de-privacidade/">Política de Privacidade</a>', 1)
        itens.append(f'<details class="dfaq" data-pergunta="{esc(p)}"><summary><h3>{esc(p)}</h3></summary><p>{r_html}</p></details>')
    return "\n".join(itens)


def _jsonld(site):
    c = CONFIG
    org = {"@type": "Organization", "@id": f"{site}/#organizacao", "name": "DiasInvestindo", "url": f"{site}/",
           "email": "contato@diasinvestindo.com.br", "sameAs": ["https://www.instagram.com/diasinvestindo/"]}
    app = {"@type": "SoftwareApplication", "@id": f"{site}{URL}#diana", "name": "Diana", "url": f"{site}{URL}",
           "description": DESCRICAO, "applicationCategory": "FinanceApplication", "operatingSystem": "WhatsApp",
           "inLanguage": "pt-BR", "image": f"{site}{OG}", "publisher": {"@id": f"{site}/#organizacao"}}
    if isinstance(c.get("preco_numero"), (int, float)):
        app["offers"] = {"@type": "Offer", "price": f'{c["preco_numero"]:.2f}', "priceCurrency": "BRL",
                         "url": f"{site}{URL}#planos", "availability": "https://schema.org/InStock"}
    faqpage = {"@type": "FAQPage", "@id": f"{site}{URL}#faq", "mainEntity": [
        {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq()]}
    trilha = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{site}/"},
        {"@type": "ListItem", "position": 2, "name": "Diana", "item": f"{site}{URL}"}]}
    dados = {"@context": "https://schema.org", "@graph": [org, app, faqpage, trilha]}
    return '<script type="application/ld+json">' + json.dumps(dados, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"


def pagina_diana(pagina, site, dados, arquivo_modelo):
    c = CONFIG
    corpo = open(arquivo_modelo, encoding="utf-8").read()
    cta = {"modo": c["cta_modo"], "whatsapp": c["whatsapp"], "checkout": c["checkout"]}
    trocas = {"faq": _faq_html(), "plano": esc(c["plano"]), "preco": esc(c["preco"]),
              "periodo_teste": esc(c["periodo_teste"]), "garantia": esc(c["garantia"]),
              "cta_json": esc(json.dumps(cta, ensure_ascii=False))}
    corpo = re.sub(r"\{\{(\w+)\}\}", lambda m: trocas[m.group(1)], corpo)
    ga = ""
    if c.get("ga4"):
        g = esc(c["ga4"])
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>\n'
              f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{g}");</script>\n')
    extra = ('<link rel="stylesheet" href="/assets/diana.css">\n<meta name="theme-color" content="#0F6E55">\n'
             + _jsonld(site) + ga + '<script defer src="/assets/diana.js"></script>\n')
    aviso = "A Diana organiza e calcula com base nas informações que você envia. Ela não faz recomendação de investimento."
    return pagina(TITULO, DESCRICAO, f"{site}{URL}", corpo, dados, extra_head=extra, cheia=True, aviso=aviso, og_imagem=f"{site}{OG}")
