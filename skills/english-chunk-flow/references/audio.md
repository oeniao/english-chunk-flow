# Audio and runtime

On macOS `say` + `afconvert` generate the selected installed system voice as a continuous sentence. This is local synthesized speech, not a premium API voice or a claim of authenticated US/GB/AU accent. Default Samantha is only used if present. Use `say -v '?'` to inspect actual installed voices; do not silently substitute another accent.

Optional Python requirement: pocketsphinx==5.1.1. For a fresh installation run `python3 /path/to/english-chunk-flow/scripts/setup.py`; this downloads the dependency from PyPI into the skill’s own `.venv`. Then use `python3 /path/to/english-chunk-flow/scripts/run.py ...`. Install into a user-controlled venv, not the OS Python. `lesson.py doctor` reports availability. Acoustic word alignment uses the packaged English pronunciation dictionary and 16kHz PCM input. Out-of-dictionary words are rejected with the missing terms; don't invent pronunciations, silently drop words, or invent proportional times. Explain alternatives: authorized word timestamps, an aligner with pronunciation support, or text-only output.

Original audio: standard PCM WAV works directly. On macOS, afconvert can decode supported other formats; otherwise an installed ffmpeg can convert locally. No decoder means an actionable error. Raw files are never uploaded by these scripts. Mismatch checks compare independent local recognition against the supplied transcript; this weak English model can flag correct recordings, so warnings require review rather than pretending to certify a match. Clear mismatches are refused. `--allow-mismatch` must only be used after the user explicitly confirms the correct transcript/version; warnings remain in the output.

Timing JSON can be supplied with `--word-times`; it must contain `words:[{word,start,end}]`, `duration`, `provenance`, and cover the complete normalized spoken words. Validate audio duration and monotonicity. The caller is responsible for real provenance; labeling invented times as vendor timestamps is forbidden.

No ASR-only, OCR or arbitrary YouTube extraction backend is bundled in v0.1. Host tools may supply a verified transcript/media, after which the supported paths work. Be explicit about this first-version boundary.

Serve a lesson:

```sh
python3 /path/to/english-chunk-flow/scripts/lesson.py serve --root /abs/lesson --port 8770
```

The listener binds loopback only, supports audio Range reads and a small per-lesson state API. Review state is stored atomically beside the output, using browser localStorage as fallback if the API isn't available (such as opening lesson.html with file://). Key APIs are not included and there is no hosted backend.


## Linux local speech

Python extraction, validation, original-audio processing, packaging and loopback serving are portable. Synthesized audio uses eSpeak NG with FFmpeg normalization to 16kHz mono PCM16, then the same acoustic alignment pipeline. `--tts auto` selects this backend when available; `--tts espeak-ng` requires it explicitly. `--voice` defaults to `en-us` for this backend; inspect installed voices with `espeak-ng --voices=en`. This is intelligible local synthetic speech, not a naturalness or regional-accent guarantee. No speech model or cloud API is downloaded by the build command.

For Debian/Ubuntu (run installation only with the user's authorization):

```sh
sudo apt-get update
sudo apt-get install python3 python3-venv espeak-ng ffmpeg
python3 /path/to/english-chunk-flow/scripts/setup.py
python3 /path/to/english-chunk-flow/scripts/run.py doctor
python3 /path/to/english-chunk-flow/scripts/run.py build --source /abs/source.txt --annotation /abs/annotation.json --out /abs/lesson --tts espeak-ng
```

Other distributions should install equivalent packages through their own package manager. A headless Linux machine needs no audio device for WAV synthesis. Browser audio playback occurs on the learner's device. Missing alignment dependencies still fail explicitly; install PocketSphinx in the isolated venv or supply verified original-audio timings / use text-only. No fabricated timings or silent text-only fallback.
