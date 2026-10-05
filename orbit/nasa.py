from datetime import date, timedelta
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_asteroid_data_for_dates(start_date, end_date):
    url = "https://api.nasa.gov/neo/rest/v1/feed"

    api_key = os.getenv("NASA_API_KEY")

    if not api_key:
        raise ValueError(
            "NASA_API_KEY was not found."
        )

    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "api_key": api_key
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()

def get_asteroid_data(days_ahead=0):
    url = "https://api.nasa.gov/neo/rest/v1/feed"

    today = date.today()
    end_date = today + timedelta(days=days_ahead)

    params = {
        "start_date": today.isoformat(),
        "end_date": end_date.isoformat(),
        "api_key": os.getenv("NASA_API_KEY")
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()

def get_asteroid_data_range(days_ahead=7):
    all_near_earth_objects = {}

    start_date = date.today()
    final_date = start_date + timedelta(days=days_ahead)

    current_start = start_date

    while current_start <= final_date:

        current_end = min(
            current_start + timedelta(days=6),
            final_date
        )

        data = get_asteroid_data_for_dates(
            current_start,
            current_end
        )

        near_earth_objects = data.get(
            "near_earth_objects",
            {}
        )

        all_near_earth_objects.update(
            near_earth_objects
        )

        current_start = current_end + timedelta(days=1)

    return {
        "near_earth_objects": all_near_earth_objects
    }