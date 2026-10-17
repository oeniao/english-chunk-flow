# English Chunk Flow · Agent Skill

**هذه Skill مفتوحة المصدر للاستماع بالإنجليزية، تُثبَّت داخل مساعد ذكاء اصطناعي. جُرّبت على Codex لسطح المكتب.**

استدعِ `$english-chunk-flow` وقدّم نصًا إنجليزيًا أو موضوعًا؛ يُنشئ المساعد المقاطع النحوية والترجمة ودرسًا قابلًا للتشغيل. المهارة هي نقطة البداية، والمشغّل هو واجهة التعلّم الناتجة.

**اسمع الكلمات وافهم بنية الجملة.**

[English / full technical guide](../../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Português](README.pt.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

English Chunk Flow مهارة مفتوحة المصدر لتعلّم الاستماع بالإنجليزية. تقسّم الجمل إلى مقاطع نحوية، وتستخدم الألوان والخلفيات المتداخلة لعرض الفاعل والفعل والجمل التابعة وروابط التعديل، مع شرح المعنى باللغة المختارة.

![English Chunk Flow](../images/player.png)

## الميزات

تمرير مستمر وإعادة تشغيل المقطع أو المجموعة أو الجملة. يواصل الطابع الزمني تشغيل الدرس. احفظ بالنقر الأيمن أو الضغط المطوّل أو Shift+F10 وراجع من Lesson menu → Saved chunks. يدعم الشرح بالعربية والصينية واليابانية والكورية والإسبانية والبرتغالية والألمانية والروسية والإنجليزية. واجهة المنتج بالإنجليزية.

## التثبيت

تحتاج إلى مساعد يدعم المهارات والأدوات المحلية وPython 3.10+. توليد الصوت المحلي يستخدم say وafconvert على macOS؛ المحاذاة اختيارية عبر PocketSphinx 5.1.1. المسار الافتراضي ~/.agents/skills/english-chunk-flow ولا تُستبدل المجلدات الموجودة.

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

## الاستخدام

> Use $english-chunk-flow to preserve my English article and explain every grammar chunk in Arabic.

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

[http://127.0.0.1:8770/index.html](http://127.0.0.1:8770/index.html) · `output/workday/lesson.html`

## المدخلات والحدود

يدعم النص وHTML وDOCX وSRT/VTT والصوت الأصلي مع نص مراجَع، ومواد يكتبها المساعد حسب الموضوع. المساعد يحلل اللغة ويترجم؛ الأدوات تتحقق وتجهز المشغّل. ليس محللًا مستقلًا آليًا. تفريغ الصوت وحده واستخراج YouTube وOCR وخدمات الصوت المدفوعة والتبديل الفوري للغة غير مدمجة. التوقيت تقديري والقواعد والترجمة تحتاجان مراجعة. لم تُثبت فعالية التعلّم بدراسة.

## الخصوصية والمصدر المفتوح

تُعالج الملفات محليًا، لكن نموذج المساعد قد يعمل سحابيًا حسب إعداداته. لا تنشر التسجيلات الخاصة أو السجل أو المفاتيح. ترخيص MIT للمشروع وتبقى تراخيص الاعتماديات مستقلة. نرحب بتحسينات الترجمة والقواعد والتشغيل وإمكانية الوصول.

[MIT](../../LICENSE) · [Contributing](../../CONTRIBUTING.md) · [Privacy](../../SECURITY.md) · [Architecture](../ARCHITECTURE.md) · [Testing](../TESTING.md) · [Third-party notices](../../THIRD_PARTY_NOTICES.md)
