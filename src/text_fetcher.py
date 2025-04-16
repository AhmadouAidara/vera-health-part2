import requests

def fetch_text_from_url(url):
    """
    Tente de récupérer le texte brut d’un document en ligne à partir de son URL.
    Utilisé comme fallback si le texte ou l’abstract ne sont pas disponibles
    dans les métadonnées ZeroEntropy.

    Args:
        url (str): URL du fichier source (PDF ou HTML généralement)

    Returns:
        str: Contenu texte brut récupéré depuis l’URL, ou chaîne vide en cas d’erreur.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Erreur récupération texte ({response.status_code}) pour {url}")
    except Exception as e:
        print(f"Erreur récupération texte: {e}")
    return ""