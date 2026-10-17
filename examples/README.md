# Original examples

`workday` contains six original sentences with Chinese explanations. `ja` contains one original sentence with Japanese explanations. Annotations are real host-authored grammar/meaning data, not an automatic standalone parser. Audio and learning state are deliberately not committed.

From the repository root, build on macOS after setup:

```sh
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

Open `http://127.0.0.1:8770/index.html`. For a portable file, open `output/workday/lesson.html`. On a system without local speech, use `--text-only` and a different output folder. Do not call a text-only package an audio demo.
