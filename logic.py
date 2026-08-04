import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from helper import to_eastern, format_time, get_status

# Returns the event 
def get_events(artist):
    api_key = os.getenv("TICKETMASTER_KEY")
    # The Ticketmaster events endpoint
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    # The details of our request
    params = {"apikey": api_key, "keyword": artist}
    # Make the requests
    response = requests.get(url, params=params)
    if response.status_code != 200:# TODO: try to find away to also return status code (idea tuple maybe)
        return ("failed", None) 
    
    data = response.json()

    try:
        events = data["_embedded"]["events"]
    except KeyError:
        return ("empty", [])

    return ("ok", events)


def proccess_events(events, current_day):
    all_presales = []
    for event in events:
        presales = event.get("sales", {}).get("presales", [])
        proccessed = proccess_presales(presales, current_day)
        if proccessed:
            all_presales.extend(proccessed)

    return all_presales

        
        

def proccess_presales(presales, current_day):
    result = []
    if presales:
        for presale in presales:
            event_name = presale.get("name", "Unamed")
            start = presale.get("startDateTime")
            try:
                # format time
                start_eastern = to_eastern(start)
                formatted_start = format_time(start_eastern)

            except(ValueError, TypeError):
                formatted_start = "no start time"

            end = presale.get("endDateTime")
            try:
                end_eastern = to_eastern(end)
                formatted_end = format_time(end_eastern)
                try:
                    status = get_status(start_eastern, end_eastern, current_day)
                except(NameError):
                    continue
            except(ValueError, TypeError):
                formatted_end = "no end time"
                status = "unknown"

            result.append({'event_name': event_name, 'status': status, 'start': formatted_start, 'end': formatted_end})
        return result
    else:
        return None

def event_presale_to_string(events_info):

    result = "\n".join(
        f"Event Name: {event_info['event_name']} | Status: {event_info['status']} | Start Date: {event_info['start']} | End Dates: {event_info['end']}"
        for event_info in events_info
    )
    return result

        
        