# English Chunk Flow

**Слушайте слова. Понимайте структуру.**

[English / full technical guide](../../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Português](README.pt.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

English Chunk Flow — открытый навык для тренировки английского на слух через грамматические блоки. Цвета и вложенные фоны показывают подлежащее, сказуемое, придаточные и уточнения. Он помогает тем, кто знает слова, но не успевает понять предложение целиком.

![English Chunk Flow](../images/player.png)

## Возможности

Непрерывная прокрутка и повтор блоков, групп и предложений. Метка времени продолжает воспроизведение. Сохраняйте правой кнопкой, долгим нажатием или Shift+F10; повторяйте в Lesson menu → Saved chunks. Объяснения на русском, китайском, японском, корейском, арабском, испанском, португальском, немецком или английском. Интерфейс английский.

## Установка

Нужны помощник с поддержкой навыков и локальных инструментов и Python 3.10+. Локальный синтез использует say/afconvert в macOS; необязательное выравнивание — PocketSphinx 5.1.1. По умолчанию установка в ~/.agents/skills/english-chunk-flow; существующая папка не перезаписывается.

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

## Использование

> Use $english-chunk-flow to preserve my English article and explain every grammar chunk in Russian.

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

[http://127.0.0.1:8770/index.html](http://127.0.0.1:8770/index.html) · `output/workday/lesson.html`

## Входные данные и ограничения

Поддерживаются текст, HTML, DOCX, SRT/VTT, исходное аудио с проверенным текстом и тематические материалы, написанные помощником. Помощник анализирует и переводит; CLI проверяет и упаковывает. Это не автономный парсер. Не встроены распознавание аудио без текста, автоматическое извлечение YouTube, OCR, платные голосовые API и переключение языка во время воспроизведения. Временные границы приблизительны; грамматику и переводы нужно проверять. Учебная эффективность не доказана.

## Приватность и открытый код

Файлы обрабатываются локально, но модель помощника может работать в облаке согласно настройкам. Не публикуйте личные записи, историю или ключи. Лицензия MIT; зависимости сохраняют свои лицензии. Приветствуются улучшения перевода, грамматики, воспроизведения и доступности.

[MIT](../../LICENSE) · [Contributing](../../CONTRIBUTING.md) · [Privacy](../../SECURITY.md) · [Architecture](../ARCHITECTURE.md) · [Testing](../TESTING.md) · [Third-party notices](../../THIRD_PARTY_NOTICES.md)
