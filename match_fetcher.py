from datetime import datetime, timedelta

# Liste de tes joueurs
JOUERS_SUIVIS = [
    "Novak Djokovic",
    "Carlos Alcaraz",
    "Jannik Sinner",
    "Arthur Fils",
    "Loïs Boisson"
]

# Simule des matchs du jour (remplace par vrai scraping ensuite)
def get_today_matches():
    now = datetime.now()
    matches = [
        {"player1": "Novak Djokovic", "player2": "Random Player", "start": now.replace(hour=17, minute=10)},
        {"player1": "Carlos Alcaraz", "player2": "Joueur Inconnu", "start": now.replace(hour=20, minute=30)}
    ]
    return [m for m in matches if m["player1"] in JOUERS_SUIVIS or m["player2"] in JOUERS_SUIVIS]
