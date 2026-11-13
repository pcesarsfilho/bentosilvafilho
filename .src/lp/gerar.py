import json, html, urllib.parse, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from conteudo import PAGINAS
import ilus
from vis import IC, VIS
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
BASE='https://bentosilvafilho.com.br/'
AV=json.load(open(os.path.join(ROOT,'avaliacoes.json')))
WA_ICON='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.2-1.4A9.9 9.9 0 1 0 12.04 2zm0 18.1a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7 3.9zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3a.5.5 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.5 2.5 0 0 0 1.7-1.2 2 2 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3z"/></svg>'
CHK='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
G_LOGO='<svg viewBox="0 0 48 48" aria-hidden="true" width="18" height="18"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.6 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
CSS=open(os.path.join(os.path.dirname(__file__),'lp.css')).read()
def e(s): return html.escape(s,quote=True)
def card(n,t,d,ic=None): return f'<div class="hip">'+(f'<span class="hip-ic">{IC[ic]}</span>' if ic else f'<span class="hip-n">{n:02d}</span>')+f'<h3>{e(t)}</h3><p>{e(d)}</p></div>'
def page(p):
    wa=f"https://wa.me/{p['wa']}?text="+urllib.parse.quote(p['msg'])
    def btn(cls,txt,tag): return f'<a class="wa-btn {cls}" href="{wa}" target="_blank" rel="noopener" data-track="{tag}">{WA_ICON}<span>{e(txt)}</span></a>'
    V=VIS.get(p['slug'],{})
    ics=V.get('ic',[])
    hips=''.join(card(i+1,t,d,ics[i] if i<len(ics) else None) for i,(t,d) in enumerate(p['hip']))
    stats_html=''
    if V.get('stats'):
        stats_html='<section class="stats"><div class="wrap stats-in">'+''.join(f'<div class="stat"><b>{e(n)}</b><span>{e(l)}</span><small>{e(s)}</small></div>' for n,l,s in V['stats'])+'</div></section>'
    linha_html=''
    if V.get('linha'):
        linha_html=f'<div class="tl"><h3 class="tl-t">{e(V.get("linha_t",""))}</h3><ol class="tl-l">'+''.join(f'<li><span class="tl-d"></span><b>{e(m)}</b><span>{e(d)}</span></li>' for m,d in V['linha'])+'</ol></div>'
    docs=''.join(f'<li>{CHK}<span>{e(d)}</span></li>' for d in p['docs'])
    faq=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in p['faq'])
    rv=[x for x in AV['avaliacoes'] if x.get('nota')==5 and x.get('texto','').strip()]
    rvs=''.join(f'<figure class="rv"><div class="st">★★★★★</div><blockquote>“{e(x["texto"])}”</blockquote><figcaption>{e(x["nome"])} · Google</figcaption></figure>' for x in rv)
    DEF_STEPS=[('Você manda a mensagem','Conte o que aconteceu pelo WhatsApp, a qualquer hora. Fotos e documentos podem ir pelo próprio celular.'),('Analisamos o seu caso','Verificamos os documentos e explicamos com clareza as possibilidades, os prazos e os próximos passos.'),('Acompanhamento até o fim','Atendimento personalizado pelo advogado, com notícias de cada etapa, sem precisar sair de casa.')]
    st=p.get('steps',DEF_STEPS)
    steps_html=f"<h2>{p.get('steps_t','Rápido, on-line e <em>do seu jeito</em>')}</h2><ol class=\"steps n{len(st)}\">"+''.join(f'<li><span>{i+1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i,(t,d) in enumerate(st))+'</ol>'
    comp_html=''
    if p.get('comp'):
        cards=''.join(f'<div class="cmp-c{" alt" if k else ""}"><h3>{e(t)}</h3><ul>'+''.join(f'<li>{CHK}<span>{e(x)}</span></li>' for x in it)+'</ul></div>' for k,(t,it) in enumerate(p['comp']))
        comp_html=f'<section class="sec"><div class="wrap"><div class="eyebrow dk">Comparativo</div><h2>{e(p.get('comp_t','Inventário em cartório ou na Justiça'))}</h2><div class="cmp">{cards}</div><p class="cmp-note">{e(p.get('comp_note','A escolha depende dos herdeiros, dos bens e dos documentos. Essa análise é a primeira etapa do nosso atendimento.'))}</p></div></section>'
    chips=''.join(f'<li>{CHK}{e(c)}</li>' for c in p['chips'])
    url=BASE+p['slug']+'/'
    adv,oab=p['adv']
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['title'])} | Poços de Caldas e todo o Brasil</title>
<meta name="description" content="{e(p['desc'])}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0E1B33">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="../favicon.png">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Montserrat:wght@400;500;600;700&display=swap">
<!-- Google Ads / Analytics: troque GTAG_ID pelo ID (AW-XXXX ou G-XXXX) e apague as duas linhas de comentário. Cada clique no WhatsApp dispara o evento "clique_whatsapp" (use como conversão).
<script async src="https://www.googletagmanager.com/gtag/js?id=GTAG_ID"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','GTAG_ID');</script>
-->
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"LegalService","name":"Bento & Silva Filho Advogados","url":url,"image":BASE+"img/og.jpg","telephone":"+"+p['wa'],"address":{"@type":"PostalAddress","streetAddress":"Av. Dr. David Benedito Ottoni, 645, sala 02, Jardim dos Estados","addressLocality":"Poços de Caldas","addressRegion":"MG","postalCode":"37701-069","addressCountry":"BR"},"areaServed":[{"@type":"City","name":"Poços de Caldas"},{"@type":"State","name":"Minas Gerais"},{"@type":"State","name":"São Paulo"},{"@type":"Country","name":"Brasil"}],"description":p['desc']},ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="../" aria-label="Bento & Silva Filho Advogados, página inicial"><img src="../img/monograma-128.png" alt="" width="42" height="42"><span class="brand-tx"><span class="brand-n">BENTO <i>&amp;</i> SILVA FILHO</span><span class="brand-s">ADVOGADOS</span></span></a>
  {btn('wa-sm','WhatsApp','whatsapp_topo')}
