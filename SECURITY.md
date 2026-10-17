# Security and privacy

The CLI processes files locally. It does not call a cloud translation or speech API. The host assistant can still process text using its configured model; this is not a claim of fully offline inference. Audio generation may use macOS system speech services. Optional dependency installation contacts PyPI.

The lesson server binds `127.0.0.1` only, supports audio Range requests and stores per-lesson state beside output. It is a local development server, not a production hosting service. Do not expose it to the public internet. Portable HTML embeds source and audio; review its contents before sharing. Browser localStorage behavior varies, especially for local files.

For a suspected vulnerability, use GitHub's private vulnerability reporting if enabled. Otherwise open a minimal issue requesting a private reporting channel without publishing exploit details, private material or secrets. Never put API keys or sensitive transcripts in issues.
