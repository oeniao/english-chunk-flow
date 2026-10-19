# English Chunk Flow · Agent Skill

**An open-source Agent Skill for learning English through chunks.**

*Hear the words. Follow the structure.*

Install the skill in your AI assistant and invoke **`$english-chunk-flow`** with your English material or a topic. The assistant uses the skill to prepare sentence-level grammar chunks, contextual translations and a playable listening lesson. Includes installation guidance for WorkBuddy, Grok Build and Claude, plus macOS and Linux runtime paths. See [host compatibility](skills/english-chunk-flow/references/hosts.md) for requirements and verification limits.

**The skill is the entry point; the bundled player is the learning interface it generates.**

[![Core tests](https://img.shields.io/badge/tests-24_passed_locally-green.svg)](docs/TESTING.md) [![MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

English · [简体中文](docs/i18n/README.zh-CN.md) · [日本語](docs/i18n/README.ja.md) · [한국어](docs/i18n/README.ko.md) · [العربية](docs/i18n/README.ar.md) · [Español](docs/i18n/README.es.md) · [Português](docs/i18n/README.pt.md) · [Deutsch](docs/i18n/README.de.md) · [Русский](docs/i18n/README.ru.md)

## Latest player demo · 2026-10-19

[![Watch the latest player with complete English and Chinese sentence scripts](docs/images/player.png)](https://github.com/oeniao/english-chunk-flow/raw/refs/heads/main/docs/images/workday-demo.mp4)

**[Watch or download the complete workday example · MP4 · 27 seconds](https://github.com/oeniao/english-chunk-flow/raw/refs/heads/main/docs/images/workday-demo.mp4)**

Latest tested UI: complete English sentence and selected-language translation above the colored grammar chunks, one translation toggle, adaptive reading layout, and sentence export. This six-sentence, 85-word original example uses macOS Samantha synthesized speech and PocketSphinx word alignment; actual audio duration is 26.70 seconds. This recording does not demonstrate Linux speech reliability.

[Earlier full-length news demo · MP4 · 4:58](https://github.com/oeniao/english-chunk-flow/releases/download/v0.1.0/musk-roadster-full-lesson.mp4)

## Why this exists

Knowing the words is not always enough to understand spoken English. This project helps learners catch **who/what + action/state + object/complement**, then connect clauses and modifiers without losing the flow of audio.

This skill is an early alpha with bundled local processing tools and a lesson player. The host assistant performs linguistic analysis and translation; the Python tools validate and package that work. This is **not** a standalone automatic parser, a new trained language model or a complete desktop learning manager. Learning benefits remain a hypothesis to test with learners; no efficacy claim is made.

## What you can do

- Bring English text, TXT/MD/HTML/DOCX/SRT/VTT, or **original audio plus a checked transcript**.
- Ask the host assistant to write original practice material from a topic and level.
- Read sentence units while captions scroll continuously. Role colors and nested backgrounds show ownership; long clauses reveal local structure and long phrases can expose core chunks.
- Use Chinese, Japanese, Korean, Arabic, Spanish, Portuguese, German or Russian meanings, or English explanations. **Product controls remain English.** A lesson has one explanation language; multiple languages are separate versions.
- Switch between **Structure** and **Bilingual script** views, with an independent translation toggle. Adaptive tablet/desktop layouts use a wider reading area and larger text, with a responsive phone layout.
- **Copy & export** on each sentence copies English, translation and syntax as text and downloads a standalone HTML file containing colored, nested grammar chunks and the embedded sentence audio clip. Text-only lessons explicitly omit audio.
- Tap a chunk or its subtle replay icon. Parent blocks replay their entire span. The sentence replay icon stops after that sentence; the left timestamp continues the lesson.
- Save a difficult chunk via right-click, long-press or Shift+F10. Review it in **Lesson menu → Saved chunks**. Position, intentional replays and saved chunks persist locally where storage is available.
- Generate a local player folder and an offline single HTML file with embedded audio. The last timeline node shows the actual end time, a check and **Finished listening**.

| Input | Current implementation |
| --- | --- |
| Text / original topic | Host annotation, macOS or Linux speech and acoustic alignment |
| Audio + transcript | Retain original recording, local decode/alignment, mismatch guard |
| SRT/VTT | Extract and rejoin into sentences; cue boundaries are not grammar boundaries |
| Article link | Host browser retrieves readable text; CLI does not fetch URLs |
| YouTube link / audio alone / scanned PDF | No bundled extraction, transcription or OCR backend |

## Requirements

- A host assistant that can load `SKILL.md` and execute local tools; tested in the Codex desktop environment.
- Python 3.10+ for extraction, validation and packaging.
- Local synthesis: **macOS** with `say` + `afconvert`, or **Linux** with `espeak-ng` + `ffmpeg`. `--tts auto` detects an available backend; voices default to `Samantha` / `en-us` respectively.
- Optional PocketSphinx **5.1.1** for acoustic alignment. Setup installs dependencies from PyPI into a skill-local virtual environment.

No additional text-model API key is needed when the host assistant generates the annotations. Your host model/account may still incur its normal costs. Local file processing does not mean the assistant itself runs offline. The project bundles no premium speech API, voice model download or verified US/UK/Australian accent selector.

## Install the skill

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
```

The installer copies only the skill into `~/.agents/skills/english-chunk-flow` and refuses to overwrite an existing installation. To use another location supported by your host, pass `--dest /absolute/skill/directory`. Local skill discovery locations are described in [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills).

Host-specific installation (the default above remains `~/.agents/skills`):

```sh
python3 scripts/install.py --host claude
python3 scripts/install.py --host grok
python3 scripts/install.py --host workbuddy --project /absolute/workspace
```

For WorkBuddy personal installation, use its **Add skill → Upload skill** UI with the ZIP. Claude chat supports custom skill import where enabled. Grok Build discovery is supported; ordinary Grok chat requires actual file/code tools. See [host instructions](skills/english-chunk-flow/references/hosts.md).

On Debian/Ubuntu install `python3-venv espeak-ng ffmpeg` through your package manager, then run the isolated setup below. See [Linux audio setup](skills/english-chunk-flow/references/audio.md#linux-local-speech). No operating-system packages are installed by the skill installer.

Optional local alignment setup:

```sh
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

Open a new host conversation or refresh skill discovery, then invoke **`$english-chunk-flow`**. The ZIP in GitHub Releases is a portable skill folder, not a macOS application or a one-click ChatGPT mobile extension. Its runtime is not bundled.

## Use the skill

> Use $english-chunk-flow to turn my English article into a listening lesson. Keep the original English and explain each grammar chunk in Japanese.

> Use $english-chunk-flow with this recording and checked transcript. Keep the original audio, use Chinese explanations, and open the player.

> Use $english-chunk-flow to write an approximately five-minute English lesson about working from home. Use mostly familiar vocabulary and Korean explanations. Check the actual audio duration.

> Use $english-chunk-flow to reopen my previous lesson and review my saved chunks.

The agent creates source and annotation files; **the CLI does not translate or parse arbitrary text on its own**. See [annotation contract](skills/english-chunk-flow/references/annotation.md).

## Run the included example

From the repository root, use the installed runtime if needed:

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts auto
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

Open `http://127.0.0.1:8770/index.html`. `output/workday/lesson.html` is the portable version. On hosts without speech support, use `--text-only` and a separate output directory; no sound or fabricated timing is generated. See [examples](examples/README.md) for the Japanese variant.

## Accuracy and limitations

- Structural validation guarantees source coverage and schema consistency, **not** correct grammar or translation. Review the backbone, negation and attachment before delivery.
- eSpeak/PocketSphinx can miss sentence-final words. By default, affected synthesized sentences retain whole-sentence playback with an explicit timing warning and disabled chunk replay. Use `--alignment-failure strict` to require full word timing. Completed audio is cached for retries; see [recovery and pronunciation setup](skills/english-chunk-flow/references/audio.md#alignment-failures-sentence-playback-and-retry).
- Acoustic boundaries are estimates. Dictionary-missing words and unsupported digit normalization fail explicitly; there is no word-count timing fallback.
- Independent local recognition is weak. Its mismatch guard can reject correct recordings and cannot certify a transcript. Investigate rather than bypassing the warning.
- Automatic audio-only transcription, YouTube media extraction, OCR, premium TTS, live translation switching and a full desktop library are **not implemented**.
- No exam-score estimates, CEFR certification or human-voice quality benchmark is provided. Browser storage and offline-file persistence depend on the browser.

## Development and open source

A pinned GitHub Actions workflow is provided as [an opt-in template](docs/ci/ci.yml). Automated Actions are not enabled in the initial publication because the publishing token lacks GitHub’s `workflow` scope. See [CI setup](docs/ci/README.md); the local test results above are not a hosted CI result.

```sh
python3 -m unittest discover -s tests -v
node --check skills/english-chunk-flow/assets/player/app.js
python3 scripts/check_docs.py
python3 scripts/package_skill.py
```

[Architecture](docs/ARCHITECTURE.md) · [Testing](docs/TESTING.md) · [Contributing](CONTRIBUTING.md) · [Security & privacy](SECURITY.md) · [Changelog](CHANGELOG.md) · [Third-party notices](THIRD_PARTY_NOTICES.md)

Code, documentation, original examples and screenshots are released under the **[MIT License](LICENSE)**. Dependencies retain their own licenses. Do not upload private learning material or redistribute source recordings/transcripts you do not have permission to share. Contributions in grammar analysis, translations, timing, accessibility and input adapters are welcome.
