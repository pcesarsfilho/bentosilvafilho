const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const f of process.argv.slice(2)){const reels=/capa_reels|Capa Reels/.test(f);const fs=require('fs');const H=fs.readFileSync(f,'utf8').includes('height:1920px')?1920:1440;
 const p=await b.newPage({viewport:{width:1080,height:H}});await p.goto('file://'+f);await p.waitForTimeout(400);
 await p.screenshot({path:f.replace(/\.html$/,'.png')});await p.close();}
await b.close()})();
