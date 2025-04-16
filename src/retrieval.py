import os  
from zeroentropy import ZeroEntropy

import os
from zeroentropy import ZeroEntropy

zclient = ZeroEntropy(api_key=os.getenv("ZEROENTROPY_API_KEY"))
print(f"API KEY Loaded: {os.getenv('ZEROENTROPY_API_KEY')}")
def get_zclient():
    """
    Initialise un client ZeroEntropy avec la clé d'API stockée dans l’environnement.
    Soulève une erreur si la variable n’est pas définie.
    """
    import os
    from zeroentropy import ZeroEntropy
    api_key = os.getenv("ZEROENTROPY_API_KEY")
    if not api_key:
        raise ValueError("ZEROENTROPY_API_KEY is not set in environment")
    return ZeroEntropy(api_key=api_key)


def query_zero_entropy(question, k=50):
    """
    Envoie une requête à ZeroEntropy avec un filtre strict :
    - Le document est une guideline (is_guidelines = true)
    - Il a au moins 10 citations
    - Il a au moins 2 citations influentes
    """
    zclient = get_zclient()
    response = zclient.queries.top_documents(
        collection_name="VeraScientia-HighThroughput",
        query=question,
        k=k,
        filter={
            "$and": [
                { "is_guidelines": { "$eq": "true" } },
                { "citation_count": { "$gt": "10" } },
                { "influential_citation_count": { "$gt": "2" } }
            ]
        },
        include_metadata=True
    )
    return response.results

def query_multi_strategy(question, k=20):
    """
    Applique plusieurs stratégies de recherche complémentaires :
    - no_filter : tous les documents
    - is_guidelines : uniquement les recommandations
    - citation_only : documents avec beaucoup de citations
    Déduplique les résultats en utilisant le chemin unique de chaque document.
    """
    zclient = get_zclient()
    strategies = {
        "no_filter": None,
        "is_guidelines": {
            "is_guidelines": { "$eq": "true" }
        },
        "citation_only": {
            "$and": [
                { "citation_count": { "$gt": "10" } },
                { "influential_citation_count": { "$gt": "2" } }
            ]
        }
    }

    all_results = []
    seen_paths = set()

    for label, filt in strategies.items():
        try:
            response = zclient.queries.top_documents(
                collection_name="VeraScientia-HighThroughput",
                query=question,
                k=k,
                filter=filt,
                include_metadata=True
            )
            for doc in response.results:
                if doc.path not in seen_paths:
                    all_results.append(doc)
                    seen_paths.add(doc.path)
        except Exception as e:
            print(f"Erreur dans la stratégie '{label}': {e}")

    print(f" Total combiné : {len(all_results)} documents uniques récupérés")  
    return all_results