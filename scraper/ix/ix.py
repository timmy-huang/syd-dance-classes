import requests
import json
from helper import get_or_create_choreographer, determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def ix(start_date, end_date):
    """
    Fetch IX Dance Studio schedule data and sync to API.
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_ix_classes(start_date, end_date)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "IX",
            "https://www.ixdancestudio.com/booking"
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("ix", transformed)
    return result


def scrape_ix_classes(start_date, end_date):
    """
    Scrape IX Dance Studio classes from Wix Bookings API
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        List of class dictionaries
    """
    url = "https://www.ixdancestudio.com"
    
    # Get auth token
    auth_token = getAuthToken(url)
    if not auth_token:
        print("❌ Failed to get auth token for IX")
        return []
    
    print("✓ Received auth token for IX")
    
    # Get bulk data (services)
    bulk = get_bulk_data(auth_token, url)
    if not bulk:
        return []
    
    # Extract service IDs (filter out hidden services)
    service_ids = []
    for service in bulk["responseServices"]['services']:
        service_obj = service['service']
        # IX specific: skip hidden services
        if service_obj.get("customProperties", {}).get("uouHidden") == "true":
            continue
        service_ids.append(service_obj['id'])
    
    if not service_ids:
        print("⚠️  No visible services found for IX")
        return []
    
    # Query availability
    query = get_availability(auth_token, url, service_ids, start_date, end_date)
    if not query:
        return []
    
    # Process and structure data
    classes = []
    for slot in query["availabilityEntries"]:
        choreographer = get_or_create_choreographer(slot["slot"]["resource"]["name"])
        
        class_data = {
            "serviceId": slot["slot"]["serviceId"],
            "start": slot["slot"]["startDate"],
            "end": slot["slot"]["endDate"],
            "choreo": choreographer,
            "location": slot["slot"]["location"]["formattedAddress"],
            "totalSpots": slot["totalSpots"],
            "openSpots": slot["openSpots"]
        }
        
        # Find service name from bulk data
        for service in bulk["responseServices"]['services']:
            if service["service"]['id'] == class_data["serviceId"]:
                class_data["name"] = service["service"]["info"]["name"]
                break
        
        # Add level and style
        class_data["level"] = determine_level(class_data["name"])
        class_data["style"] = determine_style(class_data["name"])
        
        classes.append(class_data)
    
    print(f"✓ Scraped {len(classes)} classes from IX")
    return classes


def getAuthToken(url):
    """Get authentication token from Wix"""
    try:
        r = requests.get(url + '/_api/v1/access-tokens', headers={
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "ssr-caching=cache#desc=miss#varnish=miss_miss#dc#desc=fastly_42_g",
            "priority": "u=1, i",
            "referer": url,
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
        }, timeout=30)

        if r.status_code != 200:
            print(f"❌ Error getting IX auth token: {r.status_code}")
            return None

        # Skip first app, use second one (IX specific)
        skip_first = True
        for key, item in r.json()["apps"].items():
            if skip_first:
                skip_first = False
                continue
            return item["instance"]
        
        return None
    
    except Exception as e:
        print(f"❌ Error getting IX auth token: {e}")
        return None


def get_bulk_data(auth, url):
    """Get bulk service data from Wix Bookings"""
    try:
        r = requests.post((url + '/_api/services-catalog/bulk'), headers={
            "authorization": auth,
            "commonconfig": "%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%221aebc0fe-8af4-452a-9ec0-4fff44cd9558%7C2%22%2C%22siteRevision%22%3A%22932%22%2C%22renderingFlow%22%3A%22NONE%22%2C%22language%22%3A%22en%22%2C%22locale%22%3A%22en-au%22%7D",
            "content-type": "application/json",
            "referer": "https://www.ixdancestudio.com/_partials/wix-thunderbolt/dist/clientWorker.404350a0.bundle.min.js",
            "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 CrKey/1.54.250320",
            "x-wix-brand": "wix",
            "x-wix-client-artifact-id": "bookings-viewer-script"
        }, json={
            "requestServices": {
                "includeDeleted": False,
                "query": {
                    "fieldsets": [],
                    "filter": "{\"schedules.tags\": \"GROUP\"}",
                    "paging": {"limit": 500},
                    "fields": [],
                    "sort": []
                }
            },
            "requestBusiness": {
                "suppressNotFoundError": False
            },
            "requestListResources": {
                "query": {
                    "fieldsets": [],
                    "filter": None,
                    "paging": {"limit": 500},
                    "fields": [],
                    "sort": []
                }
            }
        }, timeout=30)

        if r.status_code != 200:
            print(f"❌ Error getting IX bulk data: {r.status_code}")
            print(r.text)
            return None
        
        return r.json()
    
    except Exception as e:
        print(f"❌ Error getting IX bulk data: {e}")
        return None


def get_availability(auth, url, service_ids, start_date, end_date):
    """Query availability for IX services"""
    try:
        r = requests.post(url + '/_api/availability-calendar/v1/availability/query', headers={
            "authorization": auth,
            "commonconfig": "%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%22f1cdc301-a785-4f39-8430-3eecd21e9537%7C1%22%7D",
            "content-type": "application/json",
            "x-wix-brand": "wix",
            "x-wix-client-artifact-id": "bookings-viewer-script"
        }, json={
            "timezone": "Australia/Sydney",
            "query": {
                "filter": {
                    "serviceId": service_ids,
                    "startDate": start_date.isoformat(),
                    "endDate": end_date.isoformat()
                }
            }
        }, timeout=30)

        if r.status_code != 200:
            print(f"❌ Error querying IX availability: {r.status_code}")
            print(r.text)
            return None
        
        return r.json()
    
    except Exception as e:
        print(f"❌ Error querying IX availability: {e}")
        return None


if __name__ == "__main__":
    # Example usage for testing
    from datetime import date, timedelta
    
    today = date.today()
    end = today + timedelta(days=14)
    
    result = ix(today, end)
    print(f"Result: {result}")