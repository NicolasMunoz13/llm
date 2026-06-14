# FORGED — Strength & Nutrition

Capstone del módulo **M9 (End-to-End Project)** del curso *AI Engineering* de KeepCoding.
Una web de marca de fuerza y nutrición **+ un Coach IA (RAG)**, construida con el
flujo **SDD** y la estructura **MWP**.

> **Las 3 respuestas** · hobby: negocio de fuerza/nutrición · color: azul/teal ·
> voz: David Goggins. → web exclusiva, no "web de IA genérica". **Stay hard.**

## Estructura (MWP · Model Workspace Protocol)

```
capstone-forged/
├── CLAUDE.md          # schema que el agente lee al arrancar (7 secciones)
├── 00-TOOLS/          # scripts reutilizables (check de theme)
├── 01-DOCS/           # spec · plan · design-system · decisions  (SDD)
├── app/               # Next.js App Router (/, /coach, theme)
├── components/        # Navbar, Hero, Manifesto, Programs, Nutrition, Proof, Coach, LeadMagnet, Footer
├── lib/content.ts     # contenido tipado (única fuente de copy)
└── ai/                # Coach IA: notebook RAG (Colab) + Space de Hugging Face
```

## Stack

Next.js 15 (App Router) · React 19 · TypeScript · Tailwind v4 (config CSS-first,
**sin shadcn**) · fuentes Oswald + Inter. Coach IA: RAG (LangChain/Chroma) servido
con Gradio en Hugging Face Spaces.

## Desarrollo local

```bash
npm install
cp .env.example .env.local   # opcional: rellena NEXT_PUBLIC_COACH_URL
npm run dev                  # http://localhost:3000
```

Otros scripts:

```bash
npm run build         # build de producción (debe pasar limpio)
npm run check:theme   # valida que la paleta existe en globals.css
```

## Variables de entorno

| Variable | Para qué | Si está vacía |
|---|---|---|
| `NEXT_PUBLIC_COACH_URL` | URL del HF Space del Coach IA (iframe) | Se muestra un fallback |
| `NEXT_PUBLIC_NEWSLETTER_ENDPOINT` | POST `{ email }` del lead magnet | El form abre `mailto:` |

## Deploy de la web → Vercel

1. Sube este proyecto a un repo de GitHub (o usa `vercel` directamente).
2. Opción CLI:
   ```bash
   npx vercel            # primer deploy (preview)
   npx vercel --prod     # a producción
   ```
   O conecta el repo en https://vercel.com/new (framework: Next.js, detectado solo).
3. En **Settings → Environment Variables** de Vercel añade `NEXT_PUBLIC_COACH_URL`
   con la URL de tu Space y vuelve a desplegar.

## Deploy del Coach IA → Hugging Face Spaces

Todo el detalle está en [`ai/README.md`](ai/README.md). Resumen:

1. Abre [`ai/notebooks/01-rag-coach-forged.ipynb`](ai/notebooks/01-rag-coach-forged.ipynb) en Google Colab.
2. Ejecútalo de arriba a abajo: construye el RAG y prueba Gradio en local (`share=True`).
3. La última sección sube `ai/space/` a un Space (Gradio) con tu `HF_TOKEN`.
4. Añade `GEMINI_API_KEY` como **secret** del Space (key gratis en https://aistudio.google.com/apikey).
5. Copia la URL pública del Space en `NEXT_PUBLIC_COACH_URL` (local y en Vercel).

## Checklist de aceptación (ver `01-DOCS/spec.md`)

- [x] `npm install && npm run build` sin errores.
- [x] Landing con 9 secciones tematizadas + `/coach`.
- [x] Paleta azul/teal por CSS vars (sin gris/azul shadcn).
- [x] Copy con voz Goggins.
- [x] Notebook RAG + carpeta `ai/space/` listos.
- [ ] Web en Vercel (URL pública) · *paso manual*.
- [ ] Coach en HF Spaces (URL pública) · *paso manual*.
