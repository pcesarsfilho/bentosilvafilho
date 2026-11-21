// Atualiza os painéis de acompanhamento processual a partir da API Pública do DataJud (CNJ).
// Entrada: .github/acompanhamento/lista.json  { itens: [{ h, n, ate }] }
//   h   = SHA-256 (hex) do código do link; o código em si nunca é gravado aqui
//   n   = número do processo (só dígitos)
//   ate = validade do link (AAAA-MM-DD)
// Saída: a/d/<h>.json (dados mostrados na página a/index.html)
// Regras de remoção: item fora da lista, vencido ou com processo encerrado (baixa/arquivamento definitivo, mais 30 dias).
import fs from 'node:fs';
import path from 'node:path';

const DIR = '.github/acompanhamento';
const LISTA = path.join(DIR, 'lista.json');
const TOMB = path.join(DIR, 'encerrados.json');
const OUT = 'a/d';
const KEY = process.env.DATAJUD_KEY || 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==';
const DIAS_APOS_FIM = 30;
const HOJE = new Date().toISOString().slice(0, 10);

const lerJson = (f, pad) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return pad; } };
const gravar = (f, obj) => { const txt = JSON.stringify(obj, null, 1) + '\n'; if (!fs.existsSync(f) || fs.readFileSync(f, 'utf8') !== txt) fs.writeFileSync(f, txt); };
const norm = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const diasEntre = (a, b) => Math.round((Date.parse(b) - Date.parse(a)) / 86400000);

// Número CNJ (NNNNNNNDDAAAAJTROOOO) -> índice da API pública
const UF = {1:'ac',2:'al',3:'ap',4:'am',5:'ba',6:'ce',7:'dft',8:'es',9:'go',10:'ma',11:'mt',12:'ms',13:'mg',14:'pa',15:'pb',16:'pr',17:'pe',18:'pi',19:'rj',20:'rn',21:'rs',22:'ro',23:'rr',24:'sc',25:'se',26:'sp',27:'to'};
function indice(n) {
  const j = n[13], tr = parseInt(n.slice(14, 16), 10);
  if (j === '8' && UF[tr]) return 'tj' + UF[tr];
  if (j === '4' && tr >= 1 && tr <= 6) return 'trf' + tr;
  if (j === '5' && tr >= 1 && tr <= 24) return 'trt' + tr;
  return null;
}

// Tradução das movimentações para linguagem simples. No DataJud cada movimentação vem em pedaços (nome + complementos tabelados,
// ex.: "Conclusão" + "para julgamento"; "de Conciliação" + "designada"), então a regra olha para o texto junto e, quando existe, para o código da tabela do CNJ.
// A mais recente que casar define a situação. Rotina (juntadas, expedições, publicações etc.) é ignorada.
const RUIDO = /^(publicacao|disponibilizacao|expedicao|expedida|expedido|documento|peticao|mero expediente|ato ordinatorio|decurso|confirmada|em secretaria|mandado|juntada|remessa|processo devolvido|defensor|recebimento)/;
const REGRAS = [
  { re: /baixa definitiva|^definitivo$/, fim: true, fase: 'Processo encerrado', texto: 'O processo foi encerrado e arquivado.', prox: 'Nenhuma providência pendente por aqui.' },
  { re: /transito em julgado/, fase: 'Decisão definitiva', texto: 'Não cabe mais recurso da decisão proferida nesta fase do processo.', prox: 'Se houver próxima etapa, como o cumprimento da decisão, o escritório informa.' },
  { re: /alvara|levantamento de (valor|deposito)|pagamento (efetuado|realizado)/, fase: 'Pagamento em andamento', texto: 'Há providências de pagamento ou liberação de valores em andamento.', prox: 'O escritório avisa quando houver confirmação.' },
  { re: /^(procedencia|improcedencia|homologacao de decisao de juiz leigo|homologacao de (transacao|acordo)|extincao)/, fase: 'Sentença proferida', texto: 'Foi proferida a decisão de primeira instância.', prox: 'O escritório analisa e orienta sobre os efeitos e os próximos passos.' },
  { re: /^(provimento|nao provimento|desprovimento|nao conhecimento de recurso|acordao)/, fase: 'Recurso julgado', texto: 'O recurso foi julgado pela instância superior.', prox: 'O escritório analisa e orienta sobre os próximos passos.' },
  { re: /^conclusao.*(para julgamento|para sentenca)|^para julgamento de merito/, fase: 'Aguardando decisão do juiz', texto: 'O processo está com o juiz para decisão final.', prox: 'Aguardar. Não há providência necessária da sua parte.' },
  { re: /^de (conciliacao|instrucao( e julgamento)?|mediacao|justificacao).*realizada/, fase: 'Audiência realizada', texto: 'A audiência já foi realizada.', prox: 'Aguardar a decisão do juiz.' },
  { re: /^de (conciliacao|instrucao( e julgamento)?|mediacao|justificacao).*(designada|redesignada)/, fase: 'Audiência marcada', texto: 'Há audiência marcada neste processo.', prox: 'O escritório combina os detalhes de data e comparecimento.' },
  { re: /^distribuicao/, fase: 'Processo iniciado', texto: 'O processo foi distribuído e está no início da tramitação.', prox: 'Aguardar os primeiros atos do juízo.' },
];
const R_RECURSO = { fase: 'Fase de recurso', texto: 'O processo está em fase de recurso, na Turma Recursal ou no tribunal.', prox: 'Aguardar o julgamento. O prazo depende da pauta.' };
const R_CUMPR = { fase: 'Cumprimento da decisão', texto: 'O processo está na fase de fazer valer o que foi decidido.', prox: 'Acompanhamento pelo escritório. Avisamos quando houver novidade relevante.' };
const PADRAO = { fase: 'Em andamento', texto: 'O processo segue em tramitação normal, sem novidade relevante no momento.', prox: 'Não há providência necessária da sua parte.' };

