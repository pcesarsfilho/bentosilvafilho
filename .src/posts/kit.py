"""Kit de artes do Instagram do Bento & Silva Filho (padrão 3:4, 1080x1440; capas de Reels 1080x1920).
Uso: python3 render.py spec.json <pasta_saida>. Ver LEIAME.md."""
import base64,sys,os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0,os.path.join(ROOT,'.src','lp')); from vis import IC
F=os.path.join(HERE,'node_modules','@fontsource')
def ff(p): return 'data:font/woff2;base64,'+base64.b64encode(open(p,'rb').read()).decode()
fonts=''
for w,s in [(400,'normal'),(500,'normal'),(400,'italic'),(500,'italic'),(600,'normal')]:
    fonts+=f"@font-face{{font-family:Cr;font-weight:{w};font-style:{s};src:url({ff(f'{F}/crimson-pro/files/crimson-pro-latin-{w}-{s}.woff2')})}}"
for w in (300,400,500,600):
    fonts+=f"@font-face{{font-family:Po;font-weight:{w};src:url({ff(f'{F}/poppins/files/poppins-latin-{w}-normal.woff2')})}}"
def b64(p,m): return f'data:{m};base64,'+base64.b64encode(open(p,'rb').read()).decode()
MONOD=b64(os.path.join(HERE,'assets','mono-escuro.svg'),'image/svg+xml')
MONOC=b64(os.path.join(HERE,'assets','mono-claro.svg'),'image/svg+xml')
MONO=b64(os.path.join(HERE,'assets','mono-principal.svg'),'image/svg+xml')
FOTO={k:b64(os.path.join(ROOT,'img',k+'.jpg'),'image/jpeg') for k in ('paulo','heloisa','dupla')}
N,G,C='#0A1326','#C5A063','#F4F0E5'
def big(icon,size,color,sw=1.2):
    return IC[icon].replace('<svg ',f'<svg style="width:{size}px;height:{size}px;color:{color}" ').replace('stroke-width="1.8"',f'stroke-width="{sw}"')
CSS=fonts+f"""*{{margin:0;padding:0;box-sizing:border-box}}body{{position:relative;overflow:hidden;font-family:Po;-webkit-font-smoothing:antialiased}}
.fr{{position:absolute;inset:48px;border:1.5px solid {G};pointer-events:none}}
.eb{{font-family:Po;font-weight:500;font-size:22px;letter-spacing:.42em;color:{G}}}
.t{{font-family:Cr;font-weight:500;line-height:1.04;letter-spacing:-.005em}}
.t em{{font-style:italic;color:{G}}}
.p{{font-family:Po;font-weight:300;line-height:1.55}}
.cnt{{position:absolute;top:84px;right:92px;font-family:Po;font-weight:500;font-size:20px;letter-spacing:.2em}}
.ft{{position:absolute;left:0;right:0;bottom:86px;text-align:center}}
.ft i{{display:block;width:110px;height:2px;background:{G};margin:0 auto 22px}}
.ft b{{display:block;font-family:Po;font-weight:400;font-size:26px;color:{G};letter-spacing:.04em}}
.ft s{{display:block;text-decoration:none;font-family:Po;font-size:16px;letter-spacing:.38em;margin-top:8px}}
.lei{{font-family:Po;font-weight:500;font-size:20px;letter-spacing:.12em;color:{G};margin-top:34px}}
.sw{{position:absolute;right:96px;bottom:92px;font-family:Po;font-weight:500;font-size:20px;letter-spacing:.24em;color:{G}}}
"""
def page(w,h,bg,body,fg):
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body style='width:{w}px;height:{h}px;background:{bg};color:{fg}'>{body}</body></html>"
def foot(dark):
    return f"<div class=ft><i></i><b>@bentosilvafilhoadv</b><s style='color:{'#B9BCC6' if dark else '#5B6274'}'>POÇOS DE CALDAS · MG</s></div>"
W,H=1080,1440
def capa(n,tot,eb,titulo,sub,icon,swipe=True):
    b=f"""<div class=fr></div><div class=cnt style='color:{G}'>{n}/{tot}</div>
<img src='{MONOD}' style='position:absolute;left:96px;top:96px;width:120px'>
<div style='position:absolute;right:-120px;top:330px;opacity:.07'>{big(icon,760,C,.7)}</div>
<div style='position:absolute;left:96px;right:96px;top:420px'><div class=eb>{eb}</div>
<div class=t style='font-size:104px;margin-top:34px;color:{C}'>{titulo}</div>
<div class=p style='font-size:31px;margin-top:40px;color:#C9CCD6;max-width:800px'>{sub}</div></div>
{"<div class=sw>ARRASTE &nbsp;→</div>" if swipe else ""}
<img src='{MONOD}' style='position:absolute;left:96px;bottom:84px;width:0'>"""
    return page(W,H,N,b,C)
def miolo(n,tot,num,titulo,texto,lei,icon,dark,extra=''):
    bg,fg,mut=(N,C,'#C9CCD6') if dark else (C,N,'#3B4256')
    b=f"""<div class=fr></div><div class=cnt style='color:{G}'>{n}/{tot}</div>
<div style='position:absolute;left:96px;top:140px'><div style='width:150px;height:150px;border-radius:50%;border:1.5px solid {G};display:flex;align-items:center;justify-content:center'>{big(icon,72,G,1.5)}</div></div>
<div style='position:absolute;right:96px;top:120px;font-family:Cr;font-style:italic;font-size:230px;line-height:1;color:{G};opacity:.35'>{num}</div>
<div style='position:absolute;left:96px;right:96px;top:360px'>
<div class=t style='font-size:92px;color:{fg}'>{titulo}</div>
<div class=p style='font-size:35px;margin-top:40px;color:{mut}'>{texto}</div>
{f"<div class=lei>{lei}</div>" if lei else ""}{extra}</div>{foot(dark)}"""
    return page(W,H,bg,b,fg)
