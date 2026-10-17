document.documentElement.classList.toggle('embedded',new URLSearchParams(location.search).has('embedded'));
const $=s=>document.querySelector(s), audio=$('#audio'), viewer=$('#viewer');
const dictionaries={
'zh-CN':{s:'主语',v:'谓语',o:'宾语',c:'从句',a:'修饰',k:'关键短语',b:'表语',e:'宾补'},
ja:{s:'主語',v:'述語',o:'目的語',c:'節',a:'修飾',k:'まとまり',b:'補語',e:'目的格補語'},
ko:{s:'주어',v:'서술어',o:'목적어',c:'절',a:'수식어',k:'핵심 구',b:'보어',e:'목적격 보어'},
ar:{s:'فاعل',v:'فعل',o:'مفعول به',c:'جملة تابعة',a:'وصف',k:'عبارة أساسية',b:'خبر',e:'متمم المفعول'},
es:{s:'Sujeto',v:'Predicado',o:'Objeto',c:'Subordinada',a:'Modificador',k:'Grupo clave',b:'Atributo',e:'Complemento'},
pt:{s:'Sujeito',v:'Predicado',o:'Objeto',c:'Oração',a:'Modificador',k:'Expressão',b:'Predicativo',e:'Complemento'},
de:{s:'Subjekt',v:'Prädikat',o:'Objekt',c:'Nebensatz',a:'Angabe',k:'Wortgruppe',b:'Prädikativ',e:'Ergänzung'},
ru:{s:'Подлежащее',v:'Сказуемое',o:'Дополнение',c:'Придаточное',a:'Определение',k:'Смысловой блок',b:'Именная часть',e:'Дополнение'},
en:{s:'Subject',v:'Predicate',o:'Object',c:'Clause',a:'Modifier',k:'Core chunk',b:'Complement',e:'Object complement'}};
const roles=dictionaries[MATERIAL.locale]||dictionaries['zh-CN'];
const HAS_AUDIO=MATERIAL.media.kind!=='none', TOTAL_DURATION=MATERIAL.media.duration||0;
let learningState={materialId:MATERIAL.id,position:0,replays:[],saved:[]},stateReady=false,saveTimer,menuChunk=null;
const stateKey='chunk-listening:'+MATERIAL.id;
const defaultState=()=>({materialId:MATERIAL.id,position:0,replays:[],saved:[]});
const validState=x=>x&&x.materialId===MATERIAL.id&&Array.isArray(x.saved)&&Array.isArray(x.replays);
function scheduleSave(){if(!stateReady)return;if(saveTimer)return;saveTimer=setTimeout(()=>{saveTimer=null;persist()},500)}
function persist(){try{localStorage.setItem(stateKey,JSON.stringify(learningState))}catch(e){}if(location.protocol==='http:')fetch('/api/state',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(learningState),keepalive:true}).catch(()=>{});}
async function restore(){let state;try{state=JSON.parse(localStorage.getItem(stateKey)||'null')}catch(e){}if(location.protocol==='http:'){try{const r=await fetch('/api/state');if(r.ok){const server=await r.json();if(validState(server))state=server}}catch(e){}}if(validState(state))learningState=state;stateReady=true;const pos=Math.min(TOTAL_DURATION,Math.max(0,Number(learningState.position)||0));if(HAS_AUDIO&&pos>0)seek(pos);renderSaved();}

