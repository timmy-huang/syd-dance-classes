import requests
import json
import re
from datetime import datetime

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
        # Parse the class name to extract information
        name_parts = display_name.split('|')
        
        print(display_name)
        
        # Extract level from the class name
        level = []
        level_indicators = ['Beg', 'Int', 'Adv', 'Open']
        for indicator in level_indicators:
            if indicator.lower() in display_name.lower():
                level.append(indicator)
        
        # Parse datetime strings
        start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        
        class_data = {
            "serviceId": class_name_raw,  # Using the raw class name as serviceId
            "start": start.strftime('%Y-%m-%d %H:%M:%S'),
            "end": end.strftime('%Y-%m-%d %H:%M:%S'),
            "choreo": trainer.strip(),
            "choreoInsta": trainer.strip(),  # Using same as choreo if no Instagram handle available
            "name": display_name.strip(),
            "studio": "Crossover",  # Hardcoded as this is specifically for Crossover
        }
        formatted_classes.append(class_data)

    formatted_json = json.dumps(formatted_classes, indent=4)
    with open(location + "crossover.json", 'w') as file:
        file.write(formatted_json)

    print("Scraped Crossover")