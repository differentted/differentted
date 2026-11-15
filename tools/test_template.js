// Playwright 测试模板：用本地服务器打开网页，拦截所有云端请求，绝不碰真实的孩子数据。
// 用法：先 python3 tools/devserver.py ，再 node tools/test_template.js
// 需要：npm i playwright（或用已装好的 Playwright）；3D 测试加 --use-gl=swiftshader
const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch({args:['--use-gl=swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:430,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  // 关键：拦截打卡乐园的云端(Supabase)、存钱银行的云端、发邮件服务，测试时不读写真实数据
  await p.route('**/*supabase.co/**',r=>r.abort());
  await p.route('**/*emailjs.com/**',r=>r.abort());
  // （可选）固定日期，比如测试"第二天"的逻辑
  // await p.addInitScript(()=>{ const RD=Date; const off=new RD(2026,10,15,11,0,0).getTime()-RD.now(); class D extends RD{ constructor(...a){ a.length?super(...a):super(RD.now()+off); } static now(){ return RD.now()+off; } } window.Date=D; });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(3000);
  // 在页面里直接调用函数做测试，例如：
  const r=await p.evaluate(()=>({hasState:!!window.state, pets:(state&&state.pets||[]).length}));
  console.log(r);
  await p.screenshot({path:'test_shot.png'});
  console.log('页面报错：',errs.slice(0,5));
  await b.close();
})();
