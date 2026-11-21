const KEY = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==';
const lista = ['10048417420268130518','50147288220248130518','50039545620258130518','10021822920258130518','10008777320268130518'];
const cont = new Map();
for (const n of lista) {
  for (let t = 0; t < 6; t++) {
    const r = await fetch('https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search', { method: 'POST', headers: { Authorization: 'APIKey ' + KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ size: 5, query: { match: { numeroProcesso: n } } }) });
    if (r.status === 429) { await new Promise(o => setTimeout(o, 12000)); continue; }
    const j = await r.json().catch(() => ({}));
    for (const h of (j.hits && j.hits.hits) || []) for (const m of h._source.movimentos || []) {
      const comp = (m.complementosTabelados || []).map(c => c.nome).join('/');
      const k = m.codigo + ' | ' + m.nome + ' | ' + comp; cont.set(k, (cont.get(k) || 0) + 1);
    }
    break;
  }
  await new Promise(o => setTimeout(o, 5000));
}
for (const [k, v] of [...cont.entries()].sort((a, b) => b[1] - a[1])) console.log('amostra mov', v, k);
