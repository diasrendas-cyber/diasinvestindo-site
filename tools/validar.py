"""Valida o bloco de dados das notícias (site-data) do index.html antes de publicar.
Uso: python3 tools/validar.py index.html   (sai com código 1 se houver erro)"""
import json, re, sys
s = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<script type="application/json" id="site-data">(.*?)</script>', s, re.S)
erros = []
if not m:
    sys.exit("ERRO: bloco site-data não encontrado")
try:
    d = json.loads(m.group(1))
except Exception as e:
    sys.exit(f"ERRO: JSON inválido: {e}")
data_re = re.compile(r"^\d{2}/\d{2}/\d{4}$")
if not data_re.match(d.get("atualizado", "")): erros.append("atualizado deve ser dd/mm/aaaa")
t = d.get("ticker", {})
for k in ["selic", "ibov", "ibovVar", "dolar", "dolarVar", "data"]:
    if not t.get(k): erros.append(f"ticker.{k} ausente")
for k in ["ibovVar", "dolarVar"]:
    if t.get(k) and not re.match(r"^[+-]\d+,\d+%$", t[k]): erros.append(f"ticker.{k} deve ser como +0,67% ou -0,82%")
ns = d.get("noticias", [])
if len(ns) != 3: erros.append(f"são esperadas 3 notícias, há {len(ns)}")
TIPOS = {"linha", "indicador", "barras", "cena"}
TEMAS = {"juros", "fiscal", "ia", "bolsa", "cambio", "inflacao", "energia", "tecnologia", "imoveis", "emprego"}
for i, n in enumerate(ns, 1):
    p = f"noticia {i}"
    for k in ["editoria", "data", "titulo", "resumo"]:
        if not n.get(k): erros.append(f"{p}: {k} ausente")
    if n.get("data") and not data_re.match(n["data"]): erros.append(f"{p}: data deve ser dd/mm/aaaa")
    tx = n.get("texto", [])
    if len(tx) != 3: erros.append(f"{p}: texto deve ter exatamente 3 parágrafos (tem {len(tx)})")
    for j, par in enumerate(tx, 1):
        if len(par) < 200: erros.append(f"{p}: parágrafo {j} curto demais ({len(par)} caracteres; mínimo 200)")
    f = n.get("fontes", [])
    if not f or not all(x.get("nome") and str(x.get("url", "")).startswith("https://") for x in f): erros.append(f"{p}: fontes precisam de nome e url https")
    a = n.get("arte", {})
    if a.get("tipo") not in TIPOS: erros.append(f"{p}: arte.tipo deve ser um de {sorted(TIPOS)}")
    if a.get("tema") not in TEMAS: erros.append(f"{p}: arte.tema deve ser um de {sorted(TEMAS)}")
    if a.get("tipo") == "linha" and len(a.get("pontos", [])) < 2: erros.append(f"{p}: arte linha precisa de 2+ pontos [rótulo, número]")
    if a.get("tipo") == "barras" and not (1 <= len(a.get("barras", [])) <= 4): erros.append(f"{p}: arte barras precisa de 1 a 4 barras")
    if a.get("tipo") == "barras" and not all(isinstance(b.get("valor"), (int, float)) for b in a.get("barras", [])): erros.append(f"{p}: valor das barras deve ser número")
    if a.get("tipo") == "indicador" and not (a.get("valor") and a.get("rotulo")): erros.append(f"{p}: arte indicador precisa de rotulo e valor")
if erros:
    print("\n".join("ERRO: " + e for e in erros)); sys.exit(1)
print("OK: site-data válido (3 notícias, 3 parágrafos cada)")
