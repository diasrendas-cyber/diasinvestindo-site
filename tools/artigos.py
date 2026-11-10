"""Artigos do portal: leitura dos arquivos em conteudo/artigos/*.md e geração das páginas.

Cada artigo é um arquivo de texto com cabeçalho entre linhas '---' (campos 'chave: valor') e corpo em Markdown
simples: '## Subtítulo', parágrafos, **negrito**, [link](url), tabelas com '|', '> destaque' e ':: nota final'.
O nome do arquivo (sem .md) é o endereço permanente: /artigos/<nome>/.
"""
import html, json, os, re
from urllib.parse import quote

CATEGORIAS = {
    "financas-pessoais": ("Finanças Pessoais", "Orçamento, juros compostos e aposentadoria: a base para o dinheiro trabalhar por você."),
    "investimentos": ("Investimentos", "Tesouro Direto e renda fixa: como funciona cada título e qual escolher para cada objetivo."),
    "produtividade": ("Produtividade", "Trabalhar melhor com inteligência artificial, organização e boas rotinas."),
}
OBRIGATORIOS = ["titulo", "categoria", "data", "leitura", "resumo", "linha_fina", "arte"]
esc = lambda t: html.escape(str(t if t is not None else ""), quote=True)


def iso(d):
    dd, mm, aa = d.split("/")
    return f"{aa}-{mm}-{dd}"


def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    def link(m):
        txt, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        return f'<a href="{url}"' + (' target="_blank" rel="noopener"' if ext else " data-fecha-leitor") + f">{txt}</a>"
    return re.sub(r"\[(.+?)\]\((.+?)\)", link, t)


def markdown(corpo):
    blocos, saida = re.split(r"\n\s*\n", corpo.strip()), []
    for b in blocos:
        b = b.strip()
        if b.startswith("## "):
            saida.append(f"<h2>{inline(b[3:])}</h2>")
        elif b.startswith("|"):
            linhas = [l.strip().strip("|").split("|") for l in b.splitlines() if not re.match(r"^\|?\s*-", l.strip().strip("|").strip())]
            cab, resto = linhas[0], linhas[1:]
            t = '<div class="tablebox"><table class="fig"><thead><tr>' + "".join(f"<th>{inline(c.strip())}</th>" for c in cab) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c.strip())}</td>" for c in r) + "</tr>" for r in resto)
            saida.append(t + "</tbody></table></div>")
        elif b.startswith("> "):
            saida.append(f'<p class="callout">{inline(" ".join(l[2:] if l.startswith("> ") else l for l in b.splitlines()))}</p>')
        elif b.startswith(":: "):
            saida.append(f'<p class="src">{inline(b[3:])}</p>')
        elif all(re.match(r"^\d+\. ", l) for l in b.splitlines()):
            saida.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l))}</li>" for l in b.splitlines()) + "</ol>")
        elif all(l.startswith("- ") for l in b.splitlines()):
            saida.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in b.splitlines()) + "</ul>")
        else:
            saida.append(f"<p>{inline(' '.join(b.splitlines()))}</p>")
    return "\n".join(saida)


