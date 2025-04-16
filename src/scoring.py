import pandas as pd

def score_documents(documents, weights, journals_df=None):
    """
    Calcule un score de fiabilité pour chaque document en fonction des métadonnées
    et des poids fournis. Utilise un bonus SJR si le DataFrame des journaux est fourni.
    
    Args:
        documents (list): liste des documents Zero-Entropy (filtrés)
        weights (dict): poids optimisés du score (Partie 1)
        journals_df (DataFrame): table optionnelle des journaux avec colonnes 'journal' et 'sjr'
    
    Returns:
        list: documents enrichis avec un champ 'reliability_score' dans metadata
    """
    for doc in documents:
        metadata = doc.metadata or {}

        publication_type_score = 1 if metadata.get("is_guidelines") == "true" else 0
        impact_factor = float(metadata.get("impact_factor_normalized", 0))
        citations_per_year = float(metadata.get("#citations/year_normalized", 0))
        influential_citations = float(metadata.get("#influential_citations_normalized", 0))
        citation_score = 0.75 * citations_per_year + 0.25 * influential_citations
        recency_score = 1 if int(metadata.get("year", 0)) > 2016 else 0

        sjr_bonus = 0
        if journals_df is not None:
            journal = metadata.get("journal", "").strip().lower()
            match = journals_df[journals_df["journal"].str.lower() == journal]
            if not match.empty:
                sjr_value = match.iloc[0].get("sjr", 0)
                if pd.notna(sjr_value):
                    sjr_bonus = float(sjr_value) / 100

        score = (
            weights["publication_type_score"] * publication_type_score +
            weights["impact_factor_normalized"] * impact_factor +
            weights["citation_score"] * citation_score +
            weights["recency_score"] * recency_score +
            0.1 * sjr_bonus
        )

        doc.metadata["reliability_score"] = round(score, 4)

    return documents