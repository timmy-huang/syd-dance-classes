import requests
import json
import re

# pre sure these guys use square space

# They seem to use a widget within their squarespace called mindbody which is some sort of scheduling software
# We can use their js call "load_markup" to get the data
# /widgets/schedules/86397/load_markup?callback=jQuery36408016788701280633_1713673043345&options%5Bstart_date%5D=2024-04-21&_=1713673043348

# curl ^"https://widgets.mindbodyonline.com/widgets/schedules/86397/load_markup?callback=jQuery36408016788701280633_1713673043345&options^%^5Bstart_date^%^5D=2024-04-21&_=1713673043348^" ^
#   -H "accept: */*" ^
#   -H "accept-language: en-US,en;q=0.9" ^
#   -H "referer: https://imient.com.au/" ^
#   -H ^"sec-ch-ua: ^\^"Google Chrome^\^";v=^\^"123^\^", ^\^"Not:A-Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"123^\^"^" ^
#   -H "sec-ch-ua-mobile: ?1" ^
#   -H ^"sec-ch-ua-platform: ^\^"Android^\^"^" ^
#   -H "sec-fetch-dest: script" ^
#   -H "sec-fetch-mode: no-cors" ^
#   -H "sec-fetch-site: cross-site" ^
#   -H "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
  

def imi(callback, start_date, _id, location):
    url = "https://widgets.mindbodyonline.com/widgets/schedules/86397/load_markup"
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
    # print(class_names)

    # Extract start times
    start_times = re.findall(r'timeclass=\\"hc_starttime\\"datetime=\\"(.*?)\\"', html)
    # Extract end times
    end_times = re.findall(r'timeclass=\\"hc_endtime\\"datetime=\\"(.*?)\\"', html)

    # print(start_times)
    # print(end_times)

    # # Extract staff names
    staff = re.findall(r'divclass=\\"bw-session__staff\\"style=\\"\\"\\u003e\\n(.*?)\\n', html)
    # print(staff)

    data = []

    for i in range(len(class_names)):
        classData = {}
        classData["start"] = start_times[i]
        classData["end"] = end_times[i]
        classData["choreo"] = staff[i].split("|")[0]
        classData["choreoInsta"] = staff[i].split("|")[0]
        classData["name"] = class_names[i].replace("_", " ").title()
        # print("Class Name:", class_names[i])
        # print("Start Time:", start_times[i])
        # print("End Time:", end_times[i])
        # print("Staff:", staff[i])
        # print("-----")
        data.append(classData)

    formatted_json = json.dumps(data, indent=4)
    with open(location + "imi.json", 'w') as file:
        file.write(formatted_json)
