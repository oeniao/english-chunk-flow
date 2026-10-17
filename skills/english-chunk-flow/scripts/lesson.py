#!/usr/bin/env python3
"""Host-annotated learning packages; local speech/alignment, never synthetic timestamps."""
import argparse, threading, copy, hashlib, html, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, time, wave, zipfile
from pathlib import Path
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
ROLES=set('svobacke')
LOCALES={'zh-CN','ja','ko','ar','es','pt','de','ru','en'}
LANGUAGE_ALIASES={
 'zh-CN':['中文','汉语','简体中文','Chinese','zh'],
 'ja':['日语','日文','日本语','日本語','Japanese','ja-JP'],
 'ko':['韩语','韩文','韩国语','한국어','Korean','ko-KR'],
 'ar':['阿拉伯语','阿语','العربية','Arabic'],
 'es':['西班牙语','西语','español','Spanish','es-ES'],
 'pt':['葡萄牙语','葡语','português','Portuguese','pt-BR','pt-PT'],
 'de':['德语','德文','Deutsch','German','de-DE'],
 'ru':['俄语','俄文','русский','Russian','ru-RU'],
 'en':['英语','英文','英语解释','English','en-US','en-GB']}
def normalize_locale(value):
 if not isinstance(value,str):raise Error('Explanation language must be a string')
 key=value.strip().replace('_','-').casefold()
 for locale,aliases in LANGUAGE_ALIASES.items():
  if key in [x.casefold() for x in [locale,*aliases]]:return locale
 raise Error('Unsupported explanation language. Choose 中文/日本語/한국어/العربية/español/português/Deutsch/русский/English.')
