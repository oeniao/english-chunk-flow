# Translation languages

| Requested language / aliases | Canonical locale |
| --- | --- |
| 中文、汉语、简体中文、Chinese、zh、zh-CN | zh-CN |
| 日语、日文、日本语、日本語、Japanese、ja、ja-JP | ja |
| 韩语、韩文、韩国语、한국어、Korean、ko、ko-KR | ko |
| 阿拉伯语、阿语、العربية、Arabic、ar | ar |
| 西班牙语、西语、español、Spanish、es、es-ES | es |
| 葡萄牙语、葡语、português、Portuguese、pt、pt-BR、pt-PT | pt |
| 德语、德文、Deutsch、German、de、de-DE | de |
| 俄语、俄文、русский、Russian、ru、ru-RU | ru |
| 英语解释、English、en、en-US、en-GB | en |

Translate meaning in context, preserving negation, modal strength, tense and referents. Japanese and Korean explanations should sound natural in those languages; do not force English word order onto the explanation. Keep English word order in the spoken leaves. A role hint remains subtle and italic; the translated meaning is primary. Arabic explanation labels use RTL isolation while English stays LTR.

A locale normalizer accepts the aliases above, but does not translate text itself. Host language reasoning supplies translations. Regional Portuguese aliases currently select the common Portuguese role labels; no guaranteed regional dialect customization is implemented. Traditional Chinese is not a distinct implemented locale; don't silently promise a separate locale.

All product UI copy, navigation, controls, status, empty states and accessibility labels use English. Learning explanations and grammar roles use the selected explanation language. Supported translation languages do not imply localized outer UI, non-English learning audio, or a live language switch. One built lesson has one explanation language.

Examples:

- 使用 $english-chunk-flow，把这篇英语文章做成听力，用日语解释。
- 使用 $english-chunk-flow，保留这个录音，用韩文翻译语法块。
- 使用 $english-chunk-flow，把已有课程另存为西班牙语解释版，保留英文和声音。
