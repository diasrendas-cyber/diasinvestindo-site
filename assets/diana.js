/* Diana (/diana/): destino dos botões, abas de exemplos, lista de espera e eventos de medição. */
(function(){
"use strict";
var raiz=document.getElementById("diana");if(!raiz)return;

/* ---------- Medição: window.dataLayer (GTM/GA4) e gtag, se existir ---------- */
function ev(nome,p){p=p||{};window.dataLayer=window.dataLayer||[];
  var o={event:nome};for(var k in p)o[k]=p[k];window.dataLayer.push(o);
  if(typeof window.gtag==="function")window.gtag("event",nome,p);}
window.dianaEvento=ev;

/* ---------- Destino dos botões (configurado em tools/diana.py -> CONFIG) ---------- */
var cfg={};try{cfg=JSON.parse(raiz.getAttribute("data-config")||"{}")}catch(e){}
var destino=cfg.modo==="whatsapp"&&cfg.whatsapp?cfg.whatsapp:cfg.modo==="checkout"&&cfg.checkout?cfg.checkout:"";
raiz.querySelectorAll("a[data-cta]").forEach(function(a){
  if(destino){a.href=destino;a.target="_blank";a.rel="noopener"}
  a.addEventListener("click",function(){ev("diana_cta_clique",{secao:a.getAttribute("data-secao")||"",destino:cfg.modo||"lista"})});
});
if(destino){var ls=document.getElementById("lista");if(ls)ls.hidden=true;}

/* ---------- Abas de exemplos (teclado: setas, Home, End) ---------- */
var abas=[].slice.call(raiz.querySelectorAll('[role="tab"]'));
function ativar(t,foco){abas.forEach(function(b){var s=b===t;b.setAttribute("aria-selected",s?"true":"false");b.tabIndex=s?0:-1;
  document.getElementById(b.getAttribute("aria-controls")).hidden=!s});if(foco)t.focus();ev("diana_exemplo",{aba:t.id})}
abas.forEach(function(b,i){b.addEventListener("click",function(){ativar(b)});
  b.addEventListener("keydown",function(e){var j=null;if(e.key==="ArrowRight")j=(i+1)%abas.length;else if(e.key==="ArrowLeft")j=(i-1+abas.length)%abas.length;
    else if(e.key==="Home")j=0;else if(e.key==="End")j=abas.length-1;if(j!==null){e.preventDefault();ativar(abas[j],true)}})});

/* ---------- FAQ: abertura de cada pergunta ---------- */
raiz.querySelectorAll("details.dfaq").forEach(function(d){d.addEventListener("toggle",function(){if(d.open)ev("diana_faq_abrir",{pergunta:d.getAttribute("data-pergunta")})})});

/* ---------- Rolagem até Preços (uma vez) ---------- */
var planos=document.getElementById("planos");
if(planos&&"IntersectionObserver" in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){ev("diana_viu_precos",{});io.disconnect()}},{threshold:.35});io.observe(planos)}

/* ---------- Lista de espera (Supabase do projeto Diana; a chave pública só permite inserir) ---------- */
var API="https://lhpehgymzouwolxgdmwv.supabase.co/rest/v1/lista_espera";
var CHAVE="sb_publishable_hDWzPvPv_DQQ9vwnUU5BqQ_-HAmXhXN";
var live=/(^|\.)diasinvestindo\.com\.br$/.test(location.hostname);
var f=raiz.querySelector(".d-form");if(!f)return;
var msg=f.querySelector(".msg"),btn=f.querySelector("button[type=submit]");
var tel=f.querySelector('[name="whatsapp"]');
tel.addEventListener("input",function(){var d=tel.value.replace(/\D/g,"").slice(0,11);var o=d;
  if(d.length>2)o="("+d.slice(0,2)+") "+d.slice(2);if(d.length>7)o="("+d.slice(0,2)+") "+d.slice(2,d.length-4)+"-"+d.slice(-4);tel.value=o});
function origem(){var q=new URLSearchParams(location.search),o={pagina:location.pathname};
  ["utm_source","utm_medium","utm_campaign","utm_content","utm_term"].forEach(function(k){var v=q.get(k);if(v)o[k]=v.slice(0,100)});
  if(document.referrer){try{o.referencia=new URL(document.referrer).hostname}catch(e){}}return o}
function erro(campo,texto){msg.className="msg err";msg.textContent=texto;if(campo){campo.setAttribute("aria-invalid","true");campo.focus()}}
f.addEventListener("submit",function(e){e.preventDefault();
  f.querySelectorAll("[aria-invalid]").forEach(function(x){x.removeAttribute("aria-invalid")});
  var nome=f.nome.value.trim(),num=tel.value.replace(/\D/g,""),prof=f.profissao.value,usoEl=f.querySelector('[name="uso"]:checked'),ok=f.consentimento.checked;
  if(f.site.value)return;
  if(nome.length<2)return erro(f.nome,"Escreva o seu nome.");
  if(!/^[1-9][0-9]9?[0-9]{8}$/.test(num)||(num.length!==10&&num.length!==11))return erro(tel,"Confira o WhatsApp com DDD, por exemplo (61) 99999-9999.");
  if(!prof)return erro(f.profissao,"Escolha a sua profissão.");
  if(!usoEl)return erro(f.querySelector('[name="uso"]'),"Diga se vai usar para pessoal, empresa ou os dois.");
  if(!ok)return erro(f.consentimento,"Para entrar na lista, marque a concordância com a Política de Privacidade.");
  if(!live){msg.className="msg err";msg.textContent="Esta é a prévia: o cadastro funciona no site publicado em diasinvestindo.com.br.";return}
  btn.disabled=true;btn.textContent="Enviando…";msg.className="msg";msg.textContent="";
  fetch(API,{method:"POST",headers:{"Content-Type":"application/json",apikey:CHAVE,Authorization:"Bearer "+CHAVE,Prefer:"return=minimal"},
    body:JSON.stringify({nome:nome.slice(0,120),whatsapp:"55"+num,profissao:prof,uso:usoEl.value,consentimento:true,origem:origem()})})
  .then(function(r){if(!r.ok)throw new Error(r.status);
    f.classList.add("enviado");msg.className="msg ok";msg.textContent="Pronto! Você está na lista. A Diana vai te chamar no WhatsApp.";
    ev("diana_lista_envio",{profissao:prof,uso:usoEl.value})})
  .catch(function(){msg.className="msg err";msg.textContent="Não foi possível concluir agora. Tente de novo em instantes.";btn.disabled=false;btn.textContent="Entrar na lista do piloto"});
});
})();