def final(n,tot,titulo,texto):
    b=f"""<div class=fr></div><div class=cnt style='color:{G}'>{n}/{tot}</div>
<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 130px;margin-top:-80px'>
<img src='{MONOD}' style='width:190px'>
<div class=t style='font-size:80px;margin-top:56px;color:{C}'>{titulo}</div>
<div class=p style='font-size:30px;margin-top:34px;color:#C9CCD6'>{texto}</div>
<div style='margin-top:56px;font-family:Cr;font-size:40px;letter-spacing:.08em;color:{C}'>BENTO <span style='color:{G};font-style:italic'>&amp;</span> SILVA FILHO</div>
<div style='font-family:Po;font-size:17px;letter-spacing:.5em;color:{G};margin-top:10px'>ADVOGADOS</div></div>{foot(True)}"""
    return page(W,H,N,b,C)
def chips(items,dark):
    bd='rgba(197,160,99,.55)'; fg=C if dark else N
    return "<div style='display:flex;flex-wrap:wrap;gap:16px;margin-top:46px'>"+"".join(f"<span style='border:1.5px solid {bd};border-radius:40px;padding:14px 28px;font-family:Po;font-size:26px;color:{fg}'>{i}</span>" for i in items)+"</div>"
def duas(a,b,dark):
    fg=C if dark else N; bx='rgba(244,240,229,.06)' if dark else 'rgba(10,19,38,.05)'
    cell=lambda t,d:f"<div style='flex:1;background:{bx};border-top:3px solid {G};padding:30px 30px 34px'><div style='font-family:Cr;font-size:44px;color:{G};font-style:italic'>{t}</div><div style='font-family:Po;font-weight:300;font-size:27px;line-height:1.45;margin-top:12px;color:{fg}'>{d}</div></div>"
    return f"<div style='display:flex;gap:22px;margin-top:50px'>{cell(*a)}{cell(*b)}</div>"
def conheca_capa(foto,nome,eb='CONHEÇA'):
    b=f"""<img src='{foto}' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 20%'>
<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,19,38,0) 45%,rgba(10,19,38,.75) 70%,{N} 92%)'></div>
<div class=fr></div><div class=cnt style='color:{G}'>1/3</div>
<div style='position:absolute;left:96px;right:96px;bottom:150px'><div class=eb>{eb}</div>
<div class=t style='font-size:96px;margin-top:22px;color:{C}'>{nome}</div></div><div class=sw>ARRASTE &nbsp;→</div>"""
    return page(W,H,N,b,C)
def conheca_bio(nome,oab,form,atua):
    b=f"""<div class=fr></div><div class=cnt style='color:{G}'>2/3</div>
<div style='position:absolute;left:96px;right:96px;top:150px'>
<div class=eb>{oab}</div><div class=t style='font-size:76px;margin-top:22px;color:{N}'>{nome}</div>
<div style='height:2px;width:110px;background:{G};margin:46px 0'></div>
<div class=eb style='font-size:19px'>FORMAÇÃO</div>
<div class=p style='font-size:30px;color:#3B4256;margin-top:16px'>{form}</div>
<div class=eb style='font-size:19px;margin-top:46px'>ATUAÇÃO</div>
<div class=p style='font-size:30px;color:#3B4256;margin-top:16px'>{atua}</div></div>{foot(False)}"""
    return page(W,H,C,b,N)
def conheca_fim(frase,assin):
    b=f"""<div class=fr></div><div class=cnt style='color:{G}'>3/3</div>
<div style='position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 120px;margin-top:-60px'>
<div style='font-family:Cr;font-size:220px;line-height:.6;color:{G};height:90px'>“</div>
<div class=t style='font-size:66px;color:{C};font-style:italic;font-weight:400'>{frase}</div>
<div class=eb style='margin-top:44px;font-size:19px'>{assin}</div></div>{foot(True)}"""
    return page(W,H,N,b,C)
def capa_reels(eb,titulo,lei,adv,icon,dark):
    bg,fg=(N,C) if dark else (C,N)
    b=f"""<div class=fr></div>
<div style='position:absolute;left:50%;top:330px;transform:translateX(-50%);width:640px;height:640px;border-radius:50%;border:1.5px solid {G};display:flex;align-items:center;justify-content:center'>
<div style='position:absolute;inset:48px;border-radius:50%;background:{G};opacity:.08'></div>{big(icon,330,G,1.1)}</div>
<img src='{MONOD if dark else MONOC}' style='position:absolute;left:50%;top:120px;transform:translateX(-50%);width:130px'>
<div style='position:absolute;left:96px;right:96px;top:1100px'><div class=eb>{eb}</div>
<div class=t style='font-size:96px;margin-top:30px;color:{fg}'>{titulo}</div>
<div style='width:110px;height:2px;background:{G};margin:46px 0 26px'></div>
<div style='display:flex;justify-content:space-between;font-family:Po;font-size:22px;letter-spacing:.06em'><span style='color:{G}'>{lei}</span><span style='letter-spacing:.2em;color:{'#C9CCD6' if dark else '#5B6274'}'>{adv}</span></div></div>"""
    return page(1080,1920,bg,b,fg)
