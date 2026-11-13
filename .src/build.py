"""Gera as páginas de artigos do site a partir de artigos.json.
Uso: python3 build.py  (escreve em /home/claude/bentosilvafilho)"""
import json, html, os, re
from datetime import date

REPO = '/home/claude/bentosilvafilho'
BASE = 'https://bentosilvafilho.com.br/'
LINKEDIN = 'https://www.linkedin.com/company/bentosilvafilhoadv/'
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
arts = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'artigos.json'), encoding='utf-8'))
arts.sort(key=lambda a: a['data'], reverse=True)


def data_ext(s):
    y, m, d = map(int, s.split('-'))
    return f'{d} de {MESES[m-1]} de {y}'


CSS = """
:root{--navy:#0E1B33;--navy-deep:#0A1426;--gold:#C9A55A;--gold-ink:#7A5C26;--cream:#F3EBDD;--paper:#F6F1E7;--white:#fff;--ink:#1E1E1E;--text:#3A3A3A;--muted:#D9D2C3;
--display:'Cormorant Garamond',Georgia,'Times New Roman',serif;--body:'Montserrat','Segoe UI',Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.75}
a{color:inherit}.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.site-header{position:sticky;top:0;z-index:50;background:var(--navy);color:var(--cream);border-bottom:1px solid rgba(201,165,90,.25)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:68px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--cream)}.brand img{width:44px;height:44px}
.brand span{font-family:var(--display);font-weight:500;font-size:20px;letter-spacing:.06em;white-space:nowrap}.brand em{font-style:italic;color:var(--gold)}
.back{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--gold);text-decoration:none}
@media(max-width:520px){.brand span{font-size:15px}.back{font-size:11px}}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.32em;text-transform:uppercase;color:var(--gold-ink)}
h1,h2,h3{font-family:var(--display);font-weight:500;margin:0;color:var(--navy);text-wrap:balance}
h1{font-size:clamp(2.1rem,6vw,3rem);line-height:1.1}h1 em{font-style:italic;color:var(--gold-ink)}
.head{background:var(--navy);color:var(--cream);padding:clamp(48px,8vw,80px) 0}.head h1{color:var(--cream)}.head h1 em{color:var(--gold)}.head .eyebrow{color:var(--gold)}
.head p{color:var(--muted);max-width:60ch;margin:14px 0 0}
.lista{display:grid;gap:22px;padding:56px 0 80px}
.card{display:block;background:var(--white);border-top:2px solid var(--gold);padding:26px 26px 24px;text-decoration:none;transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(14,27,51,.12)}
.card .meta{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-ink);font-weight:600}
.card h2{font-size:1.75rem;line-height:1.2;margin:8px 0 6px}.card p{margin:0;color:var(--text);font-size:.95rem}
.card .ler{display:inline-block;margin-top:12px;font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--navy);border-bottom:1px solid var(--gold)}
.artigo{max-width:720px;margin:0 auto;padding:56px 20px 72px}
.artigo h2{font-size:1.7rem;margin:34px 0 8px}.artigo p{margin:0 0 16px;color:#2E2E2E;text-align:justify;hyphens:auto}
.nota{margin-top:36px;padding:18px 20px;border-left:3px solid var(--gold);background:var(--white);font-size:.85rem;color:var(--text)}
.guia{display:block;margin-top:36px;padding:24px 26px;background:var(--navy);color:var(--cream);text-decoration:none;border-left:4px solid var(--gold)}.guia-t{display:block;font-family:var(--display);font-size:1.6rem;color:#FBF6EC;line-height:1.2}.guia-d{display:block;margin-top:6px;font-size:.95rem;color:var(--muted)}.guia-l{display:inline-block;margin-top:12px;font-size:12px;font-weight:600;letter-spacing:.16em;color:var(--gold)}
.acoes{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 22px;text-decoration:none;font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;border:1px solid var(--gold);color:var(--navy)}
.btn-navy{background:var(--navy);color:var(--gold)}.btn svg{width:18px;height:18px}
.site-footer{background:var(--navy-deep);color:#A9A293;font-size:.8rem}.site-footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;padding:28px 20px}
.site-footer a{color:var(--gold);text-decoration:none}.site-footer p{margin:0}
.vazio{padding:40px 0;color:var(--text)}
.card.com-capa{display:grid;grid-template-columns:240px 1fr;gap:24px;align-items:start}.card.com-capa img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
@media(max-width:640px){.card.com-capa{grid-template-columns:1fr}}
.tag{display:inline-block;background:var(--navy);color:var(--gold);padding:2px 8px;margin-right:8px;letter-spacing:.14em}
.galeria{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin:28px 0 8px}
.galeria a{display:block;overflow:hidden;background:var(--navy)}.galeria img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;transition:transform .3s}
.galeria a:hover img{transform:scale(1.04)}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
"""

LI_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.65 4.77 6.1V21h-4v-4.9c0-1.17-.02-2.68-1.63-2.68-1.64 0-1.89 1.28-1.89 2.6V21h-4z"/></svg>'


