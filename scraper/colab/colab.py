import requests
from datetime import datetime
import json
from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def parse_nextjs_response(response_text):
    """
    Parse the Next.js Server Action response format.
    Response format is like: "0:data\n1:data\n2:data"
    """
    lines = response_text.strip().split('\n')
    parsed_data = {}
    
    for line in lines:
        if ':' in line:
            # Split only on first colon
            idx, data = line.split(':', 1)
            try:
                # Parse the JSON data
                parsed_data[idx] = json.loads(data)
            except json.JSONDecodeError:
                parsed_data[idx] = data
    
    return parsed_data


def colab(start_date, end_date):
    """
    Fetch Co-Lab Quarters schedule data and sync to API.
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_colab_classes(start_date, end_date)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "Co-Lab Quarters",
            "https://www.colabquarters.com.au"  # Replace with actual booking URL
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("colab", transformed)
    return result


def scrape_colab_classes(start_date, end_date):
    """
    Scrape Co-Lab Quarters classes
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        List of class dictionaries
    """
    # Convert date objects to ISO format with time
    # Assuming Sydney timezone (UTC+11)
    from_date = f"{start_date.isoformat()}T13:00:00.000Z"
    to_date = f"{end_date.isoformat()}T12:59:59.999Z"
    
    # API endpoint
    url = "https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/562306b3ba/schedule"
    
    # Headers
    headers = {
        "accept": "text/x-component",
        "accept-language": "en-US,en;q=0.9",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjIxMTg0NDkiLCJhcCI6IjE4MzUwMzcyMDIiLCJpZCI6IjdkODlhNzYxZTcwYThjNzgiLCJ0ciI6IjEzNzdlMDcyMzQyYTZhNjkxNGI2OGE0NTZmZTU5NmJlIiwidGkiOjE3NjI0ODQ0NDg0MTEsInRrIjoiODQ0NjcifX0=",
        "next-action": "4f5d69414e1b758541ec223c15d6e1f87de21681",
        "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%5B%22locale%22%2C%22en%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22widgets%22%2C%7B%22children%22%3A%5B%22schedules%22%2C%7B%22children%22%3A%5B%5B%22preview%22%2C%22view%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%5B%22widgetId%22%2C%22562306b3ba%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22schedule%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fcomponents%2Fwidgets%2Fschedules%2Fview%2F562306b3ba%2Fschedule%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%5D",
        "origin": "https://brandedweb-next.mindbodyonline.com",
        "priority": "u=1, i",
        "referer": "https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/562306b3ba/schedule",
        "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "traceparent": "00-1377e072342a6a6914b68a456fe596be-7d89a761e70a8c78-01",
        "tracestate": "84467@nr=0-1-2118449-1835037202-7d89a761e70a8c78----1762484448411",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36"
    }
    
    # Cookies
    cookies = {
        "_cfuvid": "ei498bJ0wHHIsFHc2a4JuFvTgaHYslQCnPvcAeN3CS8-1762484440221-0.0.1.1-604800000",
        "cf_clearance": "4wPFWdangUO8JbqdJ7X9DgK.8ybDQDOiYspCorDn2Jg-1762483832-1.2.1.1-2rmiwSLWHCQzJ_KVBMMq7FBDTm8jN9tV5xw.CtPWInxci9xipPjgePCS2zEnUmA9c7sDUyR3vaB7ci5z6N.QOVHHfD6AHbVQ3h_lnEWxNoeRJI.nCfvETZfCdnyHdqeLvSuP.hyJJkKokv91MZ5FF_HH6Cnz5ffjLC96a_3amCZ7t4l7GzqKWgyObQDCvYMTHZW7sopikS.HtsWglbu6tj1QV1XK3_sf6yxxENyLirg"
    }
    
    # The token - you'll need to update this periodically from your browser
    token = "Ls/jQ/npoH70XN8IDoO8KQgBvxV7/Kjuo9rMsTkD7O0ZAv19g2UOXStXdSIg6eulz2osoGeyliYC8esO3QKAaU2XCrD/XSAcThaqFa4yxXlpBp5bDuo43tiLEH1hzQ1qnxCdlVYmonomSZ70vUE1Bovxcpwp+3NacJjlfNYPVTUnvZjPet55kg+qVpTEC4iZLRKuqL2CIU7CE2vI"
    
    # Prepare multipart form data
    files = {
        '1': (None, f'"{token}"'),
        '0': (None, f'["$@1",{{"fromDate":"{from_date}","toDate":"{to_date}"}}]'),
    }
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies, files=files, timeout=30)
        
        if response.status_code != 200:
            raise Exception(
                f"Co-Lab request failed with status code {response.status_code}. "
                "Possible causes: expired token, invalid session, or server blocking request."
            )
        
        # Parse the Next.js response
        parsed = parse_nextjs_response(response.text)
        
        # The actual class data is in key "1"
        if '1' not in parsed:
            print("⚠️  No class data found in Co-Lab response")
            return []
        
        classes = parsed['1']
        data = []
        
        for class_item in classes:
            # Extract instructor information
            staff_list = class_item.get('staff', [])
            if staff_list:
                instructor = staff_list[0]
                name = instructor.get('displayLabel', 'Unknown')
                insta = ""  # Not available in API response
                choreographer = {"name": name, "instagram": insta}
            else:
                choreographer = {"name": "Unknown", "instagram": ""}
            
            # TODO: Find the actual serviceId/class ID from the Co-Lab API response
            # For now, skip classes without a proper ID
            service_id = class_item.get('id')
            
            if not service_id:
                print(f"⚠️  Skipping Co-Lab class '{class_item['name']}' - no serviceId found in API response")
                print(f"   Available fields: {list(class_item.keys())}")
                continue
            
            # Format the class data
            classData = {
                "serviceId": str(service_id),
                "start": class_item['startDateTime'],
                "end": class_item['endDateTime'],
                "choreo": choreographer,
                "name": class_item['name'],
                "location": class_item.get('location', {}).get('name', 'Co-Lab Quarters'),
                "level": determine_level(class_item['name']),
                "style": determine_style(class_item['name'])
            }
            data.append(classData)
        
        print(f"✓ Scraped {len(data)} classes from Co-Lab Quarters")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping Co-Lab: {e}")
        return []


if __name__ == "__main__":
    # Example usage for testing
    from datetime import date, timedelta
    
    today = date.today()
    end = today + timedelta(days=14)
    
    result = colab(today, end)
    print(f"Result: {result}")