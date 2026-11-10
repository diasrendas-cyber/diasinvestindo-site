"""Gera as páginas do portal a partir de noticias.json.

Uso: python3 tools/gerar.py

- noticias.json guarda TODAS as notícias, da mais nova para a mais antiga (a tarefa diária acrescenta no topo).
- Atualiza o bloco site-data do index.html (régua + 10 notícias mais recentes).
- Gera /noticias/<slug>/index.html (uma página por notícia), /noticias/index.html (arquivo),
  /privacidade/index.html, 404.html, sitemap.xml, robots.txt e feed.xml.
"""
import html, json, os, re, shutil, sys, unicodedata
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import artigos as ART
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://diasinvestindo.com.br"
HOTMART = "https://go.hotmart.com/R108167327G"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

esc = lambda t: html.escape(str(t if t is not None else ""), quote=True)


def caminho(*p):
    return os.path.join(RAIZ, *p)


def iso(d):  # dd/mm/aaaa -> aaaa-mm-dd
    dd, mm, aa = d.split("/")
    return f"{aa}-{mm}-{dd}"


def slugify(texto, limite=70):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    if len(t) > limite:
        t = t[:limite].rsplit("-", 1)[0]
    return t


def sinal(v):
    v = str(v or "").strip().replace("−", "-")
    if v.startswith("-"):
        return "down"
    if v.startswith("+") and re.search(r"[1-9]", v):
        return "up"
    return ""


def fmtvar(v):
    return re.sub(r"^-", "−", str(v or ""))


def ticker_html(t):
    partes = []
    if t.get("selic"):
        partes.append(f'<span><span class="lbl">Selic</span> {esc(t["selic"])}</span>')
    if t.get("ibov"):
        partes.append(f'<span><span class="lbl">Ibovespa</span> {esc(t["ibov"])} <span class="{sinal(t.get("ibovVar"))}">{esc(fmtvar(t.get("ibovVar")))}</span></span>')
    if t.get("dolar"):
        partes.append(f'<span><span class="lbl">Dólar</span> {esc(t["dolar"])} <span class="{sinal(t.get("dolarVar"))}">{esc(fmtvar(t.get("dolarVar")))}</span></span>')
    if t.get("data"):
        partes.append(f'<span class="when">Fechamento de {esc(t["data"])}</span>')
    partes.append('<span class="btc" data-btc hidden></span>')  # Bitcoin ao vivo, preenchido por assets/comum.js
    return "".join(partes)


def arte_div(arte):
    return f'<div class="art" data-arte="{esc(json.dumps(arte or {"tipo": "cena", "tema": "bolsa"}, ensure_ascii=False))}"></div>'


def pagina(titulo, descricao, url, corpo, dados, tipo="website", extra_head=""):
    """Moldura comum: cabeçalho, régua, faixa de patrocínio, coluna lateral e rodapé."""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(descricao)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="{tipo}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:locale" content="pt_BR">
<link rel="alternate" type="application/rss+xml" title="Dias Investindo: notícias" href="/feed.xml">
<!-- ADSENSE -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2224422141615380" crossorigin="anonymous"></script>
<!-- /ADSENSE -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/assets/estilo.css">
{extra_head}</head>
<body>
<header class="site" id="topo">
  <div class="wrap bar">
    <a class="logo" href="/"><b>Dias<span>Investindo</span></b><small>viva os dias investindo em você</small></a>
    <nav class="tabs" aria-label="Seções do site">
      <a href="/#inicio">Início</a>
      <a href="/noticias/" aria-current="{'true' if '/noticias/' in url else 'false'}">Notícias</a>
      <a href="/#financas">Finanças Pessoais</a>
      <a href="/#investimentos">Investimentos</a>
      <a href="/#produtividade">Produtividade</a>
      <a href="/#ferramentas">Ferramentas</a>
      <a href="/#videoblog">VideoBlog</a>
      <a href="/#sobre">Sobre</a>
    </nav>
  </div>
  <div class="ticker"><div class="wrap" aria-label="Indicadores de mercado">{ticker_html(dados.get("ticker", {}))}</div></div>
