import requests
import re
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data

ACCOUNT_ID = "2ed6415f-e0a0-49de-91ca-52efa470d8d4"
API_URL = f"https://api.ola.godaddy.com/v3/accounts/{ACCOUNT_ID}/services"
SYDNEY_TZ = ZoneInfo("Australia/Sydney")
BOOKING_URL = "https://2swaggstudio.com/bookings"
LOCATION = "Level 6/ 630 George St, Sydney NSW 2000"


def parse_time_from_name(name):
    """Extract local class time from name like 'KPOP w Chris | 5 PM' or '| 5:00 PM'."""
    match = re.search(r'\|\s*(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)', name, re.IGNORECASE)
    if not match:
        return None

    time_str = match.group(1).strip().upper()

    # Normalise: add :00 if missing minutes, add PM if no period marker
    if not re.search(r'[AP]M', time_str):
        time_str += " PM"
    if ':' not in time_str:
        time_str = time_str.replace(" ", ":00 ", 1)

    try:
        return datetime.strptime(time_str, "%I:%M %p").time()
    except ValueError:
        return None


def parse_duration(iso_duration):
    """Convert ISO 8601 duration like 'PT1H', 'PT45M', 'PT2H' to minutes."""
    hours = re.search(r'(\d+)H', iso_duration)
    minutes = re.search(r'(\d+)M', iso_duration)
    total = 0
    if hours:
        total += int(hours.group(1)) * 60
    if minutes:
        total += int(minutes.group(1))
    return total or 60


def map_level(description):
    """Map the API description field to level tags."""
    desc = (description or "").strip().upper()
    if "KIDS" in desc:
        return ["youth"]
    if "ABS BEG" in desc:
        return ["beginner"]
    if "BEG" in desc:
        return ["beginner"]
    if "INT" in desc:
        return ["intermediate"]
    if "ADV" in desc:
        return ["advanced"]
    return ["advanced"]


def get_instructor(service):
    """Get instructor name from resources array, falling back to parsing the name."""
    resources = service.get("resources", [])
    for r in resources:
        if r.get("role") != "owner" and r.get("name"):
            return r["name"].strip().title()

    # Fallback: parse "... w INSTRUCTOR | ..."
    match = re.search(r'\bw\s+(.+?)\s*\|', service["name"])
    if match:
        return match.group(1).strip().title()

    # Last resort: use first resource even if owner
    if resources and resources[0].get("name"):
        return resources[0]["name"].strip().title()
    return "Unknown"


def get_recurring_dates(anchor_utc_str, start_date, end_date):
    """
    Determine the day-of-week from the UTC anchor time (in Sydney tz),
    then return all dates matching that weekday within the range.
    """
    anchor_utc = datetime.fromisoformat(anchor_utc_str.replace("Z", "+00:00"))
    anchor_syd = anchor_utc.astimezone(SYDNEY_TZ)
    target_weekday = anchor_syd.weekday()  # 0=Mon, 6=Sun

    dates = []
    current = start_date
    while current <= end_date:
        if current.weekday() == target_weekday:
            dates.append(current)
        current += timedelta(days=1)
    return dates


def fetch_services():
    """Fetch all services from the GoDaddy OLA API."""
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://2swaggstudio.com",
        "Referer": "https://2swaggstudio.com/",
    }

    response = requests.get(
        API_URL,
        params={"per_page": 80, "with_category_ids": "true"},
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        print(f"⚠️  2Swagg API request failed with status {response.status_code}")
        return []

    data = response.json()
    return data.get("results", [])


def scrape_twoswagg_classes(start_date, end_date):
    """
    Fetch 2Swagg Studio classes from the GoDaddy OLA API
    and expand recurring services into individual class instances.
    """
    services = fetch_services()
    if not services:
        return []

    formatted_classes = []

    for service in services:
        if service.get("recurrence_type") != "recurring":
            continue

        class_time = parse_time_from_name(service["name"])
        if not class_time:
            print(f"⚠️  Could not parse time from: {service['name']}")
            continue

        duration_min = parse_duration(service.get("duration", "PT1H"))
        instructor = get_instructor(service)
        level = map_level(service.get("description", ""))
        style = determine_style(service["name"])
        location = service.get("custom_location_text", LOCATION)

        recurring_dates = get_recurring_dates(
            service["start_time"], start_date, end_date
        )

        for class_date in recurring_dates:
            start_dt = datetime.combine(class_date, class_time)
            end_dt = start_dt + timedelta(minutes=duration_min)

            class_data = {
                "serviceId": f"twoswagg_{service['id']}_{class_date.isoformat()}",
                "start": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "choreo": {"name": instructor, "instagram": ""},
                "name": service["name"],
                "location": location,
                "level": level,
                "style": style,
            }
            formatted_classes.append(class_data)

    print(f"✓ Scraped {len(formatted_classes)} classes from 2Swagg Studio")
    return formatted_classes


def twoswagg(start_date, end_date):
    """Fetch 2Swagg Studio schedule data and sync to API."""
    api_client = DanceClassAPI()

    classes = scrape_twoswagg_classes(start_date, end_date)

    if not classes:
        return {"created": 0, "updated": 0, "errors": []}

    transformed = [
        transform_class_data(cls, "2Swagg Studio", BOOKING_URL)
        for cls in classes
    ]

    result = api_client.sync_classes("twoswagg", transformed)
    return result


if __name__ == "__main__":
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = today + timedelta(days=(7 + 6 - today.weekday() + 1))

    result = twoswagg(monday, sunday)
    print(f"Result: {result}")
