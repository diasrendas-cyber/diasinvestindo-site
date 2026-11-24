"""Gráficos da edição de 24/11/2026. Rodar da raiz: python3 graficos/2026-11-24.py
Todos os números vêm das notícias da edição (conferidas em verificacao/2026-11-24.md)."""
import sys, os, datetime as dt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from grafico import *
import matplotlib
import matplotlib.dates as mdates

def moldura(chapeu, titulo, sub, fonte):
    fig, ax = quadro(chapeu, titulo, sub, fonte)
    ax.remove()
    return fig

src = {}

# 1) CÂMARA — linha de corte
fig = moldura("Ajuste fiscal · PLP 299/2026",
            "Aprovado com 96 votos de folga",
            "Votação na Câmara em 23/11. O texto segue para sanção (o Senado aprovou por 69 a 2).",
            "Câmara dos Deputados, via Atlas Público, TMC")
ax = fig.add_axes([0.05, 0.16, 0.9, 0.52])
limpar(ax)
ax.set_xlim(0, 486); ax.set_ylim(-1.2, 1.6)
h = 0.55
ax.barh(0, 353, height=h, color=AZUL, left=0)
ax.barh(0, 128 - 1.5, height=h, color=CINZA, left=353 + 1.5)
ax.barh(0, 5 - 1.5, height=h, color=CLARO, left=481 + 1.5)
ax.text(8, 0, "353 a favor", va="center", color="white", fontsize=11, weight="bold")
ax.text(353 + 10, 0, "128 contra", va="center", color=TINTA, fontsize=10)
ax.annotate("5 abstenções", xy=(483.5, -h / 2), xytext=(483.5, -0.75), ha="right",
            fontsize=8, color=APAGADO, arrowprops=dict(arrowstyle="-", color=APAGADO, lw=0.8))
ax.plot([257, 257], [-0.55, 0.95], ls="--", color=TINTA, lw=1.2)
ax.text(257, 1.02, "mínimo para aprovar: 257", ha="center", fontsize=9, color=TINTA)
# chave de folga
y = 0.52
ax.annotate("", xy=(257, y), xytext=(353, y),
            arrowprops=dict(arrowstyle="<->", color=AZUL, lw=1.4))
ax.text(305, y + 0.13, "+96", ha="center", color=AZUL, fontsize=11, weight="bold")
ax.set_xticks([]); ax.set_yticks([])
src["camara"] = salvar(fig, "2026-11-24-1")

# 2) PETROBRAS — comparação com plano anterior
fig = moldura("Petrobras · Plano de Negócios 2027-2031",
            "Investimento previsto sobe 12%",
            "Em US$ bilhões, total para cinco anos. Mais de 70% vai para exploração e produção.",
            "Petrobras (CVM), InfoMoney, Reuters")
ax = fig.add_axes([0.2, 0.16, 0.72, 0.52])
limpar(ax)
ax.set_xlim(0, 140); ax.set_ylim(-0.7, 1.7)
ax.barh(1, 109, height=0.5, color=CINZA)
ax.barh(0, 113, height=0.5, color=AZUL)
ax.barh(0, 9 - 0.8, height=0.5, left=113 + 0.8, color="#8DA9CC")
ax.set_yticks([1, 0]); ax.set_yticklabels(["Plano anterior", "Plano 2027-2031"], fontsize=10)
ax.get_yticklabels()[1].set_weight("bold"); ax.get_yticklabels()[1].set_color(TINTA)
ax.get_yticklabels()[0].set_color(APAGADO)
ax.text(109 + 2, 1, "109", va="center", fontsize=11, color=APAGADO)
ax.text(122 + 2, 0, "122", va="center", fontsize=13, color=TINTA, weight="bold")
ax.text(4, 0, "113 em projetos já em implantação", va="center", color="white", fontsize=9.5)
ax.annotate("9 em avaliação", xy=(117.5, -0.25), xytext=(117.5, -0.6), ha="center",
            fontsize=8, color=APAGADO, arrowprops=dict(arrowstyle="-", color=APAGADO, lw=0.8))
ax.plot([109, 109], [0.75, -0.3], ls=":", color=APAGADO, lw=1)
ax.annotate("", xy=(122, 0.5), xytext=(109, 0.5),
            arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.4))
ax.text(115.5, 0.6, "+13", ha="center", color=AZUL, fontsize=10, weight="bold")
ax.set_xticks([])
src["petrobras"] = salvar(fig, "2026-11-24-2")

