/* Aviso e preferências de cookies (LGPD; Guia Orientativo da ANPD sobre cookies, 2022).
   Cookies não necessários (Google Analytics / Google Ads) só são carregados depois do consentimento.
   Para ativar a medição, defina window.BSF_GTAG com o ID real (G-XXXX ou AW-XXXX) antes deste script. */
(function(){
  var KEY='bsf_cookies_v1';
  var ID=window.BSF_GTAG||'';
  var ATIVO=/^(G|AW)-[A-Z0-9]+$/.test(ID);
  window.dataLayer=window.dataLayer||[];
  if(typeof window.gtag!=='function'){window.gtag=function(){window.dataLayer.push(arguments);};}
  gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
  function ler(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function gravar(v){try{localStorage.setItem(KEY,v);}catch(e){}}
  var carregado=false;
  function carregar(){
    if(!ATIVO||carregado)return; carregado=true;
    gtag('consent','update',{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});
    var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(ID);document.head.appendChild(s);
    gtag('js',new Date());gtag('config',ID);
  }
  var base=(document.currentScript&&document.currentScript.src)?document.currentScript.src.replace(/cookies\.js.*$/,''):'/';
  var css='.ck{position:fixed;left:max(16px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:80;max-width:440px;background:#0E1B33;color:#F3EBDD;border:1px solid rgba(201,165,90,.55);border-radius:14px;padding:20px 20px 18px;box-shadow:0 18px 44px rgba(0,0,0,.35);font:14px/1.6 Montserrat,"Segoe UI",Arial,sans-serif;opacity:0;transform:translateY(16px);transition:opacity .4s,transform .4s}'
   +'.ck.on{opacity:1;transform:none}.ck h2{font:500 1.25rem/1.2 "Cormorant Garamond",Georgia,serif;color:#F3EBDD;margin:0 0 6px}.ck p{margin:0 0 14px;color:#D9D2C3}.ck a{color:#C9A55A}'
   +'.ck .b{display:flex;flex-wrap:wrap;gap:8px}.ck button{flex:1 1 150px;min-height:44px;border:1px solid #C9A55A;border-radius:0;background:transparent;color:#F3EBDD;font:600 11px/1.2 Montserrat,Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;cursor:pointer;padding:0 12px}'
   +'.ck button:hover,.ck button:focus-visible{background:#C9A55A;color:#0E1B33;outline:none}'
   +'@media(max-width:560px){.ck{left:12px;right:12px;max-width:none;bottom:calc(12px + env(safe-area-inset-bottom,0px))}}'
   +'body.ck-aberto .fab{bottom:calc(220px + env(safe-area-inset-bottom,0px))}@media(min-width:561px){body.ck-aberto .fab{bottom:calc(18px + env(safe-area-inset-bottom,0px))}}'
   +'@media (prefers-reduced-motion:reduce){.ck{transition:none}}';
  function mostrar(){
    if(document.getElementById('ck'))return;
    var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
    var d=document.createElement('div');d.className='ck';d.id='ck';d.setAttribute('role','dialog');d.setAttribute('aria-labelledby','ck-t');d.setAttribute('aria-describedby','ck-d');
    d.innerHTML='<h2 id="ck-t">Cookies e privacidade</h2><p id="ck-d">Usamos apenas o armazenamento necessário para o site funcionar. Com a sua autorização, também usamos cookies de medição de audiência e de anúncios do Google, para entender como o site é usado. Você pode mudar a escolha a qualquer momento. Saiba mais na <a href="'+base+'politica-de-privacidade.html#cookies">Política de privacidade</a>.</p>'
      +'<div class="b"><button type="button" id="ck-sim">Aceitar cookies</button><button type="button" id="ck-nao">Recusar cookies que não são necessários</button></div>';
    document.body.appendChild(d);document.body.classList.add('ck-aberto');
    requestAnimationFrame(function(){d.classList.add('on');});
    function fechar(v){gravar(v);d.classList.remove('on');document.body.classList.remove('ck-aberto');setTimeout(function(){d.remove();},400);if(v==='sim')carregar();}
    document.getElementById('ck-sim').addEventListener('click',function(){fechar('sim');});
    document.getElementById('ck-nao').addEventListener('click',function(){fechar('nao');});
  }
  window.bsfCookies=function(){try{localStorage.removeItem(KEY);}catch(e){}mostrar();};
  function iniciar(){
    document.querySelectorAll('[data-cookies]').forEach(function(a){a.addEventListener('click',function(e){if(!ATIVO)return;e.preventDefault();window.bsfCookies();});});
    if(!ATIVO)return; /* sem ID configurado, o site não usa cookies não necessários e o aviso não é exibido */
    var v=ler();
    if(v==='sim')carregar(); else if(v!=='nao')mostrar();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',iniciar);else iniciar();
})();
