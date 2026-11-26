"""Gráficos da edição de 26/11/2026. Rodar da raiz: python3 graficos/2026-11-26.py
Todos os números vêm das notícias da edição (conferidas em verificacao/2026-11-26.md)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from grafico import *
import matplotlib
matplotlib.rcParams["text.parse_math"] = False

def moldura(chapeu, titulo, sub, fonte):
    fig, ax = quadro(chapeu, titulo, sub, fonte)
    ax.remove()
    return fig

src = {}

# 1) MERCADO — inclinação (antes x depois) em dois quadros
fig = moldura("Bolsa e câmbio · fechamento de 25/11",
              "Bolsa sobe 1,58% e dólar cai 1,59%",
              "Fechamentos de terça (24/11) e quarta (25/11).",
              "Canal Rural (Estadão Conteúdo), O Tempo, BM&C News (Agência Brasil)")
for i, (nome, a, b, txt_a, txt_b, var, lim) in enumerate([
        ("Ibovespa (pontos)", 164089.81, 166684.61, "164.090", "166.685", "+1,58%", (163000, 168600)),
        ("Dólar comercial (R$)", 5.9107, 5.8168, "R$ 5,91", "R$ 5,82", "-1,59%", (5.76, 5.99))]):
    ax = fig.add_axes([0.08 + i * 0.47, 0.14, 0.36, 0.52])
    limpar(ax)
    ax.set_xlim(-0.35, 1.35); ax.set_ylim(*lim)
    ax.plot([0, 1], [a, b], color=AZUL, lw=3)
    ax.scatter([0], [a], s=70, color=CINZA, zorder=3)
    ax.scatter([1], [b], s=110, color=AZUL, zorder=4)
    off = (lim[1] - lim[0]) * 0.06
    ax.text(0, a + (off if b < a else -off), txt_a, ha="center", va="bottom" if b < a else "top", fontsize=12, color=APAGADO)
    ax.text(1, b + (off if b > a else -off), txt_b, ha="center", va="bottom" if b > a else "top", fontsize=15, color=AZUL, weight="bold")
    ax.text(0.5, lim[1], f"{nome}  {var}", ha="center", va="top", fontsize=13, color=TINTA, weight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["24/nov", "25/nov"], fontsize=11)
    ax.set_yticks([])
src["mercado"] = salvar(fig, "2026-11-26-1")

# 2) EMBRAER — barras divergentes (contra a maré)
fig = moldura("Embraer · proposta de tarifa dos EUA",
              "Embraer cai 4% em dia de alta da bolsa",
              "Variação no pregão de 25/11, em %.",
              "Correio Braziliense, O Tempo, BM&C News, Canal Rural")
ax = fig.add_axes([0.22, 0.16, 0.7, 0.5])
limpar(ax)
ax.barh([1, 0], [1.58, -4.0], height=0.5, color=[CINZA, VERMELHO])
ax.axvline(0, color=TINTA, lw=1.2)
ax.set_xlim(-5.2, 3.0); ax.set_ylim(-0.6, 1.6)
ax.text(1.58 + 0.12, 1, "+1,58%", va="center", fontsize=13, color=APAGADO)
ax.text(-4.0 - 0.12, 0, "-4%", va="center", ha="right", fontsize=16, color=VERMELHO, weight="bold")
ax.text(0.15, 1, "", va="center")
ax.text(-0.15, 1, "Ibovespa", va="center", ha="right", fontsize=14, color=APAGADO)
ax.text(0.15, 0, "Embraer", va="center", ha="left", fontsize=15, color=VERMELHO, weight="bold")
ax.set_yticks([])
ax.set_xticks([])
src["embraer"] = salvar(fig, "2026-11-26-2")

# 3) PCE — ponto e alvo (previsão x realizado)
fig = moldura("EUA · inflação PCE de outubro",
              "Núcleo da inflação dos EUA supera a previsão",
              "Núcleo do PCE em 12 meses, em %. Índice cheio: 3,8%.",
              "Yahoo Finanças, Fox Business, dados divulgados em 25/11/2026")
ax = fig.add_axes([0.08, 0.2, 0.84, 0.42])
limpar(ax)
ax.set_xlim(2.95, 3.55); ax.set_ylim(-1, 1)
ax.plot([2.95, 3.55], [0, 0], color=CLARO, lw=2)
ax.plot([3.2, 3.3], [0, 0], color=VERMELHO, lw=4)
ax.scatter([3.2], [0], s=320, facecolor="white", edgecolor=APAGADO, lw=2.5, zorder=3)
ax.scatter([3.3], [0], s=380, color=VERMELHO, zorder=4)
ax.text(3.2, -0.35, "Previsão\n3,2%", ha="center", va="top", fontsize=13, color=APAGADO)
ax.text(3.3, -0.35, "Outubro\n3,3%", ha="center", va="top", fontsize=15, color=VERMELHO, weight="bold")
ax.text(3.25, 0.3, "+0,1 p.p.", ha="center", va="bottom", fontsize=14, color=VERMELHO, weight="bold")
ax.set_xticks([]); ax.set_yticks([])
src["pce"] = salvar(fig, "2026-11-26-3")

# 4) OPENAI — barra 100% empilhada
fig = moldura("OpenAI · proteínas desenhadas pelo GPT-6.2",
              "35 de 322 proteínas da IA se ligaram",
              "Designs testados em laboratório (Onava) contra 5 alvos.",
              "OpenAI, Unite.AI, AlphaSignal, 24/11/2026")
ax = fig.add_axes([0.06, 0.26, 0.88, 0.3])
limpar(ax)
ax.barh(0, 35, color=AZUL, height=0.6)
ax.barh(0, 287, left=35, color=CLARO, height=0.6)
ax.set_xlim(0, 322); ax.set_ylim(-0.8, 1.0)
ax.text(2, 0.45, "35 com ligação (10,9%)", ha="left", va="bottom", fontsize=15, color=AZUL, weight="bold")
ax.text(320, 0, "287 sem ligação", ha="right", va="center", fontsize=13, color=APAGADO)
ax.set_xticks([]); ax.set_yticks([])
src["openai"] = salvar(fig, "2026-11-26-4")
print(src)
