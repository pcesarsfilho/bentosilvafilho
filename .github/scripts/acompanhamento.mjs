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

// Tradução das movimentações para linguagem simples. A mais recente que casar define a situação.
// Movimentações de rotina (juntadas, expedições etc.) não casam e são ignoradas.
const REGRAS = [
  { re: /baixa definitiva|arquivad[oa] definitiv|arquivamento definitivo/, fim: true, fase: 'Processo encerrado', texto: 'O processo foi encerrado e arquivado.', prox: 'Nenhuma providência pendente por aqui.' },
  { re: /transito em julgado/, fase: 'Decisão definitiva', texto: 'Não cabe mais recurso da decisão proferida nesta fase do processo.', prox: 'Se houver próxima etapa, como o cumprimento da decisão, o escritório informa.' },
  { re: /cumprimento de sentenca|inicio da execucao|execucao/, fase: 'Cumprimento da decisão', texto: 'O processo está na fase de fazer valer o que foi decidido.', prox: 'Acompanhamento pelo escritório. Avisamos quando houver novidade relevante.' },
  { re: /alvara|levantamento|pagamento/, fase: 'Pagamento em andamento', texto: 'Há providências de pagamento ou liberação de valores em andamento.', prox: 'O escritório avisa quando houver confirmação.' },
  { re: /acordao|julgamento .*recurso|recurso inominado|apelacao|embargos de declaracao/, fase: 'Fase de recurso', texto: 'O processo está em fase de recurso ou de julgamento de recurso.', prox: 'Aguardar o julgamento. O prazo depende da pauta do tribunal.' },
  { re: /sentenca|julgad[oa] (procedente|improcedente)|procedencia|improcedencia|homologa(cao|da|do).*(acordo|transacao)/, fase: 'Sentença proferida', texto: 'O juiz proferiu a decisão de primeira instância.', prox: 'O escritório analisa e orienta sobre os efeitos e os próximos passos.' },
  { re: /conclus[oa]s? (para|ao).*(julgamento|sentenca|decisao|despacho)/, fase: 'Aguardando decisão do juiz', texto: 'O processo está com o juiz para decisão.', prox: 'Aguardar. Não há providência necessária da sua parte.' },
  { re: /audiencia.*(realizad|concluid)|realizada.*audiencia/, fase: 'Audiência realizada', texto: 'A audiência já foi realizada.', prox: 'Aguardar a decisão do juiz.' },
  { re: /audiencia.*(designad|marcad|agendad)|designad[ao].*audiencia/, fase: 'Audiência marcada', texto: 'Há audiência marcada neste processo.', prox: 'O escritório combina os detalhes de data e comparecimento.' },
  { re: /citacao|contestacao|intimacao.*(reu|parte)/, fase: 'Fase de manifestações', texto: 'A outra parte foi comunicada e o processo segue com as manifestações.', prox: 'Aguardar. O escritório acompanha os prazos.' },
  { re: /distribuicao|ajuizamento|recebid[oa]/, fase: 'Processo iniciado', texto: 'O processo foi distribuído e está no início da tramitação.', prox: 'Aguardar os primeiros atos do juízo.' },
];
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
  const movs = hits.flatMap(h => (h._source.movimentos || []).map(m => ({ nome: m.nome, data: String(m.dataHora || '').slice(0, 10) })));
  const classe = hits.map(h => norm(h._source.classe && h._source.classe.nome)).join(' ');
  return { movs, classe };
}

function situacao({ movs, classe }) {
  const eventos = [];
  for (const m of movs) {
    const nm = norm(m.nome);
    const reg = REGRAS.find(r => r.re.test(nm));
    if (reg && m.data) eventos.push({ reg, data: m.data });
  }
  eventos.sort((a, b) => a.data.localeCompare(b.data));
  let ult = eventos[eventos.length - 1];
  // Trânsito em julgado encerra apenas a fase de conhecimento: o painel só encerra com baixa/arquivamento definitivo.
  if (!ult) {
    if (/cumprimento/.test(classe)) return { ...REGRAS.find(r => r.fase === 'Cumprimento da decisão'), data: null };
    return { ...PADRAO, data: null };
  }
  return { ...ult.reg, data: ult.data };
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
