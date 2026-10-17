# English Chunk Flow · Agent Skill

**AI アシスタントにインストールして使う、オープンソースの英語リスニング Skill です。Codex デスクトップで動作を確認しています。**

`$english-chunk-flow` を呼び出して英文やテーマを渡すと、アシスタントが文法チャンク、翻訳、再生可能なレッスンを作成します。Skill が入口で、プレーヤーは生成される学習画面です。

**単語を聞き取り、文の構造をつかむ。**

[English / full technical guide](../../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Português](README.pt.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

English Chunk Flow は、英文を文単位のチャンクに分け、主語・述語・節・修飾の関係を色と入れ子の背景で示すオープンソースの英語リスニングスキルです。単語は分かるのに文全体を理解しにくい学習者を支援します。

![English Chunk Flow](../images/player.png)

## 機能

連続スクロール、チャンク・親ブロック・文のリプレイ、時刻からの連続再生に対応。右クリック、長押し、Shift+F10 で保存し、Lesson menu → Saved chunks で復習できます。日本語、中国語、韓国語、アラビア語、スペイン語、ポルトガル語、ドイツ語、ロシア語、英語の解説に対応。操作画面は英語です。

## インストール

ローカルツールを実行できるスキル対応アシスタントと Python 3.10+ が必要です。音声合成は macOS の say/afconvert、音響アライメントは任意の PocketSphinx 5.1.1 を使用します。既定のインストール先は ~/.agents/skills/english-chunk-flow。既存フォルダーは上書きしません。

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

## 使い方

> Use $english-chunk-flow to keep my English article unchanged and explain every grammar chunk in Japanese.

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

[http://127.0.0.1:8770/index.html](http://127.0.0.1:8770/index.html) · `output/workday/lesson.html`

## 入力と制限

テキスト、HTML、DOCX、SRT/VTT、音声と確認済み原稿、アシスタントが作成するテーマ別教材に対応。言語分析と翻訳はアシスタントが担当し、CLI は検証とパッケージ化を行います。独立した自動構文解析器ではありません。音声のみの文字起こし、YouTube 自動抽出、OCR、有料音声 API、再生中の解説言語切替は未実装。時刻は推定値で、文法と訳の確認が必要です。学習効果は認証されていません。

## プライバシーと公開

ファイル処理はローカルですが、ホストのモデルまでオフラインとは限りません。個人の録音、履歴、キーを公開しないでください。MIT ライセンス。依存関係には各自のライセンスが適用されます。翻訳・文法・再生・アクセシビリティへの貢献を歓迎します。

[MIT](../../LICENSE) · [Contributing](../../CONTRIBUTING.md) · [Privacy](../../SECURITY.md) · [Architecture](../ARCHITECTURE.md) · [Testing](../TESTING.md) · [Third-party notices](../../THIRD_PARTY_NOTICES.md)
