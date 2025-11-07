import requests
import json
import re
import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python < 3.9
    from backports.zoneinfo import ZoneInfo
from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def endless(start_date, end_date):
    """
    Fetch Endless Dance schedule data and sync to API.
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_endless_classes(start_date, end_date)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "Endless Dance",
            "https://endlessdance.com.au/classes"
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("endless", transformed)
    return result


def scrape_endless_classes(start_date, end_date):
    """
    Scrape Endless Dance classes from Firestore API
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        List of class dictionaries
    """
    # Convert date objects to ISO format strings with timezone
    start_date_str = f"{start_date.isoformat()}T00:00:00.000000000Z"
    end_date_str = f"{end_date.isoformat()}T23:59:59.999999999Z"
    
    ver = "8"
    
    # Step 1: Get SID and gsessionid
    url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?VER=8&database=projects%2Fendless-demo-lh8xa7%2Fdatabases%2F(default)&RID=16256&CVER=22&X-HTTP-Session-Id=gsessionid&zx=auywsytmpiax&t=1"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://endlessdance.com.au",
        "priority": "u=1, i",
        "referer": "https://endlessdance.com.au/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-fetch-storage-access": "active",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    }
    
    # Prepare form data
    form_data = {
        "X-Goog-Api-Client": "gl-js/ fire/10.11.1",
        "Content-Type": "text/plain",
        "X-Firebase-GMPID": "1:815212911105:web:9c0a28f5b222c0b50ffe00",
        "req0___data__": json.dumps({
            "database": "projects/endless-demo-lh8xa7/databases/(default)",
            "addTarget": {
                "query": {
                    "structuredQuery": {
                        "from": [{"collectionId": "lessons"}],
                        "where": {
                            "compositeFilter": {
                                "op": "AND",
                                "filters": [
                                    {
                                        "fieldFilter": {
                                            "field": {"fieldPath": "is_user_based"},
                                            "op": "EQUAL",
                                            "value": {"booleanValue": False}
                                        }
                                    },
                                    {
                                        "fieldFilter": {
                                            "field": {"fieldPath": "start_date_time"},
                                            "op": "GREATER_THAN",
                                            "value": {"timestampValue": start_date_str}
                                        }
                                    },
                                    {
                                        "fieldFilter": {
                                            "field": {"fieldPath": "start_date_time"},
                                            "op": "LESS_THAN_OR_EQUAL",
                                            "value": {"timestampValue": end_date_str}
                                        }
                                    }
                                ]
                            }
                        },
                        "orderBy": [
                            {
                                "field": {"fieldPath": "start_date_time"},
                                "direction": "ASCENDING"
                            },
                            {
                                "field": {"fieldPath": "__name__"},
                                "direction": "ASCENDING"
                            }
                        ]
                    },
                    "parent": "projects/endless-demo-lh8xa7/databases/(default)/documents"
                },
                "targetId": 2
            }
        })
    }
    
    try:
        # Get session credentials
        response = requests.post(url, headers=headers, data=form_data, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️  Endless session request failed with status code {response.status_code}")
            return []
        
        data = json.loads(response.text.split()[1])
        sid = data[0][1][1]
        gsessionid = response.headers["X-Http-Session-Id"]
        
        print(f"✓ Got Endless session (SID: {sid[:8]}...)")
        
        # Step 2: Get classes using session credentials
        url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?gsessionid={gsessionid}&VER=8&database=projects%2Fendless-demo-lh8xa7%2Fdatabases%2F(default)&RID=rpc&SID={sid}&AID=0&CI=0&TYPE=xmlhttp&zx=apcursuep04w&t=1"
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️  Endless classes request failed with status code {response.status_code}")
            return []
        
        # Parse the response
        classes = parse_endless_response_text(response.text)
        
        print(f"✓ Scraped {len(classes)} classes from Endless Dance Studio")
        return classes
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping Endless: {e}")
        return []
    except Exception as e:
        print(f"❌ Error processing Endless data: {e}")
        return []


def parse_endless_response_text(content):
    """
    Parse Endless Dance Firestore API response
    
    Args:
        content: Response text from Firestore API
        
    Returns:
        List of class dictionaries
    """
    # Skip the first line which is just a number
    if content.strip() and content.strip()[0].isdigit():
        content = content.split('\n', 1)[1] if '\n' in content else content
    
    try:
        # Find the first '[' which should be the start of our JSON array
        json_start = content.find('[[')
        if json_start == -1:
            print("⚠️  Could not find start of JSON array in Endless response")
            return []
        
        # Find the matching closing brackets for the outermost array
        bracket_count = 0
        json_end = -1
        
        for i in range(json_start, len(content)):
            if content[i] == '[':
                bracket_count += 1
            elif content[i] == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    json_end = i + 1
                    break
        
        if json_end == -1:
            print("⚠️  Could not find end of JSON array in Endless response")
            return []
        
        # Extract just the JSON part
        json_content = content[json_start:json_end]
        
        # Parse the extracted JSON
        data = json.loads(json_content)
        
        classes = []
        
        # Iterate through the response to find document changes
        for item in data:
            if len(item) > 1 and isinstance(item[1], list):
                for doc_item in item[1]:
                    if "documentChange" in doc_item:
                        doc = doc_item["documentChange"]["document"]
                        fields = doc["fields"]
                        
                        # Extract choreographer name from title
                        title = fields["title"]["stringValue"]
                        choreo_name = title.split('/')[0].strip() if '/' in title else "Unknown"
                        
                        # Remove name from title
                        class_name = title.split('/')[1].strip() if '/' in title else title
                        
                        # Create choreographer object (backend API handles creation)
                        choreographer = {
                            "name": choreo_name,
                            "instagram": ""
                        }
                        
                        # Extract start time
                        start_time = fields["start_date_time"]["timestampValue"]
                        # Parse UTC timestamp from Firestore
                        start_datetime_utc = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        
                        # Convert from UTC to Australia/Sydney timezone
                        sydney_tz = ZoneInfo("Australia/Sydney")
                        start_datetime = start_datetime_utc.astimezone(sydney_tz)
                        
                        # Calculate end time based on minutes
                        minutes = int(fields["minutes"]["integerValue"])
                        end_datetime = start_datetime + datetime.timedelta(minutes=minutes)
                        
                        # Extract location
                        location_detail = fields["location"]["mapValue"]["fields"]["detail"]["stringValue"]
                        location_title = fields["location"]["mapValue"]["fields"]["title"]["stringValue"]
                        location_str = f"{location_title}, {location_detail}"
                        
                        # Extract level
                        level_str = fields["level"]["mapValue"]["fields"]["title"]["stringValue"]
                        level = determine_level(level_str)
                        
                        # Determine style
                        style = determine_style(class_name)
                        
                        # Extract serviceId from document name (the Firestore document ID)
                        service_id = doc["name"].split('/')[-1]
                        
                        # Create class data
                        class_data = {
                            "serviceId": service_id,
                            "start": start_datetime.isoformat(),
                            "end": end_datetime.isoformat(),
                            "choreo": choreographer,
                            "name": class_name,
                            "location": location_str,
                            "level": level,
                            "style": style,
                            "totalSpots": int(fields["max_ppl"]["integerValue"]),
                            "openSpots": int(fields["max_ppl"]["integerValue"]) - int(fields["booked_ppl"]["integerValue"])
                        }
                        
                        classes.append(class_data)
        
        return classes
    
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing Endless JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Error processing Endless data: {e}")
        return []


if __name__ == "__main__":
    # Example usage for testing
    from datetime import date, timedelta
    
    today = date.today()
    end = today + timedelta(days=14)
    
    result = endless(today, end)
    print(f"Result: {result}")