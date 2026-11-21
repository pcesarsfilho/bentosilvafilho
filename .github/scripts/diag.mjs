const KEY = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==';
async function q(rotulo, n, body) {
  for (let t = 0; t < 4; t++) {
    const r = await fetch('https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search', { method: 'POST', headers: { Authorization: 'APIKey ' + KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    if (r.status === 429) { await new Promise(o => setTimeout(o, 10000)); continue; }
    const j = await r.json().catch(() => ({}));
    const h = (j.hits && j.hits.hits) || [];
    console.log(rotulo, 'status', r.status, 'total', j.hits && j.hits.total && j.hits.total.value, 'graus', h.map(x => x._source.grau).join(','), 'nmov', h.map(x => (x._source.movimentos || []).length).join(','), 'chaves', h[0] ? Object.keys(h[0]._source).join('|') : '');
    return;
  }
  console.log(rotulo, 'sempre 429');
}
const teste = '10132962820268130518';
await q('teste match', teste, { size: 5, query: { match: { numeroProcesso: teste } } });
await q('teste term', teste, { size: 5, query: { term: { numeroProcesso: teste } } });
await q('controle 2021', '', { size: 5, query: { match: { numeroProcesso: '13668284120218130024' } } });
await q('controle 2026 qualquer', '', { size: 1, query: { range: { dataAjuizamento: { gte: '2026-11-01' } } } });
