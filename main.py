from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from logic import get_events, proccess_events, event_presale_to_string, filter_upcoming_active_presales, is_valid_artist

def main():
    
    load_dotenv()
    artist = ""
    while True:
        artist = input("'q' to Quit, Search for an artist: ")
        if artist == 'q':
            break
        if not is_valid_artist(artist):
            print(f"Invalid artist name {artist}. Please try again")
            continue
        time_now = datetime.now(ZoneInfo("America/New_York"))
        result, events, status_code = get_events(artist) # returns tuple + unpack
        if result == "empty":
            print("No artist found")
            continue
        elif result == "failed":
            print(f"Request failed with status code {status_code}. Please try again.")
            continue
        
        events_info = proccess_events(events, time_now)

        filter_status = input("1) To filter UPCOMING & ACTIVE presales 2) To print all event info: ")
        print(f"Printing presale information for {artist.title()}")
        if  filter_status == '1':
            filtered_events = filter_upcoming_active_presales(events_info)
            if filtered_events:
                filtered_events_string = event_presale_to_string(filtered_events)
                print(filtered_events_string)
            else: 
                print("No UPCOMING or ACTIVE presales!")
        elif filter_status == '2':
            event_info_string = event_presale_to_string(events_info)
            print(event_info_string)
            continue
        

if __name__ == "__main__":
    main()