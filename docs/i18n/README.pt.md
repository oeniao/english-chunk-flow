# English Chunk Flow

**Ouça as palavras. Entenda a estrutura.**

[English / full technical guide](../../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Português](README.pt.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

English Chunk Flow é uma habilidade de código aberto para praticar a compreensão oral do inglês por blocos gramaticais. Cores e fundos aninhados mostram sujeito, predicado, orações e modificadores para quem conhece as palavras, mas perde o sentido da frase.

![English Chunk Flow](../images/player.png)

## Recursos

Rolagem contínua e repetição de blocos, grupos e frases. O horário permite continuar a reprodução. Salve com clique direito, toque longo ou Shift+F10 e revise em Lesson menu → Saved chunks. Explicações em português, chinês, japonês, coreano, árabe, espanhol, alemão, russo ou inglês. A interface é em inglês.

## Instalação

Requer assistente com habilidades e ferramentas locais, além de Python 3.10+. A síntese local usa say/afconvert no macOS; o alinhamento opcional usa PocketSphinx 5.1.1. O destino padrão é ~/.agents/skills/english-chunk-flow; instalações existentes não são sobrescritas.

```sh
git clone https://github.com/oeniao/english-chunk-flow.git
cd english-chunk-flow
python3 scripts/install.py
python3 ~/.agents/skills/english-chunk-flow/scripts/setup.py
python3 ~/.agents/skills/english-chunk-flow/scripts/run.py doctor
```

## Uso

> Use $english-chunk-flow to preserve my English article and explain every grammar chunk in Portuguese.

```sh
python3 skills/english-chunk-flow/scripts/setup.py
python3 skills/english-chunk-flow/scripts/run.py build --source examples/workday/source.txt --annotation examples/workday/annotation.json --out output/workday --tts say
python3 skills/english-chunk-flow/scripts/run.py serve --root output/workday --port 8770
```

[http://127.0.0.1:8770/index.html](http://127.0.0.1:8770/index.html) · `output/workday/lesson.html`

## Entradas e limitações

Aceita texto, HTML, DOCX, SRT/VTT, áudio original com transcrição revisada e material temático escrito pelo assistente. O assistente analisa e traduz; a CLI valida e empacota. Não é um analisador autônomo. Transcrição só de áudio, extração automática do YouTube, OCR, APIs de voz premium e troca de idioma durante a reprodução não estão integrados. Os tempos são estimativas; revise gramática e tradução. Não há comprovação de eficácia pedagógica.

## Privacidade e código aberto

Os arquivos são processados localmente; o modelo do assistente pode usar a nuvem conforme sua configuração. Não publique gravações privadas, histórico ou chaves. Licença MIT; dependências mantêm as próprias licenças. Contribuições de tradução, gramática, reprodução e acessibilidade são bem-vindas.

[MIT](../../LICENSE) · [Contributing](../../CONTRIBUTING.md) · [Privacy](../../SECURITY.md) · [Architecture](../ARCHITECTURE.md) · [Testing](../TESTING.md) · [Third-party notices](../../THIRD_PARTY_NOTICES.md)
