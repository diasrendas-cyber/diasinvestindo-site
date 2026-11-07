// Testes funcionais do site Dias Investindo (jsdom)
const fs = require("fs");
const { JSDOM, VirtualConsole } = require("jsdom");
const html = fs.readFileSync(process.argv[2], "utf8");
let falhas = 0, ok = 0;
const check = (cond, nome, extra = "") => { if (cond) { ok++; } else { falhas++; console.log("FALHOU:", nome, extra); } };
const erros = [];
const vc = new VirtualConsole();
vc.on("error", e => erros.push(String(e))); vc.on("jsdomError", e => { if (!/Could not load|Not implemented: window.scrollTo/.test(e.message)) erros.push(e.message); });

function carregar(url = "https://diasinvestindo.com.br/") {
  const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true, url, virtualConsole: vc });
  return dom;
}
const dom = carregar();
const w = dom.window, d = w.document, $ = id => d.getElementById(id);
const fire = (el, tipo) => el.dispatchEvent(new w.Event(tipo, { bubbles: true }));
const setv = (id, v) => { $(id).value = v; fire($(id), "input"); };

// Estrutura de página única
const links = [...d.querySelectorAll("nav.tabs a")].map(a => a.getAttribute("href"));
check(links.length === 8, "8 abas no menu", links.join(","));
links.forEach(h => check(!!d.getElementById(h.slice(1)), "seção existe " + h));
check(d.querySelectorAll("section[hidden]").length === 0, "nenhuma seção escondida (página única)");
["#contato", "#calc-milhao", "#calc-aposentadoria"].forEach(h => check(!!d.querySelector(h), "âncora " + h));
check(!!d.querySelector('script[src*="ca-pub-2224422141615380"]'), "script AdSense no head");
check(d.querySelector(".rail") && d.querySelector(".sponsor-slot"), "espaços de patrocínio");

// Régua
const DADOS = JSON.parse(d.getElementById("site-data").textContent);
const tk = $("ticker").textContent;
check(/Selic/.test(tk) && tk.includes(DADOS.ticker.ibov) && tk.includes(DADOS.ticker.dolar), "régua com dados", tk);
check($("ticker").querySelectorAll(".up,.down").length >= 1, "cores da régua por sinal");

// Notícias
check(d.querySelectorAll("#destaques [data-open-noticia]").length === 3, "3 destaques");
check(d.querySelectorAll("#news-list [data-open-noticia]").length === 3, "3 notícias na seção");
d.querySelectorAll("#news-list .art svg").forEach((s, i) => check(s.querySelectorAll("path,rect,text").length > 10, "arte rica notícia " + i));
DADOS.noticias.forEach((n, i) => {
  const svg = d.querySelectorAll("#news-list .art svg")[i].textContent;
  const esperado = n.arte.titulo || n.arte.valor || n.arte.rotulo || "";
  check(!esperado || svg.includes(esperado), "arte contextual da notícia " + (i + 1), esperado);
});

// Leitor de notícia
d.querySelectorAll("#news-list [data-open-noticia]")[1].click();
const dlg = $("leitor");
check(dlg.hasAttribute("open"), "notícia abre o leitor");
check($("leitor-corpo").querySelectorAll("article > p:not(.dek):not(.src):not(.callout)").length === 3, "notícia com 3 parágrafos", $("leitor-corpo").querySelectorAll("p").length);
check($("leitor-corpo").textContent.includes(DADOS.noticias[1].fontes[0].nome), "fonte na notícia");
$("leitor-fechar").click();
check(!dlg.hasAttribute("open"), "leitor fecha");
// Destaque grande também abre
d.querySelector("#destaques [data-open-noticia]").click();
check(dlg.hasAttribute("open") && $("leitor-corpo").textContent.includes(DADOS.noticias[0].titulo), "destaque abre a notícia certa");
w.document.dispatchEvent(new w.KeyboardEvent("keydown", { key: "Escape" }));
check(!dlg.hasAttribute("open"), "Esc fecha");

// Artigos
["juros", "financas", "aposentadoria"].forEach(a => {
  const b = d.querySelector(`[data-open-artigo="${a}"]`); b.click();
  check(dlg.hasAttribute("open") && $("leitor-corpo").querySelector("h1"), "artigo abre " + a);
  check($("leitor-corpo").querySelector(".art svg"), "arte no artigo " + a);
  $("leitor-fechar").click();
});
// Link interno do artigo fecha o leitor
d.querySelector('[data-open-artigo="juros"]').click();
$("leitor-corpo").querySelector("[data-fecha-leitor]").click();
check(!dlg.hasAttribute("open"), "link para calculadora fecha o leitor");
// Privacidade
$("abrir-privacidade").click();
check(dlg.hasAttribute("open") && /LGPD/.test($("leitor-corpo").textContent), "política abre");
$("leitor-fechar").click();
check(d.querySelectorAll(".capture form").length === 3, "3 formulários de captura", d.querySelectorAll(".capture form").length);
d.querySelector(".link-priv").click();
check(dlg.hasAttribute("open"), "link da política no formulário"); $("leitor-fechar").click();

// Formulário: validação local
const f = d.querySelector(".capture form");
f.querySelector("[name=email]").value = "invalido"; f.dispatchEvent(new w.Event("submit", { cancelable: true }));
check(/Confira o e-mail/.test(f.querySelector(".msg").textContent), "valida e-mail");