</div></header>

<section class="hero"><div class="wrap hero-in">
  <div class="hero-tx">
    <div class="eyebrow">{e(p['eyebrow'])}</div>
    <h1>{p['h1']}</h1>
    <p class="lead">{e(p['lead'])}</p>
    {btn('wa-lg pulse',p['cta'],'whatsapp_hero')}
    <ul class="chips">{chips}</ul>
  </div>
  <div class="hero-art">{getattr(ilus,p['ilus'])}</div>
</div></section>
{stats_html}

<section class="sec"><div class="wrap">
  <div class="eyebrow dk">Hipóteses</div>
  <h2>{e(p['hip_t'])}</h2>
  <div class="hips">{hips}</div>
  <div class="mid-cta"><p>Se você se identificou com alguma dessas situações, envie os detalhes agora.</p>{btn('wa-md pulse','Falar pelo WhatsApp','whatsapp_hipoteses')}</div>
</div></section>

<section class="sec alt"><div class="wrap">{linha_html}</div><div class="wrap two">
  <div><div class="eyebrow dk">Entenda</div><h2>{e(p['info_t'])}</h2><p class="body">{e(p['info'])}</p></div>
  <div class="box"><h3>O que separar para a análise</h3><ul class="docs">{docs}</ul><p class="alert"><b>Atenção:</b> {e(p['prazo'])}</p></div>
</div></section>

{comp_html}
<section class="sec dark"><div class="wrap">
  <div class="eyebrow">Como funciona</div>
  {steps_html}
  {btn('wa-lg pulse',p['cta'],'whatsapp_passos')}
</div></section>

<section class="sec"><div class="wrap">
  <div class="eyebrow dk">Dúvidas frequentes</div>
  <h2>Perguntas comuns</h2>
  <div class="faq">{faq}</div>
</div></section>

<section class="sec rv-sec"><div class="wrap">
  <div class="rv-head"><span class="rv-score">{G_LOGO}<b>5,0</b><span class="st">★★★★★</span></span><span class="rv-lbl">Avaliações de clientes no Google</span></div>
  <div class="rv-vp"><div class="rvs" id="rvs">{rvs}</div></div><div class="rv-dots" id="rv-dots"></div>
