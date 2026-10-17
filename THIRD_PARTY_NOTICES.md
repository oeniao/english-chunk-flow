# Third-party components and sample content

Project-authored source, documentation, examples and screenshots are under MIT. Optional dependencies retain their own licenses; this project does not relicense them.

- PocketSphinx 5.1.1: CMU Sphinx, BSD-style license. Installed through PyPI; code, acoustic models and pronunciation dictionaries are **not vendored** in this repository or skill archive. See [upstream](https://github.com/cmusphinx/pocketsphinx) and its license. Bundled upstream models may include their own notices; consult the installed package before redistributing those assets.
- PocketSphinx's transitive Python dependencies, including sounddevice/CFFI, retain their upstream licenses and are installed by pip.
- `say` and `afconvert`: Apple system utilities, not redistributed. Installed system voices are not bundled; voice availability and rights are governed by the user's platform and applicable terms.
- The player uses system fonts and inline vector icons. No commercial font file or external UI library is bundled.

Examples were authored for this project. Screenshots show those original examples in the actual player. No YouTube transcript, publisher recording, real exam audio, private learning history or API key is included. Screenshots depict synthesized or text-only samples; they are not a claim of human voice quality or proven learning outcomes.
