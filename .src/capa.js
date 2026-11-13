// Gera as capas 1920x1080 dos artigos para o LinkedIn.
// Uso: (na pasta .src) npm i playwright @fontsource/cormorant-garamond @fontsource/montserrat ; node capa.js <saida_dir>
// Lê artigos.json e cria <saida_dir>/capa-<slug>.png para cada artigo.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const out=process.argv[2]||'capas';fs.mkdirSync(out,{recursive:true});
const nm=path.resolve(__dirname,'node_modules');const mono=path.resolve(__dirname,'../img/monograma.png');
const F=`@font-face{font-family:'CG';font-weight:500;src:url(file://${nm}/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}
@font-face{font-family:'CG';font-weight:500;font-style:italic;src:url(file://${nm}/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2)}
@font-face{font-family:'MS';font-weight:500;src:url(file://${nm}/@fontsource/montserrat/files/montserrat-latin-500-normal.woff2)}`;
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
for(const a of JSON.parse(fs.readFileSync(path.join(__dirname,'artigos.json'),'utf8'))){
 let t=esc(a.titulo);if(t.includes(':')){const i=t.indexOf(':');t=t.slice(0,i+1)+'<br><em>'+t.slice(i+1).trim()+'</em>';}
 const h=`<!doctype html><html><head><meta charset=utf-8><style>${F}*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;background:#0E1B33;color:#F3EBDD;font-family:MS;position:relative;overflow:hidden}
.wm{position:absolute;right:-160px;top:90px;width:900px;opacity:.07}.c{position:absolute;left:150px;top:0;bottom:0;width:1320px;display:flex;flex-direction:column;justify-content:center}
.k{font-size:30px;letter-spacing:.38em;color:#C9A55A;text-transform:uppercase}.r{width:110px;height:3px;background:#C9A55A;margin:40px 0}
h1{font-family:CG;font-weight:500;font-size:104px;line-height:1.08}h1 em{color:#C9A55A}
.f{position:absolute;left:150px;bottom:90px;display:flex;align-items:center;gap:24px;font-size:26px;letter-spacing:.3em}.f img{width:84px}</style></head>
<body><img class=wm src="file://${mono}"><div class=c><div class=k>${esc(a.area)}</div><div class=r></div><h1>${t}</h1></div><div class=f><img src="file://${mono}">BENTO &amp; SILVA FILHO ADVOGADOS</div></body></html>`;
 await p.setContent(h);await p.waitForTimeout(600);await p.screenshot({path:path.join(out,'capa-'+a.slug+'.png')});}
await b.close();})();
