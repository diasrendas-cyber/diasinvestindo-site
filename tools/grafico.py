"""Biblioteca dos gráficos das notícias (método Storytelling with Data).

Uso, num script da edição (graficos/AAAA-MM-DD.py):
    import sys; sys.path.insert(0, "tools"); from grafico import *
    fig, ax = quadro("Câmbio · dólar", "Dólar encosta em R$ 6", "Subtítulo curto.", "Fonte: ...")
    ... desenha em ax com as cores abaixo ...
    salvar(fig, "2026-11-24-3")   # -> assets/img/noticias/2026-11-24-3.png (1600x900)

Regras visuais (ver a skill "graficos-noticias-swd"):
- Título = a conclusão. Cinza para contexto, UMA cor de destaque para o que importa.
- Sem bordas, sem grade pesada, sem legenda separada: rótulos direto nos dados.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "assets", "img", "noticias")

TINTA = "#1F2937"    # texto principal
APAGADO = "#6B7280"  # texto secundário, eixos
CINZA = "#BFC5CD"    # dado de contexto
CLARO = "#E5E7EB"    # grade, partes menores
AZUL = "#1D4E89"     # destaque neutro/positivo
AZUL_CLARO = "#8DA9CC"
VERMELHO = "#B42318" # destaque de alerta (perda, acima do teto, abaixo da meta)
VERMELHO_BG = "#F6DCDA"
VERDE = "#1E7B4A"    # destaque de valor dentro da faixa-alvo (inflação entre piso e teto)
VERDE_BG = "#DDF0E4"

_fontes = [f for f in fm.findSystemFonts() if os.path.basename(f).startswith("Inter")]
for f in _fontes:
    fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter" if _fontes else "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

W, H, DPI = 8, 4.5, 200  # 1600 x 900 px (16:9)


def br(x, casas=2, prefixo="", sufixo=""):
    """Número no padrão brasileiro: br(5926.2, 1) -> '5.926,2'."""
    s = f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{prefixo}{s}{sufixo}"


def quadro(chapeu, titulo, subtitulo, fonte, area=(0.07, 0.15, 0.86, 0.55)):
    """Cria a figura com chapéu, título-conclusão, subtítulo, fonte e marca. Devolve (fig, ax)."""
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor("white")
    fig.text(0.05, 0.925, chapeu.upper(), fontsize=8.5, color=APAGADO, weight="semibold")
    fig.text(0.05, 0.845, titulo, fontsize=17, color=TINTA, weight="bold")
    fig.text(0.05, 0.785, subtitulo, fontsize=9.5, color=APAGADO)
    fonte = fonte if fonte.lower().startswith("fonte") else f"Fonte: {fonte}"
    fig.text(0.05, 0.035, fonte, fontsize=7.5, color=APAGADO)
    fig.text(0.95, 0.035, "diasinvestindo.com.br", fontsize=7.5, color=APAGADO, ha="right", weight="semibold")
    ax = fig.add_axes(list(area))
    limpar(ax)
    return fig, ax


def limpar(ax, grade_y=False):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0, colors=APAGADO, labelsize=8)
    if grade_y:
        ax.grid(axis="y", color=CLARO, lw=0.6)
        ax.set_axisbelow(True)


def salvar(fig, nome):
    """Salva em assets/img/noticias/<nome>.png e devolve o src para noticias.json."""
    os.makedirs(PASTA, exist_ok=True)
    caminho = os.path.join(PASTA, f"{nome}.png")
    fig.savefig(caminho, dpi=DPI)
    plt.close(fig)
    try:  # reduz o peso se o pngquant existir
        import subprocess
        subprocess.run(["pngquant", "--force", "--skip-if-larger", "--quality=70-95", "--output", caminho, caminho],
                       check=False, capture_output=True)
    except FileNotFoundError:
        pass
    print(f"ok {caminho} ({os.path.getsize(caminho)//1024} KB)")
    return f"/assets/img/noticias/{nome}.png"


def banda_meta(ax, valor, rotulo_valor, piso=1.5, centro=3.0, teto=4.5, ymin=0.0, ymax=6.0,
               sufixo="%", casas=2, nome_centro="Meta"):
    """Faixa da meta de inflação (regra de 27/11/2026, pedido do editor).

    Três linhas horizontais: teto em cima, centro (meta) no meio e piso embaixo.
    Valor DENTRO da faixa: faixa sombreada e ponto em VERDE.
    Valor FORA (acima do teto ou abaixo do piso): a região de fora sombreada e o ponto em VERMELHO.
    """
    limpar(ax)
    ax.set_xlim(0, 1); ax.set_ylim(ymin, ymax)
    dentro = piso <= valor <= teto
    cor = VERDE if dentro else VERMELHO
    if dentro:
        ax.axhspan(piso, teto, xmin=0.05, xmax=0.95, color=VERDE_BG, lw=0)
    elif valor > teto:
        ax.axhspan(teto, ymax, xmin=0.05, xmax=0.95, color=VERMELHO_BG, lw=0)
    else:
        ax.axhspan(ymin, piso, xmin=0.05, xmax=0.95, color=VERMELHO_BG, lw=0)
    for y, nome, estilo, peso in ((teto, "Teto", "--", "semibold"), (centro, nome_centro, ":", "normal"),
                                  (piso, "Piso", "--", "semibold")):
        ax.plot([0.05, 0.95], [y, y], ls=estilo, color=TINTA if nome != nome_centro else APAGADO, lw=1.3)
        ax.text(0.06, y + (ymax - ymin) * 0.015, f"{nome} {br(y, 1 if y % 1 else 0, sufixo=sufixo)}",
                ha="left", va="bottom", fontsize=10, color=TINTA if nome != nome_centro else APAGADO, weight=peso)
    ax.scatter([0.62], [valor], s=230, color=cor, zorder=4)
    folga = (ymax - ymin) * 0.03
    y_txt, va = (valor + folga, "bottom") if valor > teto else ((valor - folga, "top") if valor < piso else (valor, "center"))
    ax.text(0.70, y_txt, rotulo_valor, ha="left", va=va, fontsize=15, color=cor, weight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    return dentro
