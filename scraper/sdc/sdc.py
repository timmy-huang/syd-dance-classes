import requests
from datetime import datetime
import json
from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


def parse_nextjs_response(response_text):
    """
    Parse the Next.js Server Action response format.
    Response format is like: "0:data\n1:data\n2:data"
    """
    lines = response_text.strip().split('\n')
    parsed_data = {}
    
    for line in lines:
        if ':' in line:
            # Split only on first colon
            idx, data = line.split(':', 1)
            try:
                # Parse the JSON data
                parsed_data[idx] = json.loads(data)
            except json.JSONDecodeError:
                parsed_data[idx] = data
    
    return parsed_data


def sdc(start_date, end_date):
    """
    Fetch Sydney Dance Company schedule data and sync to API.
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        Dict with created/updated/errors counts
    """
    api_client = DanceClassAPI()
    
    # Scrape classes
    classes = scrape_sdc_classes(start_date, end_date)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    # Transform to API format
    transformed = [
        transform_class_data(
            cls,
            "Sydney Dance Company",
            "https://www.sydneydancecompany.com/classes/classes-schedule/"
        )
        for cls in classes
    ]
    
    # Sync to API
    result = api_client.sync_classes("sdc", transformed)
    return result


def scrape_sdc_classes(start_date, end_date):
    """
    Scrape Sydney Dance Company classes
    
    Args:
        start_date: datetime.date object
        end_date: datetime.date object
        
    Returns:
        List of class dictionaries
    """
    # Convert date objects to ISO format with time
    # Assuming Sydney timezone (UTC+11)
    from_date = f"{start_date.isoformat()}T13:00:00.000Z"
    to_date = f"{end_date.isoformat()}T12:59:59.999Z"
    
    # API endpoint - Sydney Dance Company widget ID: e89579590
    url = "https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/e89579590/schedule"
    
    # Headers
    headers = {
        "accept": "text/x-component",
        "accept-language": "en-US,en;q=0.9",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjIxMTg0NDkiLCJhcCI6IjE4MzUwMzcyMDIiLCJpZCI6ImU5ZTM4NzEzZmFhOGVkZmQiLCJ0ciI6IjQyZDU1NWQyNjBiZjBiODM1Y2VjMzBiOTBkMzMyYTQ0IiwidGkiOjE3Njk5NTA0MjQ3NzIsInRrIjoiODQ0NjcifX0=",
        "next-action": "4f5d69414e1b758541ec223c15d6e1f87de21681",
        "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%5B%22locale%22%2C%22en%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22widgets%22%2C%7B%22children%22%3A%5B%22schedules%22%2C%7B%22children%22%3A%5B%5B%22preview%22%2C%22view%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%5B%22widgetId%22%2C%22e89579590%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22schedule%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D",
        "origin": "https://brandedweb-next.mindbodyonline.com",
        "priority": "u=0",
        "referer": "https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/e89579590/schedule",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="147", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-42d555d260bf0b835cec30b90d332a44-e9e38713faa8edfd-01",
        "tracestate": "84467@nr=0-1-2118449-1835037202-e9e38713faa8edfd----1769950424772",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"
    }
    
    # Cookies
    cookies = {
        "_cfuvid": "u6TiPn0LOqPorpnhcKLBpYsYxFYEVduo9d9fNQaS89o-1769950275759-0.0.1.1-604800000",
        "cf_clearance": "E2AwOiMOO5whJ3b5RnMMXNVggbYEqwSP_iIbqxG79w0-1769950277-1.2.1.1-rA.C2MrOBixTYhDKN2KvFl4Ia680hmsUDS90UTgkNOnKJi01FfcQZQjkq1A9svtnzWvDZ3cOBIem3w2maFMybihOUrqbC8.nf._b7oFcAILrN09e5yvyCoaSyQDCWvMJNhwAe5jUuWcHDfKwpkWAsZ7CbG_vs7.thSBDfgFCpHIPb5dDHdYpF9T9dq2DimyCNJtdLM5AY4ltj._wwIRN5mZg78nQFGtuixah6Ta1hqM"
    }
    
    # The token - you'll need to update this periodically from your browser
    token = "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"
    
    # Prepare multipart form data
    files = {
        '1': (None, f'"{token}"'),
        '0': (None, f'["$@1",{{"fromDate":"{from_date}","toDate":"{to_date}"}}]'),
    }
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies, files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️  Sydney Dance Company request failed with status code {response.status_code}")
            print("This could be due to:")
            print("1. The encrypted token may have expired")
            print("2. The session may no longer be valid")
            print("3. The server may be detecting this as not coming from a browser")
            return []
        
        # Parse the Next.js response
        parsed = parse_nextjs_response(response.text)
        
        # The actual class data is in key "1"
        if '1' not in parsed:
            print("⚠️  No class data found in Sydney Dance Company response")
            return []
        
        classes = parsed['1']
        data = []
        
        for class_item in classes:
            # Extract instructor information
            staff_list = class_item.get('staff', [])
            if staff_list:
                instructor = staff_list[0]
                name = instructor.get('displayLabel', 'Unknown')
                insta = ""  # Not available in API response
                choreographer = {"name": name, "instagram": insta}
            else:
                choreographer = {"name": "Unknown", "instagram": ""}
            
            # Get the class ID
            service_id = class_item.get('id')
            
            if not service_id:
                print(f"⚠️  Skipping Sydney Dance Company class '{class_item.get('name', 'Unknown')}' - no serviceId found")
                print(f"   Available fields: {list(class_item.keys())}")
                continue
            
            # Format the class data
            classData = {
                "serviceId": str(service_id),
                "start": class_item['startDateTime'],
                "end": class_item['endDateTime'],
                "choreo": choreographer,
                "name": class_item['name'],
                "location": class_item.get('location', {}).get('name', 'Sydney Dance Company'),
                "level": determine_level(class_item['name']),
                "style": determine_style(class_item['name'])
            }
            data.append(classData)
        
        print(f"✓ Scraped {len(data)} classes from Sydney Dance Company")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping Sydney Dance Company: {e}")
        return []


if __name__ == "__main__":
    # Example usage for testing
    from datetime import date, timedelta
    
    today = date.today()
    end = today + timedelta(days=14)
    
    result = sdc(today, end)
    print(f"Result: {result}")
