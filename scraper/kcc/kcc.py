import requests
import json
import re
from helper import get_or_create_choreographer, determine_level, determine_style


def kcc(callback, start_date, _id, location):
    url = "https://widgets.mindbodyonline.com/widgets/schedules/182160/load_markup"
    params = {
        "callback": callback,
        "options[start_date]": start_date,
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
        "referrer": "(link unavailable)",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }

    html = requests.get(url, params=params, headers=headers).text.replace(" ", "")

    # Extract class names
    class_names = re.findall(r'data-bw-widget-mbo-class-name=\\"(.*?)\\"', html)
    
    # Extract start times
    start_times = re.findall(r'timeclass=\\"hc_starttime\\"datetime=\\"(.*?)\\"', html)
    # Extract end times
    end_times = re.findall(r'timeclass=\\"hc_endtime\\"datetime=\\"(.*?)\\"', html)

    # Extract staff names
    staff = re.findall(r'divclass=\\"bw-session__staff\\"style=\\"\\"\\u003e\\n(.*?)\\n', html)

    data = []

    for i in range(len(class_names)):
        name = staff[i].split("|")[0]
        insta = staff[i].split("|")[1]
        
        # Get or create choreographer object
        choreographer = get_or_create_choreographer(name, insta)

        classData = {
            "start": start_times[i],
            "end": end_times[i],
            "choreo": choreographer,
            "name": class_names[i].replace("_", " ").title(),
            "level": determine_level(class_names[i].replace("_", " ").title()),
            "style": determine_style(class_names[i].replace("_", " ").title())
        }
        
        print(classData)
        data.append(classData)

    formatted_json = json.dumps(data, indent=4)
    with open(location + "kcc.json", 'w+') as file:
        file.write(formatted_json)

    print("Scraped KCC")