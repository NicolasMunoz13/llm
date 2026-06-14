# design-system.md · FORGED

> Diseño exclusivo, no "web de IA genérica". Paleta de TU color (azul/teal),
> voz de TU famoso (Goggins), secciones tematizadas en TU hobby (fuerza/nutrición).

## Concepto

Estética de **gimnasio de fuerza de noche**: fondo oscuro casi negro azulado,
acentos teal/cyan que parecen luz de neón sobre acero. Tipografía con titulares
condensados y pesados (acero forjado), cuerpo legible. Bordes finos, mucho
contraste, cero degradados pastel. Sensación: intenso, nocturno, sin excusas.

## Paleta (CSS custom properties)

Definidas en `app/globals.css` con `@theme inline` (Tailwind v4).

| Token | Hex | Uso |
|---|---|---|
| `--color-bg` | `#06121A` | Fondo base (navy casi negro) |
| `--color-surface` | `#0E2630` | Cards, secciones alternas |
| `--color-surface-2` | `#13323E` | Hover / bordes elevados |
| `--color-primary` | `#14B8A6` | Teal principal (CTAs, acentos) |
| `--color-primary-deep` | `#0D9488` | Teal oscuro (hover de CTA) |
| `--color-accent` | `#38BDF8` | Cyan/azul (highlights, links) |
| `--color-fg` | `#EAF6F4` | Texto principal |
| `--color-muted` | `#8FB0AD` | Texto secundario |
| `--color-line` | `#1C4350` | Líneas/bordes |
| `--color-danger` | `#F97362` | Énfasis "sin excusas" (rojo cálido puntual) |

Contraste: `--color-fg` sobre `--color-bg` ≈ 14:1 (AAA). `--color-muted` sobre
`--color-bg` ≈ 5:1 (AA). CTAs teal con texto `--color-bg` oscuro encima.

## Tipografía

- **Display/titulares**: `Oswald` (condensada, peso 600–700), uppercase con
  `letter-spacing` ligero. Forja/acero.
- **Cuerpo**: `Inter` (variable). Pesos 400/500/600.
- Cargadas con `next/font/google` en `app/layout.tsx` → CSS vars `--font-display`, `--font-sans`.
- Escala: hero `clamp(2.5rem, 8vw, 5.5rem)`; h2 `clamp(1.8rem, 4vw, 3rem)`.

## Componentes y patrones

- **Botón primario**: fondo `--color-primary`, texto `--color-bg`, uppercase,
  `font-display`, hover → `--color-primary-deep`, focus ring `--color-accent`.
- **Botón ghost**: borde `--color-line`, texto `--color-fg`, hover borde teal.
- **Card**: `--color-surface`, borde `--color-line` 1px, radio 14px, hover sube
  borde a teal + translateY(-2px).
- **Eyebrow / kicker**: texto pequeño uppercase teal con tracking (encabeza secciones).
- **Sección**: `max-w-6xl mx-auto px-6 py-20/24`, alterna `bg` y `surface`.
- **Número de sección**: contador grande translúcido detrás de los títulos (estética track).

## Voz (David Goggins) — guía de copy

- Frases **cortas**. Imperativas. Segunda persona.
- Confronta, no consuela: "Nadie viene a salvarte.", "Hazlo cuando no te apetezca."
- Conceptos firma (reinterpretados, sin copiar literal): *callo mental*,
  *el espejo de la responsabilidad*, *la regla del 40%*, *taking souls*.
- Cierre recurrente: **"Stay hard."**
- Microcopy de botones: "Empieza hoy", "Sin excusas", "Habla con el Coach", "Descarga la guía".
- Evitar: "descubre tu mejor versión", "journey", "wellness blando", emojis.

## Anti-patrones (prohibido)

- shadcn por defecto, gris/azul corporativo, copy de plantilla ("Welcome to...").
- Degradados violeta/rosa de "IA".
- Hero con stock photo genérica + 3 cards iguales sin alma.
