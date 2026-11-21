const KEY = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==';
const lista = ['10112982520268130518','10048417420268130518','50147288220248130518','50039545620258130518','10021822920258130518','10132962820268130518','10081388920268130518','10111649520268130518','10008777320268130518','50006852320248130460'];
for (const n of lista) {
  for (let t = 0; t < 4; t++) {
    const r = await fetch('https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search', { method: 'POST', headers: { Authorization: 'APIKey ' + KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ size: 5, query: { match: { numeroProcesso: n } } }) });
    if (r.status === 429) { await new Promise(o => setTimeout(o, 8000)); continue; }
    const j = await r.json().catch(() => ({})); const h = (j.hits && j.hits.hits) || [];
    console.log('amostra', n.slice(0, 4) + '…' + n.slice(-6), 'hits', h.length, 'graus', h.map(x => x._source.grau).join(','), 'nmov', h.map(x => (x._source.movimentos || []).length).join(','), 'sigilo', h.map(x => x._source.nivelSigilo).join(','));
    break;
  }
  await new Promise(o => setTimeout(o, 2500));
}
