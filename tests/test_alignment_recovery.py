"""Failure-injection tests distinguish known sentence bounds from word alignment."""
import importlib.util,json,tempfile,unittest,wave
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('recovery_lesson',ROOT/'skills/english-chunk-flow/scripts/lesson.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RecoveryTests(unittest.TestCase):
 def pcm(self,path):
  with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\0\0'*16000)
 def fake_run(self,args):
  if args[0]=='ffmpeg':self.assertEqual(args[1:3],['-v','error']);self.pcm(args[-1])
 def test_failed_sentence_preserves_later_sentences_and_disables_chunk_bounds(self):
  a,_=m.prepare('Hello. World. Again.',{'sentences':[{'text':t,'parts':[{'role':'k','en':t,'zh':'含义'}]} for t in ['Hello.','World.','Again.']]})
  def align(path,text):
   if text=='World.':raise m.Error('Aligner did not cover every spoken word')
   return {'words':[{'word':text.lower().strip('.'),'start':0.1,'end':0.8}],'duration':1,'provenance':'test-fixture'}
  with tempfile.TemporaryDirectory() as t,patch.object(m,'speech_backend',return_value='espeak-ng'),patch.object(m,'run',side_effect=self.fake_run),patch.object(m,'align',side_effect=align):
   times,media=m.make_audio(a,Path(t),None,130,None,None,False)
   m.attach(a,times)
   self.assertEqual(media['duration'],3);self.assertEqual([s['timing_quality'] for s in a['sentences']],['word','sentence','word'])
   self.assertAlmostEqual(a['sentences'][2]['leaves'][0]['start'],2.1)
   self.assertEqual(a['sentences'][1]['leaves'][0]['timing_quality'],'sentence')
   self.assertEqual([w['word'] for w in times['words']],['hello','again'])
   self.assertIn('chunk replay disabled',times['warnings'][0])
 def test_strict_failure_retains_cache_and_retry_does_not_synthesize(self):
  a={'sentences':[{'text':'Hello.'},{'text':'World.'}]}
  with tempfile.TemporaryDirectory() as t,patch.object(m,'speech_backend',return_value='espeak-ng'),patch.object(m,'run',side_effect=self.fake_run) as run,patch.object(m,'align',side_effect=m.Error('partial timeline')):
   root=Path(t);cache=root/'cache'
   with self.assertRaises(m.Error):m.make_audio(a,root,None,130,None,None,False,alignment_failure='strict',cache_dir=cache)
   self.assertEqual(len(list(cache.glob('*.wav'))),2);self.assertEqual(len(json.loads((cache/'failures.json').read_text())['failures']),2)
   run.reset_mock()
   times,_=m.make_audio(a,root,None,130,None,None,False,cache_dir=cache)
   run.assert_not_called();self.assertEqual(len(times['sentences']),2);self.assertFalse((cache/'failures.json').exists())
 def test_custom_pronunciation_validation(self):
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'phones.json';path.write_text(json.dumps({'anthropic':'AE N TH R AA P IH K'}))
   self.assertEqual(m.load_pronunciations(path)['anthropic'],'AE N TH R AA P IH K')
   path.write_text(json.dumps({'anthropic':'invented phones'}))
   with self.assertRaises(m.Error):m.load_pronunciations(path)
 def test_portable_file_inlines_versioned_assets(self):
  with tempfile.TemporaryDirectory() as t:
   import subprocess,sys
   out=Path(t)/'lesson'
   subprocess.run([sys.executable,str(ROOT/'skills/english-chunk-flow/scripts/lesson.py'),'build','--source',str(ROOT/'examples/workday/source.txt'),'--annotation',str(ROOT/'examples/workday/annotation.json'),'--out',str(out),'--text-only'],check=True,capture_output=True)
   portable=(out/'lesson.html').read_text()
   self.assertNotIn('src="app.js',portable);self.assertNotIn('href="style.css',portable);self.assertIn('function exportSentence',portable)
if __name__=='__main__':unittest.main()
