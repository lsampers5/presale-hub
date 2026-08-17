import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from helper import to_eastern, format_time, get_status

# Returns the events of an artist
def get_events(artist):
        api_key = os.getenv("TICKETMASTER_KEY")
        # The Ticketmaster events endpoint
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        # The details of our request
        params = {"apikey": api_key, "keyword": artist}
        # Make the requests
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return ("failed", None, response.status_code) 
        
        data = response.json()

        try:
            events = data["_embedded"]["events"]
        except KeyError:
            return ("empty", [], None)

        return ("ok", events, None)

def is_valid_artist(artist_name):
    return len(artist_name.strip()) >= 2
 
# Returns a flat list of dictionaries with presale information accross all valid events

def proccess_events(events, current_day):
    all_presales = []
    for event in events:
        presales = event.get("sales", {}).get("presales", [])
        proccessed = proccess_presales(presales, current_day)
        if proccessed:
            all_presales.extend(proccessed) # extend merges list to keep it flat

    return all_presales
 
# returns a list of dictionaries
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
                if start_eastern and end_eastern:
                    status = get_status(start_eastern, end_eastern, current_day)
                else:
                    status = 'unknown'
            except(ValueError, TypeError):
                formatted_end = "no end time"
                status = "unknown"

            result.append({'event_name': event_name, 'status': status, 'start': formatted_start, 'end': formatted_end})
        return result
    else:
        return None

def filter_upcoming_active_presales(events_info):
    filtered_events = []
    for event_info in events_info:
        if event_info['status'] != 'PAST':
            filtered_events.append(event_info)


    return filtered_events



def event_presale_to_string(events_info):

    result = "\n".join(
        f"Event Name: {event_info['event_name']} | Status: {event_info['status']} | Start Date: {event_info['start']} | End Dates: {event_info['end']}"
        for event_info in events_info
    )
    return result
