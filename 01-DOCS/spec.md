# spec.md · FORGED — Strength & Nutrition

> Fuente de verdad del capstone (M9). El código es la salida de este documento.
> Flujo SDD: **spec → plan → execute → review → deploy**.

## Las 3 respuestas (brainstorm)

| Pregunta | Respuesta | Qué define |
|---|---|---|
| **Hobby / tema** | Negocio de fuerza y nutrición (content brand) | Qué muestra la web |
| **Color preferido** | Azul/teal profundo | La paleta (primary, accent, dark) |
| **Famoso a copiar la voz** | David Goggins | El copy y el microcopy (tono crudo, sin excusas) |

## Objetivo

Construir y desplegar la web de marca **FORGED**, un *content brand* de
entrenamiento de fuerza y nutrición. La web vende contenido (programas y guías)
y captura leads. Incluye un **Coach IA (RAG)** que responde dudas de
entrenamiento/nutrición usando el corpus de la marca — el componente de AI
Engineering que conecta el capstone con el resto del curso (M18–M20, M27–M32).

El resultado: una URL pública (Vercel) que **no parece "web de IA genérica"**:
paleta propia, voz propia (Goggins), secciones tematizadas en el hobby.

## Público y propuesta de valor

- **Público**: gente que entrena (o quiere empezar) y está harta de excusas.
- **Promesa**: programas y nutrición sin humo + un coach que te responde 24/7.
- **Tono**: directo, confrontacional, responsabilidad personal. "Nadie viene a
  salvarte." Frases cortas. Cero marketing blando.

## Páginas

1. `/` — Landing principal (todas las secciones below).
2. `/coach` — Coach IA a pantalla completa (embebe el HF Space vía iframe).

## Secciones de la landing (`/`)

1. **Navbar** — logo FORGED + anclas (Programas, Nutrición, Resultados, Coach) + CTA.
2. **Hero** — titular Goggins + sub + CTA primario (Empieza hoy) y secundario (Habla con el Coach).
3. **Manifiesto / Mentalidad** — 3–4 principios (callo mental, accountability mirror, 40% rule, sin excusas).
4. **Programas** — 3 cards: *Fuerza Base 5×5*, *Hipertrofia Forjada*, *Recomposición Brutal*. Cada una: nivel, duración, qué incluye, precio.
5. **Nutrición** — 3 protocolos: *Proteína Primero*, *Déficit Sin Excusas*, *Volumen Limpio*.
6. **Resultados / Pruebas** — 3 testimonios con métrica (kg, semanas).
7. **Coach IA (RAG)** — bloque que presenta el coach + embed del Space + link a `/coach`.
8. **Lead magnet** — "La Guía de las 0 Excusas" (PDF) con form de email (newsletter).
9. **Footer** — marca, redes, aviso, "Stay hard.".

## Componente de AI Engineering · Coach IA (RAG)

- **Notebook Colab** (`ai/notebooks/01-rag-coach-forged.ipynb`) que construye un
  RAG sobre un corpus de fuerza/nutrición de la marca y lo expone con Gradio.
- **Despliegue**: Hugging Face Spaces (`ai/space/`: `app.py`, `requirements.txt`, `README.md`).
- **Integración**: la web embebe el Space por `iframe` y lo configura con
  `NEXT_PUBLIC_COACH_URL`. Si la var no existe, se muestra un fallback con CTA.
- **Estándar de laboratorio** (igual que M19/M32): celdas markdown en español,
  secciones `##` numeradas, código real y ejecutable, deploy a HF Spaces.

## Contratos / interfaces

- **Paleta** (CSS vars, ver `design-system.md`): `--color-bg`, `--color-surface`,
  `--color-primary`, `--color-primary-deep`, `--color-accent`, `--color-fg`, `--color-muted`.
- **Datos de contenido**: arrays tipados en `lib/content.ts` (programas, protocolos,
  testimonios, principios) → componentes los renderizan. Sin backend ni DB.
- **Coach embed**: `process.env.NEXT_PUBLIC_COACH_URL` (URL del HF Space).
- **Newsletter**: form que hace POST a un endpoint configurable
  (`NEXT_PUBLIC_NEWSLETTER_ENDPOINT`) o, si no existe, abre `mailto:` (sin backend).

## Requisitos no funcionales

- Next.js 15 (App Router) + TypeScript + Tailwind v4 (config CSS-first, sin shadcn).
- Responsive (mobile-first), accesible (contraste AA sobre fondo oscuro, focus visible).
- Lighthouse: Performance y Accessibility ≥ 90 en móvil.
- Sin dependencias pesadas de UI. Iconos como SVG inline / lucide-react opcional.
- `next build` pasa sin errores de tipos ni de lint.

## Criterios de aceptación

- [ ] `npm install && npm run build` termina sin errores.
- [ ] `npm run dev` sirve la landing con las 9 secciones tematizadas.
- [ ] Paleta azul/teal aplicada vía CSS vars; **no** hay gris/azul shadcn por defecto.
- [ ] El copy tiene voz Goggins (frases cortas, accountability, "stay hard").
- [ ] `/coach` embebe el Space si `NEXT_PUBLIC_COACH_URL` está; si no, fallback.
- [ ] El notebook RAG corre top-to-bottom en Colab y lanza Gradio.
- [ ] Existe `ai/space/` listo para subir a HF Spaces.
- [ ] Web desplegada en Vercel con URL pública.

## Fuera de alcance (igual de importante)

- No hay autenticación, carrito, ni pasarela de pago real (los precios son display).
- No hay CMS ni base de datos (contenido en código).
- No se entrena un modelo propio (el RAG usa un LLM vía API; el fine-tuning queda
  como reto opcional, no en este alcance).
- No multi-idioma: la web es en español.
