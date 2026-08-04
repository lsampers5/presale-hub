from datetime import datetime
from zoneinfo import ZoneInfo

# Methods
# get_day_suffix returns suffix in a day 'st','nd','rd','th'
# to_eastern takes raw time and puts into eastern raw eastern time
# format_time - formats time from eastern to a more readble ex. May 6th, 2025 at 12:00 AM
# get_status - gets status of the presale ex. 'PAST', 'ACTIVE', 'UPCOMING'

# This is were the basic helper methods will go

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

# Formats time to make it more readable
def format_time(raw_eastern_time):
    day = raw_eastern_time.day
    day_suffix = get_day_suffix(day)
    formatted_time = f"{raw_eastern_time.strftime('%B')} {day}{day_suffix}, {raw_eastern_time.strftime('%Y')} at {raw_eastern_time.strftime('%I:%M %p')}"
    return formatted_time

# Checks whether the presale date is upcoming or past
def get_status(start, end, current_day):
    if start < current_day and current_day < end:
        return "ACTIVE"
    elif start > current_day:
        return "UPCOMING"
    else:
        return "PAST"

# Convert to eastern
def to_eastern(raw_time):
    utc_time = datetime.fromisoformat(raw_time)
    raw_eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))
    return raw_eastern_time