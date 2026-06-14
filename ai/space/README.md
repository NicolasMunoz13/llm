---
title: FORGED Coach IA
emoji: 🏋️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
short_description: Coach IA de fuerza y nutrición (RAG) · voz Goggins · FORGED
---

# FORGED · Coach IA (RAG)

Coach de fuerza y nutrición con voz David Goggins. Usa **RAG** sobre el corpus de
la marca (carpeta `data/`) y cita sus fuentes. Es el componente de AI Engineering
del capstone M9 (curso *AI Engineering*, KeepCoding).

LLM: **Google Gemini** (tier gratuito) — embeddings + generación con una sola key.

## Cómo funciona

1. Al arrancar, embebe los documentos de `data/*.md` (`text-embedding-004`, task type RETRIEVAL_DOCUMENT).
2. Por cada pregunta: recupera top-3 chunks por similitud coseno (query con RETRIEVAL_QUERY).
3. Genera la respuesta con el contexto recuperado (`gemini-2.0-flash`, voz Goggins, cita fuentes).
4. Safety lite: filtro de prompt injection en la entrada + disclaimer médico.

## Configuración

Añade el secret **`GEMINI_API_KEY`** en *Settings → Secrets and variables* del Space.
Consíguela gratis en https://aistudio.google.com/apikey.
(Opcional) `FORGED_CHAT_MODEL` / `FORGED_EMBED_MODEL` para cambiar de modelo.

## Probar en local

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=...
python app.py
```

> Aviso: información educativa, no consejo médico. Ante dudas de salud, consulta a
> un profesional. **Stay hard.**