</div></section>

<section class="final"><div class="wrap">
  <h2>Envie sua situação <em>e receba uma análise.</em></h2>
  <p>Atendimento ágil e personalizado, pelo WhatsApp, para todo o Brasil.</p>
  {btn('wa-lg pulse',p['cta'],'whatsapp_final')}
</div></section>

<section class="local"><div class="wrap local-in">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" fill="currentColor"/></svg>
  <p><b>Escritório em Poços de Caldas-MG.</b> Atendimento presencial em Poços de Caldas e região (Sul de Minas e divisa com São Paulo) e <b>on-line para clientes de todo o Brasil</b>, por WhatsApp e videochamada.</p>
</div></section>

<footer class="foot"><div class="wrap">
  <p>Conteúdo de caráter informativo, que não substitui a análise individual de cada caso. Atendimento: {e(adv)}, {e(oab)} · <a href="../">Bento &amp; Silva Filho Advogados</a> · Poços de Caldas-MG · <a href="../politica-de-privacidade.html">Política de privacidade</a></p>
</div></footer>

<div class="sticky">{btn('wa-sticky pulse',p['cta'],'whatsapp_fixo')}</div>

<script>
(function(){{
  document.querySelectorAll('[data-track]').forEach(function(a){{a.addEventListener('click',function(){{
    try{{ if(window.gtag) gtag('event','clique_whatsapp',{{local:a.getAttribute('data-track'),pagina:'{p['slug']}'}}); }}catch(_e){{}}
  }});}});
  var bar=document.querySelector('.sticky'),hero=document.querySelector('.hero .wa-lg');
  if('IntersectionObserver' in window&&hero){{new IntersectionObserver(function(en){{bar.classList.toggle('on',!en[0].isIntersecting);}}).observe(hero);}}else{{bar.classList.add('on');}}
  function es(s){{return String(s).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  var tr=document.getElementById('rvs'),dt=document.getElementById('rv-dots'),pos=0,tm;
  function pv(){{return window.innerWidth<=620?1:(window.innerWidth<=900?2:3);}}
  function pg(){{return Math.max(1,tr.children.length-pv()+1);}}
  function bd(){{dt.innerHTML='';for(var i=0;i<pg();i++){{(function(i){{var b=document.createElement('button');b.setAttribute('aria-label','Avaliação '+(i+1));b.addEventListener('click',function(){{go(i);rs();}});dt.appendChild(b);}})(i);}}}}
  function go(i){{var n=pg();pos=(i+n)%n;var c=tr.children[0];var s=c?c.getBoundingClientRect().width+14:0;tr.style.transform='translateX('+(-pos*s)+'px)';[].forEach.call(dt.children,function(d,k){{d.setAttribute('aria-current',k===pos?'true':'false');}});}}
  function rs(){{clearInterval(tm);if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches)tm=setInterval(function(){{go(pos+1);}},4000);}}
  tr.addEventListener('mouseenter',function(){{clearInterval(tm);}});tr.addEventListener('mouseleave',rs);
  window.addEventListener('resize',function(){{bd();go(Math.min(pos,pg()-1));}});
  bd();go(0);rs();
  fetch('../avaliacoes.json',{{cache:'no-store'}}).then(function(r){{return r.json();}}).then(function(d){{
    var l=(d.avaliacoes||[]).filter(function(x){{return Number(x.nota)===5&&x.texto&&x.texto.trim();}});
    if(l.length){{tr.innerHTML=l.map(function(x){{return '<figure class="rv"><div class="st">★★★★★</div><blockquote>“'+es(x.texto)+'”</blockquote><figcaption>'+es(x.nome)+' · Google</figcaption></figure>';}}).join('');bd();go(0);}}
  }}).catch(function(){{}});
}})();
</script>
</body>
</html>
'''
for p in PAGINAS:
    d=os.path.join(ROOT,p['slug']); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(page(p)); print('ok',p['slug'])
