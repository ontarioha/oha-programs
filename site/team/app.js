/* OHA Team — Assistance Search (v13)
   - Team Login: temporary page-level lock. Real protection should be added on the server (cPanel Directory Privacy).
   - Program list: loaded from the central list (GitHub) when DATA_URL is set, otherwise from programs.json on this site. */
const DATA_URL = 'https://raw.githubusercontent.com/ontarioha/oha-programs/main/programs.json';
const LOGIN_HASH = '8611e2744dda54a6f478126162c6ab208f1cc5701195a8dbc14f8a9684ca9885'; // sha256('oha-team|<login lowercased>|<password>')

const CATEGORY=[['tax','Property taxes and municipal fees'],['utility','Electricity, gas, water and heating'],['repairs','Home repairs and renovations'],['adu','ADU / ARU / rental suites'],['income','Seniors and disability income benefits'],['access','Disability, accessibility and aging in place'],['housing','Mortgage, rent and housing assistance'],['health','Dental, medical and prescriptions'],['food','Food and essential living expenses'],['transport','Transportation'],['debt','Debt and financial hardship'],['community','Community and emergency assistance']];
const DEFAULT_WORDS={wordTitle:'OHA Homeowner Assistance Assessment',wordIntro:'We identified programs that may help with household expenses, home costs and financial stability. These are opportunities to review, not guaranteed benefits.',wordRepIntro:'This assessment identifies possible assistance based on the client profile. Confirm all qualification criteria, funding availability, current amounts and deadlines with the official program administrator.',wordCaution:'Potential match only. No application or eligibility has been approved. Funding may be limited, suspended or closed. Amounts are not necessarily cumulative.',wordNext:'Your Homeowner Assistance Action Plan',wordGoal:'To identify financial assistance you may qualify for, explore ways to reduce your expenses, and help you move toward a more comfortable financial future.',wordStep1:'Confirm Your Information',wordStep2:'Identify Your Best Opportunities',wordStep3:'Prioritize Your Immediate Needs',wordStep4:'Sign the Agreement to Get Started',wordAgreement:'We will review the OHA assistance agreement together, explain the services and any applicable costs, and answer your questions. Once you are comfortable with the terms and sign the agreement, OHA will begin the process within the next 7 days. We will keep you informed as we work toward results as quickly as possible.',wordAfter:'With your agreement in place, OHA can begin reviewing your assistance opportunities, coordinating next steps, and helping you pursue the programs and savings options that best fit your circumstances.',wordCommitment:'To make the process as simple, organized, and stress-free as possible while keeping you informed of our progress.'};
const COVERAGE_LABEL={Waterloo:'Waterloo Region',Simcoe:'Simcoe County (incl. Barrie and Orillia)',Wellington:'Guelph and Wellington County'};

const $=id=>document.getElementById(id);
const safe=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const store={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}},del(k){try{localStorage.removeItem(k)}catch(e){}}};
const session={get(k){try{return sessionStorage.getItem(k)}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,v)}catch(e){}},del(k){try{sessionStorage.removeItem(k)}catch(e){}}};

let programs=[],matches=[],profile=null,estimates={},lookup={municipalities:{},aliases:{},coverage:{}},dataInfo='';
let words={...DEFAULT_WORDS};try{Object.assign(words,JSON.parse(store.get('oha-words')||'{}'))}catch(e){}

/* ---------- Login ---------- */
async function sha256(text){const buf=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text));return [...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,'0')).join('')}
async function onLogin(e){e.preventDefault();const u=$('loginUser').value.trim(),p=$('loginPass').value;
  let ok=false;try{ok=(await sha256('oha-team|'+u.toLowerCase()+'|'+p))===LOGIN_HASH}catch(err){$('loginMsg').textContent='This browser cannot sign in here. Please use an up-to-date Chrome, Edge or Safari.';return}
  if(!ok){$('loginMsg').textContent='Login or password is incorrect.';$('loginPass').value='';$('loginPass').focus();return}
  session.set('oha-team',u);openApp(u)}
