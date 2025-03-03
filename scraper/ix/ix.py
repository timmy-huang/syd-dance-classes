import requests
import json
from helper import get_or_create_choreographer
# Did not need to scrape the website as we could access the APIs
# Note that currently for authorisation, the token is hardcoded and will expire after a certain time
# Get new token from accessing webpage if it doesnt work

def ix(location, start_date, end_date):
    hlocation = location + 'ix.json'

    hurstvilleURL = "https://www.ixdancestudio.com"

    hauthToken = getAuthToken(hurstvilleURL)
    print("Recieved auth token for IX")

    getData(hauthToken, hlocation, hurstvilleURL, start_date, end_date)

def getAuthToken(url):
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
        print("Error getting auth: ", r.status_code)
        return

    skipper = 1

    for key, item in r.json()["apps"].items():
        if skipper == 1:
            skipper = 0
            continue
        return item["instance"]
    
def getData(auth, location, url, start_date, end_date):
    # Get all the data
    # bulk

    r = requests.post((url + '/_api/services-catalog/bulk'), headers={
        "authorization": auth,
        "commonconfig": "%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%221aebc0fe-8af4-452a-9ec0-4fff44cd9558%7C2%22%2C%22siteRevision%22%3A%22932%22%2C%22renderingFlow%22%3A%22NONE%22%2C%22language%22%3A%22en%22%2C%22locale%22%3A%22en-au%22%7D",
        "content-type": "application/json",
        "referer": "https://www.ixdancestudio.com/_partials/wix-thunderbolt/dist/clientWorker.404350a0.bundle.min.js",
        "user-agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 CrKey/1.54.250320",
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
        print("Error Bulk: ", r.status_code)
        print(r.text)
        return

    # try:
    #     data = json.loads(r.text)
    #     formatted_json = json.dumps(data, indent=4)
    #     with open('bulk.txt', 'w') as file:
    #         file.write(formatted_json)
    # except json.JSONDecodeError:
    #     print("Response is not valid JSON.")
        
    bulk = r.json()

    # Query
    # Get a list of service ids from bulk.txt and use them in the query
        
    #print(bulk)
    service_ids = []
    for service in bulk["responseServices"]['services']:
        service = service['service']
        # IX specific add here
        if service["customProperties"]["uouHidden"] == "true":
            continue
        service_ids.append(service['id'])
        
    # print(len(service_ids))
        
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
        print("Error Query: ", r.status_code)
        print(r.text)
        return

    query = r.json()
    
    data = []

    for slot in query["availabilityEntries"]:
        choreographer = get_or_create_choreographer(slot["slot"]["resource"]["name"])
        classData = {
            "serviceId": slot["slot"]["serviceId"],
            "start": slot["slot"]["startDate"],
            "end": slot["slot"]["endDate"],
            "choreo": choreographer,
            "location": slot["slot"]["location"]["formattedAddress"],
            "totalSpots": slot["totalSpots"],
            "openSpots": slot["openSpots"]
        }

        # find the corresponding service
        for service in bulk["responseServices"]['services']:
            if service["service"]['id'] == classData["serviceId"]:
                classData["name"] = service["service"]["info"]["name"]
                #classData["description"] = service["service"]["info"]["description"]

        data.append(classData) 

    formatted_json = json.dumps(data, indent=4)
    with open(location, 'w') as file:
        file.write(formatted_json)

    print("Scraped " + location)