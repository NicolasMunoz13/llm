# ai/ · Coach IA de FORGED (RAG)

El componente de AI Engineering del capstone. Construye un **RAG** de fuerza y
nutrición y lo despliega como **Hugging Face Space** (Gradio), que la web embebe.

LLM: **Google Gemini** (tier gratuito). Una sola API key cubre embeddings
(`text-embedding-004`) y generación (`gemini-2.0-flash`) → coste 0 €.
Consíguela gratis en https://aistudio.google.com/apikey.

```
ai/
├── notebooks/
│   └── 01-rag-coach-forged.ipynb   # lab estilo M19/M32: RAG end-to-end + Gradio + deploy
└── space/
    ├── app.py                       # app Gradio (RAG + safety lite) lista para HF Spaces
    ├── requirements.txt
    ├── README.md                    # con la cabecera YAML que pide HF Spaces
    └── data/                        # corpus de la marca (7 .md): fuerza, nutrición, mentalidad...
```

## Opción A · Desde el notebook (recomendado, sigue el estándar del curso)

1. Sube `notebooks/01-rag-coach-forged.ipynb` a [Google Colab](https://colab.research.google.com/).
2. Ejecútalo de arriba a abajo. Te pedirá `GEMINI_API_KEY` (y `HF_TOKEN` al final).
3. Construye el RAG, lo prueba con varias queries y lanza Gradio (`share=True`).
4. La última sección empaqueta y **sube el Space** a tu cuenta de HF.

## Opción B · Subir la carpeta `space/` directamente

```bash
pip install huggingface_hub
huggingface-cli login        # token con scope 'write'
huggingface-cli upload <tu-usuario>/forged-coach ai/space . --repo-type=space
```

Luego, en el Space: *Settings → Secrets* → añade `GEMINI_API_KEY`.

## Conectar el Coach con la web

Copia la URL pública del Space (p. ej. `https://<usuario>-forged-coach.hf.space`) en:

- Local: `.env.local` → `NEXT_PUBLIC_COACH_URL=...`
- Vercel: *Settings → Environment Variables* → `NEXT_PUBLIC_COACH_URL` y redeploy.

La web la embebe por `iframe` en `/coach` y en la sección "Coach IA" de la landing.

## Reto opcional (cierra el moat · M14)

Sustituir el LLM de generación por un modelo open-weights afinado con la **voz del
coach** (QLoRA, como el lab "Hablar como Milei") servido en HF/Modal. Documentado
en `01-DOCS/decisions.md` (D4). Fuera del alcance base.
