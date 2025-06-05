from flask import Flask, Response
from ics import Calendar, Event
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# === CONFIGURATION ===
JOUEURS = ["Djokovic", "Alcaraz", "Sinner", "Arthur Fils", "Lois Boisson"]
GRANDSCHELEMS = [
    "roland-garros",
    "wimbledon",
    "us-open",
    "australian-open"
]
BASE_URL = "https://www.flashscore.fr/tennis/"

app = Flask(__name__)

def get_matches():
    matchs = []
    for tournoi in GRANDSCHELEMS:
        url = BASE_URL + tournoi + "/"
        try:
            html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
            soup = BeautifulSoup(html, "html.parser")

            for div in soup.find_all("div", class_="event__match"):
                match_time = div.get("data-start")
                player1 = div.get("data-home-team", "")
                player2 = div.get("data-away-team", "")

                if not match_time or not player1 or not player2:
                    continue

                # Vérifie si un joueur suivi est dans ce match
                if any(joueur.lower() in (player1 + player2).lower() for joueur in JOUEURS):
                    dt = datetime.utcfromtimestamp(int(match_time)) + timedelta(hours=2)  # Converti en heure de Paris
                    matchs.append({
                        "title": f"{player1} vs {player2}",
                        "start": dt,
                        "tournament": tournoi.replace("-", " ").title()
                    })

        except Exception as e:
            print(f"Erreur lors du chargement de {tournoi}: {e}")
    return matchs

@app.route("/calendar.ics")
def calendar():
    cal = Calendar()
    for match in get_matches():
        e = Event()
        e.name = match["title"]
        e.begin = match["start"]
        e.end = match["start"] + timedelta(hours=2)
        e.description = f"Tournoi : {match['tournament']}"

        # Ajout d'une alarme 1h avant le match
        e.extra.append("BEGIN:VALARM")
        e.extra.append("TRIGGER:-PT60M")
        e.extra.append("ACTION:DISPLAY")
        e.extra.append("DESCRIPTION:Match dans 1h")
        e.extra.append("END:VALARM")

        cal.events.add(e)

    return Response(str(cal), mimetype="text/calendar")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render définit la variable d’environnement PORT
    app.run(host="0.0.0.0", port=port)