WORDS=re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*|\d+(?:[.,]\d+)*")
def norm(s):return ' '.join(s.split())
def spoken(s):return [m.group().lower().replace('’',"'") for m in WORDS.finditer(s)]
def save(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def run(args):subprocess.run([str(a) for a in args],check=True,stdout=subprocess.DEVNULL)
class Error(Exception):pass
class Reader(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','nav','footer','header'):self.skip+=1
  elif not self.skip and t in ('p','div','br','h1','h2','h3','li','article'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','nav','footer','header'):self.skip=max(0,self.skip-1)
  elif not self.skip and t in ('p','div','li','h1','h2','h3'):self.parts.append('\n')
 def handle_data(self,s):
  if not self.skip:self.parts.append(s)
def extract(path):
 p=Path(path);suffix=p.suffix.lower()
 if suffix=='.docx':
  import xml.etree.ElementTree as ET
  with zipfile.ZipFile(p) as z:
   if z.getinfo('word/document.xml').file_size>20_000_000:raise Error('DOCX body too large')
   root=ET.fromstring(z.read('word/document.xml'))
  ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  return '\n'.join(''.join(t.text or '' for t in para.findall('.//w:t',ns)) for para in root.findall('.//w:p',ns))
 if suffix=='.pdf':raise Error('PDF extraction/OCR not bundled. Provide a checked text transcript; do not fabricate it.')
 if suffix not in ('.txt','.md','.html','.htm','.srt','.vtt'):raise Error('Unsupported text input. Use TXT, MD, HTML, DOCX, SRT or VTT.')
 s=p.read_text(encoding='utf-8-sig')
 if suffix in ('.html','.htm'):
  r=Reader();r.feed(s);s=''.join(r.parts)
 if suffix in ('.srt','.vtt'):
  lines=[]
  for block in re.split(r'\n\s*\n',s.replace('\r','')):
   raw=block.splitlines()
   if not any('-->' in l for l in raw):continue
   start=next(i for i,l in enumerate(raw) if '-->' in l)+1
   text=html.unescape(re.sub('<[^>]+>','', ' '.join(raw[start:]))).strip()
   if text and (not lines or lines[-1]!=text):lines.append(text)
  s='\n'.join(lines)
 s=re.sub(r'[ \t]+',' ',s);s=re.sub(r'\n{3,}','\n\n',s).strip()
 if not s:raise Error('No readable English text extracted.')
 return s

def prepare(source,annotation):
 if len(source)>200_000:raise Error('Source exceeds v0.1 text limit (200k characters). Split into lessons.')
 a=copy.deepcopy(annotation)
 if not isinstance(a,dict) or not isinstance(a.get('sentences'),list) or not a['sentences']:raise Error('annotation.sentences must be a nonempty array')
 a['locale']=normalize_locale(a.get('locale','zh-CN'))
 if norm(' '.join(s.get('text','') for s in a['sentences']))!=norm(source):raise Error('Sentence text differs from source (including punctuation/case); no silent rewrite allowed.')
 counter=0;depthmax=0
 for i,s in enumerate(a['sentences']):
  leaves=[]
  def visit(p,depth=0):
   nonlocal counter,depthmax
   depthmax=max(depthmax,depth)
   if depth>5:raise Error('Too many nesting levels; simplify for backbone comprehension.')
   if not isinstance(p,dict) or p.get('role') not in ROLES:raise Error('Invalid grammar role')
   if not isinstance(p.get('en'),str) or not p['en'].strip():raise Error('Every chunk needs English text')
   if not isinstance(p.get('zh'),str) or not p['zh'].strip():raise Error('Every chunk needs a contextual meaning in the selected language')
   counter+=1;p['id']=f's{i+1}p{counter}'
   p.pop('headId',None)
   if 'children' in p:
    if not isinstance(p['children'],list) or not p['children']:raise Error('children must be nonempty')
    if not p.get('containerOnly'):
     p['headId']=p['id']+'h';leaves.append({'id':p['headId'],'en':p['en'],'role':p['role'],'zh':p['zh']})
    before=len(leaves)
    for c in p['children']:visit(c,depth+1)
    if p.get('containerOnly') and norm(p['en'])!=norm(' '.join(l['en'] for l in leaves[before:])):raise Error('Container label English must equal its child span; do not repeat or invent words.')
   else:
    if p.get('containerOnly'):raise Error('containerOnly requires children')
    leaves.append({'id':p['id'],'en':p['en'],'role':p['role'],'zh':p['zh']})
  if not isinstance(s.get('parts'),list) or not s['parts']:raise Error('Every sentence needs parts')
  for p in s['parts']:visit(p)
  if norm(' '.join(l['en'] for l in leaves))!=norm(s['text']):raise Error(f'Sentence {i+1}: leaves omit/repeat/reorder source text.')
  if not spoken(s['text']):raise Error('Sentence contains no supported spoken words')
  s.update(id=f's{i+1}',index=i+1,leaves=leaves,chapter=s.get('chapter','Listening practice'))
 return a,{'sentences':len(a['sentences']),'leaves':sum(len(s['leaves']) for s in a['sentences']),'words':len(spoken(source)),'max_nesting':depthmax}

def wav_info(p):
 try:
  with wave.open(str(p),'rb') as w:
   if w.getnframes()==0:raise Error('Audio is empty. macOS say may require access to the local speech service; do not package silence.')
   return w.getparams(),w.getnframes()/w.getframerate()
 except (wave.Error,EOFError) as e:raise Error('Unreadable PCM WAV: '+str(e))
def decode(src,dest):
 if not Path(src).is_file():raise Error('Original audio file does not exist')
 try:
  params,dur=wav_info(src)
  if params.nchannels==1 and params.sampwidth==2 and params.framerate==16000:
   shutil.copyfile(src,dest);return dur
 except (Error,OSError):pass
 if shutil.which('afconvert'):run(['afconvert','-f','WAVE','-d','LEI16@16000','-c','1',src,dest])
 elif shutil.which('ffmpeg'):run(['ffmpeg','-y','-i',src,'-ac','1','-ar','16000','-c:a','pcm_s16le',dest])
 else:raise Error('Need 16kHz mono PCM16 WAV, or afconvert/ffmpeg installed for local decoding.')
 return wav_info(dest)[1]
def align(path,text,check_match=False,allow_mismatch=False):
 try:from pocketsphinx import Decoder
 except ImportError:raise Error('Local acoustic aligner missing. Install scripts/requirements.txt in your venv, provide real --word-times, or use --text-only.')
 with wave.open(str(path),'rb') as w:raw=w.readframes(w.getnframes());dur=w.getnframes()/w.getframerate()
 words=spoken(text)
 if any(re.search(r'\d',w) for w in words):raise Error('Digit normalization requires verified word times; write generated content with spoken number words, or provide --word-times for the original transcript.')
 d=Decoder(lm=None,samprate=16000,loglevel='ERROR')
 missing=sorted(set(w for w in words if not d.lookup_word(w)))
 if missing:raise Error('Pronunciation dictionary lacks: '+', '.join(missing)+'. Use a supported aligner or verified word timings; no proportional fallback.')
 warnings=[];recognition=None;ratio=None
 if check_match:
  import difflib
  r=Decoder(samprate=16000,loglevel='ERROR');r.start_utt();r.process_raw(raw,False,True);r.end_utt();recognition=r.hyp().hypstr if r.hyp() else ''
  ratio=difflib.SequenceMatcher(None,words,spoken(recognition),autojunk=False).ratio()
  if ratio<.35 and not allow_mismatch:raise Error(f'Possible wrong transcript/audio version (local recognition agreement {ratio:.2f}). Verify the recording and transcript; do not force an incorrect alignment.')
  warnings.append(f'Original transcript needs human verification; weak local ASR agreement={ratio:.2f}, not an accuracy certificate.')
  if ratio<.35:warnings.append('Mismatch guard explicitly overridden; verify original text/audio before learning.')
 d.set_align_text(' '.join(words));d.start_utt();d.process_raw(raw,False,True);d.end_utt()
 segments=list(d.seg() or [])
 result=[]
 for x in segments:
  word=re.sub(r'\(\d+\)$','',x.word)
  if word.startswith('<'):continue
  result.append({'word':word,'start':round(x.start_frame/100,3),'end':round(min(dur,(x.end_frame+1)/100),3)})
 if [x['word'] for x in result]!=words:raise Error('Aligner did not cover every spoken word. Refusing a partial timeline.')
 return {'words':result,'duration':dur,'provenance':'pocketsphinx-5.1.1-acoustic-alignment','warnings':warnings,'recognition_agreement':ratio}
def validate_times(t,text,duration):
 if not isinstance(t,dict) or not t.get('provenance'):raise Error('Word timing provenance is required')
 if abs(float(t.get('duration',-1))-duration)>.15:raise Error('Timing duration does not match audio')
 ws=t.get('words',[])
 if [str(x.get('word','')).lower().replace('’',"'") for x in ws]!=spoken(text):raise Error('Word timings do not cover the complete transcript in order')
 last=0
 for w in ws:
  start=float(w['start']);end=float(w['end'])
  if not (0<=start<end<=duration+.02) or start<last-.021:raise Error('Invalid/nonmonotonic word timing')
  if end-start>3:raise Error('Suspicious word longer than three seconds. Check audio/text alignment.')
  last=end
 return ws

def make_audio(a,out,voice,rate,audio_path,word_times,allow_mismatch):
 text=' '.join(s['text'] for s in a['sentences']);audio=out/'audio.wav'
 if audio_path:
  dur=decode(audio_path,audio)
  times=json.loads(Path(word_times).read_text()) if word_times else align(audio,text,True,allow_mismatch)
  validate_times(times,text,dur)
  return times,{'kind':'original','voice':'Original recording','source_filename':Path(audio_path).name,'duration':dur}
 if not shutil.which('say') or not shutil.which('afconvert'):raise Error('Local say speech needs macOS. Provide audio/timings or --text-only on other hosts.')
 if word_times:raise Error('--word-times is only for original supplied audio')
 allwords=[];offset=0
 with tempfile.TemporaryDirectory(prefix='chunk-speech-') as temp:
  temp=Path(temp)
  with wave.open(str(audio),'wb') as output:
   output.setnchannels(1);output.setsampwidth(2);output.setframerate(16000)
   for i,s in enumerate(a['sentences']):
    f=temp/'sentence.txt';f.write_text(s['text']);aiff=temp/'sentence.aiff';wav=temp/'sentence.wav'
    run(['say','-v',voice,'-r',rate,'-f',f,'-o',aiff]);run(['afconvert','-f','WAVE','-d','LEI16@16000','-c','1',aiff,wav])
    dur=wav_info(wav)[1];t=align(wav,s['text']);validate_times(t,s['text'],dur)
    allwords.extend(dict(w,start=round(w['start']+offset,4),end=round(w['end']+offset,4)) for w in t['words'])
    with wave.open(str(wav),'rb') as part:output.writeframes(part.readframes(part.getnframes()))
    offset+=dur
    print(f'Synthesized and acoustically aligned sentence {i+1}/{len(a["sentences"])}',flush=True)
 return {'words':allwords,'duration':offset,'provenance':'pocketsphinx-5.1.1-acoustic-alignment','warnings':['Local acoustic estimates; verify replay edges. This is system synthesized speech, not authenticated regional accent.']},{'kind':'synthesized','voice':voice,'rate':rate,'duration':offset}

def attach(a,t):
 ws=t['words'];cursor=0
 for s in a['sentences']:
  sentence_start=cursor
  for l in s['leaves']:
   n=len(spoken(l['en']))
   if not n:raise Error('Punctuation-only chunk cannot be replayed independently')
   l['start']=ws[cursor]['start'];l['end']=ws[cursor+n-1]['end'];cursor+=n
  s['start']=ws[sentence_start]['start'];s['end']=ws[cursor-1]['end'];s['duration']=s['end']-s['start']
 # Sentence navigation covers any inter-sentence silence, while chunks keep actual word bounds.
 for i,s in enumerate(a['sentences']):
  s['start']=0 if i==0 else s['start'];s['end']=a['sentences'][i+1]['start'] if i+1<len(a['sentences']) else t['duration'];s['duration']=s['end']-s['start']
 if cursor!=len(ws):raise Error('Unconsumed alignment words')

def build(args):
 source=Path(args.source).read_text(encoding='utf-8-sig');a,stats=prepare(source,json.loads(Path(args.annotation).read_text()))
 out=Path(args.out).resolve()
 if out.exists() and any(out.iterdir()) and not args.replace:raise Error('Output directory is not empty. Use another folder or explicitly --replace.')
 # Work in sibling staging folder; no half-published player on pipeline failure.
 out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='.chunk-build-',dir=out.parent) as temp:
  stage=Path(temp);warnings=[]
  if args.text_only:
   media={'kind':'none','duration':0};times=None
   for s in a['sentences']:s.update(start=0,end=0,duration=0)
   warnings=['Text-only lesson: no audio or word timing; replay is disabled.']
  else:
   times,media=make_audio(a,stage,args.voice,args.rate,args.audio,args.word_times,args.allow_mismatch);attach(a,times);warnings=times.get('warnings',[])
  media_fingerprint=hashlib.sha256((stage/'audio.wav').read_bytes()).hexdigest() if times else ''
  identity=hashlib.sha256((json.dumps(a,sort_keys=True,ensure_ascii=False)+media_fingerprint+norm(source)+a.get('locale','zh-CN')+json.dumps(media,sort_keys=True)).encode()).hexdigest()[:20]
  manifest={'schema_version':1,'id':identity,'title':a.get('title','Listening practice'),'subtitle':a.get('subtitle',''),'locale':a.get('locale','zh-CN'),'source_type':a.get('source_type','audio_transcript' if args.audio else 'text'),'source_url':a.get('source_url',''),'media':media,'alignment':times['provenance'] if times else 'none','warnings':warnings,'stats':stats,'annotation_method':'host-assistant-linguistic-analysis','created_at':time.strftime('%Y-%m-%dT%H:%M:%S%z')}
  (stage/'source.txt').write_text(source);save(stage/'annotation.json',a);save(stage/'manifest.json',manifest);save(stage/'content.json',a['sentences'])
  if times:save(stage/'word-times.json',times)
  for name in ('style.css','app.js','index.html'):shutil.copy(ROOT/'assets'/'player'/name,stage/name)
  # Escape HTML-sensitive characters before embedding JSON in script elements.
  j=lambda obj:json.dumps(obj,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
  content='const MATERIAL='+j(manifest)+';\nconst NEWS='+j(a['sentences'])+';'
  (stage/'content.js').write_text(content)
  template=(stage/'index.html').read_text().replace('style.css?v=core2','style.css').replace('app.js?v=core2','app.js')
  if not times:template=template.replace('src="audio.wav"','')
  (stage/'index.html').write_text(template)
  portable=template.replace('<link rel="stylesheet" href="style.css">','<style>'+(stage/'style.css').read_text()+'</style>').replace('<script src="content.js"></script>','<script>'+content+'</script>').replace('<script src="app.js"></script>','<script>'+(stage/'app.js').read_text()+'</script>')
  if times:
   import base64
   portable=portable.replace('src="audio.wav"','src="data:audio/wav;base64,'+base64.b64encode((stage/'audio.wav').read_bytes()).decode()+'"')
  else:portable=portable.replace('src="audio.wav"','')
  (stage/'lesson.html').write_text(portable)
  if out.exists():
   if args.replace:
    # Replace generated files only; preserve user state and unrelated documents.
    for f in ('audio.wav','word-times.json'):
     if (out/f).exists() and not (stage/f).exists():(out/f).unlink()
  else:out.mkdir()
  for f in stage.iterdir():shutil.copyfile(f,out/f.name)
 print(json.dumps({'status':'built','path':str(out),'player':str(out/'lesson.html'),'manifest':manifest},ensure_ascii=False))

def serve(args):
 root=Path(args.root).resolve()
 if not (root/'manifest.json').exists():raise Error('serve root must be a built lesson directory')
 state_lock=threading.Lock()
 class Handler(SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw):super().__init__(*a,directory=str(root),**kw)
  def do_GET(self):
   if urlparse(self.path).path=='/api/state':
    try:body=(root/'state.json').read_bytes()
    except FileNotFoundError:body=b'{}'
    self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
   return super().do_GET()
  def do_POST(self):
   if self.path!='/api/state':self.send_error(404);return
   if self.headers.get('Sec-Fetch-Site')=='cross-site':self.send_error(403);return
   origin=self.headers.get('Origin')
   if origin and origin!=f'http://{self.headers.get("Host")}':self.send_error(403);return
   if self.headers.get('Content-Type','').split(';')[0]!='application/json':self.send_error(415);return
   try:n=int(self.headers.get('Content-Length','0'))
   except ValueError:self.send_error(400);return
   if not 0<n<200_000:self.send_error(413);return
   try:
    obj=json.loads(self.rfile.read(n));manifest=json.loads((root/'manifest.json').read_text())
    if not isinstance(obj,dict) or obj.get('materialId')!=manifest['id']:raise ValueError()
    with state_lock:
     f=root/'state.json.tmp';save(f,obj);os.replace(f,root/'state.json')
   except (ValueError,TypeError):self.send_error(400);return
   self.send_response(204);self.end_headers()
  def send_head(self):
   path=Path(self.translate_path(self.path))
   if path.is_file() and path.suffix=='.wav':
    size=path.stat().st_size;start=0;end=size-1;r=self.headers.get('Range','')
    if r:
     m=re.fullmatch(r'bytes=(\d+)-(\d*)',r)
     if not m:self.send_error(416);return None
     start=int(m[1]);end=min(size-1,int(m[2]) if m[2] else size-1)
     if start>=size or start>end:self.send_error(416);return None
    self.send_response(206 if r else 200);self.send_header('Content-Type','audio/wav');self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1))
    if r:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
    self.end_headers();f=path.open('rb');f.seek(start);self.remaining=end-start+1;return f
   return super().send_head()
  def copyfile(self,s,o):
   n=getattr(self,'remaining',None)
   if n is None:return super().copyfile(s,o)
   while n:
    data=s.read(min(65536,n))
    if not data:break
    o.write(data);n-=len(data)
 print(f'PLAYER_URL=http://127.0.0.1:{args.port}/index.html',flush=True);ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 sub.add_parser('doctor')
 e=sub.add_parser('extract');e.add_argument('--input',required=True);e.add_argument('--out',required=True)
 for command in ('validate','build'):
  b=sub.add_parser(command);b.add_argument('--source',required=True);b.add_argument('--annotation',required=True)
  if command=='build':
   b.add_argument('--out',required=True);b.add_argument('--tts',choices=['say'],default='say');b.add_argument('--voice',default='Samantha');b.add_argument('--rate',type=int,default=130);b.add_argument('--audio');b.add_argument('--word-times');b.add_argument('--text-only',action='store_true');b.add_argument('--replace',action='store_true');b.add_argument('--allow-mismatch',action='store_true')
 s=sub.add_parser('serve');s.add_argument('--root',required=True);s.add_argument('--port',type=int,default=8770)
 a=p.parse_args()
 try:
  if a.command=='doctor':print(json.dumps({'python':sys.executable,'speech_say':shutil.which('say'),'decoder_afconvert':shutil.which('afconvert'),'decoder_ffmpeg':shutil.which('ffmpeg'),'acoustic_aligner':bool(importlib.util.find_spec('pocketsphinx')),'supported_inputs':['text','html','docx','srt','vtt','audio+transcript','host-generated topic'],'not_bundled':['ASR-only','PDF/OCR','YouTube extraction','premium TTS APIs']},ensure_ascii=False))
  elif a.command=='extract':Path(a.out).write_text(extract(a.input));print(a.out)
  elif a.command=='validate':print(json.dumps(prepare(Path(a.source).read_text(),json.loads(Path(a.annotation).read_text()))[1]))
  elif a.command=='build':
   if a.text_only and (a.audio or a.word_times):raise Error('--text-only cannot be combined with audio/timing inputs')
   if not 80<=a.rate<=240:raise Error('Speech rate must be between 80 and 240')
   build(a)
  elif a.command=='serve':serve(a)
 except (Error,ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:
  print(json.dumps({'status':'error','message':str(e)},ensure_ascii=False),file=sys.stderr);return 2
 return 0
if __name__=='__main__':sys.exit(main())