// ---------- Calculadoras ----------
const txt = id => $(id).textContent;
const fechadoMeses = (ini, ap, tx, meta) => { // fórmula fechada independente
  const i = Math.pow(1 + tx / 100, 1 / 12) - 1;
  if (ini >= meta) return 0;
  if (i === 0) return ap > 0 ? Math.ceil((meta - ini) / ap) : null;
  return Math.ceil(Math.log((meta * i + ap) / (ini * i + ap)) / Math.log(1 + i));
};
const casos = [[10000, 1500, 6, 1e6], [0, 1000, 6, 1e6], [500000, 0, 8, 1e6], [0, 2000, 0, 240000], [50000, 3000, 4.5, 2e6]];
casos.forEach(([ini, ap, tx, meta]) => {
  const r = w.__calc.simMilhao(ini, ap, tx, meta), m = fechadoMeses(ini, ap, tx, meta);
  check(Math.abs(r.m - m) <= 1, `milhão meses ${ini}/${ap}/${tx}`, `${r.m} vs ${m}`);
});
check(w.__calc.simMilhao(1e6, 0, 5, 1e6).m === 0, "meta já atingida");
check(w.__calc.simMilhao(0, 0, 0, 1e6).m === null, "sem aporte e sem taxa nunca chega");
// Valor do texto padrão: 10k, 1.5k, 6%, 1M
check(/anos/.test(txt("m-tempo")), "milhão padrão mostra tempo", txt("m-tempo"));
const mesesPadrao = fechadoMeses(10000, 1500, 6, 1e6);
check(txt("m-tempo") === `${Math.floor(mesesPadrao / 12)} anos` + (mesesPadrao % 12 ? ` e ${mesesPadrao % 12} ${mesesPadrao % 12 === 1 ? "mês" : "meses"}` : ""), "texto do tempo", txt("m-tempo") + " / " + mesesPadrao);
check(txt("m-tempo") === txt("mini-out"), "mini e completa iguais");
// Entrada no formato brasileiro com centavos
setv("m-ap", "R$ 1.500,00"); check(txt("m-tempo") === txt("mini-out"), "aceita R$ 1.500,00");
setv("m-ap", "1500"); check(txt("m-tempo") === txt("mini-out"), "aceita 1500");
setv("m-tx", "6,0"); check(txt("m-tempo") === txt("mini-out"), "aceita 6,0");
setv("m-meta", "0"); check(/Informe a meta/.test(txt("m-tempo")), "meta zero");
setv("m-meta", "1.000.000"); setv("m-ap", "0"); setv("m-tx", "0");
check(/Mais de 100/.test(txt("m-tempo")) && /não cresce/.test(txt("m-exp")), "sem aporte nem taxa explica");
setv("m-ap", "abc"); check($("m-ap").getAttribute("aria-invalid") === "true", "entrada inválida marcada");
setv("m-ap", "1.500"); setv("m-tx", "6");

// Aposentadoria (padrão: 40→60, 100k, 2k/mês, 10k renda, 0 outras, 5%, 4%)
const brlN = s => Number(s.replace(/[^\d,-]/g, "").replace(",", "."));
check(brlN(txt("a-nec")) === 3000000, "necessário = 10k×12÷4%", txt("a-nec"));
const i5 = Math.pow(1.05, 1 / 12) - 1, n = 240, g = Math.pow(1 + i5, n), fvf = (g - 1) / i5;
const proj = 100000 * g + 2000 * fvf, need = (3000000 - 100000 * g) / fvf;
check(Math.abs(brlN(txt("a-proj")) - proj) < 2, "projetado confere", txt("a-proj") + " vs " + Math.round(proj));
check(Math.abs(brlN(txt("a-need")) - need) < 2, "aporte necessário confere", txt("a-need") + " vs " + Math.round(need));
check(/Falta/.test(txt("a-gap-lbl")) && $("a-gap-box").classList.contains("warn"), "diferença negativa em vermelho");
check(/aos \d+ anos/.test(txt("a-exp")), "explica idade de atingir", txt("a-exp"));
setv("a-outras", "4.000");
check(brlN(txt("a-nec")) === 1800000, "outras rendas reduzem (6k×12÷4%)", txt("a-nec"));
setv("a-outras", "12.000"); check(/já cobre/.test(txt("a-exp")), "outras rendas cobrem tudo");
setv("a-outras", "0"); setv("a-ret", "0"); check(/Informe/.test(txt("a-nec")), "retirada zero tratada");
setv("a-ret", "4"); setv("a-apos", "40"); check(/maior que a idade atual/.test(txt("a-exp")), "idade inválida tratada");
setv("a-apos", "60"); setv("a-ap", "50.000"); check(/Sobra/.test(txt("a-gap-lbl")) && /folga/.test(txt("a-exp")), "cenário com folga");
setv("a-ap", "2.000"); setv("a-tx", "0");
check(Math.abs(brlN(txt("a-proj")) - (100000 + 2000 * 240)) < 2, "taxa zero soma simples", txt("a-proj"));
setv("a-tx", "5");
check($("a-chart").querySelectorAll("path").length >= 4, "gráfico da aposentadoria desenhado");
check($("m-chart").querySelectorAll("path").length >= 4, "gráfico do milhão desenhado");

// Prévia fora do domínio: formulário avisa
const dom2 = carregar("https://claude.ai/x");
const f2 = dom2.window.document.querySelector(".capture form");
f2.querySelector("[name=email]").value = "a@b.com"; f2.dispatchEvent(new dom2.window.Event("submit", { cancelable: true }));
check(/prévia/.test(f2.querySelector(".msg").textContent), "prévia avisa no formulário");

check(erros.length === 0, "sem erros de JavaScript", erros.join(" | "));
console.log(`\n${ok} verificações OK, ${falhas} falhas`);
process.exit(falhas ? 1 : 0);
