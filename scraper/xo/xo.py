import requests
import json
import re
from datetime import datetime
from helper import get_or_create_choreographer, determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def xo():
    """
    Fetch CrossOver Dance schedule data and sync to API.
    
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_xo_classes()
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "CrossOver Dance Studio",
            "https://www.crossoverdance.com.au"  # Replace with actual URL
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("crossover", transformed)
    return result


def scrape_xo_classes():
    """
    Scrape CrossOver Dance classes from MindBody JSON widget
    
    Returns:
        List of class dictionaries
    """
    url = "https://widgets.mindbodyonline.com/widgets/schedules/9b4010856f8.json"
    
    params = {
        "mobile": "false",
        "version": "0.1"
    }
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "referrer": "https://www.crossoverdance.com.au",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️  CrossOver request failed with status code {response.status_code}")
            return []
        
        html = response.json()["contents"]
        
        # Find all class rows with regex
        class_rows = re.findall(
            r'<tr[^>]*class="[^"]*filterable[^"]*"[^>]*data-hc-mbo-class-name="([^"]*)".*?'
            r'hc_starttime"[^>]*data-datetime="&quot;([^"]+)&quot;".*?'
            r'hc_endtime"[^>]*data-datetime="&quot;([^"]+)&quot;".*?'
            r'classname[^>]*><a[^>]*>([^<]+)</a>.*?'
            r'trainer"><a[^>]*>([^<]+)</a>',
            html,
            re.DOTALL
        )
        
        # TODO: Extract actual session/class ID from CrossOver MindBody widget
        # Currently using class_name_raw as a temporary identifier
        # Look for data attributes like: data-class-id, data-session-id, etc.
        session_id_pattern = re.findall(
            r'<tr[^>]*data-hc-mbo-class-id="([^"]*)"',
            html
        )
        
        formatted_classes = []
        for i, (class_name_raw, start_time, end_time, display_name, trainer) in enumerate(class_rows):
            # Get or create choreographer object
            choreographer = get_or_create_choreographer(trainer.strip())
            
            # Parse datetime strings
            start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f%z')
            end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
            
            # Try to find session ID
            # TODO: Update this when you find the correct ID field in the HTML
            if session_id_pattern and i < len(session_id_pattern):
                service_id = session_id_pattern[i]
            else:
                # Temporary fallback - log warning
                print(f"⚠️  CrossOver class '{display_name.strip()}' missing session ID")
                print(f"   Using class name as temporary ID: {class_name_raw}")
                print(f"   Please inspect HTML to find correct ID field")
                service_id = class_name_raw
            
            class_data = {
                "serviceId": str(service_id),
                "start": start.isoformat(),
                "end": end.isoformat(),
                "choreo": choreographer,
                "name": display_name.strip(),
                "location": "CrossOver Dance Studio",
                "level": determine_level(display_name.strip()),
                "style": determine_style(display_name.strip())
            }
            formatted_classes.append(class_data)
        
        print(f"✓ Scraped {len(formatted_classes)} classes from CrossOver")
        return formatted_classes
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping CrossOver: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing CrossOver JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Error processing CrossOver data: {e}")
        return []


if __name__ == "__main__":
    # Example usage for testing
    result = xo()
    print(f"Result: {result}")