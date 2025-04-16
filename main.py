import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from data.journals import load_journals, merge_journal_metadata
from src.retrieval import query_multi_strategy
from src.gpt_filter import filter_documents_with_gpt
from src.scoring import score_documents
from src.selection import select_top_15

# 1. Charger les variables d’environnement


# 2. Nettoyage des apostrophes et guillemets
def clean_question(text):
    return text.replace("’", "'").replace("“", '"').replace("”", '"')

# 3. Liste des 11 questions cliniques nettoyées
RAW_QUESTIONS = [
    "Should I use beta blocker in a patient with HFpEF and grade 3 diastolic dysfunction?",
    "What test is used to confirm celiac disease in adults?",
    "What are the latest guidelines for HPV vaccination?",
    "Are there any biopsy protocols for assessing histologic recurrence of Crohn's disease after ileocecectomy?",
    "When is amoxicillin/clavulanate preferred over amoxicillin for AOM?",
    "Which mallampati score is lowest risk for intubation failure?",
    "What is the clinical criteria used for strep throat?",
    "What are the best antibiotics for facial cellulitis?",
    "What is the recommended antibiotic choice for perirectal abscess?",
    "What does fenofibrate do for patients with high or ineffective HDL?",
    "What to do for incidental IPMN in 79 year old?"
]

QUESTIONS = [clean_question(q) for q in RAW_QUESTIONS]

# 4. Poids (issus de la Partie 1)
weights = {
    "publication_type_score":0.13099,
    "impact_factor_normalized":0.06014,
    "citation_score": 0.54444,
    "recency_score":0.26443
}

# 5. Chargement des journaux
print("Chargement des journaux...")
journal_path = "data/journals.ts"
journals_df = load_journals(journal_path)

# 6. Traitement complet par question
all_results = []

for question in QUESTIONS:
    print(f"\n Traitement de la question : {question}")

    # a. Récupération
    docs = query_multi_strategy(question, k=50)
    print(f"→ {len(docs)} documents récupérés")

    # b. Fusion avec journaux
    docs = merge_journal_metadata(docs, journals_df)

    # c. Filtrage GPT
    filtered_docs, _ = filter_documents_with_gpt(question, docs, max_docs=30, show_preview=False)
    print(f"→ {len(filtered_docs)} documents jugés pertinents")

    if not filtered_docs:
        print("⚠️ Aucun document pertinent à scorer pour cette question.")
        continue

    # d. Scoring + sélection
    scored_docs = score_documents(filtered_docs, weights, journals_df)
    top_15 = select_top_15(scored_docs)
    for doc in top_15:
        doc.metadata["question"] = question
    all_results.extend(top_15)

# 7. Export final
if all_results:
    df_final = pd.DataFrame([doc.metadata for doc in all_results])
    df_final.to_csv("results/top_15_papers.csv", index=False)
    print("\n Fichier results/top_15_papers.csv généré avec succès.")
else:
    print("\n Aucun résultat à sauvegarder.")