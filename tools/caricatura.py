"""Caricaturas editoriais das notícias, geradas pela API do Gemini.

Roda no GitHub Actions (workflow .github/workflows/caricaturas.yml), porque o
ambiente da tarefa diária não alcança a API do Google.

Entrada: caricaturas/AAAA-MM-DD.json, escrito pela tarefa diária:
{
  "data": "2026-11-27",
  "itens": [
    {
      "slug": "<slug da notícia em noticias.json>",
      "n": 1,                               # posição da notícia na edição (1 a 4)
      "modo": "caricatura" | "misto" | "objeto",  # misto = gráfico + caricatura; objeto = objeto personificado
      "pessoa": "Nome Completo",
      "prompt": "Stylized editorial caricature of ...",   # template de estilo preenchido
      "grafico_base": "/assets/img/noticias/AAAA-MM-DD-N.png",  # só no modo misto
      "alt": "descrição da figura e da conclusão",
      "fonte": "Fonte: ...",                # fonte dos dados (misto) ou "Fonte: ilustração gerada com IA (Gemini)"
      "legenda_social": "legenda curta para redes sociais"
    }
  ]
}

Para cada item sem "resultado": gera a caricatura, monta a figura 1600x900,
salva em assets/img/noticias/ e aponta o campo "grafico" da notícia para ela.
Se a geração falhar, a notícia fica com a figura que já tinha e o item recebe
"resultado": "falhou: <motivo>". O script nunca termina com erro por falha do
Gemini, para não travar a publicação.

Uso: python3 tools/caricatura.py [AAAA-MM-DD]   (sem data: o arquivo mais recente)
Teste sem API: CARICATURA_FALSA=1 python3 tools/caricatura.py AAAA-MM-DD
"""
import base64, io, json, os, sys, time, urllib.error, urllib.request

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ENTRADA = os.path.join(RAIZ, "caricaturas")
PASTA_IMG = os.path.join(RAIZ, "assets", "img", "noticias")
W, H = 1600, 900
MODELO = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image")
API = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"


def log(msg):
    print(f"[caricatura] {msg}", flush=True)


def _chamar(prompt, com_formato):
    corpo = {"contents": [{"parts": [{"text": prompt}]}],
             "generationConfig": {"responseModalities": ["IMAGE"]}}
    if com_formato:
        corpo["generationConfig"]["imageConfig"] = {"aspectRatio": "16:9"}
    req = urllib.request.Request(
        API.format(MODELO), data=json.dumps(corpo).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.load(r)
    for cand in resp.get("candidates", []):
        for parte in cand.get("content", {}).get("parts", []):
            dado = parte.get("inlineData") or parte.get("inline_data")
            if dado and dado.get("data"):
                return Image.open(io.BytesIO(base64.b64decode(dado["data"]))).convert("RGB")
    motivo = (resp.get("promptFeedback", {}).get("blockReason")
              or ",".join(c.get("finishReason", "") for c in resp.get("candidates", []))
              or "resposta sem imagem")
    raise RuntimeError(f"sem imagem ({motivo})")


def gerar_imagem(prompt):
    if os.environ.get("CARICATURA_FALSA"):
        img = Image.new("RGB", (1344, 768), "#D7261E")
        d = ImageDraw.Draw(img)
        d.ellipse((520, 120, 820, 470), fill="#F2C9A0", outline="black", width=8)
        d.rectangle((470, 470, 870, 768), fill="#1F2937", outline="black", width=8)
        return img
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY não configurada")
    ultimo = None
    for tentativa, com_formato in enumerate((True, True, False)):
        try:
            return _chamar(prompt, com_formato)
        except urllib.error.HTTPError as e:
            corpo = e.read().decode(errors="replace")[:300]
            ultimo = f"HTTP {e.code}: {corpo}"
            if e.code in (400,) and com_formato:
                continue  # tenta de novo sem imageConfig
            if e.code not in (429, 500, 502, 503, 504):
                break
        except Exception as e:  # rede, bloqueio de conteúdo, resposta vazia
            ultimo = str(e)
        time.sleep(5 * (tentativa + 1))
    raise RuntimeError(ultimo or "falha desconhecida")


def cobrir(img, w, h, foco_x=0.5):
    """Redimensiona cobrindo w x h e corta o excesso (foco horizontal em foco_x)."""
    esc = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
    x = round((img.width - w) * foco_x)
    y = round((img.height - h) / 2)
    return img.crop((x, y, x + w, y + h))


def montar(item, caric):
    if item["modo"] == "misto":
        base = os.path.join(RAIZ, item["grafico_base"].lstrip("/"))
        graf = Image.open(base).convert("RGB")
        larg_car = 560                       # faixa da caricatura à esquerda
        tela = Image.new("RGB", (W, H), graf.getpixel((graf.width - 5, graf.height // 2)))
        tela.paste(cobrir(caric, larg_car, H), (0, 0))
        larg_g = W - larg_car
        alt_g = round(graf.height * larg_g / graf.width)
        tela.paste(graf.resize((larg_g, alt_g), Image.LANCZOS), (larg_car, (H - alt_g) // 2))
        return tela
    return cobrir(caric, W, H)


def processar(data):
    caminho = os.path.join(PASTA_ENTRADA, f"{data}.json")
    pedido = json.load(open(caminho, encoding="utf-8"))
    noticias_arq = os.path.join(RAIZ, "noticias.json")
    dados = json.load(open(noticias_arq, encoding="utf-8"))
    por_slug = {n.get("slug"): n for n in dados["noticias"]}
    mudou = False
    for item in pedido.get("itens", []):
        if item.get("resultado"):
            continue
        rotulo = f"notícia {item.get('n')} ({item.get('pessoa')})"
        noticia = por_slug.get(item.get("slug"))
        if not noticia:
            item["resultado"] = "falhou: slug não encontrado em noticias.json"
            log(f"{rotulo}: {item['resultado']}"); continue
        if item.get("modo") == "misto" and not os.path.isfile(os.path.join(RAIZ, str(item.get("grafico_base", "")).lstrip("/"))):
            item["modo"] = "caricatura"
            log(f"{rotulo}: gráfico base não encontrado, segue só com a caricatura")
        try:
            caric = gerar_imagem(item["prompt"])
        except Exception as e:
            item["resultado"] = f"falhou: {e}"[:400]
            log(f"{rotulo}: {item['resultado']} (mantida a figura existente)"); continue
        sufixo = "mix" if item["modo"] == "misto" else "car"
        nome = f"{data}-{item.get('n')}-{sufixo}.png"
        montar(item, caric).save(os.path.join(PASTA_IMG, nome), optimize=True)
        cobrir(caric, W, H).save(os.path.join(PASTA_IMG, f"{data}-{item.get('n')}-car-original.png"), optimize=True)
        noticia["grafico"] = {"src": f"/assets/img/noticias/{nome}", "alt": item["alt"], "fonte": item["fonte"]}
        item["resultado"] = f"ok: /assets/img/noticias/{nome}"
        mudou = True
        log(f"{rotulo}: {item['resultado']}")
    json.dump(pedido, open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    if mudou:
        json.dump(dados, open(noticias_arq, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        open(noticias_arq, "a", encoding="utf-8").write("\n")
    return mudou


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = sys.argv[1]
    else:
        arqs = sorted(f for f in os.listdir(PASTA_ENTRADA) if f.endswith(".json"))
        if not arqs:
            log("nenhum pedido em caricaturas/"); sys.exit(0)
        data = arqs[-1][:-5]
    print("MUDOU" if processar(data) else "SEM_MUDANCA")
