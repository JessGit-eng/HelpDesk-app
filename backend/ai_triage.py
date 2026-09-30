from functools import lru_cache
from pathlib import Path


model_path = (
    Path(__file__).resolve().parent.parent
    / "AI-model"
    / "qwen2.5-1.5b-instruct-q4_k_m.gguf"
)


@lru_cache(maxsize=1)
def get_model():
    from llama_cpp import Llama

    return Llama(
        model_path=str(model_path),
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )

def triage_ticket(title, description, category):

    prompt = f"""
        You are an IT help-desk triage assistant.
        Analyse the following support ticket.
        Title: {title}
        Description: {description}
    Category: {category}

    Classify the priority as Low, Medium or High.

    Return exactly three lines:

    Priority: Low, Medium or High
    Confidence: percentage
    Reason: short explanation
    """

    response = get_model().create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=150
    )

    content = response["choices"][0]["message"]["content"]

    return content
