/* Dias Investindo: formulário de e-mail e espaços de anúncio, comuns a todas as páginas */
(function(){
"use strict";
const E=window.DIArte.E;
/* ---------- Captura de e-mail ---------- */
const API="https://nkdyvbvbwdqkwvlwfcnr.supabase.co/functions/v1/inscrever-site";
const live=/(^|\.)diasinvestindo\.com\.br$/.test(location.hostname);
let fc=0;
document.querySelectorAll(".capture-slot").forEach(slot=>{fc++;const id="cap"+fc;
  const d=document.createElement("div");d.className="capture";
  d.innerHTML=`<div><h3>Receba os próximos artigos por e-mail</h3><p>Notícias que mexem com o seu bolso, novos artigos e atualizações das calculadoras. Sem spam.</p></div>
  <form data-origem="${E(slot.dataset.origem||"site")}" novalidate>
    <label class="hp" for="${id}-site">Não preencha</label><input class="hp" id="${id}-site" name="site" tabindex="-1" autocomplete="off">
    <input id="${id}-nome" name="nome" placeholder="Seu nome" autocomplete="given-name" aria-label="Seu nome">
    <input id="${id}-email" name="email" type="email" placeholder="Seu melhor e-mail" autocomplete="email" required aria-label="Seu e-mail">
    <button class="btn" type="submit">Quero receber</button>
    <p class="msg" role="status"></p>
    <small>Você pode sair quando quiser. Veja a <button type="button" class="link-priv" style="background:none;border:0;padding:0;color:inherit;text-decoration:underline;cursor:pointer;font:inherit">Política de Privacidade</button>.</small>
  </form>`;slot.replaceWith(d)});
document.querySelectorAll(".link-priv").forEach(b=>b.addEventListener("click",()=>{if(typeof window.DIPrivacidade==="function")window.DIPrivacidade();else location.href="/privacidade/"}));
document.querySelectorAll(".capture form").forEach(f=>f.addEventListener("submit",async ev=>{
  ev.preventDefault();const msg=f.querySelector(".msg"),btn=f.querySelector("button[type=submit]");
  const q=n=>f.querySelector(`[name="${n}"]`);const email=q("email").value.trim(),nome=q("nome").value.trim();msg.className="msg";
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)){msg.classList.add("err");msg.textContent="Confira o e-mail digitado.";q("email").focus();return}
  if(!live){msg.classList.add("err");msg.textContent="Esta é a prévia: o cadastro funciona no site publicado em diasinvestindo.com.br.";return}
  btn.disabled=true;btn.textContent="Enviando…";
  try{const r=await fetch(API,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,nome,site:q("site").value,origem:f.dataset.origem})});
    const j=await r.json().catch(()=>({}));
    if(r.ok&&j.ok){msg.classList.add("ok");msg.textContent=j.jaInscrito?"Você já estava na lista. Obrigado!":"Pronto! Confira a sua caixa de entrada.";f.reset()}
    else{msg.classList.add("err");msg.textContent=j.erro||"Não foi possível concluir agora. Tente de novo em instantes."}
  }catch(e){msg.classList.add("err");msg.textContent="Sem conexão com o servidor. Tente de novo em instantes."}
  btn.disabled=false;btn.textContent="Quero receber";
}));

/* ---------- AdSense: preencha após a aprovação ---------- */
/* O script do AdSense já está no <head>. Para usar os espaços fixos, crie os blocos no AdSense e preencha os IDs abaixo. */
const ADSENSE={client:"ca-pub-2224422141615380",slots:{faixa:"",lateral:""}};
if(live&&Object.values(ADSENSE.slots).some(Boolean)){
  document.querySelectorAll("[data-ad-slot-name]").forEach(el=>{const id=ADSENSE.slots[el.dataset.adSlotName];if(!id)return;
    el.innerHTML=`<ins class="adsbygoogle ad-unit" data-ad-client="${ADSENSE.client}" data-ad-slot="${id}" data-ad-format="auto" data-full-width-responsive="true"></ins>`;
    el.style.backgroundImage="none";try{(window.adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}});
}

/* ---------- Bitcoin ao vivo na régua (CoinGecko). Sem resposta, o campo fica oculto: nunca mostra preço velho ---------- */
const BTC_URL="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true";
async function bitcoin(){
  const alvos=document.querySelectorAll("[data-btc]");if(!alvos.length||typeof fetch!=="function")return;
  try{const r=await fetch(BTC_URL);if(!r.ok)throw new Error(r.status);const b=((await r.json())||{}).bitcoin||{};
    const p=Number(b.usd),v=Number(b.usd_24h_change),t=Number(b.last_updated_at);if(!(p>0))throw new Error("sem preço");
    const hora=t?new Date(t*1000).toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit",timeZone:"America/Sao_Paulo"}):"";
    const var24=isFinite(v)?(v>=0?"+":"−")+Math.abs(v).toLocaleString("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2})+"%":"";
    alvos.forEach(el=>{el.innerHTML=`<span class="lbl">Bitcoin</span> US$ ${Math.round(p).toLocaleString("pt-BR")}${var24?` <span class="${v<0?"down":"up"}">${var24}</span>`:""} <span class="when">24h${hora?", "+hora:""}</span>`;
      el.title="Preço do Bitcoin em dólar e variação em 24 horas. Fonte: CoinGecko"+(hora?", atualizado às "+hora+" (Brasília)":"");el.hidden=false});
  }catch(e){alvos.forEach(el=>el.hidden=true)}
}
bitcoin();setInterval(()=>{if(!document.hidden)bitcoin()},5*60*1000);

window.DILive=live;
})();