</header>
<div class="sponsor" aria-label="Patrocínio"><div class="wrap">
  <div class="sponsor-slot" data-ad-slot-name="faixa">
    <div><span class="ad-tag">Patrocínio</span><br><strong>Sua marca aqui</strong><span class="t">Espaço para parceiros de educação financeira</span></div>
    <span class="ad-dim">970 × 90</span>
  </div>
</div></div>
<main class="wrap">
<div class="layout">
<div id="conteudo">
{corpo}
</div>
<aside class="rail" aria-label="Patrocínio lateral">
  <div class="slot" data-ad-slot-name="lateral">
    <span class="ad-tag">Patrocínio</span>
    <div><strong>Sua marca aqui</strong><p>Espaço para parceiros de educação financeira.</p></div>
    <span class="ad-dim">160 × 600</span>
  </div>
  <div class="slot short">
    <span class="ad-tag">Apoio</span>
    <div><strong>Anuncie</strong><p>contato@<wbr>diasinvestindo.com.br</p></div>
    <span class="ad-dim">160 × 160</span>
  </div>
</aside>
</div>
</main>
<footer class="site"><div class="wrap">
  <p><strong style="color:var(--ink)">DiasInvestindo</strong> · viva os dias investindo em você · diasinvestindo.com.br · @diasinvestindo</p>
  <p class="foot-links"><a href="/#sobre">Sobre</a><a href="/#contato">Contato</a><a href="/noticias/">Arquivo de notícias</a><a href="/privacidade/">Política de Privacidade</a></p>
  <p>Conteúdo educativo. Nada aqui constitui recomendação de investimento. Rentabilidade passada não garante resultados futuros.</p>
</div></footer>
<script src="/assets/arte.js"></script>
<script>
document.querySelectorAll("[data-arte]").forEach(function(el){{try{{el.innerHTML=window.DIArte.desenhar(JSON.parse(el.getAttribute("data-arte")))}}catch(e){{console.error(e)}}}});
var cp=document.getElementById("copiar-link");
if(cp)cp.addEventListener("click",function(){{var u=location.href.split("#")[0];
  (navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){{cp.textContent="Link copiado"}},function(){{cp.textContent=u}});}});
var f=document.querySelectorAll(".filtros button");
f.forEach(function(b){{b.addEventListener("click",function(){{var ed=b.getAttribute("data-ed");
  f.forEach(function(x){{x.setAttribute("aria-pressed",x===b?"true":"false")}});
  document.querySelectorAll(".lista li").forEach(function(li){{li.hidden=!!ed&&li.getAttribute("data-ed")!==ed}});
  document.querySelectorAll(".mes").forEach(function(h){{var ul=h.nextElementSibling;h.hidden=ul&&![].some.call(ul.children,function(li){{return !li.hidden}});ul.hidden=h.hidden}});}})}});
