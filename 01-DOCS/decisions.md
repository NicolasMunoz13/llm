# decisions.md · FORGED

Registro de decisiones (ADR ligero). Por qué, no solo qué.

## D1 · Tailwind v4 CSS-first en vez de tailwind.config.js + shadcn
El antipatrón del brief es "shadcn por defecto + gris/azul = web de IA". Para
diseñar exclusivo definimos la paleta a mano con `@theme inline` en `globals.css`.
Menos dependencias, control total del look azul/teal.

## D2 · Contenido en `lib/content.ts`, sin CMS ni DB
El capstone es una landing de marca, no una app con estado. Mantener el contenido
tipado en código hace el build trivial y el deploy a Vercel inmediato (fuera de
alcance: CMS, auth, pagos).

## D3 · Coach IA como HF Space embebido, no API en el propio Next.js
Reutilizamos el estándar de M32 (Gradio → HF Spaces). Así el coste/secreto del
LLM vive en el Space (secret `GEMINI_API_KEY` en HF), y la web sólo embebe un
`iframe`. La web no necesita backend ni exponer claves. Se conecta vía
`NEXT_PUBLIC_COACH_URL`; si falta, hay fallback.

## D4 · RAG (no fine-tuning) para el coach en el alcance base
RAG da respuestas fundamentadas en el corpus de la marca con coste y complejidad
bajos (M18–M20). El fine-tuning de un modelo "voz coach" (M14, QLoRA) queda como
reto opcional documentado, no en el alcance base.

## D5 · Idioma español
El curso y los labs están en español (p. ej. el lab de Milei). La web y el
notebook van en español para coherencia con el material y el público objetivo.

## D6 · Voz Goggins sin copiar literal
Usamos el *registro* (frases cortas, accountability, "stay hard") y conceptos
reinterpretados (callo mental, regla del 40%) en vez de transcribir frases con
copyright. Suficiente para que la web "suene a él" sin plagiar.

## D7 · Modelo LLM del coach → Google Gemini (tier gratuito)
Decidido: **Google Gemini** (AI Studio), elegido sobre Groq porque RAG necesita
*embeddings + generación* y Gemini cubre ambos en su tier gratuito con **una sola
API key** (`text-embedding-004` + `gemini-2.0-flash`). Groq solo ofrece generación,
no embeddings → exigiría un segundo proveedor. Coste del Coach: **0 €**.
El notebook y `ai/space/app.py` usan el SDK `google-genai`. Alternativa
open-weights (Gemma/Qwen, M12) válida si se prefiere autohospedaje.

> Estado: la **web ya está desplegada** en Vercel (https://llm-green-tau.vercel.app/,
> repo personal NicolasMunoz13/llm). El Coach (Gemini) se conecta vía el secret
> `GEMINI_API_KEY` en el HF Space + la env var `NEXT_PUBLIC_COACH_URL` en Vercel.