def ler(pasta):
    artigos = []
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".md"):
            continue
        bruto = open(os.path.join(pasta, nome), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", bruto, re.S)
        if not m:
            raise SystemExit(f"ERRO: {nome} sem cabeçalho entre linhas ---")
        cab = {}
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                cab[k.strip()] = v.strip()
        faltam = [k for k in OBRIGATORIOS if not cab.get(k)]
        if faltam:
            raise SystemExit(f"ERRO: {nome} sem os campos {faltam}")
        if cab["categoria"] not in CATEGORIAS:
            raise SystemExit(f"ERRO: {nome}: categoria deve ser uma de {list(CATEGORIAS)}")
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", cab["data"]):
            raise SystemExit(f"ERRO: {nome}: data deve ser dd/mm/aaaa")
        try:
            cab["arte"] = json.loads(cab["arte"])
        except Exception as e:
            raise SystemExit(f"ERRO: {nome}: arte não é JSON válido ({e})")
        a = cab["arte"]
        if a.get("tipo") in ("linha", "indicador", "barras") and not a.get("fonte"):
            raise SystemExit(f"ERRO: {nome}: ilustração com números precisa do campo fonte")
        cab["slug"] = nome[:-3]
        cab["destaque"] = cab.get("destaque", "").lower() in ("sim", "true", "1")
        cab["html"] = markdown(m.group(2))
        cab["video_id"] = video_id(cab.get("video", ""))
        artigos.append(cab)
    artigos.sort(key=lambda a: (iso(a["data"]), a["destaque"]), reverse=True)
    return artigos


def video_id(url):
    m = re.search(r"(?:youtu\.be/|v=|/embed/|/shorts/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else ""


def arte_attr(arte):
    return esc(json.dumps(arte, ensure_ascii=False))


def cartao(a, big=False):
    cat = CATEGORIAS[a["categoria"]][0]
    return (f'<a class="story{" big" if big else ""}" href="/artigos/{a["slug"]}/" data-open-artigo="{a["slug"]}">'
            f'<div class="art" data-arte="{arte_attr(a["arte"])}"></div><span class="kicker">{esc(cat)}</span>'
            f'<h3>{esc(a["titulo"])}</h3><p>{esc(a["resumo"])}</p><span class="more">Ler artigo</span></a>')


def corpo_artigo(a, h1_id=True):
    cat = CATEGORIAS[a["categoria"]][0]
    video = ""
    if a["video_id"]:
        video = (f'<div class="video-box"><iframe class="video" src="https://www.youtube-nocookie.com/embed/{a["video_id"]}" '
                 f'title="Vídeo: {esc(a["titulo"])}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>')
    h1 = '<h1 id="leitor-titulo">' if h1_id else "<h1>"
    return (f'<span class="kicker">{esc(cat)}</span>{h1}{esc(a["titulo"])}</h1>'
            f'<p class="dek">{esc(a["linha_fina"])}</p><p class="meta">Por Moisés Dias · {esc(a["leitura"])} min de leitura · publicado em {esc(a["data"])}</p>'
            f'<div class="art" data-arte="{arte_attr(a["arte"])}"></div>{video}<div class="corpo">{a["html"]}</div>')


def vitrine(artigos, categoria, limite=3):
    lista = [a for a in artigos if a["categoria"] == categoria][:limite]
    if not lista:
        return '  <p class="meta">Os primeiros artigos desta seção estão em produção. Cadastre-se para receber assim que saírem.</p>\n'
    return '  <div class="three">' + "".join(cartao(a) for a in lista) + "</div>\n"


def videoblog(artigos):
    itens = "".join(f'<li><a href="/artigos/{a["slug"]}/" data-open-artigo="{a["slug"]}"><span class="n">{i:02d}</span><b>{esc(a["titulo"])}</b></a></li>'
                    for i, a in enumerate(artigos[:12], 1))
    com_video = [a for a in artigos if a["video_id"]][:4]
    if com_video:
        vids = "".join(f'<a class="vcard" href="https://www.youtube.com/watch?v={a["video_id"]}" target="_blank" rel="noopener">'
                       f'<div class="vthumb" style="background-image:url(https://i.ytimg.com/vi/{a["video_id"]}/mqdefault.jpg);background-size:cover" aria-hidden="true"></div>'
                       f'<div><b>{esc(a["titulo"])}</b><span>Assistir no YouTube</span></div></a>' for a in com_video)
    else:
        vids = '<div class="vcard"><div class="vthumb" aria-hidden="true"></div><div><b>Os vídeos dos artigos entram aqui</b><span>Em produção para o YouTube</span></div></div>'
    return (f'  <div class="two"><div><span class="kicker">Artigos</span><ul class="vlist">{itens}</ul></div>'
            f'<div class="vstack"><span class="kicker">Vídeos</span>{vids}</div></div>\n')


def modelos(artigos):
    return "".join(f'<template id="artigo-{a["slug"]}"><article class="reading">{corpo_artigo(a)}</article></template>\n' for a in artigos)


def relacionados(a, artigos, n=3):
    mesma = [x for x in artigos if x["slug"] != a["slug"] and x["categoria"] == a["categoria"]]
    outras = [x for x in artigos if x["slug"] != a["slug"] and x["categoria"] != a["categoria"]]
    return (mesma + outras)[:n]


def pagina_artigo(a, artigos, pagina, SITE, HOTMART, dados):
    cat, _ = CATEGORIAS[a["categoria"]]
    url = f"{SITE}/artigos/{a['slug']}/"
    rel = relacionados(a, artigos)
    calc = ""
    if a.get("calculadora"):
        calc = f'<a class="btn ghost" href="{esc(a["calculadora"])}">Abrir a calculadora</a>'
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["titulo"], "description": a["resumo"],
          "datePublished": iso(a["data"]), "inLanguage": "pt-BR", "mainEntityOfPage": url,
          "author": {"@type": "Person", "name": "Moisés Dias"}, "publisher": {"@type": "Organization", "name": "Dias Investindo"}}
    corpo = f"""<article class="pagina">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <a href="/{a["categoria"]}/">{esc(cat)}</a> › <span>Artigo</span></nav>
  {corpo_artigo(a, h1_id=False)}
  <div class="share"><span>Compartilhe:</span><a href="https://wa.me/?text={quote(a["titulo"] + " " + url)}" target="_blank" rel="noopener">WhatsApp</a><button type="button" id="copiar-link">Copiar link</button>{calc}</div>
</article>
<div class="cta">
  <div><h3>Planilha Liberdade Financeira</h3><p>Descubra quanto precisa juntar, por quanto tempo e com que aporte para viver de renda.</p></div>
  <div class="btns"><a class="btn" href="{HOTMART}" target="_blank" rel="noopener">Conhecer a planilha</a><a class="btn ghost" href="/#ferramentas">Ferramentas grátis</a></div>
</div>
<section class="sec" aria-label="Leia também">
  <div class="sec-head"><h2>Leia também</h2><a href="/artigos/">Todos os artigos</a></div>
  {'<div class="three">' + "".join(cartao(x) for x in rel) + "</div>" if rel else '<p class="meta">Novos artigos em breve.</p>'}
</section>
<div class="capture-slot" data-origem="artigo"></div>"""
    head = f'<meta property="article:published_time" content="{iso(a["data"])}">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return pagina(f'{a["titulo"]} | Dias Investindo', a["resumo"], url, corpo, dados, "article", head)


def pagina_categoria(cat, artigos, pagina, SITE, dados):
    nome, desc = CATEGORIAS[cat]
    lista = [a for a in artigos if a["categoria"] == cat]
    grade = '<div class="three">' + "".join(cartao(a) for a in lista) + "</div>" if lista else '<p class="meta">Os primeiros artigos desta seção estão em produção.</p>'
    extra = ""
    if cat == "produtividade":
        extra = '<div class="soon"><div><span class="kicker">Curso gratuito</span><h3>Curso Completo de Claude: do básico ao avançado</h3><p>Oito módulos para usar inteligência artificial no trabalho e nos estudos.</p><a class="btn" href="https://curso.diasinvestindo.com.br" target="_blank" rel="noopener">Acessar o curso</a></div></div>'
    corpo = f"""<section class="sec" aria-label="{esc(nome)}">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>{esc(nome)}</span></nav>
  <div class="sec-head"><h2>{esc(nome)}</h2><span class="sub">{len(lista)} {"artigo" if len(lista) == 1 else "artigos"}</span></div>
  <p class="meta" style="margin:0;font-size:16px">{esc(desc)}</p>
  {grade}
  {extra}
</section>
<div class="capture-slot" data-origem="{cat}"></div>"""
    return pagina(f"{nome} | Dias Investindo", desc, f"{SITE}/{cat}/", corpo, dados)


def pagina_todos(artigos, pagina, SITE, dados):
    blocos = ""
    for cat, (nome, desc) in CATEGORIAS.items():
        lista = [a for a in artigos if a["categoria"] == cat]
        if not lista:
            continue
        itens = "".join(f'<li><span class="quando">{esc(a["data"])}</span><a href="/artigos/{a["slug"]}/"><span class="kicker">{esc(nome)}</span>'
                        f'<h3>{esc(a["titulo"])}</h3><p>{esc(a["resumo"])}</p></a></li>' for a in lista)
        blocos += f'<h2 class="mes"><a href="/{cat}/" style="color:inherit;text-decoration:none">{esc(nome)}</a></h2><ul class="lista">{itens}</ul>'
    corpo = f"""<section class="sec" aria-label="Artigos">
  <nav class="breadcrumb" aria-label="Você está em"><a href="/">Início</a> › <span>Artigos</span></nav>
  <div class="sec-head"><h2>Artigos</h2><span class="sub">{len(artigos)} artigos</span></div>
  <p class="meta" style="margin:0;font-size:16px">Do problema à solução, com números honestos e ferramentas para você fazer as próprias contas.</p>
  {blocos}
</section>
<div class="capture-slot" data-origem="artigos"></div>"""
    return pagina("Artigos | Dias Investindo", "Todos os artigos do Dias Investindo sobre finanças pessoais, investimentos e produtividade.", f"{SITE}/artigos/", corpo, dados)
