"""Portable routing tests; these do not claim native Linux/vendor-app execution."""
import importlib.util,json,subprocess,sys,tempfile,unittest,wave
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('portable_lesson',ROOT/'skills/english-chunk-flow/scripts/lesson.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PortabilityTests(unittest.TestCase):
 def test_linux_auto_and_missing_dependencies(self):
  for available,expected in [({'espeak-ng','ffmpeg'},'espeak-ng'),({'say','afconvert','espeak-ng','ffmpeg'},'espeak-ng')]:
   with patch.object(m.sys,'platform','linux'),patch.object(m.shutil,'which',side_effect=lambda n:n if n in available else None):
    self.assertEqual(m.speech_backend(),expected)
  with patch.object(m.shutil,'which',return_value=None):
   for requested in ['auto','say','espeak-ng']:
    with self.subTest(requested=requested),self.assertRaises(m.Error):m.speech_backend(requested)
 def test_macos_default_preserved(self):
  with patch.object(m.sys,'platform','darwin'),patch.object(m.shutil,'which',side_effect=lambda n:n):self.assertEqual(m.speech_backend(),'say')
 def test_espeak_pipeline_and_offsets(self):
  commands=[]
  def run(args):
   args=list(map(str,args));commands.append(args)
   if args[0]=='ffmpeg':
    with wave.open(args[-1],'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\0\0'*16000)
  def align(path,text):return {'words':[{'word':text.lower().rstrip('.'),'start':0.1,'end':0.8}],'duration':1,'provenance':'synthetic-test-fixture'}
  with tempfile.TemporaryDirectory() as t,patch.object(m.shutil,'which',side_effect=lambda n:n if n in ['espeak-ng','ffmpeg'] else None),patch.object(m,'run',side_effect=run),patch.object(m,'align',side_effect=align):
   times,media=m.make_audio({'sentences':[{'text':'Hello.'},{'text':'World.'}]},Path(t),None,130,None,None,False,'espeak-ng')
   self.assertEqual(media['backend'],'espeak-ng');self.assertEqual(media['voice'],'en-us');self.assertEqual(media['duration'],2)
   self.assertEqual(times['words'][1]['start'],1.1);self.assertEqual(m.wav_info(Path(t)/'audio.wav')[1],2)
   self.assertEqual([c[0] for c in commands],['espeak-ng','ffmpeg']*2)
   self.assertIn('pcm_s16le',commands[1]);self.assertIn('16000',commands[1])
 def test_host_project_install_and_refuse_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   for host,folder in [('claude','.claude'),('grok','.grok'),('workbuddy','.codebuddy')]:
    cmd=[sys.executable,str(ROOT/'scripts/install.py'),'--host',host,'--project',t]
    self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
    dest=Path(t)/folder/'skills/english-chunk-flow'
    self.assertTrue((dest/'SKILL.md').is_file());self.assertTrue((dest/'references/hosts.md').is_file())
    self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
 def test_original_audio_does_not_require_tts(self):
  with tempfile.TemporaryDirectory() as t,patch.object(m,'speech_backend',side_effect=AssertionError('Must not choose TTS')),patch.object(m,'decode',return_value=1),patch.object(m,'align',return_value={'words':[{'word':'hello','start':0,'end':1}],'duration':1,'provenance':'test-fixture'}):
   _,media=m.make_audio({'sentences':[{'text':'Hello.'}]},Path(t),None,130,'original.wav',None,False)
   self.assertEqual(media['kind'],'original')
if __name__=='__main__':unittest.main()
