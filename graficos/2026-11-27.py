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

# 2) IPCA-15 — tendência de 6 meses (linha) + faixa da meta (teto, meta e piso)
fig, ax = quadro("Inflação · IPCA-15 de novembro",
                 "Prévia desacelera, mas 12 meses passa do teto",
                 "IPCA-15 no mês (jun–nov/2026) e acumulado em 12 meses, em %.",
                 "IBGE; Fazenda, B3, Agência Gov, Exame, O Repórter, Portal do Agronegócio")
ax.remove()
a1 = fig.add_axes([0.07, 0.15, 0.5, 0.5]); limpar(a1)
meses = ["jun", "jul", "ago", "set", "out", "nov"]
mensal = [0.41, 0.06, -0.40, 0.70, 0.32, 0.22]
x = list(range(6))
a1.axhline(0, color=CLARO, lw=1.2)
a1.plot(x[:4], mensal[:4], color=CINZA, lw=2.5)
a1.plot(x[3:], mensal[3:], color=AZUL, lw=3.5)
a1.scatter(x[:3], mensal[:3], s=40, color=CINZA, zorder=3)
a1.scatter(x[3:], mensal[3:], s=[60, 60, 120], color=AZUL, zorder=4)
for i, v in enumerate(mensal):
    cor = AZUL if i >= 3 else APAGADO
    abaixo = v < 0 or i == 4
    a1.text(i, v + (-0.09 if abaixo else 0.09), br(v, 2, sufixo="%"), ha="center",
            va="top" if abaixo else "bottom", fontsize=13 if i == 5 else 11, color=cor,
            weight="bold" if i == 5 else "normal")
a1.text(4.0, -0.42, "Out–nov: duas\ndesacelerações seguidas", ha="center", va="center", fontsize=11, color=AZUL, weight="bold")
a1.set_xlim(-0.4, 5.4); a1.set_ylim(-0.65, 0.95)
a1.set_xticks(x); a1.set_xticklabels(meses, fontsize=11); a1.set_yticks([])
fig.text(0.07, 0.69, "No mês", ha="left", va="center", fontsize=13, color=TINTA, weight="bold")
a2 = fig.add_axes([0.62, 0.15, 0.34, 0.5])
banda_meta(a2, 4.64, "4,64%", ymin=0.5, ymax=5.6)
fig.text(0.62 + 0.34 * 0.05, 0.69, "Em 12 meses", ha="left", va="center", fontsize=13, color=TINTA, weight="bold")
src["ipca15"] = salvar(fig, "2026-11-27-2-v2")

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
