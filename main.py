import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from logic import get_events, proccess_events, event_presale_to_string

def main():
    load_dotenv()
    artist = input("Search for an artist: ")

    time_now = datetime.now(ZoneInfo("America/New_York"))

    events_result = get_events(artist) # returns tuple
    result, events = events_result # unpack the tuple

    if result == "empty":
        return print("No artist found")
    elif result == "failed":
        return print("Status code Error") # Try to find a way in the future to figure out how get the actual 
    

    events_info = proccess_events(events, time_now)


    event_info_string = event_presale_to_string(events_info)

    print(event_info_string)



    

        
if __name__ == "__main__":
    main()