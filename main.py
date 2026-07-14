import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

# Adds the suffix to dates
def get_day_suffix(day):
    if 11 <= day <= 13:
        return "th"
    last = day % 10
    if last == 1:
        return "st"
    elif last == 2:
        return "nd"
    elif last == 3:
        return "rd"
    else:
        return "th"

def get_status(start, current_day):
    if start > current_day:
        return "UPCOMING"
    else:
        return "past"


# Formats time to make it more readable
def format_time(raw_eastern_time):
    day = raw_eastern_time.day
    day_suffix = get_day_suffix(day)
    formatted_time = f"{raw_eastern_time.strftime('%B')} {day}{day_suffix}, {raw_eastern_time.strftime('%Y')} at {raw_eastern_time.strftime('%I:%M %p')}"
    return formatted_time

# Convert to eastern
def to_eastern(raw_time):
    utc_time = datetime.fromisoformat(raw_time)
    raw_eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))
    return raw_eastern_time



def main():
    load_dotenv()
    api_key = os.getenv("TICKETMASTER_KEY")

    # The Ticketmaster events endpoint
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    artist = input("Search for an artist: ")

    # The details of our request
    params = {
        "apikey": api_key,
        "keyword": artist
    }

    # Make the requests
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Request Failed status code {response.status_code}")
        return


    data = response.json()
    try:
        events = data["_embedded"]["events"]
    except KeyError:
        print("No artist found")
        return

    now = datetime.now(ZoneInfo("America/New_York"))

    for event in events:
        print(event["name"])

        # Not every presale has all of the fields that I am looking for so need to check if it is in the presale dictionary
        presales = event.get("sales", {}).get("presales", [])

        if presales:
            for presale in presales:
                name = presale.get("name", "Unnamed")
                start = presale.get("startDateTime")
                try:
                    start_eastern = to_eastern(start)
                    # Formats time
                    formatted_start = format_time(start_eastern)

                    # Check whether the date has past or not
                    status = get_status(start_eastern, now)

                except (TypeError, ValueError):
                    formatted_start = "no start time"
                    status = "Unknown"
                
                end = presale.get("endDateTime")
                try:
                    # Formatting time for the end date
                    end_eastern = to_eastern(end)
                    formatted_end = format_time(end_eastern)
                    

                except (TypeError, ValueError):
                    formatted_end = "no end time"    
                print(" Presale:", name, "| Status:", status, "| Starts:", formatted_start, "| Ends:", formatted_end)
        else:
            print(" No presale info")
            
        print() # Readability (Seperates events)

if __name__ == "__main__":
    main()