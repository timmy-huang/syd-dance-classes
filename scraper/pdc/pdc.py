import requests
import json
# Did not need to scrape the website as we could access the APIs
# Note that currently for authorisation, the token is hardcoded and will expire after a certain time
# Get new token from accessing webpage if it doesnt work

def pdc(location, start_date, end_date):
    hlocation = location + 'pdc.json'

    hurstvilleURL = "https://www.pdcdance.net"

    hauthToken = getAuthToken(hurstvilleURL)
    print("Recieved auth token for pdc")

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
    
    for key, item in r.json()["apps"].items():
        return item["instance"]
    
def getData(auth, location, url, start_date, end_date):
    # Get all the data
    # bulk

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
        print("Error Bulk: ", r.status_code)
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
        service_ids.append(service['id'])
        
    # print(service_ids)
        
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
        return

    # try:
    #     data = json.loads(r.text)
    #     formatted_json = json.dumps(data, indent=4)
    #     with open('query.txt', 'w') as file:
    #         file.write(formatted_json)
    # except json.JSONDecodeError:
    #     print("Response is not valid JSON.")

    query = r.json()

    data = []

    for slot in query["availabilityEntries"]:
        classData = {}
        classData["serviceId"] = slot["slot"]["serviceId"]
        classData["start"] = slot["slot"]["startDate"]
        classData["end"] = slot["slot"]["endDate"]
        classData["choreo"] = slot["slot"]["resource"]["name"]
        classData["location"] = slot["slot"]["location"]["formattedAddress"]
        classData["totalSpots"] = slot["totalSpots"]
        classData["openSpots"] = slot["openSpots"]

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