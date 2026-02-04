import asyncio
import re
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


# Widget URL for Co-Lab Quarters schedule
WIDGET_URL = "https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/562306b3ba/schedule"


def parse_time_to_datetime(time_str, date_obj):
    """Parse a time string like "9:00 AM" to a datetime object."""
    time_str = time_str.strip().upper()
    
    try:
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()
    except ValueError:
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return None
    
    return datetime.combine(date_obj, time_obj)


def extract_classes_from_text(visible_text, current_date):
    """Extract class information from visible page text."""
    classes = []
    lines = visible_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for time pattern like "9:00 AM" or "10:45 AM"
        time_match = re.match(r'^(\d{1,2}:\d{2}\s*(?:AM|PM))$', line, re.IGNORECASE)
        
        if time_match:
            time_str = time_match.group(1)
            duration = 60
            class_name = None
            instructor = "Unknown"
            
            # Look through the next few lines for class info
            for j in range(i + 1, min(i + 8, len(lines))):
                next_line = lines[j].strip()
                
                if not next_line:
                    continue
                
                # Duration pattern: "90 min"
                dur_match = re.match(r'^(\d+)\s*min', next_line, re.IGNORECASE)
                if dur_match:
                    duration = int(dur_match.group(1))
                    continue
                
                # Class name patterns - expanded for Co-Lab classes
                class_types = ['BALLET', 'CONTEMPORARY', 'THEATRE JAZZ', 'JAZZ', 'HIP HOP', 
                              'HEELS', 'STRETCH', 'PILATES', 'CONDITIONING', 'BARRE',
                              'AFRO', 'KPOP', 'K-POP', 'LYRICAL', 'HOUSE', 'WAACKING',
                              'LOCKING', 'POPPING', 'BREAKING', 'OPEN', 'GROOVES',
                              'FUNK', 'LATIN', 'COMMERCIAL', 'URBAN', 'CHOREOGRAPHY']
                for ct in class_types:
                    if next_line.upper().startswith(ct) or ct in next_line.upper():
                        class_name = next_line
                        break
                
                # Instructor pattern (after class name)
                if class_name and instructor == "Unknown":
                    # Look for name pattern
                    name_match = re.match(r'^([A-Z][a-z]+\s+[A-Z][a-z]+)', next_line)
                    if name_match:
                        instructor = name_match.group(1)
                        break
                    
                    name_match2 = re.match(r'^([A-Za-z]+\s+[A-Za-z]+)\s*[\u2013\u2014:-]', next_line)
                    if name_match2:
                        instructor = name_match2.group(1)
                        break
                
                # Stop conditions
                if re.match(r'^\d{1,2}:\d{2}\s*(?:AM|PM)$', next_line, re.IGNORECASE):
                    break
                if next_line.lower() in ['show details', 'sign up', 'unavailable', 'co-lab quarters']:
                    break
            
            if class_name:
                start_dt = parse_time_to_datetime(time_str, current_date)
                if start_dt:
                    end_dt = start_dt + timedelta(minutes=duration)
                    service_id = f"colab_{current_date.isoformat()}_{time_str.replace(' ', '').replace(':', '')}_{class_name.replace(' ', '_')[:20]}"
                    
                    classes.append({
                        "serviceId": service_id,
                        "start": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                        "choreo": {"name": instructor, "instagram": ""},
                        "name": class_name,
                        "location": "Co-Lab Quarters",
                        "level": determine_level(class_name),
                        "style": determine_style(class_name)
                    })
        
        i += 1
    
    return classes