function openApp(u){$('login').hidden=true;$('app').hidden=false;$('who').hidden=false;$('whoName').textContent=u;startApp()}
function logout(){session.del('oha-team');location.reload()}

/* ---------- Data ---------- */
async function getJSON(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error(r.status);return r.json()}
function validPrograms(d){return Array.isArray(d)&&d.length>10&&d.every(p=>p&&p.id&&p.name&&Array.isArray(p.regions)&&Array.isArray(p.categories)&&/^https:\/\//.test(p.url||''))}
async function loadData(){
  lookup=await getJSON('municipalities.json');
  let source='site copy';
  if(DATA_URL){try{const d=await getJSON(DATA_URL);if(validPrograms(d)){programs=d;source='central list'}}catch(e){}}
  if(!programs.length){const d=await getJSON('programs.json');if(validPrograms(d))programs=d}
  const dates=programs.map(p=>p.checked).filter(Boolean).sort();const last=dates[dates.length-1];
  dataInfo=`${programs.length} programs · last checked ${last?fmtDate(last):'—'} · ${source}`;
}
const fmtDate=d=>new Date(d+'T12:00:00').toLocaleDateString('en-CA',{year:'numeric',month:'long',day:'numeric'});

/* ---------- Location matching ---------- */
const norm=s=>s.trim().toLowerCase().replace(/^(city|town|township|municipality) of /,'').replace(/\s+/g,' ');
function resolveCity(input){const n=norm(input);
  const mun=Object.keys(lookup.municipalities).find(m=>m.toLowerCase()===n);if(mun)return{municipality:mun,region:lookup.municipalities[mun]};
  const al=Object.keys(lookup.aliases).find(a=>a.toLowerCase()===n);if(al){const m=lookup.aliases[al];return{municipality:m,region:lookup.municipalities[m],via:al}}
  return{municipality:input.trim(),region:null}}
function tokensFor(loc){const t=['ontario','canada','city:'+loc.municipality.toLowerCase()];if(loc.region)t.push('region:'+loc.region.toLowerCase());return t}
function linkFor(p,loc){return (p.links&&p.links[loc.municipality])||p.url}
function cityHint(){const v=$('city').value;if(!v.trim()){$('cityHint').textContent='';return}const loc=resolveCity(v);
  $('cityHint').textContent=!loc.region?'Not in the lookup — only Ontario and federal programs will show.':(loc.via?`${loc.via} is in ${loc.municipality} (${loc.region}).`:`${loc.region} area${lookup.coverage[loc.region]?' · local programs researched':' · local programs not yet researched'}`)}

/* ---------- App ---------- */
const isSenior=age=>['65-69','70-74','75+'].includes(age);
function show(tab){document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('active',x.id===tab));document.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('active',x.dataset.tab===tab));window.scrollTo({top:0,behavior:'smooth'})}
let started=false;
async function startApp(){if(started)return;started=true;
  document.querySelectorAll('.tabs button').forEach(x=>x.addEventListener('click',()=>show(x.dataset.tab)));
  $('categories').innerHTML=CATEGORY.map(([id,label])=>`<label><input type="checkbox" value="${id}" checked> ${safe(label)}</label>`).join('');
  for(const id in words)$(id).value=words[id];
  $('searchBtn').onclick=search;$('toReport').onclick=()=>{renderReport();show('report')};$('printBtn').onclick=()=>window.print();
  $('copyBtn').onclick=()=>navigator.clipboard.writeText($('reportContent').innerText).then(()=>flash('Report copied.')).catch(()=>flash('Please select and copy the report manually.'));
  $('audience').onchange=renderReport;$('length').onchange=renderReport;
  $('saveWords').onclick=()=>{for(const id in DEFAULT_WORDS)words[id]=$(id).value;store.set('oha-words',JSON.stringify(words));$('adminMsg').textContent='Wording saved in this browser.';renderReport()};
  $('resetWords').onclick=()=>{words={...DEFAULT_WORDS};store.del('oha-words');for(const id in words)$(id).value=words[id];$('adminMsg').textContent='Default wording restored.';renderReport()};
  $('exportJson').onclick=()=>download('oha-programs.json',JSON.stringify(programs,null,2));
  $('city').addEventListener('input',cityHint);
  $('dataBanner').textContent='Loading program list…';
  try{await loadData();$('dataBanner').textContent=dataInfo;
    $('cities').innerHTML=[...Object.keys(lookup.municipalities),...Object.keys(lookup.aliases)].sort().map(c=>`<option value="${safe(c)}"></option>`).join('');cityHint();
  }catch(e){$('dataBanner').textContent='The program list could not be loaded. Check the internet connection and refresh.';$('dataBanner').classList.add('bad')}
}
function flash(msg){$('adminMsg').textContent=msg;const b=$('dataBanner'),old=b.textContent;b.textContent=msg;setTimeout(()=>b.textContent=old,2500)}
function download(name,data){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([data],{type:'application/json'}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),500)}

