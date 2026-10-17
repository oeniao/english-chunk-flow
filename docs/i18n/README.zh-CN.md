# English Chunk Flow · Agent Skill

**这是一个安装到 AI 助手中使用的开源英语听力 Skill，已在 Codex 桌面端验证。**

安装后调用 `$english-chunk-flow`，提供英文材料或主题，由助手生成语法块、翻译和可播放的听力课程。Skill 是使用入口，播放器是它生成的学习界面。

**听清单词，听懂结构。**

[English / full technical guide](../../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Português](README.pt.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

English Chunk Flow 是一个开源英语听力技能：把句子拆成语法块，用颜色和嵌套背景展示主干、从句及修饰关系，并配上所选语言的含义。它面向“词都认识，但整句话听不懂”的学习者。

![English Chunk Flow](../images/player.png)

## 功能

按句解析、连续滚动；每块、父块和整句均可重听。点击句首时间继续全文。右键／长按／Shift+F10 保存难点，在 Lesson menu → Saved chunks 复习。支持中、日、韩、阿、西、葡、德、俄及英语解释；产品界面全部为英文。

## 安装

需要可加载技能并执行本机工具的宿主助手，以及 Python 3.10+。本机配音路径需要 macOS 的 say 与 afconvert；对齐可选安装 PocketSphinx 5.1.1。安装器默认写入 ~/.agents/skills/english-chunk-flow，不覆盖已有目录。

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

## 使用

> 使用 $english-chunk-flow，把我提供的英语文章做成结构听力，保留英文原文，用中文解释每个语法块。

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

[http://127.0.0.1:8770/index.html](http://127.0.0.1:8770/index.html) · `output/workday/lesson.html`

## 输入与限制

支持文字、HTML、DOCX、SRT/VTT、原音频＋已核对脚本，以及助手按主题写材料。助手负责语言分析和翻译，工具负责提取、校验、配音与对齐；不是独立自动 parser。尚未集成纯音频转录、自动 YouTube 提取、OCR、高级语音 API 或播放中切换解释语言。对齐为估计，语法仍需复核，没有学习效果认证。

## 隐私与开源

工具本地处理文件，不内置云端 API；宿主助手的模型仍遵循其账户配置，不能据此称为完全离线。别把私人录音、历史记录或密钥提交到仓库。MIT 许可证；依赖保留各自许可证。欢迎提交语法、翻译、播放与无障碍改进。

[MIT](../../LICENSE) · [Contributing](../../CONTRIBUTING.md) · [Privacy](../../SECURITY.md) · [Architecture](../ARCHITECTURE.md) · [Testing](../TESTING.md) · [Third-party notices](../../THIRD_PARTY_NOTICES.md)