</script>
<script src="/assets/comum.js"></script>
</body>
</html>
"""


def cartao_lista(n):
    return (f'<li data-ed="{esc(n["editoria"])}"><span class="quando">{esc(n.get("publicado", n["data"]))}</span>'
            f'<a href="/noticias/{esc(n["slug"])}/"><span class="kicker">{esc(n["editoria"])}</span>'
            f'<h3>{esc(n["titulo"])}</h3><p>{esc(n["resumo"])}</p></a></li>')


def pagina_noticia(n, todas, dados):
    url = f"{SITE}/noticias/{n['slug']}/"
    paragrafos = "\n".join(f"<p>{esc(t)}</p>" for t in n.get("texto", []))
    fontes = " · ".join(f'<a href="{esc(f["url"])}" target="_blank" rel="noopener">{esc(f["nome"])}</a>' for f in n.get("fontes", []))
    bolso = f'<p class="callout"><strong>Para o seu bolso:</strong> {esc(n["bolso"])}</p>' if n.get("bolso") else ""
    outras = [o for o in todas if o["slug"] != n["slug"]][:4]
    wa = "https://wa.me/?text=" + quote(f'{n["titulo"]} {url}')
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": n["titulo"], "description": n["resumo"],
          "datePublished": iso(n.get("publicado", n["data"])), "inLanguage": "pt-BR", "mainEntityOfPage": url,
          "author": {"@type": "Person", "name": "Moisés Dias"}, "publisher": {"@type": "Organization", "name": "Dias Investindo"}}
    corpo = f"""<article class="pagina">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <a href="/noticias/">Notícias</a> › <span>{esc(n["editoria"])}</span></nav>
  <span class="kicker">{esc(n["editoria"])} · {esc(n["data"])}</span>
  <h1>{esc(n["titulo"])}</h1>
  <p class="dek">{esc(n["resumo"])}</p>
  <p class="meta">Por Dias Investindo · publicado em {esc(n.get("publicado", n["data"]))}</p>
  {arte_div(n.get("arte"))}
  <div class="corpo">
{paragrafos}
{bolso}
  </div>
  <p class="src">{"Fontes" if len(n.get("fontes", [])) > 1 else "Fonte"}: {fontes}. Resumo escrito pelo Dias Investindo a partir das reportagens citadas; os números foram conferidos em mais de uma fonte ou em fonte oficial.</p>
  <div class="share"><span>Compartilhe:</span><a href="{wa}" target="_blank" rel="noopener">WhatsApp</a><button type="button" id="copiar-link">Copiar link</button></div>
</article>
<div class="cta">
  <div><h3>Planilha Liberdade Financeira</h3><p>Descubra quanto precisa juntar, por quanto tempo e com que aporte para viver de renda.</p></div>
  <div class="btns"><a class="btn" href="{HOTMART}" target="_blank" rel="noopener">Conhecer a planilha</a><a class="btn ghost" href="/#calc-aposentadoria">Simular grátis</a></div>
</div>
<section class="sec" aria-label="Mais notícias">
  <div class="sec-head"><h2>Mais notícias</h2><a href="/noticias/">Todas as notícias</a></div>
  <ul class="lista">{"".join(cartao_lista(o) for o in outras) or '<li><span></span><p class="meta">As próximas notícias aparecem aqui.</p></li>'}</ul>
</section>
<div class="capture-slot" data-origem="noticia"></div>"""
    head = f'<meta property="article:published_time" content="{iso(n.get("publicado", n["data"]))}">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return pagina(f'{n["titulo"]} | Dias Investindo', n["resumo"], url, corpo, dados, "article", head)


def pagina_arquivo(todas, dados):
    eds = sorted({n["editoria"] for n in todas})
    filtros = '<button type="button" data-ed="" aria-pressed="true">Todas</button>' + "".join(
        f'<button type="button" data-ed="{esc(e)}" aria-pressed="false">{esc(e)}</button>' for e in eds)
    grupos, atual = [], None
    for n in todas:
        pub = n.get("publicado", n["data"])
        aa, mm = iso(pub)[:4], int(iso(pub)[5:7])
        chave = f"{MESES[mm - 1].capitalize()} de {aa}"
        if chave != atual:
            grupos.append((chave, []))
            atual = chave
        grupos[-1][1].append(n)
    blocos = "".join(f'<h2 class="mes">{esc(k)}</h2><ul class="lista">{"".join(cartao_lista(n) for n in ns)}</ul>' for k, ns in grupos)
    corpo = f"""<section class="sec" aria-label="Arquivo de notícias">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>Notícias</span></nav>
  <div class="sec-head"><h2>Notícias</h2><span class="sub">{len(todas)} notícias · atualizado em {esc(dados.get("atualizado", ""))}</span></div>
  <p class="meta" style="margin:0">Economia, investimentos, inteligência artificial, produtividade e negócios, explicados pelo impacto no seu bolso.</p>
  <div class="filtros" role="group" aria-label="Filtrar por editoria">{filtros}</div>
  {blocos}
