import copy,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('lesson',ROOT/'skills/english-chunk-flow/scripts/lesson.py');m=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(m)
class CoreTests(unittest.TestCase):
 def fixture(self,lang='workday'):
  p=ROOT/'examples'/lang;return (p/'source.txt').read_text(),json.loads((p/'annotation.json').read_text())
 def test_original_coverage_and_grammar_backbone(self):
  src,a=self.fixture();b,stats=m.prepare(src,a);self.assertEqual(stats['sentences'],6);self.assertEqual(m.norm(' '.join(l['en'] for s in b['sentences'] for l in s['leaves'])),m.norm(src));self.assertEqual(b['sentences'][4]['parts'][2]['role'],'b')
 def test_dropped_repeated_and_reordered_words_rejected(self):
  src,a=self.fixture()
  for mode in ['drop','repeat','reorder']:
   b=copy.deepcopy(a);parts=b['sentences'][0]['parts']
   if mode=='drop':parts.pop()
   elif mode=='repeat':parts.append(copy.deepcopy(parts[-1]))
   else:parts.reverse()
   with self.subTest(mode=mode),self.assertRaises(m.Error):m.prepare(src,b)
 def test_silent_rewrite_rejected(self):
  src,a=self.fixture()
  with self.assertRaises(m.Error):m.prepare(src.lower(),a)
 def test_bad_role_and_missing_meaning_rejected(self):
  src,a=self.fixture()
  for key,value in [('role','wrong'),('zh','')]:
   b=copy.deepcopy(a);b['sentences'][0]['parts'][0][key]=value
   with self.assertRaises(m.Error):m.prepare(src,b)
 def test_language_alias_keeps_japanese_meanings(self):
  src,a=self.fixture('ja');a['locale']='日本語';b,_=m.prepare(src,a);self.assertEqual(b['locale'],'ja');self.assertEqual(b['sentences'][0]['parts'][0]['zh'],'市議会')
 def test_unsupported_locale_rejected(self):
  with self.assertRaises(m.Error):m.normalize_locale('unsupported')
 def test_subtitle_cues_do_not_define_sentences(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'input.srt';p.write_text('1\n00:00:00,000 --> 00:00:01,000\nThe train\n\n2\n00:00:01,000 --> 00:00:02,000\nis here.\n');self.assertEqual(m.norm(m.extract(p)),'The train is here.')
 def test_html_ignores_script_and_navigation(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'article.html';p.write_text('<nav>Ignore</nav><p>A clear plan.</p><script>bad()</script>');self.assertEqual(m.extract(p),'A clear plan.')
 def test_docx_and_vtt_extraction(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'article.docx'
   with zipfile.ZipFile(p,'w') as z:z.writestr('word/document.xml','<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:t>A clear plan.</w:t></w:r></w:p></w:document>')
   self.assertEqual(m.extract(p),'A clear plan.')
   p=Path(t)/'input.vtt';p.write_text('WEBVTT\n\n00:00.000 --> 00:01.000\nA clear plan.\n');self.assertEqual(m.extract(p),'A clear plan.')
 def test_pdf_failure_is_explicit(self):
  with self.assertRaisesRegex(m.Error,'not bundled'):m.extract('input.pdf')
 def test_invalid_word_times_rejected(self):
  # Synthetic test data for bounds validation, not real acoustic alignment.
  t={'provenance':'unit-test-only','duration':1,'words':[{'word':'hello','start':0,'end':.4},{'word':'world','start':.5,'end':.9}]}
  for mode in ['overlap','missing','duration']:
   a=copy.deepcopy(t)
   if mode=='overlap':a['words'][1]['start']=.1
   elif mode=='missing':a['words'].pop()
   else:a['duration']=4
   with self.subTest(mode=mode),self.assertRaises(m.Error):m.validate_times(a,'Hello world.',1)
 def test_text_only_build_has_no_fake_audio(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'lesson';p=ROOT/'examples/workday'
   subprocess.run([sys.executable,str(ROOT/'skills/english-chunk-flow/scripts/lesson.py'),'build','--source',str(p/'source.txt'),'--annotation',str(p/'annotation.json'),'--out',str(out),'--text-only'],capture_output=True,check=True)
   self.assertFalse((out/'audio.wav').exists());self.assertNotIn('src="audio.wav"',(out/'index.html').read_text());self.assertEqual(json.loads((out/'manifest.json').read_text())['media']['kind'],'none')
 def test_untrusted_text_does_not_close_script(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);src='Read </script> carefully.';a={'title':'</script>','sentences':[{'text':src,'parts':[{'role':'k','en':src,'zh':'Test fixture'}]}]};(p/'source.txt').write_text(src);(p/'annotation.json').write_text(json.dumps(a))
   subprocess.run([sys.executable,str(ROOT/'skills/english-chunk-flow/scripts/lesson.py'),'build','--source',str(p/'source.txt'),'--annotation',str(p/'annotation.json'),'--out',str(p/'out'),'--text-only'],capture_output=True,check=True)
   self.assertNotIn('</script>',(p/'out/content.js').read_text())
 def test_nonempty_output_is_not_overwritten(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'keep').write_text('keep');e=ROOT/'examples/workday'
   r=subprocess.run([sys.executable,str(ROOT/'skills/english-chunk-flow/scripts/lesson.py'),'build','--source',str(e/'source.txt'),'--annotation',str(e/'annotation.json'),'--out',str(p),'--text-only'],capture_output=True)
   self.assertEqual(r.returncode,2);self.assertEqual((p/'keep').read_text(),'keep')
 def test_installer_copies_only_skill(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'skill';subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--dest',str(p)],capture_output=True,check=True);self.assertTrue((p/'SKILL.md').exists());self.assertTrue((p/'LICENSE').exists());self.assertFalse((p/'examples').exists())
   r=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--dest',str(p)],capture_output=True);self.assertNotEqual(r.returncode,0)
if __name__=='__main__':unittest.main()
