import requests
import json
from helper import get_or_create_choreographer, determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data

def movement(start_date, end_date):
    """
    Scrape Movement Nation classes and sync to database
    """
    api_client = DanceClassAPI()
    
    # Hurstville location
    hurstville_url = "https://www.movementnationdancestudio.com"
    hurstville_classes = scrape_movement_nation(
        hurstville_url, 
        start_date, 
        end_date
    )
    
    # Transform and sync
    if hurstville_classes:
        transformed = [
            transform_class_data(
                cls, 
                "Movement Nation Hurstville",
                hurstville_url
            ) 
            for cls in hurstville_classes
        ]
        
        result = api_client.sync_classes("movement_nation_hurstville", transformed)
        print(f"✅ Hurstville: Created {result['created']}, Updated {result['updated']}, Errors {len(result['errors'])}")
    
    # Parramatta location
    parramatta_url = "https://2020movementnation.wixsite.com/website-1"
    parramatta_classes = scrape_movement_nation(
        parramatta_url, 
        start_date, 
        end_date
    )
    
    # Transform and sync
    if parramatta_classes:
        transformed = [
            transform_class_data(
                cls, 
                "Movement Nation Parramatta",
                parramatta_url
            ) 
            for cls in parramatta_classes
        ]
        
        result = api_client.sync_classes("movement_nation_parramatta", transformed)
        print(f"✅ Parramatta: Created {result['created']}, Updated {result['updated']}, Errors {len(result['errors'])}")


def scrape_movement_nation(url: str, start_date, end_date) -> list:
    """
    Scrape classes from Movement Nation (extracted from getData function)
    
    Returns:
        List of class dictionaries
    """
    # Get auth token
    auth_token = getAuthToken(url)
    if not auth_token:
        print(f"❌ Failed to get auth token for {url}")
        return []
    
    print(f"✓ Received auth token for {url}")
    
    # Get bulk data (services)
    bulk = get_bulk_data(auth_token, url)
    if not bulk:
        return []
    
    # Extract service IDs
    service_ids = [
        service['service']['id'] 
        for service in bulk["responseServices"]['services']
    ]
    
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
    
    print(f"✓ Scraped {len(classes)} classes from {url}")
    return classes


def getAuthToken(url):
    """Get authentication token (unchanged)"""
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
    })

    if r.status_code != 200:
        print(f"❌ Error getting auth: {r.status_code}")
        return None
    
    for key, item in r.json()["apps"].items():
        return item["instance"]


def get_bulk_data(auth: str, url: str):
    """Get bulk service data"""
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
    })

    if r.status_code != 200:
        print(f"❌ Error getting bulk data: {r.status_code}")
        return None
    
    return r.json()


def get_availability(auth: str, url: str, service_ids: list, start_date, end_date):
    """Query availability for services"""
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
    })

    if r.status_code != 200:
        print(f"❌ Error querying availability: {r.status_code}")
        return None
    
    return r.json()