def page(title, desc, url, body, prefix='', extra_head=''):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0E1B33">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{prefix}favicon.png">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Montserrat:wght@400;500;600&display=swap">
{extra_head}<style>{CSS}</style>
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="brand" href="{prefix}index.html" aria-label="Bento & Silva Filho Advogados, início"><img src="{prefix}img/monograma-128.png" alt="" width="44" height="44"><span>BENTO <em>&amp;</em> SILVA FILHO</span></a>
<a class="back" href="{prefix}artigos.html">ARTIGOS E NOTÍCIAS</a>
</div></header>
<main>
{body}
</main>
<footer class="site-footer"><div class="wrap">
<p>Bento &amp; Silva Filho Advogados · Poços de Caldas-MG · OAB/MG 22.728</p>
<p><a href="{prefix}index.html">Site</a> · <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> · <a href="https://www.instagram.com/bentosilvafilhoadv/" target="_blank" rel="noopener">Instagram</a></p>
</div></footer>
</body>
</html>
"""


def corpo_html(linhas):
    out = []
    for l in linhas:
        if l.startswith('## '):
            out.append(f'<h2>{html.escape(l[3:])}</h2>')
        else:
            out.append(f'<p>{html.escape(l)}</p>')
    return '\n'.join(out)


LP_LINK = {
    'inventario-em-cartorio': ('inventario/', 'Precisa fazer um inventário?', 'Veja como funciona o atendimento, do levantamento dos documentos à partilha, em cartório ou na Justiça.'),
    'negativacao-indevida-o-que-fazer': ('nome-negativado/', 'Seu nome foi negativado indevidamente?', 'Veja quando cabe a retirada do registro e a indenização, e envie seu caso.'),
    'cobranca-indevida-devolucao-em-dobro': ('nome-negativado/', 'A cobrança indevida virou negativação?', 'Veja o que fazer quando o seu nome é incluído no Serasa ou no SPC sem motivo.'),
    'distrato-imovel-na-planta': ('compra-de-imovel/', 'Vai comprar ou já comprou um imóvel?', 'Veja como funciona a análise jurídica da compra, do contrato ao registro.'),
    'decimo-terceiro-salario-prazos': ('direitos-trabalhistas/', 'Tem dúvidas sobre os seus direitos trabalhistas?', 'Rescisão, horas extras, FGTS, justa causa e outras questões: veja como funciona o atendimento.'),
    'voo-cancelado-ou-atrasado-nas-ferias': ('voo-cancelado-atrasado/', 'Teve problema com um voo?', 'Veja como funciona a análise do seu caso, com atendimento on-line para todo o Brasil.'),
    'holding-familiar-quando-vale-a-pena': ('holding-familiar/', 'Quer organizar a sucessão da sua família?', 'Veja como funciona o planejamento sucessório e o estudo de viabilidade da holding.'),
    'acidente-de-transito-o-que-pode-ser-cobrado': ('acidente-de-transito/', 'Sofreu um acidente de trânsito?', 'Veja o que pode ser reparado e quais documentos reunir para a análise.'),
    'golpe-do-falso-advogado': ('golpe-bancario/', 'Caiu em golpe ou teve transferências que não fez?', 'Veja quando o banco responde pela fraude e o que fazer agora.'),
}
os.makedirs(os.path.join(REPO, 'artigos'), exist_ok=True)
for a in arts:
    noticia = a.get('tipo') == 'noticia'
    url = f"{BASE}artigos/{a['slug']}.html"
    ld = json.dumps({"@context": "https://schema.org", "@type": "NewsArticle" if noticia else "Article", "headline": a['titulo'], "datePublished": a['data'],
                     "author": {"@type": "Organization", "name": "Bento & Silva Filho Advogados"},
                     "publisher": {"@type": "Organization", "name": "Bento & Silva Filho Advogados"}, "description": a['resumo']}, ensure_ascii=False)
    galeria = ''
    if a.get('imagens'):
        galeria = '<div class="galeria">' + ''.join(
            f'<a href="../{i["src"]}" target="_blank" rel="noopener"><img src="../{i["src"]}" alt="{html.escape(i["alt"])}" loading="lazy"></a>' for i in a['imagens']) + '</div>'
    guia = ''
    if a['slug'] in LP_LINK:
        href, t1, t2 = LP_LINK[a['slug']]
        guia = f'<a class="guia" href="../{href}"><span class="guia-t">{html.escape(t1)}</span><span class="guia-d">{html.escape(t2)}</span><span class="guia-l">VER COMO FUNCIONA →</span></a>'
    nota = ('Publicado também na página do escritório no LinkedIn.' if noticia else
            'Conteúdo de caráter exclusivamente informativo, que não substitui a análise individual de cada situação. Publicado também na página do escritório no LinkedIn.')
    body = f"""<section class="head"><div class="wrap">
