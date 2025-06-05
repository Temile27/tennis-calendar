from flask import Flask, Response
from ics import Calendar, Event, DisplayAlarm
from datetime import timedelta
from match_fetcher import get_today_matches

app = Flask(__name__)

@app.route("/calendar.ics")
def calendar():
    c = Calendar()

    for match in get_today_matches():
        e = Event()
        e.name = f"{match['player1']} vs {match['player2']}"
        e.begin = match["start"]
        e.duration = timedelta(hours=2)
        alarm = DisplayAlarm(trigger=timedelta(hours=-1))
        e.alarms.append(alarm)
        c.events.add(e)

    return Response(str(c), mimetype="text/calendar")

# Pour Render
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
