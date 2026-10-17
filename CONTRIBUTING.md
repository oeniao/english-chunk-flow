# Contributing

Thank you for helping people hear English structure.

1. Open an issue describing the listening problem and a small input you may share.
2. Keep English order and original audio provenance. Never replace missing timestamps with proportional estimates.
3. Use shallow structure; subdivide only when it makes the backbone clearer. Preserve negation, modality and modifier ownership.
4. Product UI must be English. Learning explanations follow the selected language. Test Japanese/Korean wrapping and Arabic RTL when relevant.
5. Run `python3 -m unittest discover -s tests -v`, `node --check skills/english-chunk-flow/assets/player/app.js`, and `python3 scripts/check_docs.py`.
6. For player changes, test play/pause, chunk/group/sentence replay, saved chunks and the final timeline node in a browser. Include a screenshot and honest limitations in your PR.

Do not commit personal lessons, transcripts from other publishers, recordings, credentials, virtual environments or state files. Use the original examples in this repository. Translation corrections are welcome; keep setup commands and capability boundaries consistent across READMEs. Contributions are accepted under this repository's MIT license; no CLA is required.
