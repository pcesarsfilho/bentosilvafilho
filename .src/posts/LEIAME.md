# Kit de artes do Instagram (Bento & Silva Filho)

Padrão desde 19/11/2026: feed em 1080x1440 (3:4), capas de Reels em 1080x1920. Azul-marinho #0A1326, dourado #C5A063, creme #F4F0E5; Crimson Pro (títulos) e Poppins (textos); filete dourado a 48px da borda.

Uso:

    cd .src/posts && npm i            # fontes (@fontsource/crimson-pro e poppins)
    python3 render.py spec.json saida/   # gera HTML e PNG (Playwright já instalado no ambiente)

Formato do spec: ver o cabeçalho de render.py. Regras de conteúdo:
- carrossel didático: capa com gancho (azul), miolos alternando claro (dark=false) e azul (dark=true), tela final "Salve/compartilhe" (azul);
- toda base legal real, vigente e conferida; sem promessa de resultado, sem captação direta, sem hashtags na legenda (Provimento 205/2021);
- fotos dos advogados (paulo, heloisa, dupla) só de vez em quando, nos posts "Conheça" ou institucionais.

Ícones: alerta, aneis, aviao, balanca, bloqueio, calendario, carro, cartao, casa, celular, chave, conexao, conversa, coracao, crianca, dinheiro, doc, escudo, familia, grafico, hospital, mais, mala, martelo, prato, predio, relogio, trabalho, usuario.