async function consultar(n) {
  const ind = indice(n);
  if (!ind) return { erro: 'tribunal' };
  // Tenta de novo com espera crescente quando a API limita o ritmo (429) ou oscila (5xx)
  let r;
  for (let t = 0; t < 5; t++) {
    r = await fetch(`https://api-publica.datajud.cnj.jus.br/api_publica_${ind}/_search`, {
      method: 'POST',
      headers: { Authorization: 'APIKey ' + KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ size: 10, query: { match: { numeroProcesso: n } } }),
    });
    if (r.status !== 429 && r.status < 500) break;
    await new Promise(ok => setTimeout(ok, 10000 * (t + 1)));
  }
  if (r.status === 401 || r.status === 403) return { erro: 'chave' };
  if (!r.ok) return { erro: 'http ' + r.status };
  const j = await r.json();
  const hits = (j.hits && j.hits.hits) || [];
  if (!hits.length) return { vazio: true };
  return { hits: hits.map(h => h._source) };
}

function situacao({ hits }) {
  const eventos = [];
  for (const h of hits) {
    const datas = (h.movimentos || []).map(m => String(m.dataHora || '').slice(0, 10)).filter(Boolean).sort();
    for (const m of h.movimentos || []) {
      const data = String(m.dataHora || '').slice(0, 10); if (!data) continue;
      const nome = norm(m.nome), comp = (m.complementosTabelados || []).map(c => norm(c.nome)).join(' ');
      if (RUIDO.test(nome)) continue;
      const texto = (nome + ' ' + comp).trim();
      const reg = REGRAS.find(r => r.re.test(nome) || r.re.test(texto));
      if (reg) eventos.push({ reg, data });
    }
    // Turma Recursal / segundo grau e cumprimento de sentença aparecem como outro grau ou outra classe do mesmo número
    if (h.grau === 'TR' || h.grau === 'G2') eventos.push({ reg: R_RECURSO, data: datas[0] || String(h.dataAjuizamento || '').slice(0, 10) });
    if (/cumprimento/.test(norm(h.classe && h.classe.nome))) eventos.push({ reg: R_CUMPR, data: String(h.dataAjuizamento || '').slice(0, 10) || datas[0] });
  }
  eventos.sort((a, b) => String(a.data).localeCompare(String(b.data)));
  // Trânsito em julgado encerra só a fase de conhecimento: o painel só encerra com baixa/arquivamento definitivo.
  const ult = eventos[eventos.length - 1];
  return ult ? { ...ult.reg, data: ult.data } : { ...PADRAO, data: null };
}

const lista = lerJson(LISTA, { itens: [] }).itens || [];
const tomb = new Set(lerJson(TOMB, { encerrados: [] }).encerrados || []);
fs.mkdirSync(OUT, { recursive: true });
const vivos = new Set();
let falhas = 0;

for (const it of lista) {
  if (!it || !/^[0-9a-f]{64}$/.test(it.h || '') || !/^\d{20}$/.test(it.n || '')) continue;
  const f = path.join(OUT, it.h + '.json');
  if (tomb.has(it.h)) continue;                                   // já encerrado: nunca recria
  if (it.ate && it.ate < HOJE) { tomb.add(it.h); continue; }      // link vencido
  const antigo = lerJson(f, null);
  const res = await consultar(it.n).catch(e => ({ erro: String(e) }));
  if (res.erro) {                                                  // falha: mantém o que já existe
    falhas++; console.log('falha ao consultar', it.h.slice(0, 8), res.erro);
    if (antigo) vivos.add(it.h);
    continue;
  }
  let dados;
  if (res.vazio) {
    dados = antigo || { fase: 'Consulta indisponível', texto: 'O andamento deste processo não está disponível para consulta online.', prox: 'Fale com o escritório para obter informações.', data: null };
  } else {
    const s = situacao(res);
    dados = { fase: s.fase, texto: s.texto, prox: s.prox, data: s.data };
    if (s.fim) dados.encerradoEm = (antigo && antigo.encerradoEm) || HOJE;
  }
  if (dados.encerradoEm && diasEntre(dados.encerradoEm, HOJE) > DIAS_APOS_FIM) { tomb.add(it.h); continue; }
  dados.ate = it.ate || null;
  gravar(f, dados);
  vivos.add(it.h);
}

// Limpeza: apaga qualquer painel que não esteja mais ativo (desativado no app, vencido ou encerrado)
for (const nome of fs.readdirSync(OUT)) {
  if (!nome.endsWith('.json')) continue;
  if (!vivos.has(nome.slice(0, -5))) { fs.unlinkSync(path.join(OUT, nome)); console.log('removido', nome.slice(0, 8)); }
}
gravar(TOMB, { encerrados: [...tomb].sort() });
console.log(`ok: ${vivos.size} ativos, ${falhas} falhas`);
if (falhas && !vivos.size) process.exitCode = 1;