let current=0, following=true, loopId=null, segmentEnd=null, last=0, liveNode=null, toastTimer=0, pendingSeek=null;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function label(p){let role=roles[p.role];return `<span class="label"><span class="role">${role}</span><span class="zh"><span class="label-separator"> · </span>${esc(p.zh)}</span></span>`}
function replayButton(id,en,group=false){return `<button class="block-replay" ${group?'data-replay-group':'data-replay-leaf'}="${id}" aria-label="Replay ${group?'group':'chunk'} ${esc(en)}" title="Replay ${group?'group':'chunk'}">↻</button>`}
function renderPart(p){if(p.children){return `<div class="group ${p.role}" data-group="${p.id}"><div class="group-caption"><span class="group-label" data-replay-group="${p.id}" tabindex="0" role="button">${label(p)}</span>${replayButton(p.id,p.en,true)}</div>${p.containerOnly?'':`<div class="head" data-leaf="${p.headId}"><span class="en leaf-text" tabindex="0" role="button" aria-label="Replay ${esc(p.en)}">${esc(p.en)}</span>${replayButton(p.headId,p.en)}</div>`}${p.relation?`<span class="relation">↳ ${esc(p.relation)}</span>`:''}<div class="kids">${p.children.map(renderPart).join('')}</div></div>`}
return `<div class="phrase ${p.role}" data-leaf="${p.id}"><span class="leaf-text" tabindex="0" role="button" aria-label="Replay ${esc(p.en)}">${label(p)}<span class="en">${esc(p.en)}</span></span>${replayButton(p.id,p.en)}</div>`}
$('#sentences').innerHTML=NEWS.map((s,i)=>`<article class="sentence ${i===0?'current':''}" data-sentence="${i}" aria-label="Sentence ${i+1}"><div class="sentence-meta"><button class="sentence-stamp" data-replay-sentence="${i}" aria-label="Play from ${fmt(s.start)}, sentence ${i+1}" title="Continue listening from here"><span class="stamp-play">▶</span><time>${fmt(s.start)}</time></button><span class="sentence-number">${String(i+1).padStart(2,'0')} <span class="sentence-state">${i===0?'Current':''}</span></span><button class="sentence-replay" data-repeat-sentence="${i}" aria-label="Replay sentence ${i+1}" title="Replay this sentence only">↻</button></div><div class="sentence-track" aria-hidden="true">${s.leaves.map(l=>`<span class="track-segment ${l.role}" style="flex-grow:${HAS_AUDIO?l.end-l.start:1}" data-timeline-leaf="${l.id}"></span>`).join('')}<i class="sentence-needle"></i></div><div class="blocks">${s.parts.map(renderPart).join('')}</div></article>`).join('');
const sentenceNodes=[...document.querySelectorAll('.sentence')],leafMap=new Map([...document.querySelectorAll('[data-leaf]')].map(el=>[el.dataset.leaf,el]));
const allLeaves=NEWS.flatMap(s=>s.leaves.map(l=>({...l,sentence:s.index-1})));
function fmt(t){t=Math.max(0,Math.floor(t));return `${String(Math.floor(t/60)).padStart(2,'0')}:${String(t%60).padStart(2,'0')}`}
function toast(msg){clearTimeout(toastTimer);$('#toast').textContent=msg;$('#toast').hidden=false;toastTimer=setTimeout(()=>$('#toast').hidden=true,2200)}
function setFollowing(on){following=on;$('#follow-label').textContent=on?'Following':'Reading'}
function findSentence(t){let i=NEWS.findIndex(s=>t+.002<s.end);return i<0?NEWS.length-1:i}
function update(){if(!HAS_AUDIO)return {t:0,node:null,leaf:allLeaves[0]};let t=Number.isFinite(audio.currentTime)?audio.currentTime:0;const i=findSentence(t);current=i;
for(let n=0;n<sentenceNodes.length;n++){sentenceNodes[n].classList.toggle('current',n===i);sentenceNodes[n].classList.toggle('past',n<i);sentenceNodes[n].querySelector('.sentence-state').textContent=n===i?(audio.ended?'Finished':(audio.paused?'Current':'Listening')):''}
sentenceNodes[i].querySelector('.sentence-needle').style.left=`${Math.max(0,Math.min(100,(t-NEWS[i].start)/NEWS[i].duration*100))}%`;
$('#chapter').textContent=NEWS[i].chapter;$('#sentence-count').textContent=`${String(i+1).padStart(2,'0')} / ${NEWS.length}`;$('#elapsed').textContent=fmt(t);$('#progress').value=t;$('#progress').style.setProperty('--pct',`${t/TOTAL_DURATION*100}%`);
const leaf=allLeaves.find(l=>t+.002>=l.start&&t<l.end-.002)||NEWS[i].leaves.filter(l=>l.start<=t+.002).at(-1)||NEWS[i].leaves[0];let node=leafMap.get(leaf.id);
if(liveNode!==node){document.querySelectorAll('.speaking,.in-play').forEach(el=>el.classList.remove('speaking','in-play'));node?.classList.add('speaking');document.querySelectorAll('.track-segment.active').forEach(el=>el.classList.remove('active'));document.querySelector(`[data-timeline-leaf="${leaf.id}"]`)?.classList.add('active');let parent=node?.parentElement;while(parent&&parent!==viewer){if(parent.classList.contains('group'))parent.classList.add('in-play');parent=parent.parentElement}liveNode=node}
return {t,node,leaf};}
function frame(stamp){let {t,node,leaf}=update();let dt=last?Math.min((stamp-last)/1000,1):.016;last=stamp;
if(!audio.paused){if(segmentEnd!==null&&t>=segmentEnd){audio.pause();segmentEnd=null;toast('Replay finished · Press Play to continue')}else if(loopId!==null&&t>=NEWS[loopId].end-.03){audio.currentTime=NEWS[loopId].start}}
if(following&&node){let fraction=Math.max(0,Math.min(1,(t-leaf.start)/(leaf.end-leaf.start)));let y=node.getBoundingClientRect().top-viewer.getBoundingClientRect().top+viewer.scrollTop;let target=y-viewer.clientHeight*.30+fraction*Math.max(0,node.offsetHeight-26);if(audio.ended)target=viewer.scrollHeight-viewer.clientHeight;target=Math.max(0,Math.min(target,viewer.scrollHeight-viewer.clientHeight));let reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;viewer.scrollTop=reduced?target:viewer.scrollTop+(target-viewer.scrollTop)*(1-Math.exp(-dt*4.5));}
requestAnimationFrame(frame)}
async function start(){if(!HAS_AUDIO){toast('Text only · No audio yet');return}segmentEnd=null;setFollowing(true);if(audio.ended||audio.currentTime>=TOTAL_DURATION-.05)audio.currentTime=0;try{await audio.play()}catch(e){toast('Unable to play audio. Please try again.');console.error(e)}}
function seek(t,play=false){const value=Math.max(0,Math.min(TOTAL_DURATION,t));if(audio.readyState<1){pendingSeek=value}else audio.currentTime=value;segmentEnd=null;setFollowing(true);if(loopId!==null)loopId=findSentence(value);const state=update();if(state.node){const y=state.node.getBoundingClientRect().top-viewer.getBoundingClientRect().top+viewer.scrollTop;viewer.scrollTop=Math.max(0,Math.min(y-viewer.clientHeight*.30,viewer.scrollHeight-viewer.clientHeight))}if(play)start()}
$('#play').onclick=()=>audio.paused?start():audio.pause();
function renderPlayback(){const playing=!audio.paused;$('#play').setAttribute('aria-label',playing?'Pause':'Play');$('#play-icon').innerHTML=playing?'<path d="M7 5h4v14H7zm7 0h4v14h-4Z"/>':'<path d="m9 5 11 7-11 7Z"/>'}
audio.addEventListener('play',renderPlayback);audio.addEventListener('pause',renderPlayback);audio.addEventListener('ended',()=>{if(segmentEnd!==null){segmentEnd=null;renderPlayback();update();toast('Replay finished');return}if(loopId!==null){audio.currentTime=NEWS[loopId].start;audio.play().catch(()=>toast('Press Play to resume the loop'));return}renderPlayback();update();toast('Lesson finished · Listen again anytime')});audio.addEventListener('error',()=>{if(HAS_AUDIO)toast('Audio failed to load. Reopen this lesson.')});
audio.addEventListener('loadedmetadata',()=>{if(pendingSeek!==null){audio.currentTime=pendingSeek;pendingSeek=null}if(Math.abs(audio.duration-TOTAL_DURATION)>.2)console.warn('Unexpected duration',audio.duration);update()});
$('#progress').addEventListener('input',e=>seek(Number(e.target.value)));
$('#previous').onclick=()=>seek(NEWS[audio.currentTime-NEWS[current].start>2?current:Math.max(0,current-1)].start);
$('#next').onclick=()=>seek(current<NEWS.length-1?NEWS[current+1].start:TOTAL_DURATION);
$('#loop').onclick=()=>{loopId=loopId===null?current:null;$('#loop').classList.toggle('active',loopId!==null);$('#loop').setAttribute('aria-pressed',loopId!==null);$('#loop').setAttribute('aria-label',loopId===null?'Enable sentence loop':'Disable sentence loop');toast(loopId===null?'Sentence loop off':`Looping sentence ${loopId+1}`)};
const speeds=[.75,1,1.25,1.5];$('#speed').onclick=()=>{audio.playbackRate=speeds[(speeds.indexOf(audio.playbackRate)+1)%speeds.length];$('#speed').textContent=(Number.isInteger(audio.playbackRate)?audio.playbackRate.toFixed(1):String(audio.playbackRate))+'×'};
$('#translations').onclick=()=>{let hidden=$('.phone').classList.toggle('hide-translations');$('#translations').classList.toggle('on',!hidden);$('#translations').setAttribute('aria-pressed',!hidden);$('#translations').innerHTML=hidden?'Grammar only <span>✓</span>':'Translations <span>✓</span>'};
viewer.addEventListener('wheel',()=>setFollowing(false),{passive:true});viewer.addEventListener('touchstart',()=>setFollowing(false),{passive:true});viewer.addEventListener('keydown',e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End'].includes(e.key))setFollowing(false)});
async function replayRange(startTime,endTime,name){if(!HAS_AUDIO){toast('Text only · No audio yet');return}learningState.replays.push({start:startTime,end:endTime,name,at:Date.now()});learningState.replays=learningState.replays.slice(-500);scheduleSave();seek(startTime);segmentEnd=endTime;toast(`Replay · ${name}`);try{await audio.play()}catch(e){segmentEnd=null;toast('Please try playing again.')}}
async function replayLeaf(el){const leaf=allLeaves.find(l=>l.id===el.dataset.leaf);if(leaf)await replayRange(leaf.start,leaf.end,leaf.en)}
async function replayGroup(id){const group=document.querySelector(`[data-group="${id}"]`);if(!group)return;const ids=[...group.querySelectorAll('[data-leaf]')].map(el=>el.dataset.leaf);const leaves=allLeaves.filter(l=>ids.includes(l.id));if(leaves.length)await replayRange(leaves[0].start,leaves[leaves.length-1].end,'Full group')}
viewer.addEventListener('click',e=>{if(suppressTap>Date.now()){suppressTap=0;e.preventDefault();return}if(!HAS_AUDIO)return;const repeat=e.target.closest('[data-repeat-sentence]');if(repeat){const sentence=NEWS[Number(repeat.dataset.repeatSentence)];replayRange(sentence.start,sentence.end,`Sentence ${sentence.index}`);return}const stamp=e.target.closest('[data-replay-sentence]');if(stamp){seek(NEWS[Number(stamp.dataset.replaySentence)].start,true);return}const caption=e.target.closest('[data-replay-group]');if(caption){replayGroup(caption.dataset.replayGroup);return}const icon=e.target.closest('[data-replay-leaf]');if(icon){replayLeaf(leafMap.get(icon.dataset.replayLeaf));return}const node=e.target.closest('[data-leaf]');if(node)replayLeaf(node)});
viewer.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('.leaf-text,.group-label')){e.preventDefault();if(e.target.matches('.group-label'))replayGroup(e.target.dataset.replayGroup);else replayLeaf(e.target.closest('[data-leaf]'))}});
audio.addEventListener('timeupdate',()=>{if(segmentEnd!==null&&audio.currentTime>=segmentEnd){const end=segmentEnd;segmentEnd=null;audio.pause();audio.currentTime=end;toast('Replay finished · Press Play to continue')}});
$('#menu').onclick=()=>{renderSaved();$('#sheet').hidden=false;$('#close-menu').focus()};$('#close-menu').onclick=()=>{$('#sheet').hidden=true;$('#menu').focus()};document.addEventListener('keydown',e=>{if(e.key==='Escape')$('#sheet').hidden=true;if(e.code==='Space'&&e.target===document.body){e.preventDefault();$('#play').click()}});
const chapters=[];NEWS.forEach(s=>{if(!chapters.some(c=>c.name===s.chapter))chapters.push({name:s.chapter,start:s.start})});$('#chapters').innerHTML=chapters.map(c=>`<button class="chapter-button" data-time="${c.start}"><span>${esc(c.name)}</span><span>${fmt(c.start)} →</span></button>`).join('');$('#chapters').onclick=e=>{const btn=e.target.closest('[data-time]');if(btn){seek(Number(btn.dataset.time));$('#sheet').hidden=true}};
requestAnimationFrame(frame);