/* Illustrative values live on each program record (value: monthly, annual, once, type, note). */
const vOf=p=>p.value||{monthly:0,annual:0,once:0,type:'project',note:'No illustration set'};
function initialEstimate(p){const v=vOf(p);return {monthly:v.monthly||0,annual:v.annual||0,once:v.once||0}}
function meta(p){const v=vOf(p);return {type:v.type,note:v.note}}
const typeLabel={cash:'Potential payment',bill:'Bill credit',tax:'Tax saving',project:'Project incentive',inkind:'Service value',financing:'Financing / deferral',referral:'Referral only (overlaps)'};
const money=n=>new Intl.NumberFormat('en-CA',{style:'currency',currency:'CAD',maximumFractionDigits:0}).format(n);
// Programs that pay the same underlying emergency energy grant: count only the largest one.
const ENERGY_EMERGENCY=['leap','neef','simcoe-leap','wellington-energy','wreap','fort211salvation'];
function estimateTotals(){
 const total={monthly:0,annual:0,once:0},extra={monthly:0,annual:0,once:0};
 for(const p of matches){const v=estimates[p.id]||{},m=meta(p);const bucket=['cash','bill'].includes(m.type)?total:extra;for(const k of ['monthly','annual','once'])bucket[k]+=Number(v[k])||0}
 const em=matches.filter(p=>ENERGY_EMERGENCY.includes(p.id)&&['cash','bill'].includes(meta(p).type)).map(p=>Number(estimates[p.id]?.once)||0);
 const overlap=em.length>1?em.reduce((a,b)=>a+b,0)-Math.max(...em):0;
 total.once=Math.max(0,total.once-overlap);
 const base=total.monthly*12+total.annual+total.once,conditional=extra.monthly*12+extra.annual+extra.once;
 return {...total,overlap,monthlyEquivalent:total.monthly+total.annual/12,firstYear:base,conditional,allIllustrations:base+conditional};
}
function estimateMarkup(){const t=estimateTotals();return `<section class="estimate-box"><h2>OHA illustrative assistance value</h2><div class="estimate-grid"><div><small>Potential monthly equivalent (payments + bill credits)</small><strong>${money(t.monthlyEquivalent)}/month</strong><small>Monthly + annual recurring ÷ 12</small></div><div><small>Potential one-time payment / bill assistance</small><strong>${money(t.once)}</strong><small>After emergency-energy overlap adjustment</small></div><div><small>Potential first-year payments and bill credits</small><strong>${money(t.firstYear)}</strong><small>Not an eligibility or approval estimate</small></div></div><div class="estimate-grid"><div><small>Additional conditional tax, renovation, services and financing illustrations</small><strong>${money(t.conditional)}</strong><small>Includes noncash and amounts requiring spending</small></div><div><small>ALL program illustrations combined</small><strong>${money(t.allIllustrations)}</strong><small>Showcase total ONLY — not receivable cash</small></div></div><p class="muted"><strong>Energy-upgrade caution:</strong> Energy Affordability, Enbridge Winterproofing, Home Renovation Savings and local retrofit programs may fund the same upgrade. Do not add alternative heat pumps, insulation pathways, or a free appliance and its purchase rebate as separate benefits.</p><p class="muted"><strong>Important:</strong> Every program has an example amount, not an average award. The combined figure may include benefits the client already receives (OAS/GIS), mutually exclusive programs, loans, deferrals and noncash services. Actual additional assistance could be $0. ${t.overlap?`${money(t.overlap)} was deducted for overlapping emergency energy grants. `:''}Confirm eligibility, funding and current rates before presenting a personalized projection.</p></section>`}
function updateEstimates(){document.querySelectorAll('.estimate-input').forEach(input=>{const id=input.dataset.id,k=input.dataset.kind;const n=Number(input.value);if(estimates[id])estimates[id][k]=Number.isFinite(n)?Math.max(0,Math.min(n,1000000)):0});$('estimateSummary').innerHTML=estimateMarkup();renderReport()}
function estimateInputs(p){const v=estimates[p.id]||{monthly:0,annual:0,once:0};return `<div class="estimate-inputs"><p><strong>Illustrative amount (CAD; editable, not guaranteed)</strong> <span class="muted">${safe(typeLabel[meta(p).type]||'')} · ${safe(meta(p).note)}</span></p>${[['monthly','Monthly $'],['annual','Annual $'],['once','One-time $']].map(([k,label])=>`<label>${label}<input class="estimate-input" data-id="${safe(p.id)}" data-kind="${k}" type="number" min="0" max="1000000" step="1" value="${v[k]||0}" aria-label="${safe(p.name)} ${label}"></label>`).join('')}</div>`}

