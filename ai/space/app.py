"""
FORGED · Coach IA (RAG) — Hugging Face Space (Gradio)
=====================================================
Coach de fuerza y nutrición con voz David Goggins. Responde fundamentándose en el
corpus de la marca (carpeta data/) y cita las fuentes. Patrón del lab M32:
RAG + Gradio + safety lite, desplegable en HF Spaces.

Requiere el secret OPENAI_API_KEY en el Space (Settings -> Secrets).
"""

import os
import re
import glob
import numpy as np
import gradio as gr
from openai import OpenAI

# ----------------------------------------------------------------------------
# 0. Config
# ----------------------------------------------------------------------------
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.getenv("FORGED_CHAT_MODEL", "gpt-4o-mini")
TOP_K = 3
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

client = OpenAI()  # lee OPENAI_API_KEY del entorno (secret del Space)

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
        parts = re.split(r"\n(?=## )", text)
        for part in parts:
            part = part.strip()
            if len(part) > 40:
                chunks.append({"source": name, "text": part})
    return chunks


def embed(texts):
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return np.array([d.embedding for d in resp.data], dtype=np.float32)


print("Cargando corpus FORGED...")
CHUNKS = load_corpus()
DOC_EMB = embed([c["text"] for c in CHUNKS])
DOC_EMB /= np.linalg.norm(DOC_EMB, axis=1, keepdims=True) + 1e-8
print(f"Corpus listo: {len(CHUNKS)} chunks de {len(set(c['source'] for c in CHUNKS))} documentos.")


# ----------------------------------------------------------------------------
# 2. Retrieval (cosine top-k)
# ----------------------------------------------------------------------------
def retrieve(query, k=TOP_K):
    q = embed([query])[0]
    q /= np.linalg.norm(q) + 1e-8
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

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # historial reciente (Gradio 'messages' format)
    for turn in history[-4:]:
        if isinstance(turn, dict):
            messages.append(turn)
    messages.append(
        {"role": "user", "content": f"CONTEXTO:\n{context}\n\nPREGUNTA: {message}"}
    )

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.6,
        max_tokens=600,
    )
    return resp.choices[0].message.content


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
    theme=gr.themes.Soft(primary_hue="teal", neutral_hue="slate"),
)

if __name__ == "__main__":
    demo.launch()
