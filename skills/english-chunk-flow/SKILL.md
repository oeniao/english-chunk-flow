---
name: english-chunk-flow
description: Turn English text, original audio with a transcript, or a requested topic into a playable listening lesson with sentence-level grammar chunks, contextual translations in Chinese, Japanese, Korean, Arabic, Spanish, Portuguese, German or Russian, replay, and saved difficult segments. Use for English intensive listening and material preparation; not for exam scoring, generic translation alone, or live meeting transcription.
---

# English Chunk Flow

Help the learner hear the sentence backbone and understand ownership of clauses and modifiers. Preserve English order. Use the bundled player; do not redesign it or output only a grammar essay.

## Start

Resolve this skill directory from the loaded SKILL.md path. Use its `scripts/lesson.py` CLI. Run `doctor` once to discover Python, local speech and acoustic alignment capabilities. Read [audio.md](references/audio.md) for one-time runtime setup. Prefer `scripts/run.py`, which uses the skill’s `.venv/bin/python` when installed, otherwise the current Python. Run `python3 scripts/run.py doctor`. Prefer an already configured Python with the optional requirements; otherwise use standard Python for text extraction/validation and explain any missing audio capability.

Read [annotation.md](references/annotation.md) before preparing a new lesson. The host assistant performs linguistic analysis and contextual translation; the CLI validates and packages it. It is not an automatic standalone parser or a privately trained model.

All product UI copy must use English, including navigation, buttons, hints, errors, empty states and accessibility labels. Keep learner-facing translations and grammar-role hints in the selected explanation language.

## Explanation language

Support 中文 (`zh-CN`), 日本語 (`ja`), 한국어 (`ko`), العربية (`ar`), español (`es`), português (`pt`), Deutsch (`de`), русский (`ru`), plus English explanations (`en`). These are language choices, not nationalities. Read [languages.md](references/languages.md) when selecting or changing translations.

Use the user's explicitly requested explanation language; otherwise retain a language already chosen in this conversation, or default to Chinese. State the selected language briefly and proceed; don't repeatedly ask. English source and listening audio stay English. Translate every chunk meaning, complete sentence translation and attachment note consistently into the selected language. Product-facing lesson titles, subtitles and chapter headings use English. Grammar-role labels are localized by the player. The `zh` data field stores the chosen language even when it is Japanese or Korean.

For requests such as “日文翻译” or “用韩语解释”, generate genuine contextual Japanese/Korean meanings, not Chinese text with a changed locale tag. To change an existing lesson, reuse its source, structure and verified audio/timings, retranslate meanings and create a separate language version. Preserve audio provenance; don't mark reused synthesized audio as an original recording. Don't overwrite the user's current lesson or mix progress between versions. If several explanation languages are requested together, deliver separate language versions; the current player does not switch translations live.

## Input routing

- English text/file: run `extract`, preserve the extracted source, annotate it, then `build --tts say` on macOS. If speech is unavailable, use `--text-only`, explicitly deliver a text-only lesson, or use a user-configured speech provider and supply its audio/timings. Do not claim it is playable without audio.
- Original audio + transcript: extract the transcript, annotate, then `build --audio ...`. This preserves the original recording and uses local acoustic alignment when available. Never replace the original with synthesized speech without a separate request. Read [audio.md](references/audio.md).
- A topic: write an original English source at the requested level and approximate duration, then annotate/build. Label it generated learning material. Only call it current news after checking sources. Check actual duration after synthesis; revise text/rate if far from target, not silence padding.
- HTML/DOCX/SRT/VTT: use supported extraction and inspect the result before analysis. A subtitle cue is not a sentence. Scanned PDFs, audio without a transcript and arbitrary video links are not automatically supported by this first version. Use available authorized extraction/ASR tools when genuinely available, otherwise say what input is missing. Never fabricate a transcript or timing.
- A webpage URL: use the host's authorized browser/web tool to obtain the readable article, preserve source URL and extracted English text, then use the text path. This CLI does not fetch arbitrary URLs. A YouTube URL alone does not supply downloadable audio or subtitles; offer transcript/subtitle and authorized media inputs.

## Build and verify

Write source.txt and annotation.json in a dedicated output folder outside the installed skill. Annotation must cover every source token exactly once in order; use shallow parents for ownership and subdivide long clauses/phrases only as needed for understanding.

Run:

```sh
python3 /path/to/english-chunk-flow/scripts/run.py validate --source /abs/source.txt --annotation /abs/annotation.json
python3 /path/to/english-chunk-flow/scripts/run.py build --source /abs/source.txt --annotation /abs/annotation.json --out /abs/lesson --tts say
```

`build` refuses a nonempty output directory unless `--replace` is explicit. It emits manifest.json, content.json, audio.wav when available, index.html and a portable lesson.html. Open index.html through `serve --root ...` for persistent review APIs, or lesson.html as an offline single file. Use the returned URL; prefer open_in_codex for showing a browser panel.

Inspect rendered UI and test play/pause, sentence and block replay, translation visibility, range end, and saved difficulty on at least one relevant sentence before saying a new lesson passed. Text coverage is necessary, not proof of linguistic correctness; review subjects/predicates/complements, negation, clause attachment and contextual translation. Avoid calling a predicate adjective an object.

Acoustic alignment is a local model estimate, not certified word precision. Build output records backend and review warnings. For original media, inspect mismatch warnings and don't claim the transcript matches just because forced alignment succeeded. Missing pronunciation words or invalid audio must produce an actionable failure, not proportional timing fallback.

## Keep learning state small

The player saves position, deliberate replays and marked chunks. “Save for review” is in the block context menu (right-click/long-press or Shift+F10), not another always-visible block icon. Review via the menu inside the same player. A replay does not prove inability. Keep original source, media/version and parent sentence references.

For “continue the previous lesson”, locate the user's existing lesson folder or player URL; reopen it rather than regenerating audio. For reviewing, open its saved-chunks menu. Never invent progress from chat history.

## Deliver

Return the player link, portable lesson file, input/source and voice provenance, actual duration, and material limitations. Never include credentials in generated files. Package files may contain the user's source/audio; keep them local unless the user asks to share. Do not label a guarded unsupported path as tested or successful.
