import requests
import json

# Did not need to scrape the website as we could access the APIs
# Note that currently for authorisation, the token is hardcoded and will expire after a certain time
# Get new token from accessing webpage if it doesnt work


# Get all the data
# bulk

r = requests.post('https://www.movementnation.com.au/_api/services-catalog/bulk', headers={
    "authorization": "GJkZRwSwZfdauOp1iNmj0us5NGdDt7LfeeuQ9MQ7GLA.eyJpbnN0YW5jZUlkIjoiZjI4MWM2ZjItOGMxMy00ZDRmLTlmYWMtYjgwYTE1NTZlZmIxIiwiYXBwRGVmSWQiOiIxM2QyMWM2My1iNWVjLTU5MTItODM5Ny1jM2E1ZGRiMjdhOTciLCJtZXRhU2l0ZUlkIjoiMzQyMGE5MjktMzUwYy00NGFkLWE1M2ItMmM0NTQ1NzMyNjM2Iiwic2lnbkRhdGUiOiIyMDI0LTA0LTIxVDAzOjUxOjI5LjcwMloiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJib29raW5ncyIsImRlbW9Nb2RlIjpmYWxzZSwiYWlkIjoiM2UzMWQ3ZWEtOGNiNS00M2RmLWE1YmUtNGY0NDY0ZmZhYmNjIiwiYmlUb2tlbiI6ImM2YTE2ZmRiLWI5MWYtMDllMi0zYTk3LTk0NGY1MDI1Yzk4NyIsInNpdGVPd25lcklkIjoiZTQ1NDYxYzMtNjRhZC00ZDlmLTg0NGUtNzc0MGJjMjU2NGE2In0",
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
    
print(service_ids)
    
r = requests.post('https://www.movementnation.com.au/_api/availability-calendar/v1/availability/query', headers={
    "authorization": "GJkZRwSwZfdauOp1iNmj0us5NGdDt7LfeeuQ9MQ7GLA.eyJpbnN0YW5jZUlkIjoiZjI4MWM2ZjItOGMxMy00ZDRmLTlmYWMtYjgwYTE1NTZlZmIxIiwiYXBwRGVmSWQiOiIxM2QyMWM2My1iNWVjLTU5MTItODM5Ny1jM2E1ZGRiMjdhOTciLCJtZXRhU2l0ZUlkIjoiMzQyMGE5MjktMzUwYy00NGFkLWE1M2ItMmM0NTQ1NzMyNjM2Iiwic2lnbkRhdGUiOiIyMDI0LTA0LTIxVDAzOjUxOjI5LjcwMloiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJib29raW5ncyIsImRlbW9Nb2RlIjpmYWxzZSwiYWlkIjoiM2UzMWQ3ZWEtOGNiNS00M2RmLWE1YmUtNGY0NDY0ZmZhYmNjIiwiYmlUb2tlbiI6ImM2YTE2ZmRiLWI5MWYtMDllMi0zYTk3LTk0NGY1MDI1Yzk4NyIsInNpdGVPd25lcklkIjoiZTQ1NDYxYzMtNjRhZC00ZDlmLTg0NGUtNzc0MGJjMjU2NGE2In0",
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

try:
    data = json.loads(r.text)
    formatted_json = json.dumps(data, indent=4)
    with open('query.txt', 'w') as file:
        file.write(formatted_json)
except json.JSONDecodeError:
    print("Response is not valid JSON.")