<div class="eyebrow">{html.escape(a['area'])} · {data_ext(a['data'])}</div>
<h1 style="margin-top:14px">{html.escape(a['titulo'])}</h1>
<p>{html.escape(a['resumo'])}</p>
</div></section>
<article class="artigo">
{corpo_html(a['corpo'])}
{galeria}
{guia}
<div class="nota">{nota}</div>
<div class="acoes">
<a class="btn btn-navy" href="{LINKEDIN}" target="_blank" rel="noopener">{LI_SVG} Seguir no LinkedIn</a>
<a class="btn" href="../artigos.html">Artigos e notícias</a>
</div>
</article>"""
    doc = page(a['titulo'] + ' | Bento & Silva Filho Advogados', a['resumo'], url, body, prefix='../',
               extra_head=f'<script type="application/ld+json">{ld}</script>\n')
    if a.get('capa'):
        doc = doc.replace(f'{BASE}img/og.jpg', BASE + a['capa'])
    open(os.path.join(REPO, 'artigos', a['slug'] + '.html'), 'w', encoding='utf-8').write(doc)

# índice publicado (o site mostra somente artigos com data de hoje ou anterior)
idx = [{k: a[k] for k in ('slug', 'data', 'titulo', 'resumo', 'area', 'tipo', 'capa') if k in a} for a in arts]
json.dump(idx, open(os.path.join(REPO, 'artigos', 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

lista = f"""<section class="head"><div class="wrap">
<div class="eyebrow">Artigos e notícias</div>
<h1 style="margin-top:14px">Informação jurídica <em>em linguagem clara</em></h1>
<p>Artigos sobre os direitos do cidadão e do consumidor e notícias do escritório. Os mesmos conteúdos são publicados na nossa página do LinkedIn.</p>
<div class="acoes"><a class="btn btn-navy" style="border-color:var(--gold)" href="{LINKEDIN}" target="_blank" rel="noopener">{LI_SVG} Seguir no LinkedIn</a></div>
</div></section>
<div class="wrap"><div class="lista" id="lista"><p class="vazio">Carregando...</p></div></div>
<script>
(function(){{
  var MESES={json.dumps(MESES, ensure_ascii=False)};
  function ext(s){{var p=s.split('-');return (+p[2])+' de '+MESES[+p[1]-1]+' de '+p[0];}}
  function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  var hoje=new Date();var h=hoje.getFullYear()+'-'+('0'+(hoje.getMonth()+1)).slice(-2)+'-'+('0'+hoje.getDate()).slice(-2);
  fetch('artigos/index.json',{{cache:'no-store'}}).then(function(r){{return r.json();}}).then(function(a){{
    a=a.filter(function(x){{return x.data<=h;}}).sort(function(x,y){{return x.data<y.data?1:-1;}});
    var el=document.getElementById('lista');
    if(!a.length){{el.innerHTML='<p class="vazio">Em breve, novos conteúdos por aqui.</p>';return;}}
    el.innerHTML=a.map(function(x){{var n=x.tipo==='noticia';var t='<div><div class="meta">'+(n?'<span class="tag">NOTÍCIA</span>':esc(x.area)+' · ')+ext(x.data)+'</div><h2>'+esc(x.titulo)+'</h2><p>'+esc(x.resumo)+'</p><span class="ler">'+(n?'LER NOTÍCIA':'LER ARTIGO')+'</span></div>';return '<a class="card'+(x.capa?' com-capa':'')+'" href="artigos/'+x.slug+'.html">'+(x.capa?'<img src="'+x.capa+'" alt="" loading="lazy">':'')+t+'</a>';}}).join('');
  }}).catch(function(){{document.getElementById('lista').innerHTML='<p class="vazio">Não foi possível carregar o conteúdo agora.</p>';}});
}})();
</script>"""
open(os.path.join(REPO, 'artigos.html'), 'w', encoding='utf-8').write(
    page('Artigos e notícias | Bento & Silva Filho Advogados', 'Artigos jurídicos e notícias do escritório Bento & Silva Filho Advogados.',
         BASE + 'artigos.html', lista, prefix=''))
print(len(arts), 'publicações')

# Sitemap: páginas fixas, landing pages e artigos já publicados (data até hoje)
import datetime, sys
_hoje = datetime.date.today().isoformat()
_urls = [BASE, BASE + 'artigos.html']
_lp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lp')
sys.path.insert(0, _lp_dir)
try:
    from conteudo import PAGINAS as _LPS
    _urls += [f"{BASE}{p['slug']}/" for p in _LPS]
except Exception:
    pass
_urls += [f"{BASE}artigos/{x['slug']}.html" for x in sorted(arts, key=lambda x: x['data'], reverse=True) if x['data'] <= _hoje]
if os.path.exists(os.path.join(REPO, 'politica-de-privacidade.html')):
    _urls.append(BASE + 'politica-de-privacidade.html')
open(os.path.join(REPO, 'sitemap.xml'), 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{u}</loc></url>\n' for u in _urls) + '</urlset>\n')
print('sitemap:', len(_urls), 'URLs')