# 3) DÓLAR — escalada até R$ 6
fig = moldura("Câmbio · dólar comercial",
            "Dólar sobe 8% desde 5/nov e encosta em R$ 6",
            "Fechamentos em reais. Em 23/11 bateu R$ 6,0055 de manhã, mas fechou em queda de 0,15%.",
            "O Povo, Metrópoles, TradeMap; fechamentos noticiados no site")
ax = fig.add_axes([0.07, 0.15, 0.78, 0.55])
limpar(ax)
d = [dt.date(2026, 11, x) for x in (5, 6, 9, 10, 12, 13, 17, 18, 19, 23)]
v = [5.49, 5.51, 5.506, 5.586, 5.65, 5.657, 5.78, 5.87, 5.93, 5.9262]
ax.set_ylim(5.4, 6.08)
ax.set_xlim(dt.date(2026, 11, 4), dt.date(2026, 11, 26))
ax.axhline(6.0, ls="--", color=VERMELHO, lw=1.1)
ax.text(dt.date(2026, 11, 4), 6.012, "R$ 6,00", color=VERMELHO, fontsize=9, weight="semibold")
ax.plot(d, v, color=AZUL, lw=2.2, solid_capstyle="round")
ax.scatter(d, v, s=14, color=AZUL, zorder=3)
ax.scatter([d[-1]], [6.0055], s=40, facecolor="white", edgecolor=VERMELHO, lw=1.5, zorder=4)
ax.plot([d[-1], d[-1]], [v[-1], 6.0055], color=VERMELHO, lw=1, ls=":")
ax.text(d[-1] - dt.timedelta(days=0.4), 6.03, "máx. do dia: R$ 6,0055", fontsize=8.5,
        color=VERMELHO, va="bottom", ha="right")
ax.text(d[-1] + dt.timedelta(days=0.4), v[-1] - 0.02, "fechou\nR$ 5,93", fontsize=9,
        color=TINTA, weight="bold", va="top")
ax.text(d[0], v[0] - 0.035, "R$ 5,49", fontsize=9, color=TINTA, ha="left", va="top")
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:.1f}".replace(".", ",")))
ax.set_yticks([5.5, 5.7, 5.9])
ax.tick_params(colors=APAGADO, labelsize=8)
ax.grid(axis="y", color=CLARO, lw=0.6)
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[5, 10, 15, 20, 23]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/nov"))
src["dolar"] = salvar(fig, "2026-11-24-3")

# 4) FOCUS — distância até o teto da meta
fig = moldura("Boletim Focus · 23/11",
            "Inflação esperada segue acima do teto",
            "Projeção do IPCA pelo mercado. Cinza: semana anterior; vermelho: agora.",
            "Banco Central (Boletim Focus), InfoMoney")
ax = fig.add_axes([0.07, 0.15, 0.68, 0.55])
limpar(ax)
ax.set_xlim(-0.6, 1.6); ax.set_ylim(2.5, 5.45)
ax.axhline(4.5, color=TINTA, lw=1.1, ls="--")
ax.axhline(3.0, color=APAGADO, lw=0.9, ls=":")
ax.text(1.62, 4.5, "teto da meta\n4,5%", va="center", fontsize=8.5, color=TINTA)
ax.text(1.62, 3.0, "centro da meta\n3%", va="center", fontsize=8.5, color=APAGADO)
dados = [("2026", 5.11, 5.15), ("2027", 5.00, 5.12)]
for i, (ano, antes, agora) in enumerate(dados):
    ax.fill_between([i - 0.36, i + 0.36], 4.5, agora, color=VERMELHO_BG, lw=0)
    xa, xb = i - 0.17, i + 0.17
    ax.plot([xa, xb], [antes, agora], color=VERMELHO, lw=1.4)
    ax.scatter([xa], [antes], s=45, color=CINZA, zorder=3)
    ax.scatter([xb], [agora], s=70, color=VERMELHO, zorder=4)
    ax.text(xb + 0.06, agora, f"{agora:.2f}%".replace(".", ","), fontsize=12,
            color=VERMELHO, weight="bold", va="center")
    ax.text(xa - 0.06, antes, f"{antes:.2f}%".replace(".", ","), fontsize=9,
            color=APAGADO, ha="right", va="center")
    gap = agora - 4.5
    ax.text(i, 4.5 + 0.17, "+" + f"{gap:.2f}".replace(".", ",") + " p.p. acima", ha="center",
            fontsize=8.5, color=VERMELHO, va="center")
    ax.text(i, 2.6, ano, ha="center", fontsize=12, color=TINTA, weight="bold")
ax.set_xticks([]); ax.set_yticks([])
src["focus"] = salvar(fig, "2026-11-24-4")
print(src)
