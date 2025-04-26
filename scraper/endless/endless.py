import requests
import json
import re
#from helper import get_or_create_choreographer, determine_level, determine_style

# Things we need
# gsessionid
# VER
# database
# RID
# SID
# AID
# CI

"""
VER: 8
database: projects/endless-demo-lh8xa7/databases/(default)
RID: 473
CVER: 22
X-HTTP-Session-Id: gsessionid
zx: f0we3zugzjgv
t: 1

VER: 8
database: projects/endless-demo-lh8xa7/databases/(default)
RID: 16256
CVER: 22
X-HTTP-Session-Id: gsessionid
zx: suywsytmpiax
t: 1
"""



def endless(start_date, end_date):
  ver = "8"  
  
# TODO create form to send
  # Get SID and gsessionid and post form
  url = f"""https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?VER=8&database=projects%2Fendless-demo-lh8xa7%2Fdatabases%2F(default)&RID=16256&CVER=22&X-HTTP-Session-Id=gsessionid&zx=auywsytmpiax&t=1"""
  headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://endlessdance.com.au",
    "priority": "u=1, i",
    "referer": "https://endlessdance.com.au/",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-fetch-storage-access": "active",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
  }
  
  #headers=X-Goog-Api-Client%3Agl-js%2F%20fire%2F10.11.1%0D%0AContent-Type%3Atext%2Fplain%0D%0AX-Firebase-GMPID%3A1%3A815212911105%3Aweb%3A9c0a28f5b222c0b50ffe00%0D%0A&count=1&ofs=0&req0___data__=%7B%22database%22%3A%22projects%2Fendless-demo-lh8xa7%2Fdatabases%2F(default)%22%2C%22addTarget%22%3A%7B%22query%22%3A%7B%22structuredQuery%22%3A%7B%22from%22%3A%5B%7B%22collectionId%22%3A%22lessons%22%7D%5D%2C%22where%22%3A%7B%22compositeFilter%22%3A%7B%22op%22%3A%22AND%22%2C%22filters%22%3A%5B%7B%22fieldFilter%22%3A%7B%22field%22%3A%7B%22fieldPath%22%3A%22is_user_based%22%7D%2C%22op%22%3A%22EQUAL%22%2C%22value%22%3A%7B%22booleanValue%22%3Afalse%7D%7D%7D%2C%7B%22fieldFilter%22%3A%7B%22field%22%3A%7B%22fieldPath%22%3A%22start_date_time%22%7D%2C%22op%22%3A%22GREATER_THAN%22%2C%22value%22%3A%7B%22timestampValue%22%3A%222025-04-24T14%3A00%3A00.000000000Z%22%7D%7D%7D%2C%7B%22fieldFilter%22%3A%7B%22field%22%3A%7B%22fieldPath%22%3A%22start_date_time%22%7D%2C%22op%22%3A%22LESS_THAN_OR_EQUAL%22%2C%22value%22%3A%7B%22timestampValue%22%3A%222025-04-25T13%3A59%3A00.000000000Z%22%7D%7D%7D%5D%7D%7D%2C%22orderBy%22%3A%5B%7B%22field%22%3A%7B%22fieldPath%22%3A%22start_date_time%22%7D%2C%22direction%22%3A%22ASCENDING%22%7D%2C%7B%22field%22%3A%7B%22fieldPath%22%3A%22__name__%22%7D%2C%22direction%22%3A%22ASCENDING%22%7D%5D%7D%2C%22parent%22%3A%22projects%2Fendless-demo-lh8xa7%2Fdatabases%2F(default)%2Fdocuments%22%7D%2C%22targetId%22%3A2%7D%7D

  # Add form data
  form_data = {
    "X-Goog-Api-Client": "gl-js/ fire/10.11.1",
    "Content-Type": "text/plain",
    "X-Firebase-GMPID": "1:815212911105:web:9c0a28f5b222c0b50ffe00",
    "req0___data__": json.dumps(
      {"database":"projects/endless-demo-lh8xa7/databases/(default)",
        "addTarget": {
          "query": {
            "structuredQuery":{
              "from":[{"collectionId":"lessons"}],
              "where":{
                "compositeFilter":{
                  "op":"AND",
                  "filters":[
                    {
                      "fieldFilter":{
                        "field":{
                          "fieldPath":"is_user_based"
                        },
                        "op":"EQUAL",
                        "value":{
                          "booleanValue":False
                        }
                      }
                    },
                    {
                      "fieldFilter":{
                        "field":{
                          "fieldPath":"start_date_time"
                        },
                        "op":"GREATER_THAN",
                        "value":{
                          "timestampValue":start_date
                        }
                      }
                    },
                    {
                      "fieldFilter":{
                        "field":{
                          "fieldPath":"start_date_time"
                        },
                        "op":"LESS_THAN_OR_EQUAL",
                        "value":{
                          "timestampValue":end_date
                        }
                      }
                    }
                  ]
                }
              },
              "orderBy":[
                {
                  "field":{
                    "fieldPath":"start_date_time"
                  },
                  "direction":"ASCENDING"
                },{
                  "field":{
                    "fieldPath":"__name__"
                  },
                  "direction":"ASCENDING"
                }
              ]
            },
            "parent":"projects/endless-demo-lh8xa7/databases/(default)/documents"
          },
          "targetId":2
        }
      }
    )
  }


  # Make request and dump to file
  with open("dump.html", "w") as f:
    response = requests.post(url, headers=headers, data=form_data)
    f.write(response.text)
    data = json.loads(response.text.split()[1])
    sid = data[0][1][1]
    print("SID: ", sid)
    # Get gsessionid from header X-Http-Session-Id
    gsessionid = response.headers["X-Http-Session-Id"]
    print("gsessionid: ", gsessionid)

  # Get classes
  url = f"""https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?gsessionid={gsessionid}&VER=8&database=projects%2Fendless-demo-lh8xa7%2Fdatabases%2F(default)&RID=rpc&SID={sid}&AID=0&CI=0&TYPE=xmlhttp&zx=apcursuep04w&t=1"""
    
  headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://endlessdance.com.au",
    "priority": "u=1, i",
    "referer": "https://endlessdance.com.au/",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-fetch-storage-access": "active",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
  }

  # Make request and dump to file
  with open("endless.html", "w") as f:
    response = requests.get(url, headers=headers)
    print(response)
    f.write(response.text)
    

if __name__ == "__main__":
  endless("2025-04-24T14:00:00.000000000Z", "2025-04-25T13:59:00.000000000Z")
  
