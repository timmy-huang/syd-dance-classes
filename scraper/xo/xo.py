import requests
import json
import re
from datetime import datetime
from helper import get_or_create_choreographer, determine_level, determine_style

def xo(location):
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
        "referrer": "(link unavailable)",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }

    html = requests.get(url, params=params, headers=headers).json()["contents"]

    # Find all class rows
    class_rows = re.findall(r'<tr[^>]*class="[^"]*filterable[^"]*"[^>]*data-hc-mbo-class-name="([^"]*)".*?'
                           r'hc_starttime"[^>]*data-datetime="&quot;([^"]+)&quot;".*?'
                           r'hc_endtime"[^>]*data-datetime="&quot;([^"]+)&quot;".*?'
                           r'classname[^>]*><a[^>]*>([^<]+)</a>.*?'
                           r'trainer"><a[^>]*>([^<]+)</a>',
                           html, re.DOTALL)

    formatted_classes = []

    for class_name_raw, start_time, end_time, display_name, trainer in class_rows:
        # Get or create choreographer object
        choreographer = get_or_create_choreographer(trainer.strip())
        
        # Parse datetime strings
        start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        
        class_data = {
            "serviceId": class_name_raw,
            "start": start.strftime('%Y-%m-%d %H:%M:%S'),
            "end": end.strftime('%Y-%m-%d %H:%M:%S'),
            "choreo": choreographer,
            "name": display_name.strip(),
            "studio": "Crossover",
            "level": determine_level(display_name.strip()),
            "style": determine_style(display_name.strip())
        }
        formatted_classes.append(class_data)

    formatted_json = json.dumps(formatted_classes, indent=4)
    with open(location + "crossover.json", 'w+') as file:
        file.write(formatted_json)

    print("Scraped Crossover")