</section>
<div class="capture-slot" data-origem="arquivo"></div>"""
    return pagina("Notícias | Dias Investindo", "Todas as notícias do Dias Investindo sobre economia, investimentos, IA e negócios, explicadas pelo impacto no seu bolso.", f"{SITE}/noticias/", corpo, dados)


def pagina_privacidade(index_html, dados):
    m = re.search(r'<template id="politica-privacidade">\s*(.*?)\s*</template>', index_html, re.S)
    artigo = m.group(1).replace(' id="leitor-titulo"', "").replace('class="reading"', 'class="pagina"')
    return pagina("Política de Privacidade | Dias Investindo", "Como o Dias Investindo trata os dados pessoais, em conformidade com a LGPD.", f"{SITE}/privacidade/", artigo, dados)


def pagina_404(dados):
    corpo = """<article class="pagina"><span class="kicker">Erro 404</span><h1>Página não encontrada</h1>
<p class="dek">O endereço pode ter mudado. Veja as notícias mais recentes ou volte para o início.</p>
<div class="btns"><a class="btn" href="/">Ir para o início</a><a class="btn ghost" href="/noticias/">Ver as notícias</a></div></article>"""
    return pagina("Página não encontrada | Dias Investindo", "Página não encontrada.", f"{SITE}/404", corpo, dados)


def main():
    dados = json.load(open(caminho("noticias.json"), encoding="utf-8"))
    todas = dados["noticias"]
    mudou = False
    for n in todas:
        if not n.get("slug"):
            n["slug"] = f'{iso(n["data"])}-{slugify(n["titulo"])}'
            mudou = True
    slugs = [n["slug"] for n in todas]
    if len(slugs) != len(set(slugs)):
        sys.exit("ERRO: há notícias com o mesmo slug (título e data repetidos)")
    if mudou:
        with open(caminho("noticias.json"), "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            f.write("\n")

    # home: régua + 10 mais recentes
    idx = open(caminho("index.html"), encoding="utf-8").read()
    bloco = json.dumps({"atualizado": dados["atualizado"], "ticker": dados["ticker"], "noticias": todas[:10]}, ensure_ascii=False, indent=2)
    novo, qtd = re.subn(r'(<script type="application/json" id="site-data">\n).*?(\n</script>)', lambda m: m.group(1) + bloco + m.group(2), idx, flags=re.S)
    if qtd != 1:
        sys.exit("ERRO: bloco site-data não encontrado no index.html")
    # artigos: vitrines da home, VideoBlog e modelos da prévia
    arts = ART.ler(caminho("conteudo", "artigos"))
    def preencher(html_, marca, conteudo):
        r, q = re.subn(rf"(<!-- GERADO:{marca} -->\n).*?(<!-- /GERADO -->)", lambda m: m.group(1) + conteudo + m.group(2), html_, flags=re.S)
        if q != 1:
            sys.exit(f"ERRO: marcador GERADO:{marca} não encontrado no index.html")
        return r
    home = ([a for a in arts if a["destaque"]] + [a for a in arts if not a["destaque"]])[:2]
    novo = preencher(novo, "home-artigos", "".join(ART.cartao(a) for a in home) + "\n")
    for cat in ART.CATEGORIAS:
        novo = preencher(novo, cat, ART.vitrine(arts, cat))
    novo = preencher(novo, "videoblog", ART.videoblog(arts))
    na_home = {a["slug"] for a in home} | {a["slug"] for c in ART.CATEGORIAS for a in [x for x in arts if x["categoria"] == c][:3]} | {a["slug"] for a in arts[:12]}
    novo = preencher(novo, "modelos-artigos", ART.modelos([a for a in arts if a["slug"] in na_home]))
    open(caminho("index.html"), "w", encoding="utf-8").write(novo)
    for pasta_ in ["artigos"] + list(ART.CATEGORIAS):
        if os.path.isdir(caminho(pasta_)):
            shutil.rmtree(caminho(pasta_))
    os.makedirs(caminho("artigos"))
    for a in arts:
        os.makedirs(caminho("artigos", a["slug"]))
        open(caminho("artigos", a["slug"], "index.html"), "w", encoding="utf-8").write(ART.pagina_artigo(a, arts, pagina, SITE, HOTMART, dados))
    open(caminho("artigos", "index.html"), "w", encoding="utf-8").write(ART.pagina_todos(arts, pagina, SITE, dados))
    for cat in ART.CATEGORIAS:
        os.makedirs(caminho(cat))
        open(caminho(cat, "index.html"), "w", encoding="utf-8").write(ART.pagina_categoria(cat, arts, pagina, SITE, dados))

    # páginas de notícia (recria a pasta para não deixar páginas órfãs)
    pasta = caminho("noticias")
    if os.path.isdir(pasta):
        shutil.rmtree(pasta)
    os.makedirs(pasta)
    for n in todas:
        os.makedirs(os.path.join(pasta, n["slug"]))
        open(os.path.join(pasta, n["slug"], "index.html"), "w", encoding="utf-8").write(pagina_noticia(n, todas, dados))
    open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(pagina_arquivo(todas, dados))
    os.makedirs(caminho("privacidade"), exist_ok=True)
    open(caminho("privacidade", "index.html"), "w", encoding="utf-8").write(pagina_privacidade(novo, dados))
    open(caminho("404.html"), "w", encoding="utf-8").write(pagina_404(dados))

    # índice da busca da home: todas as notícias e artigos (título, resumo, editoria, data e endereço)
    busca = [{"k": "Notícia", "t": n["titulo"], "r": n["resumo"], "c": n["editoria"], "d": n.get("publicado", n["data"]), "u": f"/noticias/{n['slug']}/"} for n in todas]
    busca += [{"k": "Artigo", "t": a["titulo"], "r": a["resumo"], "c": ART.CATEGORIAS[a["categoria"]][0], "d": a["data"], "u": f"/artigos/{a['slug']}/", "s": a["slug"]} for a in arts]
    with open(caminho("busca.json"), "w", encoding="utf-8") as f:
        json.dump(busca, f, ensure_ascii=False, separators=(",", ":"))

    # sitemap, robots e RSS
    hoje = iso(dados["atualizado"])
    urls = [(f"{SITE}/", hoje, "daily"), (f"{SITE}/noticias/", hoje, "daily"), (f"{SITE}/privacidade/", "2026-11-06", "yearly")]
    urls += [(f"{SITE}/artigos/", hoje, "weekly")] + [(f"{SITE}/{c}/", hoje, "weekly") for c in ART.CATEGORIAS]
    urls += [(f"{SITE}/artigos/{a['slug']}/", iso(a["data"]), "monthly") for a in arts]
    urls += [(f"{SITE}/noticias/{n['slug']}/", iso(n.get("publicado", n["data"])), "monthly") for n in todas]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{esc(u)}</loc><lastmod>{d}</lastmod><changefreq>{c}</changefreq></url>" for u, d, c in urls]
    sm.append("</urlset>")
    open(caminho("sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
    open(caminho("robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /verificacao/\nDisallow: /conteudo/\nDisallow: /noticias.json\n\nSitemap: {SITE}/sitemap.xml\n")
    meses_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    def rfc(d):
        a = date.fromisoformat(iso(d))
        return f'{["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][a.weekday()]}, {a.day:02d} {meses_en[a.month-1]} {a.year} 09:00:00 -0300'
    itens = "".join(
        f"<item><title>{esc(n['titulo'])}</title><link>{SITE}/noticias/{esc(n['slug'])}/</link><guid>{SITE}/noticias/{esc(n['slug'])}/</guid>"
        f"<pubDate>{rfc(n.get('publicado', n['data']))}</pubDate><description>{esc(n['resumo'])}</description></item>" for n in todas[:20])
    rss = (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Dias Investindo: notícias</title>'
           f"<link>{SITE}/noticias/</link><description>Notícias que mexem com o seu bolso, explicadas.</description><language>pt-br</language>{itens}</channel></rss>\n")
    open(caminho("feed.xml"), "w", encoding="utf-8").write(rss)
    print(f"OK: {len(todas)} notícias, {len(arts)} artigos, páginas, arquivos, sitemap ({len(urls)} URLs), RSS e home atualizados")


if __name__ == "__main__":
    main()
