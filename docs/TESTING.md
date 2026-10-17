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