// The product shell keeps this player mounted when switching tabs.
window.addEventListener('message',e=>{if(e.origin===location.origin&&e.source===window.parent&&e.data?.type==='chunk-player-pause')audio.pause()});

// Adapt the approved layout to the supplied lesson, never a hard-coded news demo.
document.title=MATERIAL.title+' · English Chunk Flow';
$('.header h2').textContent=MATERIAL.title;
$('.edition').textContent='ENGLISH CHUNK FLOW';
$('.subtitle').textContent=MATERIAL.subtitle||'Catch the backbone, then the details';
$('.layer-note').textContent=MATERIAL.media.kind==='original'?'Original audio · Local alignment':HAS_AUDIO?'Synthesized audio · Local alignment':'Text only · No audio';
$('.phone').classList.toggle('text-only',!HAS_AUDIO);
$('.phone').classList.toggle('arabic',MATERIAL.locale==='ar');
$('#progress').max=TOTAL_DURATION;
$('#sentence-count').textContent=`01 / ${NEWS.length}`;
$('.times').lastElementChild.textContent=fmt(TOTAL_DURATION);
$('#ending time').textContent=fmt(TOTAL_DURATION);
$('.intro>p').textContent=MATERIAL.title;
$('.specs').children[1].textContent=HAS_AUDIO?'Duration '+fmt(TOTAL_DURATION):'Text only';
$('.intro small').textContent=(MATERIAL.media.kind==='original'?'Original recording':HAS_AUDIO?'Local synthesized speech':'No audio')+' · '+MATERIAL.warnings.join(' ');
$('.sheet .eyebrow').textContent='ENGLISH CHUNK FLOW · '+NEWS.length+' sentences';
$('.sheet h3').textContent='Listen & review';
$('.sheet>p').textContent='Your position is saved automatically. Long-press or right-click a chunk to save it.';
$('.disclosure').textContent='Analysis: assistant language reasoning. Alignment: '+MATERIAL.alignment+'. '+MATERIAL.warnings.join(' ');
if(!HAS_AUDIO){audio.removeAttribute('src');$('.foot-note').textContent='Text only · Long-press a chunk to save it';$('.specs').children[2].textContent='No audio yet';for(const el of document.querySelectorAll('.leaf-text,.group-label')){el.setAttribute('aria-disabled','true');if(el.hasAttribute('aria-label'))el.setAttribute('aria-label',el.getAttribute('aria-label').replace(/^Replay /,'Read '))}for(const el of document.querySelectorAll('.transport button,#progress,.sentence-stamp,.sentence-replay,.block-replay,#restart'))el.disabled=true;setFollowing(false);$('.now').firstElementChild.textContent='Text only';}
function renderSaved(){const target=$('#saved-chunks');if(!target)return;target.innerHTML=learningState.saved.length?learningState.saved.map(x=>'<div class="saved-card"><button data-review-saved="'+esc(x.id)+'"><b>'+esc(x.en)+'</b><span>'+esc(x.zh)+'</span><small>Sentence '+(x.sentence+1)+' · '+fmt(x.start)+'</small></button><button data-remove-saved="'+esc(x.id)+'" aria-label="Remove '+esc(x.en)+'">×</button></div>').join(''):'<p class="empty-saved">No saved chunks yet. Long-press or right-click an English chunk to save it.</p>';}
function contextFor(target){const block=target.closest('[data-leaf]');if(block){const l=allLeaves.find(x=>x.id===block.dataset.leaf);if(l)return {id:l.id,en:l.en,zh:l.zh,sentence:l.sentence,start:l.start||0,end:l.end||0};}return null;}
function showContext(target){const c=contextFor(target);if(!c)return;menuChunk=c;$('#chunk-title').textContent=c.en;$('#chunk-menu').hidden=false;$('#save-chunk').textContent=learningState.saved.some(x=>x.id===c.id)?'Saved':'Save for review';}
viewer.addEventListener('contextmenu',e=>{if(contextFor(e.target)){e.preventDefault();showContext(e.target)}});
viewer.addEventListener('keydown',e=>{if(e.key==='F10'&&e.shiftKey){e.preventDefault();showContext(e.target)}});
let holdTimer,suppressTap=false;
viewer.addEventListener('touchstart',e=>{clearTimeout(holdTimer);const target=e.target;holdTimer=setTimeout(()=>{if(contextFor(target)){suppressTap=Date.now()+900;showContext(target)}},550)},{passive:true});
for(const event of ['touchend','touchcancel','touchmove'])viewer.addEventListener(event,()=>clearTimeout(holdTimer),{passive:true});
document.addEventListener('keydown',e=>{if(e.key==='Escape')$('#chunk-menu').hidden=true});
$('#save-chunk').onclick=()=>{if(!menuChunk)return;if(!learningState.saved.some(x=>x.id===menuChunk.id))learningState.saved.push({...menuChunk,at:Date.now()});scheduleSave();renderSaved();$('#chunk-menu').hidden=true;toast('Saved. Find it in the lesson menu.');};
$('#close-chunk-menu').onclick=()=>$('#chunk-menu').hidden=true;
$('#saved-chunks').onclick=e=>{const remove=e.target.closest('[data-remove-saved]');if(remove){learningState.saved=learningState.saved.filter(x=>x.id!==remove.dataset.removeSaved);scheduleSave();renderSaved();return}const btn=e.target.closest('[data-review-saved]');if(btn){const item=learningState.saved.find(x=>x.id===btn.dataset.reviewSaved);$('#sheet').hidden=true;if(item&&HAS_AUDIO)replayRange(item.start,item.end,item.en);else if(item){const el=leafMap.get(item.id);setFollowing(false);el?.scrollIntoView({block:'center'});}}};
audio.addEventListener('timeupdate',()=>{if(stateReady){learningState.position=audio.currentTime;scheduleSave()}});
audio.addEventListener('pause',()=>{if(stateReady){learningState.position=audio.currentTime;persist()}});
window.addEventListener('pagehide',()=>{if(stateReady){learningState.position=audio.currentTime;persist()}});
restore();
