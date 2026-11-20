// Regression checks for consent gating, conversion deduplication and optional DOM.
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const read = name => readFileSync(new URL('../'+name, import.meta.url), 'utf8');
function analytics({enabled=false, path='/servicios/automatizacion-ia', store=new Map()}={}) {
  const events=[]; const handlers={};
  const location={pathname:path, search:'?utm_source=instagram&utm_campaign=test&email=private',href:'https://example.test'+path};
  const document={body:{dataset:{service:'automatizacion-ia'}},addEventListener:(name,fn)=>handlers[name]=fn};
  const sessionStorage={getItem:key=>store.get(key)||null,setItem:(key,value)=>store.set(key,value),removeItem:key=>store.delete(key)};
  const window={SAC_ANALYTICS_CONFIG:{enabled},dispatchEvent:event=>events.push(event.detail)};
  vm.runInNewContext(read('analytics.js'),{window,document,location,sessionStorage,URLSearchParams,URL,Date,JSON,CustomEvent:class {constructor(name,{detail}){this.detail=detail}}});
  return {api:window.SACAnalytics,events,store,handlers};
}
let a=analytics();a.api.setConsent(true);a.api.markSubmission('automatizacion-ia');assert.equal(a.events.length,0);assert.equal(a.store.size,0);
a=analytics({enabled:true});a.api.markSubmission('automatizacion-ia');assert.equal(a.events.length,0);assert.equal(a.store.size,0);
a.api.setConsent(true);assert.equal(a.events[0].event,'landing_view');assert.equal(a.events[0].utm_source,'instagram');assert.equal(a.events[0].email,undefined);
a.api.markSubmission('automatizacion-ia');assert.equal(a.events.at(-1).event,'contact_submit');assert.equal(a.store.size,1);
const returned=analytics({enabled:true,path:'/gracias.html',store:a.store});returned.api.setConsent(true);assert.equal(returned.events.at(-1).event,'contact_completed');assert.equal(returned.store.size,0);returned.api.setConsent(true);assert.equal(returned.events.filter(x=>x.event==='contact_completed').length,1);
const direct=analytics({enabled:true,path:'/gracias.html'});direct.api.setConsent(true);assert.equal(direct.events.filter(x=>x.event==='contact_completed').length,0);
a.api.setConsent(false);const before=a.events.length;a.api.markSubmission('inicio');assert.equal(a.events.length,before);assert.equal(a.store.size,0);
const blocked=analytics({enabled:true,store:{get(){throw Error('blocked')},set(){throw Error('blocked')},delete(){throw Error('blocked')}}});blocked.api.setConsent(true);blocked.api.markSubmission('inicio');
const inputs=Object.fromEntries(['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].map(key=>[key,{value:''}]));
const listeners={};const form={elements:{namedItem:key=>inputs[key]},dataset:{service:'capacitacion-ia'},addEventListener:(name,fn)=>listeners[name]=fn};
const document={documentElement:{classList:{add(){}}},querySelector:selector=>selector==='#contact-form'?form:null,querySelectorAll:()=>[],getElementById:id=>id==='contact-form'?form:null,addEventListener(){}};
const window={location:{search:'?utm_campaign=workshop&utm_source=meta'},addEventListener(){},SACAnalytics:{markSubmission:service=>assert.equal(service,'capacitacion-ia')}};
vm.runInNewContext(read('main.js'),{document,window,URLSearchParams,URL,Date});assert.equal(inputs.utm_campaign.value,'workshop');assert.equal(inputs.utm_source.value,'meta');listeners.submit();
document.getElementById=()=>null;vm.runInNewContext(read('main.js'),{document,window,URLSearchParams,URL,Date});
console.log('PASS: disabled-by-default analytics; consent/revocation; no PII fields; campaign capture; no direct/repeated conversion; blocked storage; native form handler; missing page elements.');
