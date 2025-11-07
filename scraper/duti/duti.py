import requests
import json
import re
from helper import get_or_create_choreographer, determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def duti(callback, start_date, _id):
    """
    Fetch Duti Dance schedule data and sync to API.
    
    Args:
        callback: jQuery callback string
        start_date: datetime.date object
        _id: Request ID string
        
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_duti_classes(callback, start_date, _id)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "DUTI",
            "https://www.dutistudios.com.au/timetable"
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("duti", transformed)
    return result


def scrape_duti_classes(callback, start_date, _id):
    """
    Scrape Duti Dance classes from MindBody widget
    
    Args:
        callback: jQuery callback string
        start_date: datetime.date object
        _id: Request ID string
        
    Returns:
        List of class dictionaries
    """
    url = "https://widgets.mindbodyonline.com/widgets/schedules/68257/load_markup"
    
    # Convert date to string format expected by API
    date_str = start_date.strftime("%Y-%m-%d")
    
    params = {
        "callback": callback,
        "options[start_date]": date_str,
        "_": _id
    }
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "referrer": "https://www.dutidance.com",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️  Duti request failed with status code {response.status_code}")
            return []
        
        html = response.text.replace(" ", "")
        
        # Extract session IDs (the unique identifier for each class)
        session_ids = re.findall(r'data-bw-widget-id=\\"(.*?)\\"', html)
        
        # Extract class names
        class_names = re.findall(r'data-bw-widget-mbo-class-name=\\"(.*?)\\"', html)
        
        # Extract start times
        start_times = re.findall(r'timeclass=\\"hc_starttime\\"datetime=\\"(.*?)\\"', html)
        
        # Extract end times
        end_times = re.findall(r'timeclass=\\"hc_endtime\\"datetime=\\"(.*?)\\"', html)
        
        # Extract staff names
        staff = re.findall(r'divclass=\\"bw-session__staff\\"style=\\"\\"\\u003e\\n(.*?)\\n', html)
        
        # Validate we have matching data
        if not (len(session_ids) == len(class_names) == len(start_times) == len(end_times) == len(staff)):
            print(f"⚠️  Duti data mismatch:")
            print(f"   Session IDs: {len(session_ids)}")
            print(f"   Class names: {len(class_names)}")
            print(f"   Start times: {len(start_times)}")
            print(f"   End times: {len(end_times)}")
            print(f"   Staff: {len(staff)}")
            return []
        
        data = []
        for i in range(len(class_names)):
            name = staff[i].split("|")[0]
            # Normalize DUTI name by adding a space before capital letters except for the first letter
            name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
            
            choreographer = get_or_create_choreographer(name)
            
            classData = {
                "serviceId": str(session_ids[i]),
                "start": start_times[i],
                "end": end_times[i],
                "choreo": choreographer,
                "name": class_names[i].replace("_", " ").title(),
                "location": "DUTI Studios",
                "level": determine_level(class_names[i].replace("_", " ").title()),
                "style": determine_style(class_names[i].replace("_", " ").title())
            }
            data.append(classData)
        
        print(f"✓ Scraped {len(data)} classes from Duti")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping Duti: {e}")
        return []
    except Exception as e:
        print(f"❌ Error parsing Duti data: {e}")
        return []


if __name__ == "__main__":
    # Example usage for testing
    from datetime import date
    
    callback = "jQuery364011093063789286006_1740274810344"
    _id = "1740274810346"
    
    result = duti(callback, date.today(), _id)
    print(f"Result: {result}")