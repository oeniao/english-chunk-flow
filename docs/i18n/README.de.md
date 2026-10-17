# English Chunk Flow

**Höre die Wörter. Verstehe die Struktur.**

[English / full technical guide](../../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Português](README.pt.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

English Chunk Flow ist ein quelloffener Skill zum Englisch-Hörtraining mit grammatischen Sinneinheiten. Farben und verschachtelte Hintergründe zeigen Subjekt, Prädikat, Nebensätze und Ergänzungen – für Lernende, die einzelne Wörter kennen, aber den Satz nicht schnell erfassen.

![English Chunk Flow](../images/player.png)

## Funktionen

Fortlaufendes Scrollen und Wiederholung von Chunks, Gruppen oder Sätzen. Zeitstempel starten die fortlaufende Wiedergabe. Per Rechtsklick, langem Drücken oder Shift+F10 speichern; unter Lesson menu → Saved chunks wiederholen. Erklärungen auf Deutsch, Chinesisch, Japanisch, Koreanisch, Arabisch, Spanisch, Portugiesisch, Russisch oder Englisch. Die Oberfläche ist Englisch.

## Installation

Benötigt einen Skill-fähigen Assistenten mit lokalen Werkzeugen und Python 3.10+. Lokale Spracherzeugung nutzt macOS say/afconvert; optionale akustische Ausrichtung nutzt PocketSphinx 5.1.1. Standardziel: ~/.agents/skills/english-chunk-flow. Bestehende Installationen werden nicht überschrieben.

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

## Verwendung

> Use $english-chunk-flow to preserve my English article and explain every grammar chunk in German.

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

[http://127.0.0.1:8770/index.html](http://127.0.0.1:8770/index.html) · `output/workday/lesson.html`

## Eingaben und Grenzen

Unterstützt Text, HTML, DOCX, SRT/VTT, Originalaudio mit geprüftem Transkript und vom Assistenten verfasste Themenübungen. Der Assistent analysiert und übersetzt; die CLI validiert und verpackt. Kein eigenständiger automatischer Parser. Reine Audiotranskription, automatischer YouTube-Import, OCR, Premium-Sprach-APIs und Sprachwechsel während der Wiedergabe sind nicht integriert. Zeitgrenzen sind Schätzungen; Grammatik und Übersetzungen müssen geprüft werden. Die Lernwirksamkeit wurde nicht nachgewiesen.

## Datenschutz und Open Source

Dateien werden lokal verarbeitet; das Modell des Assistenten kann je nach Konfiguration in der Cloud laufen. Keine privaten Aufnahmen, Verläufe oder Schlüssel veröffentlichen. MIT-Lizenz; Abhängigkeiten behalten eigene Lizenzen. Beiträge zu Übersetzung, Grammatik, Wiedergabe und Barrierefreiheit sind willkommen.

[MIT](../../LICENSE) · [Contributing](../../CONTRIBUTING.md) · [Privacy](../../SECURITY.md) · [Architecture](../ARCHITECTURE.md) · [Testing](../TESTING.md) · [Third-party notices](../../THIRD_PARTY_NOTICES.md)