let waitingTimer=null;
function search(){
  if(waitingTimer!==null)return;
  if(!$('city').value.trim()){alert('Enter a municipality.');return}
  if(!document.querySelector('#categories input:checked')){alert('Select at least one category.');return}
  if(!programs.length){alert('The program list did not load. Please refresh the page.');return}
  const wait=$('searchWait'),button=$('searchBtn');button.disabled=true;wait.hidden=false;let remaining=10;
  const tick=()=>{$('waitSeconds').textContent=remaining;$('waitBar').setAttribute('aria-valuenow',String(10-remaining));$('waitFill').style.width=`${(10-remaining)*10}%`};
  tick();
  waitingTimer=setInterval(()=>{remaining--;tick();if(remaining===0){clearInterval(waitingTimer);waitingTimer=null;wait.hidden=true;button.disabled=false;performSearch()}},1000);
  $('cancelWait').onclick=()=>{if(waitingTimer!==null){clearInterval(waitingTimer);waitingTimer=null}wait.hidden=true;button.disabled=false};
}
const levelRank=p=>/municipal/i.test(p.level)?0:/regional|community/i.test(p.level)?1:/ontario/i.test(p.level)?2:3;
function performSearch(){const cityInput=$('city').value.trim();const loc=resolveCity(cityInput);
  profile={city:loc.municipality,cityInput,region:loc.region,clientName:$('clientName').value.trim(),streetAddress:$('streetAddress').value.trim(),postalCode:$('postalCode').value.trim(),age:$('age').value,income:$('income').value,household:$('household').value,housing:$('housing').value,gis:$('gis').value,utility:$('utility').value,account:$('account').value,categories:[...document.querySelectorAll('#categories input:checked')].map(x=>x.value)};
  const tokens=tokensFor(loc);
  matches=programs.filter(p=>p.categories.some(c=>profile.categories.includes(c))&&p.regions.some(r=>tokens.includes(r.toLowerCase()))&&(!p.housing||p.housing.includes(profile.housing)))
   .filter(p=>!['gis','gains','osdcp'].includes(p.id)||isSenior(profile.age))
   .filter(p=>p.id!=='cdb'||!isSenior(profile.age))
   .filter((p,i,arr)=>arr.findIndex(q=>q.id===p.id)===i)
   .sort((a,b)=>{const urgent=p=>profile.utility==='disconnection'&&ENERGY_EMERGENCY.concat(['oesp']).includes(p.id)?-1:0;return urgent(a)-urgent(b)||levelRank(a)-levelRank(b)});
  estimates=Object.fromEntries(matches.map(p=>[p.id,initialEstimate(p)]));
  const local=matches.filter(p=>levelRank(p)<2).length;
  $('resultCount').textContent=`(${matches.length})`;
  $('resultMeta').textContent=`${matches.length} possible programs (${local} local) · ${loc.via?loc.via+', ':''}${loc.municipality}${loc.region?' · '+loc.region:''} · ${profile.housing==='owner'?'Homeowner':profile.housing==='renter'?'Renter':'Housing unknown'}`;
  $('coverageNote').innerHTML=!loc.region?`<div class="warning bad"><strong>“${safe(cityInput)}” isn't in the city lookup.</strong> Only Ontario and federal programs are shown. Check the spelling, or search 211 Ontario for local help.</div>`:(!lookup.coverage[loc.region]?`<div class="warning"><strong>Local programs for the ${safe(loc.region)} area haven't been fully researched yet.</strong> Ontario and federal programs are complete; local ones may be missing. Researched so far: ${Object.keys(lookup.coverage).map(k=>COVERAGE_LABEL[k]||k).join(', ')}.</div>`:'');
  $('resultsList').innerHTML=matches.length?matches.map(p=>`<div class="program"><h3>${safe(p.name)}</h3><span class="pill">${safe(p.level)}</span>${/paused|not confirmed|closed/i.test(p.status||'')?'<span class="pill warn">Check status</span>':''}<span class="pill">Potential match — not confirmed</span><p><strong>Assistance:</strong> ${safe(p.amount)}</p><p><strong>Who qualifies:</strong> ${safe(p.requirements)}</p><p><strong>Status:</strong> ${safe(p.status)}</p><p><strong>Next step:</strong> ${safe(p.action)}</p>${p.phone?`<p><strong>Phone:</strong> <a href="tel:${safe(p.phone.replace(/[^0-9+]/g,'').slice(0,11))}">${safe(p.phone)}</a></p>`:''}<p><a class="official" href="${safe(linkFor(p,loc))}" target="_blank" rel="noopener noreferrer">Official information / application ↗</a> <span class="checked">${p.checked?'Checked '+fmtDate(p.checked):'Not yet re-checked'}</span></p>${estimateInputs(p)}</div>`).join(''):'<p>No programs found for these selections. This does not mean no assistance exists. Try more categories or search 211 Ontario.</p>';
  $('estimateSummary').innerHTML=estimateMarkup();document.querySelectorAll('.estimate-input').forEach(el=>el.addEventListener('input',updateEstimates));renderReport();show('results')}
