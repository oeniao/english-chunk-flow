# Validation

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
node --check skills/english-chunk-flow/assets/player/app.js
python3 scripts/check_docs.py
```

The opt-in CI template validates source coverage/rejection cases, subtitle/document extraction, locale aliases, malformed timing rejection, package generation, no fake audio in text-only output, inline-script escaping, and documentation links. Core tests use no private material, audio download, model key or macOS speech service.

Local development additionally exercised system speech, PocketSphinx alignment, retained PCM, mismatch guards, audio Range requests, atomic state saving and browser playback. These checks are not equivalent to automatic ASR accuracy on authentic exam recordings, multilingual translation certification, a naturalness blind test or a learning-effectiveness study.

Browser checklist: English controls; selected-language grammar meanings; no chunk overflow; play/pause; chunk/group/sentence stop boundaries; left timestamp continues the lesson; saved chunk persists; final timeline ends with actual duration + check + Finished listening. Confirm portable HTML contains actual audio before claiming offline playback. Time-only and text-only variants must not fabricate audio.


## Portability checks

`tests/test_portability.py` covers Linux backend selection and missing dependencies, macOS preference, eSpeak/FFmpeg command routing with synthetic PCM fixtures, sentence audio offsets, original-audio preservation, host installation locations and overwrite refusal. These run locally alongside the core suite (20 tests total); synthesis/alignment are mocked in the portability pipeline test. They are not native Linux or vendor-app end-to-end results.

To exercise real Linux speech after installing dependencies, from the repository root run:

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py doctor
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/linux-workday --tts espeak-ng
```

Check manifest media backend/voice, actual WAV duration, acoustic replay edges and the portable lesson in a browser. This native Linux run has not been performed on the macOS development host. Vendor-app import/invocation must also be checked in each actual product.


## Linux failure recovery regression coverage

The suite now has 24 tests. `test_alignment_recovery.py` injects alignment failures to verify that later sentences continue, word-aligned offsets remain correct, sentence-only timing is explicit, strict failures retain audio for retry, custom pronunciation input is validated, FFmpeg logging is quiet and portable HTML actually inlines versioned assets. These are deterministic failure-path tests, not native Linux speech tests. User testing of eSpeak NG 1.52.0 demonstrated incomplete PocketSphinx coverage on the workday example; the new sentence-only fallback preserves lesson playback but does not establish reliable word alignment.


## Full sentence scripts and refreshed demo (2026-10-19)

Built `examples/workday` with the real macOS `say` / Samantha voice at 130 wpm and PocketSphinx 5.1.1: 6 sentences, 85 words, 48 leaves, 26.6955625 seconds, all six sentences word-aligned. Opened the generated offline `lesson.html` in Chromium and verified complete English and Chinese header scripts, translation visibility without hiding English, Structure / Bilingual script switching, no duplicate header in script mode, no overflow or action overlap at 1280px / 1024px / 390px, and sentence export. Played the entire lesson to completion and captured the screenshot and video shown on the homepage, with the generated audio muxed into the video. Also built Japanese and Arabic text-only examples and verified their header text, locale and shared translation toggle. These runs do not establish native Linux speech reliability.

The portable-file regression now parses inline script elements as HTML and checks each extracted JavaScript body with Node when available, catching accidental closing script tags inside embedded export templates.

Latest refinement retested on the same workday example: small English-only headers, no full header translations, explicit sentence replay focus, normal-playback focus reset, retained bilingual script translation, and 1280px / 1024px / 390px layouts. Screenshot and full video recaptured.


Final header restoration verified against the new 49-sentence, 708-word space-news learning lesson (294.482375 seconds, macOS Samantha, all sentences word-aligned). Online and standalone HTML show no full header script, Bilingual script view remains available, and the latest 40-second real-playback excerpt is recorded from this final layout with its matching synthesized audio. The 24-test suite and JavaScript syntax checks pass.
