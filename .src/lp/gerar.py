import json, html, urllib.parse, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from conteudo import PAGINAS
import ilus
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
BASE='https://bentosilvafilho.com.br/'
AV=json.load(open(os.path.join(ROOT,'avaliacoes.json')))
WA_ICON='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.2-1.4A9.9 9.9 0 1 0 12.04 2zm0 18.1a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7 3.9zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3a.5.5 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.5 2.5 0 0 0 1.7-1.2 2 2 0 0 0 .1-1.2c0-.1-.2-.2-.4-.3z"/></svg>'
CHK='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
G_LOGO='<svg viewBox="0 0 48 48" aria-hidden="true" width="18" height="18"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.6 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
CSS=open(os.path.join(os.path.dirname(__file__),'lp.css')).read()
def e(s): return html.escape(s,quote=True)
def card(n,t,d): return f'<div class="hip"><span class="hip-n">{n:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
def page(p):
    wa=f"https://wa.me/{p['wa']}?text="+urllib.parse.quote(p['msg'])
    def btn(cls,txt,tag): return f'<a class="wa-btn {cls}" href="{wa}" target="_blank" rel="noopener" data-track="{tag}">{WA_ICON}<span>{e(txt)}</span></a>'
    hips=''.join(card(i+1,t,d) for i,(t,d) in enumerate(p['hip']))
    docs=''.join(f'<li>{CHK}<span>{e(d)}</span></li>' for d in p['docs'])
    faq=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in p['faq'])
    rv=[x for x in AV['avaliacoes'] if x.get('nota')==5 and len(x['texto'])>40][:3]
    rvs=''.join(f'<figure class="rv"><div class="st">★★★★★</div><blockquote>“{e(x["texto"])}”</blockquote><figcaption>{e(x["nome"])} · Google</figcaption></figure>' for x in rv)
    chips=''.join(f'<li>{CHK}{e(c)}</li>' for c in p['chips'])
    url=BASE+p['slug']+'/'
    adv,oab=p['adv']
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['title'])}</title>
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
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap top-in">
  <a class="mark" href="../" aria-label="Página inicial"><img src="../img/monograma-128.png" alt="" width="40" height="40"></a>
  <span class="top-tag">Atendimento on-line · em todo o Brasil</span>
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

<section class="sec"><div class="wrap">
  <div class="eyebrow dk">Hipóteses</div>
  <h2>{e(p['hip_t'])}</h2>
  <div class="hips">{hips}</div>
  <div class="mid-cta"><p>Se você se identificou com alguma dessas situações, envie os detalhes agora.</p>{btn('wa-md pulse','Falar pelo WhatsApp','whatsapp_hipoteses')}</div>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div><div class="eyebrow dk">Entenda</div><h2>{e(p['info_t'])}</h2><p class="body">{e(p['info'])}</p></div>
  <div class="box"><h3>O que separar para a análise</h3><ul class="docs">{docs}</ul><p class="alert"><b>Atenção:</b> {e(p['prazo'])}</p></div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="eyebrow">Como funciona</div>
  <h2>Rápido, on-line e <em>do seu jeito</em></h2>
  <ol class="steps">
    <li><span>1</span><h3>Você manda a mensagem</h3><p>Conte o que aconteceu pelo WhatsApp, a qualquer hora. Fotos e documentos podem ir pelo próprio celular.</p></li>
    <li><span>2</span><h3>Analisamos o seu caso</h3><p>Verificamos os documentos e explicamos com clareza as possibilidades, os prazos e os próximos passos.</p></li>
    <li><span>3</span><h3>Acompanhamento até o fim</h3><p>Atendimento personalizado pelo advogado, com notícias de cada etapa, sem precisar sair de casa.</p></li>
  </ol>
  {btn('wa-lg pulse',p['cta'],'whatsapp_passos')}
</div></section>

<section class="sec"><div class="wrap">
  <div class="eyebrow dk">Dúvidas frequentes</div>
  <h2>Perguntas comuns</h2>
  <div class="faq">{faq}</div>
</div></section>

<section class="sec rv-sec"><div class="wrap">
  <div class="rv-head"><span class="rv-score">{G_LOGO}<b>5,0</b><span class="st">★★★★★</span></span><span class="rv-lbl">Avaliações de clientes no Google</span></div>
  <div class="rvs" id="rvs">{rvs}</div>
</div></section>

<section class="final"><div class="wrap">
  <h2>Envie sua situação <em>e receba uma análise.</em></h2>
  <p>Atendimento ágil e personalizado, pelo WhatsApp, para todo o Brasil.</p>
  {btn('wa-lg pulse',p['cta'],'whatsapp_final')}
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
  fetch('../avaliacoes.json',{{cache:'no-store'}}).then(function(r){{return r.json();}}).then(function(d){{
    var l=(d.avaliacoes||[]).filter(function(x){{return Number(x.nota)===5&&x.texto&&x.texto.length>40;}}).slice(0,3);
    if(l.length)document.getElementById('rvs').innerHTML=l.map(function(x){{return '<figure class="rv"><div class="st">★★★★★</div><blockquote>“'+es(x.texto)+'”</blockquote><figcaption>'+es(x.nome)+' · Google</figcaption></figure>';}}).join('');
  }}).catch(function(){{}});
}})();
</script>
</body>
</html>
'''
for p in PAGINAS:
    d=os.path.join(ROOT,p['slug']); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(page(p)); print('ok',p['slug'])
