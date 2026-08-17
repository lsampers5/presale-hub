from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from logic import get_events, is_valid_artist, proccess_events
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/presales")
def get_presales(artist: str):
    if not is_valid_artist(artist):
        raise HTTPException(status_code=400, detail="Invalid Artist Name")

    result, events, status_code = get_events(artist)

    if result == "empty":
        raise HTTPException(status_code=404, detail="No artist found")
    if result == "failed":
        raise HTTPException(status_code=502, detail=f"Ticketmaster request failed with status {status_code}")

    # Got Events from the presale
    time_now = datetime.now(ZoneInfo("America/New_York"))
    return proccess_events(events, time_now)
