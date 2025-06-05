import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

# Liste des joueurs à suivre
JOUEURS_SUIVIS = [
    "Djokovic",
    "Alcaraz",
    "Sinner",
    "Arthur Fils",
    "Loïs Boisson"
]

# Noms des 4 Grands Chelems (à détecter dans le nom du tournoi)
GRAND_CHELEMS = [
    "Australian Open",
    "Roland Garros",
    "Wimbledon",
    "US Open"
]

def get_today_matches():
    url = "https://www.flashscore.fr/tennis/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    matchs = []
    now = datetime.now()

    for match in soup.select(".event__match"):
        try:
            player1 = match.select_one(".event__participant--home").text.strip()
            player2 = match.select_one(".event__participant--away").text.strip()
            hour_text = match.select_one(".event__time").text.strip()

            # Ex : 14:30 → datetime object
            match_time = datetime.strptime(hour_text, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )

            # Tournoi (remonté via parent ou déduit du contexte)
            tournament = match.find_previous("div", class_="event__title").text.strip()

            # Filtrer par joueurs suivis
            if not any(nom.lower() in (player1 + player2).lower() for nom in JOUEURS_SUIVIS):
                continue

            # Filtrer par Grands Chelems
            if not any(gc.lower() in tournament.lower() for gc in GRAND_CHELEMS):
                continue

            matchs.append({
                "player1": player1,
                "player2": player2,
                "start": match_time,
            })

        except Exception as e:
            continue  # en cas d'erreur sur un match, on le saute

    return matchs
