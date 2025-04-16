import os  # AJOUTER CETTE LIGNE
from zeroentropy import ZeroEntropy

import os
from zeroentropy import ZeroEntropy

zclient = ZeroEntropy(api_key=os.getenv("ZEROENTROPY_API_KEY"))
print(f"API KEY Loaded: {os.getenv('ZEROENTROPY_API_KEY')}")
def get_zclient():
    import os
    from zeroentropy import ZeroEntropy
    api_key = os.getenv("ZEROENTROPY_API_KEY")
    if not api_key:
        raise ValueError("ZEROENTROPY_API_KEY is not set in environment")
    return ZeroEntropy(api_key=api_key)


def query_zero_entropy(question, k=50):
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
    Récupère des documents selon plusieurs stratégies complémentaires.
    Agrège et déduplique les résultats.
    """
    zclient = get_zclient()
    strategies = {
        "no_filter": None
    }

    all_results = []
    seen_paths = set()

    for label, filt in strategies.items():
        try:
            print(f"🔎 Envoi de la requête à ZeroEntropy pour : {question} | filtre : {label}")
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