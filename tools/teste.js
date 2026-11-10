(async () => {
// Testes funcionais do site Dias Investindo (jsdom)
const fs = require("fs");
const { JSDOM, VirtualConsole } = require("jsdom");
const path = require("path");
const { execFileSync } = require("child_process");
const RAIZ = path.join(__dirname, "..");
const autocontido = rel => { const out = path.join(require("os").tmpdir(), "di-" + rel.replace(/[\/]/g, "_"));
  execFileSync("python3", [path.join(RAIZ, "tools/preview.py"), path.join(RAIZ, rel), out, "--completo"]); return fs.readFileSync(out, "utf8"); };
const html = autocontido("index.html");
let falhas = 0, ok = 0;
const check = (cond, nome, extra = "") => { if (cond) { ok++; } else { falhas++; console.log("FALHOU:", nome, extra); } };
const erros = [];
const vc = new VirtualConsole();
vc.on("error", e => erros.push(String(e))); vc.on("jsdomError", e => { if (!/Could not load|Not implemented: (window.scrollTo|navigation)/.test(e.message)) erros.push(e.message); });

function carregar(url = "https://claude.ai/previa", fonte = html) {
  return new JSDOM(fonte, { runScripts: "dangerously", pretendToBeVisual: true, url, virtualConsole: vc });
}
const dom = carregar();
const w = dom.window, d = w.document, $ = id => d.getElementById(id);
const fire = (el, tipo) => el.dispatchEvent(new w.Event(tipo, { bubbles: true }));
const formDe = id => $(id).closest("form");
/* digita e confirma no botão Calcular/Simular (os resultados só mudam ao confirmar) */
const setv = (id, v) => { $(id).value = v; fire($(id), "input"); const f = formDe(id); if (f) f.dispatchEvent(new w.Event("submit", { cancelable: true })); };

// Estrutura de página única
const links = [...d.querySelectorAll("nav.tabs a")].map(a => a.getAttribute("href"));
check(links.length === 8, "8 abas no menu", links.join(","));
links.forEach(h => check(!!d.getElementById(h.slice(1)), "seção existe " + h));
check(d.querySelectorAll("section[hidden]").length === 0, "nenhuma seção escondida (página única)");
["#contato", "#calc-milhao", "#calc-aposentadoria", "#conversor", "#calculadoras"].forEach(h => check(!!d.querySelector(h), "âncora " + h));
check(links.includes("#ferramentas") && !links.includes("#calculadoras"), "aba Ferramentas no lugar de Calculadoras");
check(d.querySelector(".logo small").textContent.trim()==="em você" && /Viva os dias investindo em você/.test(d.title), "slogan no cabeçalho e no título");
check(!d.querySelector("#inicio .author") && d.querySelector("#sobre .creds"), "apresentação do autor só no Sobre");
check([...d.querySelectorAll("#conteudo > section")].pop().id === "sobre", "Sobre é a última seção da página");
const intro = d.querySelector(".intro"), ordem = [...intro.children].map(e => e.tagName + (e.id ? "#" + e.id : ""));
check(ordem.join(",") === "H1,FORM#busca,P", "busca entre o título e o texto de apresentação", ordem.join(","));
check(/ca-pub-2224422141615380/.test(fs.readFileSync(path.join(RAIZ, "index.html"), "utf8").split("</head>")[0]), "script AdSense no head");
check(d.querySelector(".rail") && d.querySelector(".sponsor-slot"), "espaços de patrocínio");

// Régua
const DADOS = JSON.parse(d.getElementById("site-data").textContent);
const tk = $("ticker").textContent;
check(/Selic/.test(tk) && tk.includes(DADOS.ticker.ibov) && tk.includes(DADOS.ticker.dolar), "régua com dados", tk);
check($("ticker").querySelectorAll(".up,.down").length >= 1, "cores da régua por sinal");

// Notícias
check(d.querySelectorAll("#destaques [data-open-noticia]").length === 4, "4 destaques");
const maisEsperado = Math.max(0, Math.min(4, Math.min(10, DADOS.noticias.length) - 4));
check(d.querySelectorAll("#mais-noticias [data-open-noticia]").length === maisEsperado, "bloco Mais notícias com 4", d.querySelectorAll("#mais-noticias [data-open-noticia]").length);
check([...d.querySelectorAll("#mais-noticias [data-open-noticia]")].every((a, k) => a.dataset.openNoticia === String(k + 4)), "Mais notícias continua depois dos destaques");
check(d.querySelector("#mais-noticias").compareDocumentPosition(d.querySelector("#destaques")) & 2, "Mais notícias logo abaixo dos destaques");
// régua: espaço do Bitcoin existe e fica oculto sem cotação (nunca mostra preço velho)
check(d.querySelector("#ticker [data-btc]") && d.querySelector("#ticker [data-btc]").hidden, "Bitcoin oculto sem cotação ao vivo");
check(d.querySelectorAll("#news-list [data-open-noticia]").length === Math.min(10, JSON.parse(d.getElementById("site-data").textContent).noticias.length), "notícias na seção (até 10)");
d.querySelectorAll("#news-list .art svg").forEach((s, i) => check(s.querySelectorAll("path,rect,text,circle,line,polyline").length > 5, "arte desenhada na notícia " + i));
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
const ARTS = fs.readdirSync(path.join(RAIZ, "conteudo/artigos")).filter(f => f.endsWith(".md")).map(f => f.slice(0, -3));
check(d.querySelectorAll("#inicio [data-open-artigo]").length === Math.min(2, ARTS.length), "vitrine de artigos na home");
// A home mostra os mais recentes (vitrines e VideoBlog com até 12); os demais ficam em /artigos/ e nas páginas de categoria
const TODOS_ARTS = fs.readFileSync(path.join(RAIZ, "artigos/index.html"), "utf8");
check(!!d.querySelector('#videoblog a[href="/artigos/"]'), "VideoBlog tem link para todos os artigos");
ARTS.forEach(a => {
  check(TODOS_ARTS.includes(`/artigos/${a}/`), "artigo listado em /artigos/ " + a);
  const b = d.querySelector(`[data-open-artigo="${a}"]`);
  if (ARTS.length <= 12) check(!!b, "artigo listado na home ou no VideoBlog " + a);
  if (!b) return;
  b.click();
  check(dlg.hasAttribute("open") && $("leitor-corpo").querySelector("h1"), "artigo abre " + a);
  check($("leitor-corpo").querySelector(".art svg"), "arte no artigo " + a);
  $("leitor-fechar").click();
});
// Link interno do artigo fecha o leitor
{ const comLink = [...d.querySelectorAll("a.story[data-open-artigo]")].find(a => { const t = $("artigo-" + a.dataset.openArtigo); return t && t.innerHTML.includes("data-fecha-leitor"); });
  if (comLink) { comLink.click(); $("leitor-corpo").querySelector("[data-fecha-leitor]").click(); check(!dlg.hasAttribute("open"), "link para calculadora fecha o leitor"); } }
// Privacidade
$("abrir-privacidade").click();
check(dlg.hasAttribute("open") && /LGPD/.test($("leitor-corpo").textContent), "política abre");
$("leitor-fechar").click();
check(d.querySelectorAll(".capture form").length === 3, "3 formulários de captura", d.querySelectorAll(".capture form").length);
d.querySelector(".link-priv").click();
check(dlg.hasAttribute("open"), "link da política no formulário"); $("leitor-fechar").click();

// Busca (na prévia usa as notícias e artigos da página; no site, o índice completo /busca.json)
const semAc = t => t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
const palavra = t => semAc(t).split(/[^a-z0-9]+/).filter(x => x.length >= 5).sort((a, b) => b.length - a.length)[0];
const bq = $("busca-q"), espera = () => new Promise(r => setTimeout(r, 30));
bq.dispatchEvent(new w.Event("focus"));
const pN = palavra(DADOS.noticias[0].titulo);
bq.value = pN; fire(bq, "input"); await espera();
const resB = [...d.querySelectorAll("#busca-res li[role=option]")];
check(resB.length >= 1 && semAc(resB[0].textContent).includes(pN), "busca encontra notícias (título primeiro)", pN + " " + resB.length);
const art1 = d.querySelector("a.story[data-open-artigo] h3");
if (art1) { const pA = palavra(art1.textContent); bq.value = pA.toUpperCase(); fire(bq, "input"); await espera();
  check([...d.querySelectorAll("#busca-res li[role=option] a")].some(a => a.dataset.openArtigo), "busca encontra artigos (sem diferenciar maiúsculas)", pA); }
const comAcento = DADOS.noticias.map(n => n.titulo.split(/\s+/).find(x => /[áéíóúâêôãõç]/i.test(x) && x.length >= 5)).find(Boolean);
if (comAcento) { bq.value = semAc(comAcento).replace(/[^a-z0-9]/g, ""); fire(bq, "input"); await espera();
  check(d.querySelector("#busca-res li[role=option]"), "busca ignora acentos", comAcento); }
bq.value = "xyzxyz"; fire(bq, "input"); await espera();
check(/Nada encontrado/.test($("busca-res").textContent), "busca sem resultado avisa");
bq.value = pN; $("busca").dispatchEvent(new w.Event("submit", { cancelable: true })); await espera();
check(dlg.hasAttribute("open"), "Enter na busca abre o primeiro resultado"); $("leitor-fechar").click();
{ const idx = JSON.parse(fs.readFileSync(path.join(RAIZ, "busca.json"), "utf8")), todasN = JSON.parse(fs.readFileSync(path.join(RAIZ, "noticias.json"), "utf8")).noticias;
  const arts = fs.readdirSync(path.join(RAIZ, "conteudo/artigos")).filter(f => f.endsWith(".md")).map(f => f.slice(0, -3));
  check(todasN.every(n => idx.some(x => x.u === `/noticias/${n.slug}/`)) && arts.every(a => idx.some(x => x.u === `/artigos/${a}/`)), "índice da busca com todas as notícias e artigos"); }

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
$("m-ap").value = "abc"; fire($("m-ap"), "input"); check($("m-ap").value === "", "máscara recusa letras");
// Máscara de milhar automática
[["m-ini", "1234567", "1.234.567"], ["m-ini", "1234567,891", "1.234.567,89"], ["m-tx", "6,555", "6,55"], ["a-idade", "4a5", "45"], ["m-meta", "0001000", "1.000"]].forEach(([id, dig, esp]) => {
  $(id).value = dig; fire($(id), "input"); check($(id).value === esp, `máscara ${id}: ${dig} → ${esp}`, $(id).value); });
$("a-idade").value = "40"; $("m-tx").value = "6"; $("m-ini").value = "10.000";
// Resultado só muda ao clicar em Calcular
$("m-ini").value = "10.000"; $("m-meta").value = "2.000.000"; fire($("m-meta"), "input");
const antesClique = txt("m-tempo");
check(formDe("m-meta").classList.contains("pendente") && /Calcular/.test(formDe("m-meta").querySelector(".aviso").textContent), "avisa que precisa calcular");
formDe("m-meta").querySelector("button[type=submit]").click();
check(txt("m-tempo") !== antesClique && !formDe("m-meta").classList.contains("pendente"), "botão Calcular atualiza", antesClique + " → " + txt("m-tempo"));
check(formDe("a-ap").querySelector("button[type=submit]").textContent === "Simular", "simulador tem botão Simular");
check(formDe("mini-ap").querySelector("button[type=submit]").textContent === "Calcular", "mini calculadora tem botão Calcular");
setv("m-meta", "1.000.000");
setv("m-ap", "1.500"); setv("m-tx", "6");

// Aposentadoria (padrão: 40→60, 100k, 2k/mês, 10k renda, 0 outras, 5%, 4%)
const brlN = s => Number(s.replace(/[^\d,-]/g, "").replace(",", "."));
check(brlN(txt("a-nec")) === 3000000, "necessário = 10k×12÷4%", txt("a-nec"));
const i5 = Math.pow(1.05, 1 / 12) - 1, n = 240, g = Math.pow(1 + i5, n), fvf = (g - 1) / i5;
const proj = 100000 * g + 2000 * fvf, need = (3000000 - 100000 * g) / fvf;
check(Math.abs(brlN(txt("a-proj")) - proj) < 2, "projetado confere", txt("a-proj") + " vs " + Math.round(proj));
check(Math.abs(brlN(txt("a-need")) - need) < 2, "aporte necessário confere", txt("a-need") + " vs " + Math.round(need));
check(/Falta/.test(txt("a-gap-lbl")) && $("a-gap-box").classList.contains("warn"), "diferença negativa em vermelho");
{ let sm = 100000, mm = 0; while (sm < 3000000) { sm = sm * (1 + i5) + 2000; mm++; }
  const esperado = `em ${Math.floor(mm / 12)} anos e ${mm % 12} meses, aos ${40 + Math.floor(mm / 12)} anos de idade`;
  check(txt("a-exp").includes(esperado), "idade em que atinge a meta (sem arredondar para cima)", txt("a-exp") + " | esperado: " + esperado); }
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

// Conversor: sem acesso ao Banco Central (prévia), usa só o dólar comercial verificado da régua
await new Promise(r => setTimeout(r, 50));
const dolarRegua = parseFloat(DADOS.ticker.dolar.replace(/[^\d,]/g, "").replace(",", "."));
$("cv-de").value = "USD"; $("cv-para").value = "BRL"; setv("cv-valor", "1.000"); await new Promise(r => setTimeout(r, 50));
check(Math.abs(brlN(txt("cv-out")) - 1000 * dolarRegua) < 0.02, "conversor USD→BRL pela cotação da régua", txt("cv-out"));
check(/régua/.test(txt("cv-exp")), "conversor informa a cotação usada");
$("cv-trocar").click(); await new Promise(r => setTimeout(r, 50));
check($("cv-de").value === "BRL" && Math.abs(brlN(txt("cv-out").replace("US$", "")) - 1000 / dolarRegua) < 0.02, "inverter moedas", txt("cv-out"));
$("cv-para").value = "EUR"; formDe("cv-para").dispatchEvent(new w.Event("submit", { cancelable: true })); await new Promise(r => setTimeout(r, 50));
check(/Indisponível/.test(txt("cv-out")), "sem cotação oficial não inventa valor");
// Conversor com a PTAX do Banco Central (resposta simulada no formato oficial)
const pt = w.__calc.PTAX; pt.EUR = { v: 6.4, d: "2026-11-09 13:07:00.000", f: "ptax" }; pt.USD = { v: 5.5, d: "2026-11-09 13:07:00.000", f: "ptax" };
$("cv-de").value = "EUR"; $("cv-para").value = "USD"; setv("cv-valor", "100"); await new Promise(r => setTimeout(r, 50));
check(Math.abs(brlN(txt("cv-out").replace("US$", "")) - 100 * 6.4 / 5.5) < 0.01 && /PTAX/.test(txt("cv-exp")) && /09\/11\/2026/.test(txt("cv-exp")), "conversão cruzada pela PTAX", txt("cv-out") + " | " + txt("cv-exp"));

// ---------- Site publicado: notícias são links para páginas próprias ----------
const live = carregar("https://diasinvestindo.com.br/");
const ld = live.window.document;
const cards = [...ld.querySelectorAll("#news-list a[data-open-noticia]")];
check(cards.length === Math.min(10, DADOS.noticias.length), "notícias da home como links");
cards.forEach((a, i) => check(a.getAttribute("href") === `/noticias/${DADOS.noticias[i].slug}/`, "link da notícia " + (i + 1), a.getAttribute("href")));
cards[0].click();
check(!ld.getElementById("leitor").hasAttribute("open"), "no site publicado o link abre a página, não o leitor");
check(!ld.querySelector('a[href="/noticias/"]').hidden, "link para o arquivo visível no site");
check(d.querySelector('a[href="/noticias/"]').hidden, "link para o arquivo escondido na prévia");

// ---------- Páginas de notícia geradas ----------
const todas = JSON.parse(fs.readFileSync(path.join(RAIZ, "noticias.json"), "utf8")).noticias;
todas.forEach((n, i) => {
  const rel = `noticias/${n.slug}/index.html`;
  check(fs.existsSync(path.join(RAIZ, rel)), "página gerada " + n.slug);
  const pg = carregar(`https://diasinvestindo.com.br/noticias/${n.slug}/`, autocontido(rel)).window.document;
  check(pg.querySelector("h1").textContent === n.titulo, "título da página " + (i + 1));
  check(pg.querySelectorAll(".corpo > p:not(.callout)").length === 3, "3 parágrafos na página " + (i + 1));
  check(pg.querySelector(".art svg") && pg.querySelector(".art svg").textContent.includes(n.arte.titulo || n.arte.valor || ""), "ilustração na página " + (i + 1));
  check(pg.querySelector(".capture form"), "formulário na página " + (i + 1));
  check(pg.querySelector(".ticker .wrap").textContent.includes("Selic"), "régua na página " + (i + 1));
  check(pg.querySelector('script[type="application/ld+json"]'), "dados estruturados na página " + (i + 1));
  check(pg.querySelector('link[rel="canonical"]').getAttribute("href").endsWith(`/noticias/${n.slug}/`), "canonical na página " + (i + 1));
});
const sm = fs.readFileSync(path.join(RAIZ, "sitemap.xml"), "utf8");
// ---------- Artigos: páginas, categorias e links no site publicado ----------
ld.querySelectorAll("[data-open-artigo]").forEach(a => check(a.tagName === "A" && a.getAttribute("href") === `/artigos/${a.dataset.openArtigo}/`, "link do artigo " + a.dataset.openArtigo));
ld.querySelector("[data-open-artigo]").click();
check(!ld.getElementById("leitor").hasAttribute("open"), "no site o artigo abre a página própria");
check(d.querySelectorAll(".so-site").length > 0 && [...d.querySelectorAll(".so-site")].every(x => x.hidden), "links de categoria escondidos na prévia");
ARTS.forEach(slug => {
  const rel = `artigos/${slug}/index.html`;
  check(fs.existsSync(path.join(RAIZ, rel)), "página do artigo " + slug);
  const pg = carregar(`https://diasinvestindo.com.br/artigos/${slug}/`, autocontido(rel)).window.document;
  check(pg.querySelector("h1") && pg.querySelector(".corpo h2"), "corpo do artigo " + slug);
  check(pg.querySelector(".art svg"), "ilustração do artigo " + slug);
  check(pg.querySelectorAll("section .three .story").length >= 1, "leia também " + slug);
  check(pg.querySelector('link[rel="canonical"]').getAttribute("href").endsWith(`/artigos/${slug}/`), "canonical do artigo " + slug);
});
["financas-pessoais", "investimentos", "produtividade", "artigos"].forEach(c => {
  const rel = `${c}/index.html`;
  check(fs.existsSync(path.join(RAIZ, rel)), "página " + c);
  const pg = carregar(`https://diasinvestindo.com.br/${c}/`, autocontido(rel)).window.document;
  check(pg.querySelector("h2") && pg.querySelector(".capture form"), "conteúdo da página " + c);
});
check(ARTS.every(a => sm.includes(`/artigos/${a}/`)), "sitemap com todos os artigos");

// Arquivo com filtro por editoria
const arq = carregar("https://diasinvestindo.com.br/noticias/", autocontido("noticias/index.html")).window.document;
check(arq.querySelectorAll(".lista li").length === todas.length, "arquivo lista todas as notícias");
const bt = [...arq.querySelectorAll(".filtros button")].find(b => b.dataset.ed);
bt.click();
check([...arq.querySelectorAll(".lista li")].every(li => li.hidden === (li.dataset.ed !== bt.dataset.ed)), "filtro por editoria");
// Arquivos de apoio
["sitemap.xml", "robots.txt", "feed.xml", "ads.txt", "404.html", "privacidade/index.html"].forEach(f => check(fs.existsSync(path.join(RAIZ, f)), "arquivo " + f));
check(todas.every(n => sm.includes(`/noticias/${n.slug}/`)), "sitemap com todas as notícias");

// Prévia fora do domínio: formulário avisa
const dom2 = carregar("https://claude.ai/x");
const f2 = dom2.window.document.querySelector(".capture form");
f2.querySelector("[name=email]").value = "a@b.com"; f2.dispatchEvent(new dom2.window.Event("submit", { cancelable: true }));
check(/prévia/.test(f2.querySelector(".msg").textContent), "prévia avisa no formulário");

check(erros.length === 0, "sem erros de JavaScript", erros.join(" | "));
console.log(`\n${ok} verificações OK, ${falhas} falhas`);
process.exit(falhas ? 1 : 0);
})();
