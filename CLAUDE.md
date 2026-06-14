# CLAUDE.md · FORGED — Strength & Nutrition

Schema que el agente lee al arrancar. Patrón MWP. Detalle en `01-DOCS/`.

## 1. Project Overview
Web de marca (capstone M9) de un *content brand* de fuerza y nutrición.
Landing + Coach IA (RAG). Voz **David Goggins**, paleta **azul/teal**, español.
Objetivo: URL pública (Vercel) que NO parezca "web de IA genérica".
Spec completo en `01-DOCS/spec.md`.

## 2. Tech Stack
- Next.js 15 (App Router) + React 19 + TypeScript.
- Tailwind v4 (config CSS-first en `app/globals.css`, sin shadcn).
- Fuentes: Oswald (display) + Inter (body) vía `next/font`.
- Coach IA: notebook RAG (Colab) → Hugging Face Spaces (Gradio), embebido por iframe.
- Deploy: Vercel (web) + HF Spaces (coach).

## 3. Code Style
- Componentes funcionales en `components/`, uno por archivo, PascalCase.
- Contenido tipado en `lib/content.ts` (no hardcodear copy en JSX disperso).
- Estilos con utilidades Tailwind + CSS vars de la paleta (`--color-*`). No estilos inline salvo dinámicos.
- Copy: frases cortas, imperativas, voz Goggins (ver `01-DOCS/design-system.md`).
- TypeScript estricto; nada de `any` sin justificar.

## 4. Key File Index
- `app/page.tsx` — landing (compone las secciones).
- `app/coach/page.tsx` — Coach IA full-screen (iframe del Space).
- `app/globals.css` — paleta + estilos base (fuente de verdad del theme).
- `lib/content.ts` — programas, nutrición, testimonios, principios, nav.
- `components/` — Navbar, Hero, Manifesto, Programs, Nutrition, Proof, CoachSection, LeadMagnet, Footer, ui.
- `ai/notebooks/01-rag-coach-forged.ipynb` + `ai/space/` — el Coach RAG.

## 5. Off-Limits
- No introducir shadcn, MUI ni librerías de UI pesadas.
- No paletas gris/azul corporativo ni degradados violeta de "IA".
- No claves/API keys en el repo; el LLM vive en el Space (secret de HF). Usar `.env.local`.
- No tocar `01-DOCS/spec.md` sin reflejar el cambio en el código (spec = fuente de verdad).

## 6. Test Requirements
- `npm run build` debe pasar sin errores de tipos ni de lint.
- `npm run dev` sirve `/` (9 secciones) y `/coach`.
- `node 00-TOOLS/check.mjs` valida que las CSS vars del design-system existen.
- Contraste AA sobre fondo oscuro; focus visible en interactivos.

## 7. Workflow
1. Lee `01-DOCS/spec.md` y `design-system.md` antes de tocar nada.
2. Sigue `01-DOCS/plan.md` (tareas atómicas, una ≈ un commit).
3. Cambios de diseño → primero actualiza `design-system.md`, luego el código.
4. Antes de cerrar: `npm run build` + repaso de copy (voz Goggins) + criterios del spec.
