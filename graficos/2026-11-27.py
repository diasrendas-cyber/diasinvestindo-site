"""Gráficos da edição de 27/11/2026. Rodar da raiz: python3 graficos/2026-11-27.py
Todos os números vêm das notícias da edição (conferidas em verificacao/2026-11-27.md)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from grafico import *
import matplotlib
matplotlib.rcParams["text.parse_math"] = False

src = {}

# 1) MERCADO — linha com fases anotadas (eixo de datas real: 20/11 feriado, 21-22/11 fim de semana)
fig, ax = quadro("Ibovespa · fechamento por pregão",
                 "Bolsa tem maior alta desde outubro: +6,07%",
                 "Pontos no fechamento, de 19/11 a 26/11/2026.",
                 "Jornal do Comércio, O Repórter, Campo Grande News; fechamentos já publicados no site",
                 area=(0.07, 0.15, 0.84, 0.52))
limpar(ax)
dias = [19, 23, 24, 25, 26]
pts = [166376, 164796, 164090, 166685, 176800]
rot = ["19/nov", "23/nov", "24/nov", "25/nov", "26/nov"]
ax.plot(dias[:4], pts[:4], color=CINZA, lw=3)
ax.plot(dias[3:], pts[3:], color=AZUL, lw=4)
ax.scatter(dias[:4], pts[:4], s=50, color=CINZA, zorder=3)
ax.scatter([26], [176800], s=140, color=AZUL, zorder=4)
ax.set_xlim(18.5, 27.4); ax.set_ylim(160500, 180500)
ax.text(19, 166376 + 900, "166.376", ha="center", va="bottom", fontsize=13, color=APAGADO)
ax.text(24, 164090 - 900, "164.090", ha="center", va="top", fontsize=13, color=APAGADO)
ax.text(25.85, 176800, "176.800", ha="right", va="center", fontsize=17, color=AZUL, weight="bold")
ax.text(21.0, 161700, "23–24/nov: duas quedas seguidas", ha="center", fontsize=13, color=APAGADO)
ax.text(26.15, 171200, "26/nov: Trabuco\ncotado para a\nFazenda, +6,07%", ha="left", va="center",
        fontsize=13, color=AZUL, weight="bold")
ax.set_xticks(dias); ax.set_xticklabels(rot, fontsize=12)
ax.set_yticks([])
src["mercado"] = salvar(fig, "2026-11-27-1")

# 2) IPCA-15 — inclinação (out x nov) + faixa de referência (12 meses x teto)
fig, ax = quadro("Inflação · IPCA-15 de novembro",
                 "Prévia desacelera, mas 12 meses passa do teto",
                 "Variação mensal e acumulado em 12 meses, em %.",
                 "IBGE, via O Repórter, Portal do Agronegócio e CNN Brasil, 26/11/2026")
ax.remove()
a1 = fig.add_axes([0.08, 0.15, 0.34, 0.5]); limpar(a1)
a1.set_xlim(-0.4, 1.4); a1.set_ylim(0.1, 0.42)
a1.plot([0, 1], [0.32, 0.22], color=AZUL, lw=3)
a1.scatter([0], [0.32], s=80, color=CINZA, zorder=3)
a1.scatter([1], [0.22], s=130, color=AZUL, zorder=4)
a1.text(0, 0.34, "0,32%", ha="center", va="bottom", fontsize=14, color=APAGADO)
a1.text(1, 0.20, "0,22%", ha="center", va="top", fontsize=17, color=AZUL, weight="bold")
a1.text(0.5, 0.42, "No mês", ha="center", va="top", fontsize=14, color=TINTA, weight="bold")
a1.set_xticks([0, 1]); a1.set_xticklabels(["Outubro", "Novembro"], fontsize=12); a1.set_yticks([])
a2 = fig.add_axes([0.52, 0.15, 0.42, 0.5]); limpar(a2)
a2.set_xlim(2.5, 5.3); a2.set_ylim(-1, 1.2)
a2.axvspan(4.5, 5.3, color=VERMELHO_BG, lw=0)
a2.plot([2.5, 5.3], [0, 0], color=CLARO, lw=2)
a2.axvline(4.5, color=TINTA, ls="--", lw=1.3)
a2.axvline(3.0, color=APAGADO, ls=":", lw=1.2)
a2.text(4.47, 0.55, "Teto 4,5%", ha="right", fontsize=13, color=TINTA)
a2.text(3.03, 0.55, "Meta 3%", ha="left", fontsize=13, color=APAGADO)
a2.scatter([4.64], [0], s=260, color=VERMELHO, zorder=4)
a2.text(4.9, -0.3, "4,64%", ha="center", va="top", fontsize=17, color=VERMELHO, weight="bold")
a2.text(3.75, 1.15, "Em 12 meses", ha="center", va="top", fontsize=14, color=TINTA, weight="bold")
a2.set_xticks([]); a2.set_yticks([])
src["ipca15"] = salvar(fig, "2026-11-27-2")

# 4) OPEP+ — barras ordenadas, só o protagonista colorido
fig, ax = quadro("Petróleo · reunião da Opep+ em 29/11",
                 "Cota do Iraque é menos da metade da saudita",
                 "Metas atuais, em milhões de barris por dia. O Iraque pede base maior.",
                 "The Rio Times e House of Saud, com dados da Opep, 26/11/2026",
                 area=(0.26, 0.16, 0.66, 0.5))
limpar(ax)
nomes = ["Arábia Saudita", "Rússia", "Iraque"]
vals = [10.5, 9.9, 4.4]
ys = [2, 1, 0]
ax.barh(ys, vals, height=0.55, color=[CINZA, CINZA, AZUL])
for y, n, v in zip(ys, nomes, vals):
    cor = AZUL if n == "Iraque" else APAGADO
    ax.text(-0.25, y, n, ha="right", va="center", fontsize=15, color=cor, weight="bold" if n == "Iraque" else "normal")
    ax.text(v + 0.2, y, br(v, 1), ha="left", va="center", fontsize=16 if n == "Iraque" else 14, color=cor,
            weight="bold" if n == "Iraque" else "normal")
ax.set_xlim(0, 12); ax.set_ylim(-0.6, 2.6)
ax.set_xticks([]); ax.set_yticks([])
src["opep"] = salvar(fig, "2026-11-27-4")
print(src)
