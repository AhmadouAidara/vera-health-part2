def select_top_15(documents):
    """
    Trie les documents par score de fiabilité décroissant
    et retourne les 15 premiers.

    Args:
        documents (list): liste des documents avec champ 'reliability_score'

    Returns:
        list: top 15 documents classés par fiabilité
    """
    # Vérifier que tous les documents ont un score
    scored_docs = [
        doc for doc in documents
        if "reliability_score" in doc.metadata
    ]

    top_docs = sorted(
        scored_docs,
        key=lambda d: d.metadata["reliability_score"],
        reverse=True
    )

    return top_docs[:15]