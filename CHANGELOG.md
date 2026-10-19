# Changelog

## Unreleased — 2026-10-19

Latest refinement: Structure headers show only small, muted English; explicit sentence replay brightens the reference. Bilingual script view and exports retain translations. Updated demo media reflects this refinement.

- Show complete English and selected-language sentence scripts above grammar chunks. Reuse the translation toggle, retain English when translations are hidden, and avoid duplicate headers in Bilingual script view.
- Refresh the screenshot and full workday playback video after an actual macOS synthesis/alignment and browser test; verify Japanese and Arabic text-only language variants.
- Escape the sentence export's embedded closing script tag so portable lessons execute correctly offline.

Follow-up after Linux user testing:

- Retain synthesized sentence playback when word alignment fails, explicitly disable unavailable chunk replay, and expose per-sentence timing quality. Strict mode still requires complete word alignment.
- Cache completed sentence WAVs for retries and collect failures across sentences rather than stopping at the first error.
- Accept checked custom pronunciations for alignment and original-recording mismatch checking. Do not guess missing-name pronunciations.
- Silence FFmpeg startup logs with `-v error` and fix portable HTML inlining of versioned player assets.
- Add failure-injection regression coverage. These checks do not claim native Linux acoustic alignment reliability.


- Add Structure / Bilingual script views, independent translation visibility, and adaptive tablet/desktop reading layouts with larger text.
- Add per-sentence copy and standalone HTML export with embedded sentence audio. Preserve role colors, nested ownership, translations, attachment notes and structured JSON in a centered responsive document.
- Add Linux eSpeak NG + FFmpeg synthesis, automatic backend selection and backend-dependent default voices; retain macOS speech and original-audio paths.
- Document WorkBuddy skill import, Claude / Grok Build discovery and cloud-session delivery. Add host-specific installer destinations without overwriting existing skills.
- Add portability coverage: 20 local tests pass. Native Linux speech and vendor-app end-to-end checks remain unverified.

## 0.1.0 — 2026-10-17

Initial open-source alpha: host-assisted annotation, multilingual meanings, local extraction/speech/alignment, sentence and chunk replay, saved chunks, English product UI and a compact final timeline timestamp. Includes original examples, screenshots, portable packaging, documentation in nine languages, and a core test suite and opt-in CI template.

Audio-only transcription, automatic YouTube extraction, OCR, premium voice APIs, live explanation-language switching and a full desktop library are not implemented.
