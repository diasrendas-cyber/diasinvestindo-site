"""Gráficos da edição de 28/11/2026. Rodar da raiz: python3 graficos/2026-11-28.py
Todos os números vêm das notícias da edição (conferidas em verificacao/2026-11-28.md)."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from grafico import *
import matplotlib
matplotlib.rcParams["text.parse_math"] = False

src = {}

# 1) DÓLAR — linha com fases anotadas, eixo de datas real (20/11 feriado; 21-22/11 fim de semana)
fig, ax = quadro("Câmbio · dólar comercial no fechamento",
                 "Dólar cai 7,07% na semana e fecha a R$ 5,52",
                 "Reais por dólar, de 19/11 a 27/11/2026. Na semana: -7,07%.",
                 "", area=(0.07, 0.15, 0.82, 0.52))
limpar(ax)
d = [dt.date(2026, 11, x) for x in (19, 23, 24, 25, 26, 27)]
v = [5.934, 5.926, 5.911, 5.817, 5.744, 5.516]
ax.plot(d[:5], v[:5], color=CINZA, lw=3)
ax.plot(d[4:], v[4:], color=AZUL, lw=4)
ax.scatter(d[:5], v[:5], s=50, color=CINZA, zorder=3)
ax.scatter([d[5]], [v[5]], s=150, color=AZUL, zorder=4)
ax.text(d[0], v[0] + 0.025, "R$ 5,93", ha="center", va="bottom", fontsize=14, color=APAGADO)
ax.text(d[5] + dt.timedelta(days=0.6), v[5], "R$ 5,52", ha="left", va="center", fontsize=18,
        color=AZUL, weight="bold")
ax.text(d[2], 5.70, "23–26/nov: quatro\nquedas menores", ha="center", va="center", fontsize=13, color=APAGADO)
ax.text(d[4] - dt.timedelta(days=0.2), 5.53, "27/nov: 1º pregão\ncom Trabuco\nconfirmado: -3,97%", ha="right",
        va="center", fontsize=13, color=AZUL, weight="bold")
ax.set_xlim(d[0] - dt.timedelta(days=0.6), d[5] + dt.timedelta(days=2.0))
ax.set_ylim(5.42, 6.02)
ax.set_xticks(d); ax.set_xticklabels([x.strftime("%d/nov") for x in d], fontsize=12)
ax.set_yticks([])
src["dolar"] = salvar(fig, "2026-11-28-1")

# 2) IGP-M — número grande + exemplo de reajuste de aluguel (conta: 2.000 x 1,0626)
fig, ax = quadro("Inflação · IGP-M de novembro",
                 "Aluguel pelo IGP-M sobe 6,26% em 12 meses",
                 "IGP-M acumulado em 12 meses até novembro de 2026.",
                 "", area=(0.07, 0.12, 0.86, 0.6))
ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0.0, 0.60, "6,26%", ha="left", va="center", fontsize=82, color=VERMELHO, weight="bold")
ax.text(0.0, 0.30, "1,24% só em novembro", ha="left", va="center", fontsize=17, color=APAGADO)
ax.text(0.60, 0.74, "Exemplo de reajuste", ha="left", va="center", fontsize=16, color=TINTA, weight="bold")
ax.text(0.60, 0.58, "Aluguel de R$ 2.000", ha="left", va="center", fontsize=18, color=APAGADO)
ax.text(0.60, 0.44, "passa a R$ 2.125,20", ha="left", va="center", fontsize=22, color=VERMELHO, weight="bold")
ax.text(0.60, 0.31, "(+R$ 125,20 por mês)", ha="left", va="center", fontsize=16, color=APAGADO)
src["igpm"] = salvar(fig, "2026-11-28-2")

# 3) DESEMPREGO — inclinação antes x agora (trimestres móveis) com a mínima da série tracejada
fig, ax = quadro("Emprego · PNAD Contínua",
                 "Desemprego cai a 5,1% e iguala o recorde",
                 "Taxa de desocupação por trimestre móvel, em %.",
                 "", area=(0.10, 0.15, 0.78, 0.52))
limpar(ax)
x = [0, 1, 2]
t = [5.4, 5.3, 5.1]
rot = ["ago–out\n2025", "mai–jul\n2026", "ago–out\n2026"]
ax.plot([-0.4, 1.95], [5.1, 5.1], color=AZUL, lw=1.5, ls="--", alpha=0.6)
ax.text(-0.35, 5.085, "mínima da série (dez/2025): 5,1%", ha="left", va="top", fontsize=13, color=AZUL)
ax.plot(x[:2], t[:2], color=CINZA, lw=3)
ax.plot(x[1:], t[1:], color=AZUL, lw=4)
ax.scatter(x[:2], t[:2], s=70, color=CINZA, zorder=3)
ax.scatter([2], [5.1], s=170, color=AZUL, zorder=4)
ax.text(0, 5.4 + 0.025, "5,4%", ha="center", va="bottom", fontsize=16, color=APAGADO)
ax.text(1, 5.3 + 0.025, "5,3%", ha="center", va="bottom", fontsize=16, color=APAGADO)
ax.text(2.12, 5.1, "5,1%", ha="left", va="center", fontsize=20, color=AZUL, weight="bold")
ax.set_xlim(-0.4, 2.6); ax.set_ylim(4.95, 5.5)
ax.set_xticks(x); ax.set_xticklabels(rot, fontsize=13)
ax.set_yticks([])
src["desemprego"] = salvar(fig, "2026-11-28-3")
print(src)
