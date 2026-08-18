import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from helper import to_eastern, format_time, get_status
import json

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
# Need to change this first

def proccess_events(events, current_day): # Returns [events{event_name, event_url, venue, event_date_time, presale_name, presale_status, presale_start, presale_end}]
    events_info = []
    for event in events:
        event_date_time = f"LocalDate: {event["dates"]["start"]["localDate"]} | LocalTime: {event["dates"]["start"]["localTime"]}"
        event_info = {
            'event_name': event.get('name'),
            'event_url': event.get('url'),
            'event_date_time': event_date_time,
            'event_id': event.get('id'),
        }
        try :
            event_info['venue'] = event["_embedded"]['venues'][0]['name']
        except (KeyError):
            event_info['venue'] = 'Unknown Venue'
    
        presales = event.get("sales", {}).get("presales", [])
        proccessed = proccess_presales(presales, current_day, event_info)
        if proccessed:
            events_info.extend(proccessed)

    return events_info
 
# returns a list of dictionaries
def proccess_presales(presales, current_day, event_info):
    result = []
    if presales:
        for presale in presales:
            presale_name = presale.get("name", "Unamed")
            presale_start = presale.get("startDateTime")
            try:
                # format time
                presale_start_eastern = to_eastern(presale_start)
                presale_formatted_start = format_time(presale_start_eastern)

            except(ValueError, TypeError):
                presale_formatted_start = "no start time"

            presale_end = presale.get("endDateTime")
            try:
                presale_end_eastern = to_eastern(presale_end)
                presale_formatted_end = format_time(presale_end_eastern)
                if presale_start_eastern and presale_end_eastern:
                    presale_status = get_status(presale_start_eastern, presale_end_eastern, current_day)
                else:
                    presale_status = 'unknown'
            except(ValueError, TypeError):
                presale_formatted_end = "no end time"
                presale_status = "unknown"
            if presale.get('description'):
                description = presale.get('description')
            else:
                description = "No description provided."
            res = {**event_info,
                    'presale_name': presale_name,
                    'presale_status': presale_status,
                    'presale_start': presale_formatted_start,
                    'presale_end': presale_formatted_end,
                    'presale_description': description,
                }
            result.append(res)
        return result
    else:
        return None

def filter_upcoming_active_presales(events_info):
    filtered_events = []
    for event_info in events_info:
        if event_info['presale_status'] != 'PAST':
            filtered_events.append(event_info)


    return filtered_events



def event_presale_to_string(events_info):

    result = "\n".join(
        f"Event: {event_info['event_name']} | Presale: {event_info['presale_name']} | Status: {event_info['presale_status']} | Start Date: {event_info['presale_start']} | End Dates: {event_info['presale_end']}"
        for event_info in events_info
    )
    return result
