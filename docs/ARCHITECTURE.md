# Architecture and data flow

User material → host assistant extraction/review → sentence-level annotation → exact source coverage checks → original audio or local sentence speech → acoustic word alignment → chunk timing ranges → player package.

The host assistant performs language analysis and contextual translation. `lesson.py` checks coverage, known roles, nesting and temporal bounds. Valid JSON does not prove correct grammar or translation. The bundled schema is documented in [annotation.md](../skills/english-chunk-flow/references/annotation.md).

Speech is synthesized continuously per sentence, not separately for each chunk. Chunk replay uses ranges from real word timings. Original audio is retained; when compatible PCM is supplied, it is copied byte-for-byte. Other formats may be locally decoded. Acoustic estimates require edge review; a weak independent recognition check can flag a wrong transcript but cannot certify a match.

Outputs: source, annotation, manifest, content, real audio/timings when available, an HTML/CSS/JS player, and a single-file portable HTML. Material identity depends on source, annotation, language and audio to separate review state between versions. Local state stores position, intentional replays and explicitly saved chunks; a replay is not automatically a learning deficit.

No backend translation API, live speech recognition or dedicated trained parser is bundled. Source-only and schema workflows use Python standard library; alignment optionally requires PocketSphinx. macOS `say`/`afconvert` are the implemented local synthesis path.
