import requests
import json
from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def pdc(start_date, end_date):
    """
    Fetch PDC Dance schedule data and sync to API.
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_pdc_classes(start_date, end_date)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "PDC",
            "https://www.pdcdance.net"
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("pdc", transformed)
    return result


def scrape_pdc_classes(start_date, end_date):
    """
    Scrape PDC Dance classes from Wix Bookings API
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        List of class dictionaries
    """
    url = "https://www.pdcdance.net"
    
    # Get auth token
    auth_token = getAuthToken(url)
    if not auth_token:
        print("❌ Failed to get auth token for PDC")
        return []
    
    print("✓ Received auth token for PDC")
    
    # Get bulk data (services)
    bulk = get_bulk_data(auth_token, url)
    if not bulk:
        return []
    
    # Extract service IDs
    service_ids = [
        service['service']['id'] 
        for service in bulk["responseServices"]['services']
    ]
    
    if not service_ids:
        print("⚠️  No services found for PDC")
        return []
    
    # Query availability
    query = get_availability(auth_token, url, service_ids, start_date, end_date)
    if not query:
        return []
    
    # Process and structure data
    classes = []
    for slot in query["availabilityEntries"]:
        choreographer = {"name": slot["slot"]["resource"]["name"], "instagram": ""}
        
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
    
    print(f"✓ Scraped {len(classes)} classes from PDC")
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
            print(f"❌ Error getting PDC auth token: {r.status_code}")
            return None
        
        # Use first app (unlike IX which skips first)
        for key, item in r.json()["apps"].items():
            return item["instance"]
        
        return None
    
    except Exception as e:
        print(f"❌ Error getting PDC auth token: {e}")
        return None


def get_bulk_data(auth, url):
    """Get bulk service data from Wix Bookings"""
    try:
        r = requests.post((url + '/_api/services-catalog/bulk'), headers={
            "authorization": auth,
            "commonconfig": "%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%22f1cdc301-a785-4f39-8430-3eecd21e9537%7C1%22%7D",
            "content-type": "application/json",
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
            print(f"❌ Error getting PDC bulk data: {r.status_code}")
            return None
        
        return r.json()
    
    except Exception as e:
        print(f"❌ Error getting PDC bulk data: {e}")
        return None


def get_availability(auth, url, service_ids, start_date, end_date):
    """Query availability for PDC services"""
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
            print(f"❌ Error querying PDC availability: {r.status_code}")
            return None
        
        return r.json()
    
    except Exception as e:
        print(f"❌ Error querying PDC availability: {e}")
        return None


if __name__ == "__main__":
    # Example usage for testing
    from datetime import date, timedelta
    
    today = date.today()
    end = today + timedelta(days=14)
    
    result = pdc(today, end)
    print(f"Result: {result}")