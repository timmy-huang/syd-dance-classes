import requests
import json
import re
import datetime
from helper import get_or_create_choreographer, determine_level, determine_style

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

def endless(start_date, end_date, location=""):
  ver = "8"  
  
  # Convert date objects to ISO format strings if they aren't already
  if not isinstance(start_date, str):
    start_date = start_date.isoformat() + "T00:00:00.000000000Z"
  
  if not isinstance(end_date, str):
    end_date = end_date.isoformat() + "T23:59:59.999999999Z"
  
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
  response = requests.post(url, headers=headers, data=form_data)
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

  # Make request and parse response directly
  response = requests.get(url, headers=headers)
  print(response)
  
  # Parse the response and extract class information
  classes = parse_endless_response_text(response.text)
  
  # Write formatted JSON to file
  formatted_json = json.dumps(classes, indent=4)
  with open(location + "endless.json", 'w+', encoding="utf-8") as file:
    file.write(formatted_json)
  
  print("Scraped Endless Dance Studio")
  
  return classes

def parse_endless_response_text(content):
    # Skip the first line which is just a number
    if content.strip() and content.strip()[0].isdigit():
        content = content.split('\n', 1)[1] if '\n' in content else content
    
    try:
        # Find the first '[' which should be the start of our JSON array
        json_start = content.find('[[')
        if json_start == -1:
            print("Could not find start of JSON array")
            return []
        
        # Find the matching closing brackets for the outermost array
        # This handles nested arrays properly
        bracket_count = 0
        json_end = -1
        
        for i in range(json_start, len(content)):
            if content[i] == '[':
                bracket_count += 1
            elif content[i] == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    json_end = i + 1
                    break
        
        if json_end == -1:
            print("Could not find end of JSON array")
            return []
        
        # Extract just the JSON part
        json_content = content[json_start:json_end]
        
        # Parse the extracted JSON
        data = json.loads(json_content)
        
        classes = []
        
        # Iterate through the response to find document changes
        for item in data:
            if len(item) > 1 and isinstance(item[1], list):
                for doc_item in item[1]:
                    if "documentChange" in doc_item:
                        doc = doc_item["documentChange"]["document"]
                        fields = doc["fields"]
                        
                        # Extract choreographer name from title
                        title = fields["title"]["stringValue"]
                        choreo_name = title.split('/')[0].strip() if '/' in title else "Unknown"
                        
                        # Remove name from title
                        title = title.split('/')[1].strip() if '/' in title else "Unknown"
                        
                        # Create choreographer object
                        choreographer = get_or_create_choreographer(choreo_name)
                        
                        # Extract start time
                        start_time = fields["start_date_time"]["timestampValue"]
                        start_datetime = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        
                        # Calculate end time based on minutes
                        minutes = int(fields["minutes"]["integerValue"])
                        end_datetime = start_datetime + datetime.timedelta(minutes=minutes)
                        
                        # Extract location
                        location_detail = fields["location"]["mapValue"]["fields"]["detail"]["stringValue"]
                        location_title = fields["location"]["mapValue"]["fields"]["title"]["stringValue"]
                        location_str = f"{location_title}, {location_detail}"
                        
                        # Extract level
                        level_str = fields["level"]["mapValue"]["fields"]["title"]["stringValue"]
                        level = determine_level(level_str)
                        
                        # Determine style
                        style = determine_style(title)
                        
                        # Create class data
                        class_data = {
                            "serviceId": doc["name"].split('/')[-1],
                            "start": start_datetime.isoformat(),
                            "end": end_datetime.isoformat(),
                            "choreo": choreographer,
                            "name": title,
                            "studio": "Endless",
                            "location": location_str,
                            "level": level,
                            "style": style,
                            "totalSpots": int(fields["max_ppl"]["integerValue"]),
                            "openSpots": int(fields["max_ppl"]["integerValue"]) - int(fields["booked_ppl"]["integerValue"])
                        }
                        
                        classes.append(class_data)
        
        return classes
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        # Save the problematic content for debugging
        with open("debug_json.txt", "w+", encoding="utf-8") as f:
            f.write(content)
        return []
    except Exception as e:
        print(f"Error processing data: {e}")
        return []

if __name__ == "__main__":
  classes = endless("2025-04-24T14:00:00.000000000Z", "2025-04-25T13:59:00.000000000Z", "data/")
  print(f"Found {len(classes)} classes")
  
