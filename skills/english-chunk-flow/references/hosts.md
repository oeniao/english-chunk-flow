# Host compatibility and installation

The same SKILL.md, Python CLI and browser player serve every host. Host/model availability does not imply terminal, network, package-installation, local-file or audio capabilities. Check actual tools and run `doctor` first. All host-specific paths below are installation targets, not hard-coded runtime paths; resolve scripts relative to this SKILL.md.

## WorkBuddy

Use **Experts · Skills · Connectors → Skills → Add skill → Upload skill** and select the portable ZIP. Keep SKILL.md together with scripts, references and assets. Invoke by asking “Use English Chunk Flow to turn this text into a listening lesson with Chinese explanations.” Enable the installed skill if needed. For project-based development, the documented project configuration supports `.codebuddy/skills/english-chunk-flow/`; from the repository run `python3 scripts/install.py --host workbuddy --project /abs/workspace`. Prefer the UI for personal installations rather than guessing a global directory. WorkBuddy's local or cloud execution OS determines speech dependencies, independently of its model provider.

Official sources: [skill import](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market), [project configuration](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project).

## Claude

Claude Code: `python3 scripts/install.py --host claude` installs to `~/.claude/skills/english-chunk-flow`. Add `--project /abs/workspace` for `.claude/skills/english-chunk-flow` there. Invoke `/english-chunk-flow` or ask in natural language. The optional `agents/openai.yaml` is Codex metadata; the workflow does not depend on it.

Claude chat / Cowork: use the custom-skills import supported by the account and enable code execution/file creation where available. Import the skill ZIP, then request a lesson. This is a skill upload, not a filesystem installation by the local installer. In a Linux sandbox, run `doctor`; if speech tools cannot be installed, use supplied audio + verified timings or explicitly deliver text-only. Return `lesson.html` via the host's file/artifact attachment mechanism; never return a cloud localhost URL as a working user link.

Official sources: [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Grok

Grok Build: `python3 scripts/install.py --host grok` installs to `~/.grok/skills/english-chunk-flow`; `--project /abs/workspace` uses `.grok/skills/english-chunk-flow`. Invoke `/english-chunk-flow` or ask in natural language. The documented Build skill discovery does not establish that every Grok chat surface has local skill installation or shell access.

For a Grok surface without skill discovery, provide the extracted SKILL.md and supporting folder in an available workspace and ask the assistant to read them. Run the CLI only if that session actually supports Python execution and file outputs. Otherwise prepare source.txt and annotation.json and provide CLI commands for a local machine. Never invent a Grok chat skill-import UI or imply that an xAI API key enables local filesystem access.

Official source: [Grok Build skill discovery](https://docs.x.ai/build/features/skills-plugins-marketplaces).

## Linux and delivery

Read [audio.md](audio.md) for Debian/Ubuntu dependencies and `--tts espeak-ng`. No desktop GUI or physical sound device is needed to generate the lesson. For local execution, `serve` binds loopback and the learner can open that machine's browser. For a remote host, prefer downloading the self-contained `lesson.html`; do not expose a server or change its bind address automatically.

Compatibility status: host paths/import instructions are based on the linked documentation. Automated backend-selection, command-routing and packaging tests are separate from end-to-end tests inside each vendor's app. Do not report those apps or native Linux speech as tested without an actual run there.
