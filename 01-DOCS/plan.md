# plan.md · FORGED

> Tareas atómicas (cada una ≈ un commit). El código real vive en los archivos;
> aquí queda la lista ordenada con criterio de aceptación verificable por tarea.

## Fase 0 · Scaffold

- [x] **T0.1** Estructura MWP: `CLAUDE.md`, `00-TOOLS/`, `01-DOCS/`, `app/`, `components/`, `lib/`, `ai/`.
  - *AC*: las carpetas existen y `01-DOCS/` tiene spec, plan, design-system, decisions.
- [x] **T0.2** Config Next.js 15 + TS + Tailwind v4 (`package.json`, `tsconfig.json`, `next.config.mjs`, `postcss.config.mjs`).
  - *AC*: `npm install` resuelve dependencias.

## Fase 1 · Theme & layout

- [x] **T1.1** `app/globals.css` con la paleta azul/teal en `@theme inline` + estilos base.
  - *AC*: las CSS vars de `design-system.md` están definidas; fondo navy aplicado.
- [x] **T1.2** `app/layout.tsx` con fuentes (Oswald + Inter), metadata SEO, lang `es`.
  - *AC*: `<html lang="es">`, fuentes como CSS vars, title/description de FORGED.

## Fase 2 · Contenido (fuente de datos)

- [x] **T2.1** `lib/content.ts`: principios, programas, protocolos de nutrición, testimonios, nav.
  - *AC*: arrays tipados; sin texto hardcodeado disperso en componentes.

## Fase 3 · Componentes (voz Goggins, tema fuerza)

- [x] **T3.1** `components/ui.tsx` (Button, Section, Eyebrow, Card) — sistema base.
- [x] **T3.2** `components/Navbar.tsx` — logo + anclas + CTA, responsive.
- [x] **T3.3** `components/Hero.tsx` — titular Goggins, sub, 2 CTAs, fondo con textura.
- [x] **T3.4** `components/Manifesto.tsx` — 3–4 principios de mentalidad.
- [x] **T3.5** `components/Programs.tsx` — 3 cards de programas.
- [x] **T3.6** `components/Nutrition.tsx` — 3 protocolos.
- [x] **T3.7** `components/Proof.tsx` — testimonios con métrica.
- [x] **T3.8** `components/CoachSection.tsx` — bloque coach + embed/fallback + link a `/coach`.
- [x] **T3.9** `components/LeadMagnet.tsx` — guía 0 excusas + form email.
- [x] **T3.10** `components/Footer.tsx`.
  - *AC* (3.x): cada sección renderiza datos de `lib/content.ts`, usa la paleta y la voz.

## Fase 4 · Páginas

- [x] **T4.1** `app/page.tsx` — compone las 9 secciones.
- [x] **T4.2** `app/coach/page.tsx` — coach full-screen (iframe del Space + fallback).
  - *AC*: `npm run dev` muestra `/` y `/coach`.

## Fase 5 · AI Engineering (Coach RAG)

- [x] **T5.1** `ai/notebooks/01-rag-coach-forged.ipynb` — RAG end-to-end + Gradio (estándar lab, español).
  - *AC*: corre top-to-bottom en Colab; responde con fuentes; lanza Gradio.
- [x] **T5.2** `ai/space/` — `app.py`, `requirements.txt`, `README.md` para HF Spaces.
  - *AC*: carpeta lista para `huggingface_hub.upload_folder`.

## Fase 6 · Tooling, docs y deploy

- [x] **T6.1** `00-TOOLS/check.mjs` — verifica que las CSS vars del design-system existen en globals.css.
- [x] **T6.2** `README.md` (run/build/deploy a Vercel + cómo conectar el Coach) y `.gitignore`, `.env.example`.
- [ ] **T6.3** Deploy a Vercel (`npx vercel`) y al Space (HF) — *paso manual del usuario, ver README*.

## Fase 7 · Review

- [ ] **T7.1** `npm run build` limpio + repaso de accesibilidad/contraste + lectura de copy.
  - *AC*: build sin errores; criterios de aceptación del spec marcados.