async def scrape_colab_classes_async(start_date, end_date):
    """
    Scrape Co-Lab Quarters classes using Playwright headless browser.
    """
    all_classes = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"[INFO] Loading Co-Lab Quarters schedule...")
            await page.goto(WIDGET_URL, wait_until="load", timeout=30000)
            await page.wait_for_timeout(3000)
            
            # Calculate days to check
            days_to_check = (end_date - start_date).days + 1
            days_to_check = min(days_to_check, 14)
            
            print(f"[INFO] Checking {days_to_check} days for classes...")
            
            processed_dates = set()
            
            for day_offset in range(days_to_check):
                target_date = start_date + timedelta(days=day_offset)
                day_num = target_date.day
                
                # Click on the target date using role="button" elements
                try:
                    # Get all date buttons
                    date_buttons = page.locator('[role="button"]')
                    count = await date_buttons.count()
                    
                    clicked = False
                    for i in range(count):
                        btn = date_buttons.nth(i)
                        try:
                            text = await btn.inner_text()
                            # Check if this button contains our target day number
                            # Format is like "Wed 4" or "Thu 5"
                            if text.strip().endswith(str(day_num)) or f" {day_num}" in text:
                                await btn.click()
                                await page.wait_for_timeout(2000)
                                clicked = True
                                break
                        except:
                            continue
                    
                    if not clicked:
                        # Try clicking "Go to next date" link
                        go_link = page.locator(f'a:has-text("Go to"), span:has-text("Go to February {day_num}")')
                        if await go_link.count() > 0:
                            await go_link.first.click()
                            await page.wait_for_timeout(2000)
                            clicked = True
                    
                except Exception:
                    pass
                
                # Get visible text and extract current date
                visible_text = await page.evaluate("document.body.innerText")
                
                # Determine displayed date
                date_match = re.search(r'(\w+day), (\w+) (\d+)', visible_text)
                if date_match:
                    displayed_day = int(date_match.group(3))
                    displayed_month = date_match.group(2)
                    
                    date_key = f"{displayed_month}-{displayed_day}"
                    if date_key in processed_dates:
                        continue
                    processed_dates.add(date_key)
                    
                    # Parse month
                    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                                 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
                    month_num = month_map.get(displayed_month[:3], start_date.month)
                    
                    try:
                        current_date = start_date.replace(month=month_num, day=displayed_day)
                    except ValueError:
                        continue
                    
                    # Skip if no classes
                    if "no available classes" in visible_text.lower():
                        print(f"[INFO] No classes on {current_date.strftime('%b %d')}")
                        continue
                    
                    # Extract classes
                    day_classes = extract_classes_from_text(visible_text, current_date)
                    if day_classes:
                        print(f"[INFO] Found {len(day_classes)} classes on {current_date.strftime('%b %d')}")
                        all_classes.extend(day_classes)
            
        except Exception as e:
            print(f"[WARN] Error during scraping: {e}")
        finally:
            await browser.close()
        
        # Remove duplicates
        seen_ids = set()
        unique_classes = []
        for cls in all_classes:
            if cls['serviceId'] not in seen_ids:
                seen_ids.add(cls['serviceId'])
                unique_classes.append(cls)
        
        # Filter to requested date range
        filtered_classes = []
        for cls in unique_classes:
            class_date = datetime.fromisoformat(cls['start']).date()
            if start_date <= class_date <= end_date:
                filtered_classes.append(cls)
        
        all_classes = filtered_classes
    
    print(f"[OK] Scraped {len(all_classes)} classes from Co-Lab Quarters")
    return all_classes


def scrape_colab_classes(start_date, end_date):
    """Synchronous wrapper for the async scraping function."""
    return asyncio.run(scrape_colab_classes_async(start_date, end_date))


def colab(start_date, end_date):
    """Fetch Co-Lab Quarters schedule data and sync to API."""
    api_client = DanceClassAPI()
    
    classes = scrape_colab_classes(start_date, end_date)
    
    if not classes:
        return {"created": 0, "updated": 0, "errors": []}
    
    transformed = [
        transform_class_data(
            cls,
            "Co-Lab Quarters",
            "https://www.colabquarters.com.au"
        )
        for cls in classes
    ]
    
    result = api_client.sync_classes("colab", transformed)
    return result


if __name__ == "__main__":
    from datetime import date, timedelta
    
    today = date.today()
    end = today + timedelta(days=14)
    
    result = colab(today, end)
    print(f"Result: {result}")
