import requests

# pre sure these guys use square space

# They seem to use a widget within their squarespace called mindbody which is some sort of scheduling software
# They use this api call to get the stuff

# fetch("https://widgets.mindbodyonline.com/widgets/schedules/9b4010856f8.json?mobile=false&version=0.1", {
#   "headers": {
#     "accept": "*/*",
#     "accept-language": "en-US,en;q=0.9",
#     "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
#     "sec-ch-ua-mobile": "?1",
#     "sec-ch-ua-platform": "\"Android\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "cross-site"
#   },
#   "referrer": "https://www.crossoverdance.com/",
#   "referrerPolicy": "strict-origin-when-cross-origin",
#   "body": null,
#   "method": "GET",
#   "mode": "cors",
#   "credentials": "omit"
# });


r = requests.get('https://www.crossoverdance.com/timetable/')
print(r.text)
# Save to a file
with open('xo.txt', 'w', encoding='utf-8') as f:
    f.write(r.text)
  
