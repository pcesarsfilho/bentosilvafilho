"""Gera HTML e PNG a partir de um spec JSON.
spec = {"nome": "Carrossel X", "slides": [ {...}, ... ]}
Tipos de slide (os campos de texto aceitam <em>...</em> para destaque dourado):
  capa:   {"tipo":"capa","eb":"DIREITO DO DIA A DIA","titulo":"...","sub":"...","icon":"balanca","swipe":true}
  miolo:  {"tipo":"miolo","num":"01","titulo":"...","texto":"...","lei":"CDC, ART. 49","icon":"doc","dark":false,
           "chips":["a","b"]  ou  "duas":[["Título A","texto A"],["Título B","texto B"]] (opcionais)}
  final:  {"tipo":"final","titulo":"Salve para <em>quando precisar</em>","texto":"..."}
  conheca_capa: {"tipo":"conheca_capa","foto":"paulo|heloisa|dupla","nome":"..."}
  conheca_bio:  {"tipo":"conheca_bio","nome":"...","oab":"...","form":"...","atua":"..."}
  conheca_fim:  {"tipo":"conheca_fim","frase":"...","assin":"..."}
  capa_reels:   {"tipo":"capa_reels","eb":"DIREITO EM 60 SEGUNDOS","titulo":"...","lei":"...","adv":"DR. PAULO CÉSAR SILVA FILHO","icon":"relogio","dark":true}
Numeração n/tot é automática. Ícones: ver LEIAME.md.
"""
import json,os,sys,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import kit
spec=json.load(open(sys.argv[1])); out=os.path.abspath(sys.argv[2]); os.makedirs(out,exist_ok=True)
S=spec['slides']; T=len(S); files=[]
for i,s in enumerate(S,1):
    t=s['tipo']
    if t=='capa': h=kit.capa(i,T,s['eb'],s['titulo'],s.get('sub',''),s.get('icon','balanca'),s.get('swipe',T>1))
    elif t=='miolo':
        ex=kit.chips(s['chips'],s.get('dark',False)) if s.get('chips') else (kit.duas(tuple(s['duas'][0]),tuple(s['duas'][1]),s.get('dark',False)) if s.get('duas') else '')
        h=kit.miolo(i,T,s.get('num',f'{i-1:02d}'),s['titulo'],s['texto'],s.get('lei',''),s.get('icon','doc'),s.get('dark',False),ex)
    elif t=='final': h=kit.final(i,T,s['titulo'],s['texto'])
    elif t=='conheca_capa': h=kit.conheca_capa(kit.FOTO[s['foto']],s['nome'])
    elif t=='conheca_bio': h=kit.conheca_bio(s['nome'],s['oab'],s['form'],s['atua'])
    elif t=='conheca_fim': h=kit.conheca_fim(s['frase'],s['assin'])
    elif t=='capa_reels': h=kit.capa_reels(s['eb'],s['titulo'],s['lei'],s['adv'],s.get('icon','balanca'),s.get('dark',True))
    else: raise SystemExit('tipo desconhecido: '+t)
    f=os.path.join(out,f"{spec['nome']} - {i:02d}.html"); open(f,'w').write(h); files.append(f)
subprocess.run(['node',os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.js')]+files,check=True)
print('\n'.join(x.replace('.html','.png') for x in files))
