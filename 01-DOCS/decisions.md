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
LLM vive en el Space (secret `OPENAI_API_KEY` en HF), y la web sólo embebe un
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

## D7 · Modelo LLM del coach
Decidido: usar un **proveedor con tier gratuito** (Google Gemini o Groq) para que
el Coach tenga coste 0. El notebook y `ai/space/app.py` se adaptarán a ese
proveedor cuando se despliegue el Coach (paso posterior al deploy de la web).
La versión inicial quedó escrita contra OpenAI (patrón de M32); migrar el cliente
y el modelo es un cambio acotado. Alternativa open-weights (Gemma/Qwen, M12)
también válida si se prefiere autohospedaje.

> Estado: la **web se despliega primero** en Vercel (sin Coach, con fallback).
> El Coach (Gemini/Groq) se conecta después vía `NEXT_PUBLIC_COACH_URL`.
