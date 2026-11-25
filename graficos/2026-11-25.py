"""Gráficos da edição de 25/11/2026. Rodar da raiz: python3 graficos/2026-11-25.py
Todos os números vêm das notícias da edição (conferidas em verificacao/2026-11-25.md)."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from grafico import *
import matplotlib
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.dates as mdates

def moldura(chapeu, titulo, sub, fonte):
    fig, ax = quadro(chapeu, titulo, sub, fonte)
    ax.remove()
    return fig

src = {}

# 1) AJUSTE FISCAL — comparação de duas barras (antes x depois)
fig = moldura("Ajuste fiscal · lei sancionada em 24/11",
              "Teto de alta real do gasto cai para 2%",
              "Crescimento real máximo da despesa em anos com contingenciamento, a partir de 2027.",
              "Times Brasil (Estadão Conteúdo), Diário de S. Paulo, Jornal Opção")
ax = fig.add_axes([0.24, 0.17, 0.68, 0.5])
limpar(ax)
ax.set_xlim(0, 3.0); ax.set_ylim(-0.7, 1.7)
ax.barh(1, 2.5, height=0.5, color=CINZA)
ax.barh(0, 2.0, height=0.5, color=AZUL)
ax.set_yticks([1, 0]); ax.set_yticklabels(["Regra anterior", "Nova lei"], fontsize=11)
ax.get_yticklabels()[0].set_color(APAGADO)
ax.get_yticklabels()[1].set_weight("bold"); ax.get_yticklabels()[1].set_color(TINTA)
ax.text(2.5 + 0.05, 1, "2,5%", va="center", fontsize=13, color=APAGADO)
ax.text(2.0 + 0.05, 0, "2%", va="center", fontsize=15, color=TINTA, weight="bold")
ax.plot([2.5, 2.5], [0.75, -0.3], ls=":", color=APAGADO, lw=1)
ax.annotate("", xy=(2.0, -0.45), xytext=(2.5, -0.45),
            arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.4))
ax.text(2.25, -0.62, "-0,5 p.p.", ha="center", color=AZUL, fontsize=11, weight="bold")
ax.set_xticks([])
src["fiscal"] = salvar(fig, "2026-11-25-1")

# 2) ANTHROPIC — linha até a barreira (preço do IPO)
fig = moldura("Anthropic · ação na Nasdaq",
              "Ação fecha abaixo do preço do IPO",
              "Fechamento por pregão, em US$. Linha vermelha: preço da oferta, US$ 83.",
              "Yahoo Finanças, Seoul Economic Daily, CappNotes; fechamentos publicados no site")
ax = fig.add_axes([0.08, 0.15, 0.78, 0.53])
limpar(ax)
d = [dt.date(2026, 11, x) for x in (19, 20, 23, 24)]
v = [97.17, 88.91, 87.64, 81.9]
ax.set_xlim(dt.date(2026, 11, 18), dt.date(2026, 11, 25, ))
ax.set_ylim(76, 101)
ax.axhline(83, ls="--", color=VERMELHO, lw=1.1)
ax.text(dt.date(2026, 11, 18), 83.5, "IPO: US$ 83", color=VERMELHO, fontsize=10, weight="semibold", va="bottom")
ax.plot(d[:-1], v[:-1], color=CINZA, lw=2.2)
ax.plot(d[-2:], v[-2:], color=VERMELHO, lw=2.6)
ax.scatter(d[:-1], v[:-1], s=22, color=CINZA, zorder=3)
ax.scatter([d[-1]], [v[-1]], s=60, color=VERMELHO, zorder=4)
for x, y, dx in zip(d[:-1], v[:-1], (0, 0.25, 0)):
    ax.text(x + dt.timedelta(days=dx), y + 1.0, br(y, 2), ha="center", fontsize=10, color=APAGADO)
ax.text(d[-1], v[-1] - 1.3, "US$ 81,9", ha="center", va="top", fontsize=12, color=VERMELHO, weight="bold")
ax.set_yticks([]); ax.tick_params(colors=APAGADO, labelsize=9)
ax.set_xticks(d); ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/nov"))
src["anthropic"] = salvar(fig, "2026-11-25-2")

# 3) MERCADO — barras ordenadas (quem pressionou)
fig = moldura("Bolsa · fechamento de 24/11",
              "Vale cai 5,5% e pesa no Ibovespa",
              "Variação no dia, em %.",
              "O Repórter, The Rio Times, Brasil em Folhas")
ax = fig.add_axes([0.22, 0.16, 0.7, 0.52])
limpar(ax)
nomes = ["Vale ON", "Petrobras PN", "Ibovespa"]
vals = [-5.51, -1.82, -0.43]
cores = [VERMELHO, CINZA, CINZA]
ys = [2, 1, 0]
ax.barh(ys, [abs(x) for x in vals], height=0.55, color=cores)
ax.set_xlim(0, 7); ax.set_ylim(-0.6, 2.6)
for y, x, c in zip(ys, vals, cores):
    ax.text(abs(x) + 0.12, y, br(x, 2, sufixo="%"), va="center", fontsize=13 if c == VERMELHO else 11,
            color=VERMELHO if c == VERMELHO else APAGADO, weight="bold" if c == VERMELHO else "normal")
ax.set_yticks(ys); ax.set_yticklabels(nomes, fontsize=11)
ax.get_yticklabels()[0].set_weight("bold"); ax.get_yticklabels()[0].set_color(TINTA)
ax.set_xticks([])
src["mercado"] = salvar(fig, "2026-11-25-3")

# 4) BRASKEM — concentração (o que vira ação)
fig = moldura("Braskem · acordo preliminar com credores",
              "Até US$ 3,6 bi de dívida pode virar ação",
              "Em US$ bilhões. Ação PN caiu 14,09% em 24/11, a R$ 2,50.",
              "InfoMoney, CNN Brasil (Reuters), Bloomberg Línea, Times Brasil")
ax = fig.add_axes([0.3, 0.16, 0.62, 0.52])
limpar(ax)
nomes = ["Dívidas em reestruturação", "Conversão em ações (até)", "Oferta de novas ações"]
vals = [11, 3.6, 2.25]
txt = ["cerca de 11", "3,6", "2,25"]
cores = [CINZA, AZUL, CINZA]
ys = [2, 1, 0]
ax.barh(ys, vals, height=0.55, color=cores)
ax.set_xlim(0, 13.5); ax.set_ylim(-0.6, 2.6)
for y, x, t, c in zip(ys, vals, txt, cores):
    ax.text(x + 0.2, y, t, va="center", fontsize=13 if c == AZUL else 11,
            color=AZUL if c == AZUL else APAGADO, weight="bold" if c == AZUL else "normal")
ax.set_yticks(ys); ax.set_yticklabels(nomes, fontsize=10.5)
ax.get_yticklabels()[1].set_weight("bold"); ax.get_yticklabels()[1].set_color(TINTA)
ax.set_xticks([])
src["braskem"] = salvar(fig, "2026-11-25-4")
print(src)
