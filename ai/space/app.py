"""
FORGED · Coach IA (RAG) — Hugging Face Space (Gradio)
=====================================================
Coach de fuerza y nutrición con voz David Goggins. Responde fundamentándose en el
corpus de la marca (carpeta data/) y cita las fuentes. Patrón del lab M32:
RAG + Gradio + safety lite, desplegable en HF Spaces.

LLM: Google Gemini (tier gratuito) — embeddings + generación con una sola key.
Requiere el secret GEMINI_API_KEY en el Space (Settings -> Secrets).
"""

import os
import re
import glob
import numpy as np
import gradio as gr
from google import genai
from google.genai import types

# ----------------------------------------------------------------------------
# 0. Config
# ----------------------------------------------------------------------------
EMBED_MODEL = os.getenv("FORGED_EMBED_MODEL", "gemini-embedding-001")
CHAT_MODEL = os.getenv("FORGED_CHAT_MODEL", "gemini-2.5-flash")
TOP_K = 3
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

client = genai.Client()  # lee GEMINI_API_KEY (o GOOGLE_API_KEY) del entorno

SYSTEM_PROMPT = """Eres el Coach IA de FORGED, una marca de fuerza y nutrición.
Tu voz es la de David Goggins: directa, intensa, sin excusas, en segunda persona y
con frases cortas. Motivas confrontando, no consolando. Cierras a veces con "Stay hard.".

REGLAS:
- Responde SOLO con la información del CONTEXTO. Si el contexto no cubre la pregunta,
  dilo claramente y no te inventes datos ("No tengo eso en mi material...").
- Cita las fuentes que uses al final, con el formato: [Fuente: nombre-del-archivo].
- Eres educativo, no médico. Ante síntomas, dolor agudo o condiciones de salud,
  manda a la persona a un profesional. Nunca diagnostiques.
- Español. Sé útil y concreto: números, rangos, pasos. Nada de relleno motivacional vacío.
"""


# ----------------------------------------------------------------------------
# 1. Cargar y trocear el corpus (chunking simple por documento)
# ----------------------------------------------------------------------------
def load_corpus():
    chunks = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.md"))):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        # un chunk por sección "## " (mantiene el contexto del título)
        for part in re.split(r"\n(?=## )", text):
            part = part.strip()
            if len(part) > 40:
                chunks.append({"source": name, "text": part})
    return chunks


def embed(texts, task_type):
    """Embebe con Gemini (uno a uno, robusto). task_type: RETRIEVAL_DOCUMENT o RETRIEVAL_QUERY."""
    vecs = []
    for t in texts:
        resp = client.models.embed_content(
            model=EMBED_MODEL,
            contents=t,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        vecs.append(resp.embeddings[0].values)
    arr = np.array(vecs, dtype=np.float32)
    arr /= np.linalg.norm(arr, axis=1, keepdims=True) + 1e-8
    return arr


print("Cargando corpus FORGED...")
CHUNKS = load_corpus()
DOC_EMB = embed([c["text"] for c in CHUNKS], "RETRIEVAL_DOCUMENT")
print(f"Corpus listo: {len(CHUNKS)} chunks de {len(set(c['source'] for c in CHUNKS))} documentos.")


# ----------------------------------------------------------------------------
# 2. Retrieval (cosine top-k)
# ----------------------------------------------------------------------------
def retrieve(query, k=TOP_K):
    q = embed([query], "RETRIEVAL_QUERY")[0]
    scores = DOC_EMB @ q
    idx = np.argsort(-scores)[:k]
    return [CHUNKS[i] for i in idx]


# ----------------------------------------------------------------------------
# 3. Safety lite (M29 condensado): filtro de input
# ----------------------------------------------------------------------------
INJECTION_PATTERNS = [
    r"ignora (todas )?(las )?instrucciones",
    r"ignore (all )?(previous )?instructions",
    r"system prompt",
    r"act[úu]a como si",
]


def input_is_safe(text):
    low = text.lower()
    return not any(re.search(p, low) for p in INJECTION_PATTERNS)


# ----------------------------------------------------------------------------
# 4. El agente RAG
# ----------------------------------------------------------------------------
def coach(message, history):
    if not message or not message.strip():
        return "Dime algo. Las preguntas que no haces no se responden solas."

    if not input_is_safe(message):
        return "Aquí solo se habla de entrenar y comer bien. Sin jueguitos. ¿Qué quieres mejorar?"

    docs = retrieve(message)
    context = "\n\n---\n\n".join(f"[{d['source']}]\n{d['text']}" for d in docs)

    # historial reciente -> formato Gemini (roles 'user' / 'model')
    contents = []
    for turn in history[-4:]:
        if isinstance(turn, dict) and turn.get("content"):
            role = "model" if turn.get("role") == "assistant" else "user"
            contents.append(types.Content(role=role, parts=[types.Part(text=turn["content"])]))
    contents.append(
        types.Content(role="user", parts=[types.Part(text=f"CONTEXTO:\n{context}\n\nPREGUNTA: {message}")])
    )

    try:
        resp = client.models.generate_content(
            model=CHAT_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.6,
                max_output_tokens=600,
            ),
        )
        return resp.text
    except Exception as e:
        # El tier gratuito de Gemini limita a pocas peticiones/min: degradar sin tumbar el Space.
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            return "He llegado al límite de peticiones por ahora. Respira, espera un minuto y vuelve a la carga."
        if "503" in msg or "UNAVAILABLE" in msg:
            return "El modelo está saturado en este momento. Aguanta unos segundos y reintenta. Stay hard."
        return "Algo ha fallado al generar la respuesta. Reintenta en un momento."


# ----------------------------------------------------------------------------
# 5. UI Gradio
# ----------------------------------------------------------------------------
demo = gr.ChatInterface(
    fn=coach,
    type="messages",
    title="🏋️ FORGED · Coach IA",
    description=(
        "Fuerza y nutrición sin excusas. Pregunta sobre entrenamiento, hipertrofia, "
        "déficit, proteína o recuperación. Respondo con el material de FORGED y cito la "
        "fuente. **No es consejo médico.** Stay hard."
    ),
    examples=[
        "¿Cuántas series por grupo muscular a la semana?",
        "¿Cómo ajusto el déficit si me estanco?",
        "¿Cuánta proteína debo comer al día?",
        "Me duele la rodilla al sentarme, ¿qué hago?",
    ],
    cache_examples=False,  # no pre-ejecutar los ejemplos al arrancar (evita gastar la cuota gratuita y tumbar el Space)
    theme=gr.themes.Soft(primary_hue="teal", neutral_hue="slate"),
)

if __name__ == "__main__":
    demo.launch()
