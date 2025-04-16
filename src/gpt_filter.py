from openai import OpenAI
from src.text_fetcher import fetch_text_from_url
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_relevant_gpt(question, context, max_chars=1500):
    prompt = f"""You are a medical assistant.

You are given a clinical question and an article excerpt.

Determine whether the article is relevant to the question.

Question: "{question}"

Excerpt: \"\"\"{context[:max_chars]}\"\"\"

Is this document relevant? Please answer with 'Yes' or 'No' and briefly explain if 'Yes'."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
    
def filter_documents_with_gpt(question, documents, max_docs=30, show_preview=True):
    """
    Utilise GPT pour filtrer les documents pertinents.
    Si aucun texte n'est disponible dans metadata, il le récupère via file_url.
    """
    relevant_docs = []

    for i, doc in enumerate(documents[:max_docs]):
        metadata = doc.metadata or {}

        # 1. Tenter de récupérer texte depuis metadata ou fallback via URL
        text = metadata.get("abstract") or metadata.get("text") or fetch_text_from_url(getattr(doc, 'file_url', ''))

        if not text.strip():
            if show_preview:
                print(f"\n [Doc {i+1}] Skipped — no content")
            continue

        # 2. Affichage preview si demandé
        if show_preview:
            print(f"\n🔍 [Doc {i+1}] — Content preview:")
            print(text[:800] + "..." if len(text) > 800 else text)

        # 3. Passage à GPT
        result = is_relevant_gpt(question, text)

        if show_preview:
            print(f"GPT response: {result}")

        # 4. Vérification pertinence
        if result.lower().startswith(("yes", "possibly")):
            doc.metadata["relevance_gpt"] = result
            relevant_docs.append(doc)

    return relevant_docs, documents