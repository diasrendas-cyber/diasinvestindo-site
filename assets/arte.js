/* Dias Investindo: motor das ilustrações (gráficos SVG desenhados a partir dos dados de cada notícia) */
(function(){
"use strict";
const E=t=>String(t==null?"":t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const FONT_D="Schibsted Grotesk,Helvetica Neue,Arial,sans-serif", FONT_M="IBM Plex Mono,Menlo,monospace";
const brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL",maximumFractionDigits:0});
const compact=v=>{const a=Math.abs(v);if(a>=1e6)return "R$ "+(v/1e6).toLocaleString("pt-BR",{maximumFractionDigits:2})+" mi";if(a>=1e3)return "R$ "+Math.round(v/1e3).toLocaleString("pt-BR")+" mil";return brl.format(v)};
const sinal=s=>{const t=String(s||"").trim().replace("−","-");if(t.startsWith("-"))return "down";if(t.startsWith("+")&&/[1-9]/.test(t))return "up";return ""};
const fmtVar=s=>String(s||"").replace(/^-/,"−");
const W=640,H=360;
const txt=(x,y,s,o={})=>`<text x="${x}" y="${y}" font-family="${o.f||FONT_D}" font-size="${o.size||14}" font-weight="${o.w||500}" fill="${o.fill||"var(--muted)"}" text-anchor="${o.anchor||"start"}">${E(s)}</text>`;
const grid=()=>{let g=`<defs><pattern id="pg" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="var(--line)" stroke-width="0.6"/></pattern></defs><rect width="${W}" height="${H}" fill="var(--surface)"/><rect width="${W}" height="${H}" fill="url(#pg)" opacity=".55"/>`;return g};
const num=v=>Number(String(v).replace(",","."));
const nice=v=>v.toLocaleString("pt-BR",{maximumFractionDigits:2});
const passo=r=>{const b=Math.pow(10,Math.floor(Math.log10(r)));for(const m of [1,2,2.5,5,10])if(m*b>=r)return m*b;return 10*b};
const icone=(t,x=W-104,y=18)=>(CENAS[t]||CENAS.bolsa)(0,0,1).replace(/^<g transform="[^"]*"/,`<g transform="translate(${x} ${y}) scale(.34)"`).replace(/opacity="\.2\d"/,'opacity=".7"');

/* Cenas temáticas desenhadas em traço, usadas como fundo à direita */
const CENAS={
  juros(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    ${[0,1,2,3,4].map(i=>`<ellipse cx="60" cy="${150-i*18}" rx="48" ry="12" fill="var(--surface)"/><path d="M12 ${150-i*18}v10a48 12 0 0 0 96 0v-10"/>`).join("")}
    <circle cx="150" cy="40" r="16"/><circle cx="196" cy="96" r="16"/><path d="M200 30 146 106" stroke-width="5"/></g>`},
  fiscal(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <path d="M0 170H260"/><rect x="104" y="20" width="18" height="120"/><rect x="128" y="20" width="18" height="120"/><path d="M104 60h42M104 100h42"/>
    <path d="M20 150h70v-10H20z"/><path d="M28 140a27 22 0 0 1 54 0"/><path d="M170 150h70v-10h-70z"/><path d="M178 140q27 34 54 0"/></g>`},
  ia(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".24">
    <rect x="70" y="50" width="100" height="100" rx="10"/><rect x="95" y="75" width="50" height="50" rx="4"/>
    ${[0,1,2,3].map(i=>`<path d="M${84+i*24} 50V20M${84+i*24} 150v30M70 ${64+i*24}H38M170 ${64+i*24}h32"/><circle cx="${84+i*24}" cy="16" r="4"/><circle cx="${84+i*24}" cy="184" r="4"/><circle cx="34" cy="${64+i*24}" r="4"/><circle cx="206" cy="${64+i*24}" r="4"/>`).join("")}</g>`},
  bolsa(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" stroke="var(--accent)" stroke-width="3" opacity=".22">
    ${[[20,90,40],[60,70,50],[100,100,30],[140,60,70],[180,40,60],[220,20,50]].map(([cx,t,h])=>`<path d="M${cx} ${t-15}v${h+30}"/><rect x="${cx-9}" y="${t}" width="18" height="${h}" fill="var(--surface)"/>`).join("")}
    <path d="M0 150 60 120 110 135 170 80 250 40" fill="none"/></g>`},
  cambio(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <circle cx="70" cy="90" r="56"/><circle cx="190" cy="90" r="56"/>${txt(70,110,"US$",{size:34,w:700,fill:"var(--accent)",anchor:"middle"})}${txt(190,110,"R$",{size:34,w:700,fill:"var(--accent)",anchor:"middle"})}
    <path d="M100 18q30-16 60 0M152 12l8 6-10 4M160 162q-30 16-60 0M108 168l-8-6 10-4"/></g>`},
  inflacao(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <path d="M10 30h30l26 100h110l20-70H52"/><circle cx="80" cy="152" r="10"/><circle cx="160" cy="152" r="10"/><path d="M220 120V20M200 40l20-20 20 20"/></g>`},
  energia(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <path d="M70 20 30 100h40l-20 70 70-96H80l30-54z"/><path d="M190 30c-30 40-46 66-46 90a46 46 0 0 0 92 0c0-24-16-50-46-90z"/></g>`},
  tecnologia(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <rect x="20" y="30" width="170" height="110" rx="8"/><path d="M0 150h210l-12 14H12z"/><rect x="200" y="50" width="56" height="100" rx="10"/><path d="M220 138h16"/></g>`},
  imoveis(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <path d="M20 90 100 30l80 60v80H20z"/><rect x="80" y="120" width="40" height="50"/><rect x="150" y="70" width="80" height="100"/>${[0,1,2].map(i=>`<path d="M165 ${90+i*25}h50"/>`).join("")}</g>`},
  cripto(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <circle cx="90" cy="90" r="70"/><circle cx="90" cy="90" r="56"/>${txt(90,114,"₿",{size:66,w:800,fill:"var(--accent)",anchor:"middle"})}
    <path d="M176 40h50v50h-50zM196 90v24M176 130h50v50h-50z"/></g>`},
  emprego(x,y,s){return `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="var(--accent)" stroke-width="3" opacity=".22">
    <rect x="30" y="60" width="180" height="110" rx="8"/><path d="M90 60V40h60v20M30 105h180"/><rect x="105" y="95" width="30" height="20"/></g>`}
};
const cena=(t,x=380,y=100,s=1)=>(CENAS[t]||CENAS.bolsa)(x,y,s);

function artLinha(a){
  const series=a.series||[{pontos:a.pontos}];
  const all=series.flatMap(s=>s.pontos.map(p=>num(p[1])));
  let lo=Math.min(...all),hi=Math.max(...all);if(a.zero)lo=0;
  const st=passo(((hi-lo)||Math.abs(hi)||1)/3);lo=a.zero?0:Math.floor((lo-st*.25)/st)*st;hi=Math.ceil((hi+st*.35)/st)*st;
  const L=a.fmt==="mil"?96:70,R=34,T=82,B=50,n=series[0].pontos.length;
  const x=j=>L+(W-L-R)*j/(Math.max(1,n-1)),y=v=>T+(H-T-B)*(hi-v)/(hi-lo);
  let g=grid()+icone(a.tema);
  g+=txt(28,48,a.titulo||"",{size:21,w:700,fill:"var(--ink)"});
  for(let v=lo;v<=hi+1e-9;v+=st){g+=`<line x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--line)"/>`+txt(L-10,y(v)+5,a.fmt==="mil"?compact(v).replace("R$ ",""):nice(Math.round(v*100)/100),{f:FONT_M,size:15,anchor:"end"})}
  series[0].pontos.forEach((p,j)=>{if(n<=12||j%Math.ceil(n/8)===0||j===n-1)g+=txt(x(j),H-18,p[0],{size:16,w:600,anchor:"middle"})});
  series.forEach((s,si)=>{
    const cor=si===0?"var(--accent)":"var(--muted)";let d="";
    s.pontos.forEach((p,j)=>{const v=num(p[1]);if(!j)d=`M${x(j)} ${y(v)}`;else if(a.degraus)d+=` L${x(j)} ${y(num(s.pontos[j-1][1]))} L${x(j)} ${y(v)}`;else d+=` L${x(j)} ${y(v)}`});
    if(si===0)g+=`<path d="${d} L${x(n-1)} ${y(lo)} L${x(0)} ${y(lo)} Z" fill="var(--accent)" fill-opacity=".1"/>`;
    g+=`<path d="${d}" fill="none" stroke="${cor}" stroke-width="${si===0?4:2.5}" ${si?'stroke-dasharray="7 6"':""} stroke-linejoin="round" stroke-linecap="round"/>`;
  });
  if(a.rotular){const p0=series[0].pontos;p0.forEach((p,j)=>{const v=num(p[1]);if(j===0||v!==num(p0[j-1][1])){
      g+=`<circle cx="${x(j)}" cy="${y(v)}" r="4.5" fill="var(--accent)" stroke="var(--surface)" stroke-width="2"/>`+txt(x(j)+(j===n-1?-8:6),y(v)-14,v.toLocaleString("pt-BR",{minimumFractionDigits:a.decimais??2,maximumFractionDigits:a.decimais??2})+(a.sufixo||""),{f:FONT_M,size:14,w:500,fill:"var(--ink)",anchor:j===n-1?"end":"start"})}})}
  const last=series[0].pontos[n-1],lx=x(n-1),ly=y(num(last[1]));
  g+=`<circle cx="${lx}" cy="${ly}" r="8" fill="var(--signal)" stroke="var(--surface)" stroke-width="3"/>`;
  if(a.destaque){const w=a.destaque.length*10.2+28,bx=W-R-w,baixo=ly>(T+(H-T-B)/2),by=baixo?T-6:H-B-50;g+=`<rect x="${bx}" y="${by}" width="${w}" height="38" rx="7" fill="var(--ink)"/>`+txt(bx+w/2,by+25,a.destaque,{size:18,w:700,fill:"var(--surface)",anchor:"middle"})}
  if(a.fonte)g+=txt(W-12,H-4,a.fonte,{size:11,anchor:"end"});
  (a.marcas||[]).forEach(m=>{const j=m[0];const v=num(series[0].pontos[j][1]);g+=`<circle cx="${x(j)}" cy="${y(v)}" r="6" fill="var(--signal)" stroke="var(--surface)" stroke-width="2"/>`+txt(x(j)-10,y(v)-16,m[1],{size:17,w:700,fill:"var(--ink)",anchor:"end"})});
  return g;
}
function artIndicador(a){
  let g=grid()+cena(a.tema,396,96,1);
  const cl=sinal(a.variacao),cor=cl==="down"?"var(--down)":cl==="up"?"var(--up)":"var(--muted)";
  g+=txt(32,58,a.rotulo||"",{size:19,w:600});
  g+=txt(28,148,a.valor||"",{size:86,w:800,fill:"var(--ink)"});
  const v=fmtVar(a.variacao||""),w=v.length*15+52;
  g+=`<rect x="32" y="170" width="${w}" height="46" rx="23" fill="${cor}"/>`;
  g+=`<path d="M52 ${cl==="down"?186:200} l9 ${cl==="down"?14:-14} l9 ${cl==="down"?-14:14}z" fill="var(--surface)"/>`+txt(78,202,v,{f:FONT_M,size:24,w:500,fill:"var(--surface)"});
  if(a.fonte)g+=txt(W-12,H-8,a.fonte,{size:11,anchor:"end"});
  (a.secundarios||[]).slice(0,2).forEach((s,i)=>{const yy=268+i*46,c2=sinal(s.variacao);
    g+=`<line x1="32" x2="372" y1="${yy-28}" y2="${yy-28}" stroke="var(--line)"/>`+txt(32,yy,s.rotulo,{size:18,w:600,fill:"var(--muted)"})+txt(372,yy,s.valor+(s.variacao&&!/%/.test(s.valor)?"  "+fmtVar(s.variacao):""),{f:FONT_M,size:18,fill:c2==="down"?"var(--down)":c2==="up"?"var(--up)":"var(--ink)",anchor:"end"})});
  return g;
}
function artBarras(a){
  let g=grid()+icone(a.tema);
  g+=txt(28,48,a.titulo||"",{size:21,w:700,fill:"var(--ink)"});
  const bs=(a.barras||[]).slice(0,4),dec=bs.some(b=>num(b.valor)%1!==0)?1:0,mx=Math.max(...bs.map(b=>num(b.valor)))||1,L=28,maxW=W-L-170,top=96,area=H-top-(a.nota?72:24),slot=area/Math.max(1,bs.length),bh=Math.min(46,slot-34);
  bs.forEach((b,i)=>{const yy=top+i*slot,w=Math.max(4,maxW*num(b.valor)/mx),c=b.destaque?"var(--accent)":"var(--muted)";
    g+=txt(L,yy,b.rotulo,{size:17,w:600,fill:"var(--ink)"});
    g+=`<rect x="${L}" y="${yy+9}" width="${w}" height="${bh}" rx="5" fill="${c}" fill-opacity="${b.destaque?1:.4}"/>`;
    g+=txt(L+w+12,yy+9+bh/2+8,(a.prefixo||"")+num(b.valor).toLocaleString("pt-BR",{minimumFractionDigits:dec,maximumFractionDigits:2})+(a.sufixo||""),{f:FONT_M,size:22,w:500,fill:"var(--ink)"})});
  if(a.fonte)g+=txt(W-12,H-8,a.fonte,{size:11,anchor:"end"});
  if(a.nota){g+=`<rect x="28" y="${H-58}" width="${a.nota.length*9.2+30}" height="38" rx="7" fill="var(--signal-soft)"/>`+txt(43,H-33,a.nota,{size:16,w:600,fill:"var(--ink)"})}
  return g;
}
function artCena(a){
  let g=grid()+cena(a.tema,150,70,1.5).replace('opacity=".22"','opacity=".55"').replace('opacity=".24"','opacity=".55"');
  if(a.titulo)g+=`<rect x="24" y="24" width="${a.titulo.length*9+28}" height="38" rx="6" fill="var(--ink)"/>`+txt(38,49,a.titulo,{size:16,w:700,fill:"var(--surface)"});
  return g;
}
function artComparacao(a){
  /* Dois valores lado a lado: antes x depois, esperado x realizado */
  let g=grid()+icone(a.tema);
  g+=txt(28,48,a.titulo||"",{size:21,w:700,fill:"var(--ink)"});
  const A=a.a||{},B=a.b||{},top=88,h=170,w=262;
  const caixa=(x,o,forte)=>`<rect x="${x}" y="${top}" width="${w}" height="${h}" rx="10" fill="${forte?"var(--accent)":"var(--paper)"}" stroke="${forte?"var(--accent)":"var(--line)"}"/>`+
    txt(x+20,top+38,o.rotulo||"",{size:16,w:600,fill:forte?"var(--surface)":"var(--muted)"})+
    txt(x+20,top+104,o.valor||"",{size:Math.max(22,Math.min(46,Math.floor((w-40)/(Math.max(1,String(o.valor||"").length)*0.6)))),w:800,fill:forte?"var(--surface)":"var(--ink)"})+
    (o.nota?txt(x+20,top+140,o.nota,{size:15,w:500,fill:forte?"var(--surface)":"var(--muted)"}):"");
  g+=caixa(28,A,false)+caixa(W-28-w,B,true);
  g+=`<path d="M${28+w+14} ${top+h/2}h${W-56-2*w-34}" stroke="var(--ink)" stroke-width="3"/><path d="M${W-28-w-12} ${top+h/2-9}l10 9-10 9" fill="none" stroke="var(--ink)" stroke-width="3"/>`;
  if(a.variacao){const v=fmtVar(a.variacao),cl=sinal(a.variacao),cor=cl==="down"?"var(--down)":cl==="up"?"var(--up)":"var(--ink)",ww=v.length*12+30;
    g+=`<rect x="${W-28-ww}" y="${top+h+16}" width="${ww}" height="36" rx="18" fill="${cor}"/>`+txt(W-28-ww/2,top+h+40,v,{f:FONT_M,size:18,fill:"var(--surface)",anchor:"middle"})}
  if(a.nota)g+=txt(28,top+h+40,a.nota,{size:15,w:600,fill:"var(--ink)"});
  if(a.fonte)g+=txt(W-12,H-8,a.fonte,{size:11,anchor:"end"});
  return g;
}
function artFaixa(a){
  /* Um valor numa régua com a faixa de referência (ex.: inflação e o intervalo da meta) */
  let g=grid()+icone(a.tema);
  g+=txt(28,48,a.titulo||"",{size:21,w:700,fill:"var(--ink)"});
  const lo=num(a.min??0),hi=num(a.max??10),v=num(a.valor),L=40,R=40,y0=208,x=t=>L+(W-L-R)*(Math.min(hi,Math.max(lo,t))-lo)/(hi-lo),suf=a.sufixo||"";
  const f=t=>num(t).toLocaleString("pt-BR",{minimumFractionDigits:a.decimais??0,maximumFractionDigits:2})+suf;
  g+=txt(28,128,f(v),{size:72,w:800,fill:"var(--ink)"});
  if(a.rotulo)g+=txt(30,156,a.rotulo,{size:16,w:600});
  g+=`<rect x="${L}" y="${y0}" width="${W-L-R}" height="16" rx="8" fill="var(--line)"/>`;
  if(a.faixa_min!=null&&a.faixa_max!=null)g+=`<rect x="${x(num(a.faixa_min))}" y="${y0}" width="${x(num(a.faixa_max))-x(num(a.faixa_min))}" height="16" fill="var(--up)" fill-opacity=".35"/>`+
    txt((x(num(a.faixa_min))+x(num(a.faixa_max)))/2,y0+44,a.rotulo_faixa||"Faixa de referência",{size:14,w:600,fill:"var(--muted)",anchor:"middle"});
  if(a.alvo!=null)g+=`<path d="M${x(num(a.alvo))} ${y0-8}v32" stroke="var(--up)" stroke-width="3"/>`+txt(x(num(a.alvo)),y0-14,(a.rotulo_alvo||"Meta")+" "+f(a.alvo),{size:14,w:700,fill:"var(--up)",anchor:"middle"});
  [lo,hi].forEach((t,i)=>{g+=txt(i?W-R:L,y0+70,f(t),{f:FONT_M,size:13,anchor:i?"end":"start"})});
  if(a.faixa_min!=null)[a.faixa_min,a.faixa_max].forEach(t=>{g+=txt(x(num(t)),y0+70,f(t),{f:FONT_M,size:13,anchor:"middle"})});
  g+=`<circle cx="${x(v)}" cy="${y0+8}" r="13" fill="var(--signal)" stroke="var(--surface)" stroke-width="4"/>`;
  if(a.nota){const ww=a.nota.length*8.8+28;g+=`<rect x="${W-28-ww}" y="98" width="${ww}" height="38" rx="7" fill="var(--signal-soft)"/>`+txt(W-28-ww/2,123,a.nota,{size:15,w:700,fill:"var(--ink)",anchor:"middle"})}
  if(a.fonte)g+=txt(W-12,H-8,a.fonte,{size:11,anchor:"end"});
  return g;
}
function artRosca(a){
  /* Partes de um todo, até 4 fatias, com rótulos diretos */
  let g=grid()+icone(a.tema);
  g+=txt(28,48,a.titulo||"",{size:21,w:700,fill:"var(--ink)"});
  const ps=(a.partes||[]).slice(0,4),tot=ps.reduce((t,p)=>t+num(p.valor),0)||1,cx=170,cy=214,r=104,rr=62;
  const cores=["var(--accent)","var(--signal)","var(--muted)","var(--ink)"];let ang=-Math.PI/2;
  ps.forEach((p,i)=>{const fr=num(p.valor)/tot,a1=ang,a2=ang+fr*2*Math.PI-1e-4;ang+=fr*2*Math.PI;const big=a2-a1>Math.PI?1:0;
    const P=(rad,t)=>`${(cx+rad*Math.cos(t)).toFixed(1)} ${(cy+rad*Math.sin(t)).toFixed(1)}`;
    g+=`<path d="M${P(r,a1)} A${r} ${r} 0 ${big} 1 ${P(r,a2)} L${P(rr,a2)} A${rr} ${rr} 0 ${big} 0 ${P(rr,a1)}Z" fill="${cores[i]}" fill-opacity="${i===2?.45:1}" stroke="var(--surface)" stroke-width="3"/>`;
    const yy=128+i*52;g+=`<rect x="330" y="${yy-16}" width="18" height="18" rx="4" fill="${cores[i]}" fill-opacity="${i===2?.45:1}"/>`+txt(358,yy,p.rotulo,{size:17,w:600,fill:"var(--ink)"})+
      txt(W-28,yy,num(p.valor).toLocaleString("pt-BR",{maximumFractionDigits:1})+(a.sufixo||""),{f:FONT_M,size:18,fill:"var(--ink)",anchor:"end"})});
  if(a.centro)g+=txt(cx,cy+8,a.centro,{size:22,w:800,fill:"var(--ink)",anchor:"middle"});
  if(a.fonte)g+=txt(W-12,H-8,a.fonte,{size:11,anchor:"end"});
  return g;
}
function desenhar(a){
  if(!a||typeof a!=="object")a={tipo:"cena",tema:"bolsa"};
  let g;try{g=a.tipo==="linha"?artLinha(a):a.tipo==="indicador"?artIndicador(a):a.tipo==="barras"?artBarras(a):a.tipo==="comparacao"?artComparacao(a):a.tipo==="faixa"?artFaixa(a):a.tipo==="rosca"?artRosca(a):artCena(a)}catch(e){console.error("arte",e);g=artCena({tema:a.tema})}
  return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">${g}</svg>`;
}

window.DIArte={desenhar,E,sinal,fmtVar,compact,brl,FONT_D,FONT_M};
})();