function renderReport(){if(!profile){$('reportContent').innerHTML='<p>Run a search to prepare a report.</p>';return}const audience=$('audience').value,length=$('length').value;const intro=audience==='homeowner'?words.wordIntro:words.wordRepIntro;const urgent=profile.utility==='disconnection';const loc={municipality:profile.city};
 let html=`<h1>${safe(words.wordTitle)}</h1><p class="muted">${safe(profile.cityInput)}, Ontario · Prepared ${new Date().toLocaleDateString('en-CA',{year:'numeric',month:'long',day:'numeric'})} · Ontario Home Assistance</p><p>${safe(intro)}</p><h2>Client information</h2><p><strong>Name:</strong> ${safe(profile.clientName||'Not provided')} · <strong>Address:</strong> ${safe([profile.streetAddress,profile.cityInput,'Ontario',profile.postalCode].filter(Boolean).join(', '))}</p><h2>Client profile</h2><p>Age: ${safe(profile.age)} · Household: ${safe(profile.household)} · Income band: ${safe(profile.income)} · Housing: ${safe(profile.housing)} · GIS: ${safe(profile.gis)} · Utilities: ${safe(profile.utility)}</p>`;
 if(urgent)html+='<h2>Immediate priority: utility disconnection</h2><p>Contact the utility provider and the local emergency energy assistance (LEAP) intake agency promptly. Ask for a disconnection hold during assessment and a repayment arrangement. Do not assume disconnection is paused until the utility confirms it.</p>';
 html+=estimateMarkup();html+=`<h2>Potential assistance (${matches.length})</h2>`;
 for(const p of matches){const e=estimates[p.id]||{};html+=`<div class="programrow"><h3>${safe(p.name)}</h3><p><strong>Run by:</strong> ${safe(p.level)} program · <strong>Potential benefit:</strong> ${safe(p.amount)}</p><p><strong>Illustrative amounts (subject to eligibility and non-stacking rules):</strong> ${money(e.monthly||0)}/month · ${money(e.annual||0)}/year · ${money(e.once||0)} one-time</p>`;
  if(length!=='short')html+=`<p><strong>Qualification:</strong> ${safe(p.requirements)}</p>`;
  if(audience!=='homeowner'||length==='detailed')html+=`<p><strong>Funding status:</strong> ${safe(p.status)}</p>`;
  const url=linkFor(p,loc);html+=`<p class="program-link"><strong>Program information / application:</strong> <a href="${safe(url)}" target="_blank" rel="noopener noreferrer">Open official program page ↗</a> <span class="print-url">${safe(url)}</span>${p.phone?` · ${safe(p.phone)}`:''}</p>`;
  if(audience==='office')html+=`<p><strong>Action:</strong> ${safe(p.action)} · ☐ Not started ☐ Applied ☐ Approved ☐ Declined</p>`;html+='</div>'}
 html+=`<section class="action-plan"><h2>${safe(words.wordNext)}</h2><p class="plan-brand"><strong>Prepared by Ontario Home Assistance (OHA)</strong></p><p><strong>Our Goal:</strong> ${safe(words.wordGoal)}</p><h3>What We'll Do Together Today</h3><ol class="plan-steps"><li><strong>${safe(words.wordStep1)}</strong><p>Review your household income, homeownership, benefits received, and current financial concerns.</p></li><li><strong>${safe(words.wordStep2)}</strong><p>Review the assistance programs and financial savings opportunities that may be available to you. We'll explain how each could help improve your financial situation.</p></li><li><strong>${safe(words.wordStep3)}</strong><p>Identify the most urgent concerns, including overdue bills, utility disconnections, property taxes, and essential home repairs.</p></li><li><strong>${safe(words.wordStep4)}</strong><p>${safe(words.wordAgreement)}</p></li></ol><h3>What Happens Next?</h3><p>${safe(words.wordAfter)}</p><p><strong>Our commitment:</strong> ${safe(words.wordCommitment)}</p></section>`;
 html+=`<p class="muted"><strong>Important:</strong> ${safe(words.wordCaution)} Ontario Home Assistance helps clients find and apply for these programs; each program is run by the government or agency named, which makes all eligibility decisions.</p>`;$('reportContent').innerHTML=html}

window.addEventListener('DOMContentLoaded',()=>{$('loginForm').addEventListener('submit',onLogin);$('logoutBtn').onclick=logout;const u=session.get('oha-team');if(u)openApp(u);else $('loginUser').focus()});
