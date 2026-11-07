"""Valida noticias.json (todas as notícias acumuladas) antes de gerar e publicar.
Uso: python3 tools/validar.py   (sai com código 1 se houver erro)"""
import json, os, re, sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    d = json.load(open(os.path.join(raiz, "noticias.json"), encoding="utf-8"))
except Exception as e:
    sys.exit(f"ERRO: noticias.json inválido: {e}")
erros = []
data_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")
iso = lambda s: "-".join(reversed(s.split("/")))
if not data_re.match(d.get("atualizado", "")): erros.append("atualizado deve ser dd/mm/aaaa")
t = d.get("ticker", {})
for k in ["selic", "ibov", "ibovVar", "dolar", "dolarVar", "data"]:
    if not t.get(k): erros.append(f"ticker.{k} ausente")
for k in ["ibovVar", "dolarVar"]:
    if t.get(k) and not re.match(r"^[+-]\d+,\d+%$", t[k]): erros.append(f"ticker.{k} deve ser como +0,67% ou -0,82%")
ns = d.get("noticias", [])
if len(ns) < 3: erros.append(f"são esperadas pelo menos 3 notícias, há {len(ns)}")
TIPOS = {"linha", "indicador", "barras", "cena"}
TEMAS = {"juros", "fiscal", "ia", "bolsa", "cambio", "inflacao", "energia", "tecnologia", "imoveis", "emprego"}
vistos = set()
for i, n in enumerate(ns, 1):
    p = f"notícia {i} ({n.get('titulo', '')[:40]}…)"
    for k in ["editoria", "data", "titulo", "resumo"]:
        if not n.get(k): erros.append(f"{p}: {k} ausente")
    if n.get("data") and not data_re.match(n["data"]): erros.append(f"{p}: data (dia do fato) deve ser dd/mm/aaaa")
    if not data_re.match(n.get("publicado", "")): erros.append(f"{p}: publicado (dia em que entrou no site) deve ser dd/mm/aaaa")
    chave = (n.get("data"), n.get("titulo"))
    if chave in vistos: erros.append(f"{p}: notícia repetida")
    vistos.add(chave)
    tx = n.get("texto", [])
    if len(tx) != 3: erros.append(f"{p}: texto deve ter exatamente 3 parágrafos (tem {len(tx)})")
    for j, par in enumerate(tx, 1):
        if len(par) < 200: erros.append(f"{p}: parágrafo {j} curto demais ({len(par)} caracteres; mínimo 200)")
    f = n.get("fontes", [])
    if not f or not all(x.get("nome") and str(x.get("url", "")).startswith("https://") for x in f): erros.append(f"{p}: fontes precisam de nome e url https")
    a = n.get("arte", {})
    if a.get("tipo") not in TIPOS: erros.append(f"{p}: arte.tipo deve ser um de {sorted(TIPOS)}")
    if a.get("tema") not in TEMAS: erros.append(f"{p}: arte.tema deve ser um de {sorted(TEMAS)}")
    if a.get("tipo") in ("linha", "indicador", "barras") and not a.get("fonte"): erros.append(f"{p}: arte com dados precisa do campo fonte")
    if a.get("tipo") == "linha" and len(a.get("pontos", [])) < 2: erros.append(f"{p}: arte linha precisa de 2+ pontos [rótulo, número]")
    if a.get("tipo") == "barras" and not (1 <= len(a.get("barras", [])) <= 4): erros.append(f"{p}: arte barras precisa de 1 a 4 barras")
    if a.get("tipo") == "barras" and not all(isinstance(b.get("valor"), (int, float)) for b in a.get("barras", [])): erros.append(f"{p}: valor das barras deve ser número")
    if a.get("tipo") == "indicador" and not (a.get("valor") and a.get("rotulo")): erros.append(f"{p}: arte indicador precisa de rotulo e valor")
# ordem: da mais nova para a mais antiga
datas = [iso(n["publicado"]) for n in ns if data_re.match(n.get("publicado", ""))]
if datas != sorted(datas, reverse=True): erros.append("as edições devem estar da mais nova para a mais antiga (as notícias do dia entram no topo da lista)")
if ns and d.get("atualizado") and ns[0].get("publicado") != d["atualizado"]: erros.append("as primeiras notícias devem ser da edição de hoje (publicado = atualizado)")
if erros:
    print("\n".join("ERRO: " + e for e in erros)); sys.exit(1)
print(f"OK: noticias.json válido ({len(ns)} notícias)")
