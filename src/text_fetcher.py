import requests

def fetch_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Erreur récupération texte ({response.status_code}) pour {url}")
    except Exception as e:
        print(f"Erreur récupération texte: {e}")
    return ""