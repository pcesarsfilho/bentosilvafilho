# Ilustrações planas na paleta da marca (navy, dourado, creme) com acento vermelho para o "problema"
N='#0E1B33';G='#C9A55A';GD='#A8853E';C='#F3EBDD';W='#FFFFFF';R='#C2413A';L='#E9E0CF';S='#5B6B86'
F="font-family:Montserrat,Arial,sans-serif"
def base(inner): return f'<svg viewBox="0 0 480 400" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'
VOO=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<circle cx="380" cy="92" r="40" fill="{L}"/>
<g transform="translate(250 70) rotate(-12)"><path d="M0 26 L120 20 Q150 19 156 26 Q150 33 120 32 L0 26Z" fill="{N}"/><path d="M62 24 L28 -18 L44 -18 L92 23Z" fill="{N}"/><path d="M60 30 L30 70 L46 70 L90 31Z" fill="{N}"/><path d="M4 25 L-10 4 L2 4 L18 24Z" fill="{N}"/><circle cx="136" cy="25" r="2.5" fill="{G}"/></g>
<rect x="56" y="150" width="368" height="190" rx="16" fill="{N}"/>
<text x="80" y="184" style="{F};font-weight:600;font-size:15px;letter-spacing:3px" fill="{G}">PARTIDAS</text>
<g style="{F};font-weight:600;font-size:17px" fill="{C}">
<text x="80" y="226">GRU</text><text x="150" y="226">14:20</text>
<text x="80" y="268">BSB</text><text x="150" y="268">15:05</text>
<text x="80" y="310">CNF</text><text x="150" y="310">16:40</text></g>
<rect x="262" y="206" width="140" height="28" rx="14" fill="{R}"/><text x="332" y="225" text-anchor="middle" style="{F};font-weight:600;font-size:13px;letter-spacing:1.5px" fill="{W}">CANCELADO</text>
<rect x="262" y="248" width="140" height="28" rx="14" fill="{G}"/><text x="332" y="267" text-anchor="middle" style="{F};font-weight:600;font-size:13px;letter-spacing:1.5px" fill="{N}">ATRASADO</text>
<rect x="262" y="290" width="140" height="28" rx="14" fill="{G}"/><text x="332" y="309" text-anchor="middle" style="{F};font-weight:600;font-size:13px;letter-spacing:1.5px" fill="{N}">ATRASADO</text>
<line x1="80" y1="242" x2="400" y2="242" stroke="{S}" stroke-width="1"/><line x1="80" y1="284" x2="400" y2="284" stroke="{S}" stroke-width="1"/>
<g transform="translate(70 92)"><circle r="34" fill="{W}" stroke="{N}" stroke-width="5"/><path d="M0 -20 V0 L14 10" stroke="{R}" stroke-width="5" fill="none" stroke-linecap="round"/></g>
''')
NEG=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<rect x="44" y="56" width="210" height="140" rx="18" fill="{N}"/>
<rect x="66" y="82" width="42" height="30" rx="6" fill="{G}"/>
<text x="66" y="148" style="{F};font-weight:600;font-size:14px;letter-spacing:2px" fill="{C}">SEU CPF</text>
<text x="66" y="174" style="{F};font-weight:500;font-size:13px;letter-spacing:3px" fill="{S}">•••.•••.•••-••</text>
<g transform="translate(340 268) scale(.85)"><path d="M-110 0 A110 110 0 0 1 110 0" fill="none" stroke="{L}" stroke-width="26"/>
<path d="M-110 0 A110 110 0 0 1 -78 -78" fill="none" stroke="{R}" stroke-width="26"/>
<path d="M-78 -78 A110 110 0 0 1 0 -110" fill="none" stroke="{G}" stroke-width="26"/>
<path d="M0 -110 A110 110 0 0 1 110 0" fill="none" stroke="#6E9B6B" stroke-width="26"/>
<line x1="0" y1="0" x2="-78" y2="-40" stroke="{N}" stroke-width="7" stroke-linecap="round"/><circle r="12" fill="{N}"/>
<text y="44" text-anchor="middle" style="{F};font-weight:600;font-size:14px;letter-spacing:3px" fill="{N}">SCORE</text></g>
<g transform="translate(150 312) rotate(-9)"><rect x="-124" y="-30" width="248" height="60" rx="8" fill="none" stroke="{R}" stroke-width="5"/>
<text y="10" text-anchor="middle" style="{F};font-weight:600;font-size:24px;letter-spacing:3px" fill="{R}">NEGATIVADO</text></g>
<g transform="translate(400 96)"><circle r="30" fill="none" stroke="{N}" stroke-width="8"/><line x1="22" y1="22" x2="46" y2="46" stroke="{N}" stroke-width="10" stroke-linecap="round"/><text y="9" text-anchor="middle" style="{F};font-weight:600;font-size:28px" fill="{R}">?</text></g>
''')
IMO=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<circle cx="380" cy="80" r="30" fill="{L}"/>
<path d="M70 190 L170 104 L270 190Z" fill="{G}"/><rect x="86" y="186" width="168" height="134" fill="{N}"/>
<rect x="116" y="214" width="34" height="34" fill="{C}"/><rect x="190" y="214" width="34" height="34" fill="{C}"/><rect x="150" y="262" width="40" height="58" fill="{G}"/>
<line x1="50" y1="320" x2="290" y2="320" stroke="{N}" stroke-width="4"/>
<g transform="translate(290 110)"><rect width="140" height="190" rx="10" fill="{W}" stroke="{N}" stroke-width="4"/>
<text x="20" y="34" style="{F};font-weight:600;font-size:12px;letter-spacing:2px" fill="{N}">MATRÍCULA</text>
<g stroke="{S}" stroke-width="4" stroke-linecap="round"><line x1="20" y1="56" x2="120" y2="56"/><line x1="20" y1="76" x2="110" y2="76"/><line x1="20" y1="96" x2="120" y2="96"/><line x1="20" y1="116" x2="90" y2="116"/></g>
<circle cx="102" cy="154" r="20" fill="{G}"/><path d="M93 154 l7 7 l12 -14" stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round"/></g>
<g transform="translate(330 330) rotate(-20)"><circle r="18" fill="none" stroke="{GD}" stroke-width="7"/><rect x="16" y="-5" width="60" height="10" rx="4" fill="{GD}"/><rect x="58" y="4" width="8" height="12" fill="{GD}"/><rect x="70" y="4" width="6" height="9" fill="{GD}"/></g>
''')
RES=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<g transform="translate(40 92) rotate(-8)"><rect width="150" height="210" rx="12" fill="#1F3A6B"/><rect x="12" y="12" width="126" height="186" rx="8" fill="none" stroke="{G}" stroke-width="2"/>
<circle cx="75" cy="70" r="24" fill="none" stroke="{G}" stroke-width="3"/><path d="M75 56 l4 9 10 1 -8 6 3 10 -9 -6 -9 6 3 -10 -8 -6 10 -1z" fill="{G}"/>
<text x="75" y="130" text-anchor="middle" style="{F};font-weight:600;font-size:12px;letter-spacing:2px" fill="{C}">CARTEIRA DE</text><text x="75" y="148" text-anchor="middle" style="{F};font-weight:600;font-size:12px;letter-spacing:2px" fill="{C}">TRABALHO</text></g>
<g transform="translate(222 56)"><rect width="200" height="250" rx="10" fill="{W}" stroke="{N}" stroke-width="4"/>
<text x="20" y="36" style="{F};font-weight:600;font-size:12px;letter-spacing:1.5px" fill="{N}">TERMO DE RESCISÃO</text>
<g style="{F};font-size:12px;font-weight:500" fill="{S}"><text x="20" y="70">Saldo de salário</text><text x="20" y="96">Aviso prévio</text><text x="20" y="122">Férias + 1/3</text><text x="20" y="148">13º proporcional</text><text x="20" y="174">FGTS + 40%</text></g>
<g fill="{R}" style="{F};font-weight:600;font-size:16px"><text x="172" y="70">?</text><text x="172" y="96">?</text><text x="172" y="122">?</text><text x="172" y="148">?</text><text x="172" y="174">?</text></g>
<line x1="20" y1="196" x2="180" y2="196" stroke="{L}" stroke-width="2"/><text x="20" y="226" style="{F};font-weight:600;font-size:13px" fill="{N}">TOTAL</text><rect x="110" y="210" width="70" height="22" rx="4" fill="{L}"/></g>
<g transform="translate(352 278) scale(.86)"><rect width="100" height="100" rx="12" fill="{N}"/><rect width="100" height="28" rx="12" fill="{G}"/><rect y="16" width="100" height="12" fill="{G}"/>
<text x="50" y="76" text-anchor="middle" style="{F};font-weight:600;font-size:34px" fill="{C}">10</text><text x="50" y="94" text-anchor="middle" style="{F};font-weight:600;font-size:10px;letter-spacing:2px" fill="{G}">DIAS</text></g>
''')
INV=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<g transform="translate(46 70)">
<g stroke="{GD}" stroke-width="3" fill="none"><path d="M100 46 V78 M40 78 H160 M40 78 V104 M100 78 V104 M160 78 V104"/></g>
<circle cx="100" cy="28" r="22" fill="{N}"/><path d="M88 30 a12 12 0 0 1 24 0" fill="none" stroke="{G}" stroke-width="3"/><circle cx="100" cy="20" r="6" fill="{G}"/>
<g fill="{G}"><circle cx="40" cy="124" r="18"/><circle cx="100" cy="124" r="18"/><circle cx="160" cy="124" r="18"/></g>
<g fill="{N}"><circle cx="40" cy="118" r="6"/><circle cx="100" cy="118" r="6"/><circle cx="160" cy="118" r="6"/><path d="M30 134 a10 8 0 0 1 20 0z"/><path d="M90 134 a10 8 0 0 1 20 0z"/><path d="M150 134 a10 8 0 0 1 20 0z"/></g>
</g>
<g transform="translate(60 228)"><path d="M0 64 L60 14 L120 64Z" fill="{N}"/><rect x="12" y="62" width="96" height="70" fill="{W}" stroke="{N}" stroke-width="4"/><rect x="48" y="90" width="24" height="42" fill="{G}"/><rect x="22" y="76" width="18" height="18" fill="{L}"/><rect x="80" y="76" width="18" height="18" fill="{L}"/></g>
<g transform="translate(262 92)"><rect width="168" height="232" rx="10" fill="{W}" stroke="{N}" stroke-width="4"/>
<text x="20" y="34" style="{F};font-weight:600;font-size:11px;letter-spacing:1.5px" fill="{N}">FORMAL DE</text><text x="20" y="50" style="{F};font-weight:600;font-size:11px;letter-spacing:1.5px" fill="{N}">PARTILHA</text>
<g style="{F};font-size:11.5px;font-weight:500" fill="{S}"><text x="20" y="70">Herdeiro 1</text><text x="20" y="96">Herdeiro 2</text><text x="20" y="122">Herdeiro 3</text></g>
<g style="{F};font-size:12px;font-weight:600" fill="{N}"><text x="122" y="70">1/3</text><text x="122" y="96">1/3</text><text x="122" y="122">1/3</text></g>
<line x1="20" y1="142" x2="148" y2="142" stroke="{L}" stroke-width="2"/>
<g stroke="{S}" stroke-width="3" stroke-linecap="round"><line x1="20" y1="166" x2="130" y2="166"/><line x1="20" y1="184" x2="110" y2="184"/></g>
<circle cx="126" cy="204" r="18" fill="{G}"/><path d="M118 204 l6 6 l11 -13" stroke="{N}" stroke-width="4" fill="none" stroke-linecap="round"/></g>
''')
HOL=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<g transform="translate(52 96)"><rect x="0" y="40" width="150" height="190" rx="6" fill="{N}"/><path d="M-10 46 L75 0 L160 46Z" fill="{G}"/>
<g fill="{C}"><rect x="18" y="66" width="26" height="26"/><rect x="62" y="66" width="26" height="26"/><rect x="106" y="66" width="26" height="26"/><rect x="18" y="110" width="26" height="26"/><rect x="62" y="110" width="26" height="26"/><rect x="106" y="110" width="26" height="26"/></g>
<rect x="58" y="164" width="34" height="66" fill="{G}"/>
<text x="75" y="-14" text-anchor="middle" style="{F};font-weight:600;font-size:12px;letter-spacing:2px" fill="{N}">HOLDING</text></g>
<g transform="translate(336 138)"><circle r="72" fill="{W}" stroke="{N}" stroke-width="4"/>
<path d="M0 0 L0 -74 A74 74 0 0 1 64 37 Z" fill="{G}"/><path d="M0 0 L64 37 A74 74 0 0 1 -64 37 Z" fill="{N}"/><path d="M0 0 L-64 37 A74 74 0 0 1 0 -74 Z" fill="{L}"/>
<circle r="22" fill="{W}"/><text y="5" text-anchor="middle" style="{F};font-weight:600;font-size:12px" fill="{N}">%</text></g>
<g transform="translate(278 246) scale(.8)"><path d="M70 0 L130 22 V64 C130 100 104 118 70 130 C36 118 10 100 10 64 V22 Z" fill="{N}"/><path d="M48 66 l16 16 l30 -34" stroke="{G}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
''')
ACI=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<line x1="40" y1="300" x2="440" y2="300" stroke="{S}" stroke-width="3" stroke-dasharray="18 14"/>
<g transform="translate(46 196)"><path d="M10 60 L24 24 Q30 10 46 10 L110 10 Q124 10 132 22 L152 52 L170 58 Q178 62 178 72 L178 86 L0 86 L0 70 Q0 62 10 60Z" fill="{N}"/>
<path d="M36 24 L104 24 L120 50 L28 50Z" fill="{L}"/><circle cx="40" cy="88" r="18" fill="{S}"/><circle cx="40" cy="88" r="8" fill="{C}"/><circle cx="140" cy="88" r="18" fill="{S}"/><circle cx="140" cy="88" r="8" fill="{C}"/></g>
<g transform="translate(434 196) scale(-1 1)"><path d="M10 60 L24 24 Q30 10 46 10 L110 10 Q124 10 132 22 L152 52 L170 58 Q178 62 178 72 L178 86 L0 86 L0 70 Q0 62 10 60Z" fill="{G}"/>
<path d="M36 24 L104 24 L120 50 L28 50Z" fill="{L}"/><circle cx="40" cy="88" r="18" fill="{S}"/><circle cx="40" cy="88" r="8" fill="{C}"/><circle cx="140" cy="88" r="18" fill="{S}"/><circle cx="140" cy="88" r="8" fill="{C}"/></g>
<path d="M240 206 l10 -26 l6 20 l18 -14 l-8 22 l22 2 l-22 10 l12 18 l-20 -8 l-4 22 l-8 -20 l-14 14 l2 -20 l-20 -2 l18 -10z" fill="{R}"/>
<g transform="translate(176 46)"><rect width="128" height="118" rx="10" fill="{W}" stroke="{N}" stroke-width="4"/><rect x="40" y="-10" width="48" height="20" rx="6" fill="{G}"/>
<text x="64" y="44" text-anchor="middle" style="{F};font-weight:600;font-size:13px;letter-spacing:2px" fill="{N}">B.O.</text>
<g stroke="{S}" stroke-width="4" stroke-linecap="round"><line x1="22" y1="66" x2="106" y2="66"/><line x1="22" y1="84" x2="96" y2="84"/><line x1="22" y1="102" x2="80" y2="102"/></g></g>
''')
GOL=base(f'''
<rect x="20" y="20" width="440" height="360" rx="28" fill="{C}"/>
<g transform="translate(70 52)"><rect width="160" height="296" rx="26" fill="{N}"/><rect x="12" y="34" width="136" height="228" rx="10" fill="{W}"/><rect x="60" y="14" width="40" height="6" rx="3" fill="{S}"/>
<text x="80" y="66" text-anchor="middle" style="{F};font-weight:600;font-size:12px;letter-spacing:1.5px" fill="{N}">TRANSFERÊNCIA</text>
<text x="80" y="104" text-anchor="middle" style="{F};font-weight:600;font-size:22px" fill="{N}">R$ 4.980</text>
<text x="80" y="128" text-anchor="middle" style="{F};font-size:10px" fill="{S}">conta desconhecida</text>
<rect x="28" y="196" width="104" height="36" rx="18" fill="{R}"/><text x="80" y="219" text-anchor="middle" style="{F};font-weight:600;font-size:12px;letter-spacing:1px" fill="{W}">NÃO FUI EU</text></g>
<g transform="translate(270 92)"><path d="M80 0 L160 140 L0 140Z" fill="{G}"/><rect x="74" y="44" width="12" height="54" rx="6" fill="{N}"/><circle cx="80" cy="116" r="8" fill="{N}"/></g>
<g transform="translate(262 262) rotate(-8)"><rect width="168" height="96" rx="12" fill="{N}"/><rect y="20" width="168" height="18" fill="{GD}"/><rect x="16" y="56" width="40" height="26" rx="5" fill="{G}"/><g stroke="{C}" stroke-width="4" stroke-linecap="round"><line x1="72" y1="64" x2="150" y2="64"/><line x1="72" y1="78" x2="124" y2="78"/></g></g>
''')
