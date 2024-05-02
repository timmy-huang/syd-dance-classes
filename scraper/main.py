import requests
import json

# Did not need to scrape the website as we could access the APIs
# Note that currently for authorisation, the token is hardcoded and will expire after a certain time
# Get new token from accessing webpage if it doesnt work

mnauth = "6Smub3RuBJwNtNwjySqEepcqBzZpIgOke4wIQbXouBA.eyJpbnN0YW5jZUlkIjoiZjI4MWM2ZjItOGMxMy00ZDRmLTlmYWMtYjgwYTE1NTZlZmIxIiwiYXBwRGVmSWQiOiIxM2QyMWM2My1iNWVjLTU5MTItODM5Ny1jM2E1ZGRiMjdhOTciLCJtZXRhU2l0ZUlkIjoiMzQyMGE5MjktMzUwYy00NGFkLWE1M2ItMmM0NTQ1NzMyNjM2Iiwic2lnbkRhdGUiOiIyMDI0LTA1LTAyVDEwOjE2OjQ3Ljk3NVoiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJib29raW5ncyIsImRlbW9Nb2RlIjpmYWxzZSwiYWlkIjoiZGMzNmZmZDktMDFhYy00MGJjLWJiOTMtMGYzOTJiMjU4YzMzIiwiYmlUb2tlbiI6ImM2YTE2ZmRiLWI5MWYtMDllMi0zYTk3LTk0NGY1MDI1Yzk4NyIsInNpdGVPd25lcklkIjoiZTQ1NDYxYzMtNjRhZC00ZDlmLTg0NGUtNzc0MGJjMjU2NGE2In0"


# Get all the data
# bulk

r = requests.post('https://www.movementnation.com.au/_api/services-catalog/bulk', headers={
    "authorization": mnauth,
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
    exit()

try:
    data = json.loads(r.text)
    formatted_json = json.dumps(data, indent=4)
    with open('bulk.txt', 'w') as file:
        file.write(formatted_json)
except json.JSONDecodeError:
    print("Response is not valid JSON.")
    
bulk = r.json()

# Query
# Get a list of service ids from bulk.txt and use them in the query
    
#print(bulk)
service_ids = []
for service in bulk["responseServices"]['services']:
    service = service['service']
    service_ids.append(service['id'])
    
# print(service_ids)
    
r = requests.post('https://www.movementnation.com.au/_api/availability-calendar/v1/availability/query', headers={
    "authorization": mnauth,
    "commonconfig": "%7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%22f1cdc301-a785-4f39-8430-3eecd21e9537%7C1%22%7D",
    "content-type": "application/json",
    "x-wix-brand": "wix",
    "x-wix-client-artifact-id": "bookings-viewer-script"
}, json={
    "timezone": "Australia/Sydney",
    "query": {
        "filter": {
            "serviceId": service_ids,
            "startDate": "2024-04-21T00:00:00.000Z",
            "endDate": "2024-04-28T23:59:59.000Z",
        }
    }
})

if r.status_code != 200:
    print("Error Query: ", r.status_code)
    exit()

try:
    data = json.loads(r.text)
    formatted_json = json.dumps(data, indent=4)
    with open('query.txt', 'w') as file:
        file.write(formatted_json)
except json.JSONDecodeError:
    print("Response is not valid JSON.")

query = r.json()

# Link query and json information
# Output it as good stuff in a file

# Data structure of classData
# {
#     "serviceId": "string",
#     "start": "string",
#     "end": "string",
#     "choreo": "string",
#     "location": "string",
#     "totalSpots": "int",
#     "openSpots": "int",
#     "name": "string",
#     "description": "string"
# }



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

    print(classData)
    print()

    data.append(classData) 

formatted_json = json.dumps(data, indent=4)
with open('../sydney-dance-classes/data/mn-hurstville.json', 'w') as file:
    file.write(formatted_json)