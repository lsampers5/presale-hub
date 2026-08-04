# Ticketmaster Presale tracker


## What does it do
- Search an artist
- Pulls information on upcoming events
- Whether the presale passed or is upcoming
- Start and end times of presales


## Set up / How to run
Install the following libraries:
```bash
pip install requests python-dotenv tzdata
```

Make you own `.env` file with `TICKETMASTER_KEY`

```
TICKETMASTER_KEY=your_key_here
```

Then run:

```bash
python main.py
```

## Planned Features
- Filter by upcoming presales
- Alerts for presales opening soon

## Tech Stack
Python, Ticketmaster Discovery API, libraries: requests, python-dotenv, tzdata