import asyncio
import re
from datetime import datetime, timedelta

from playwright.async_api import async_playwright

from helper import determine_level, determine_style
from api_client import DanceClassAPI, transform_class_data


WIDGET_URL = "https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/0e353548137/schedule"
BOOKING_URL = "https://imient.com.au/classes"
LOCATION = "IMI Dance Studio"


def parse_time_to_datetime(time_str, date_obj):
    """Parse a widget time like "7:15 PM" into a datetime for date_obj."""
    try:
        time_obj = datetime.strptime(time_str.strip().upper(), "%I:%M %p").time()
    except ValueError:
        return None

    return datetime.combine(date_obj, time_obj)


def parse_choreographer(instructor_line):
    """Split IMI's "Name | @instagram" instructor label."""
    parts = [part.strip() for part in instructor_line.split("|")]
    name = parts[0] if parts and parts[0] else "Unknown"
    instagram = ""

    if len(parts) > 1:
        instagram = parts[1].strip()

    return {"name": name, "instagram": instagram}


def extract_displayed_date(visible_text, fallback_date):
    match = re.search(r"(\w+day),\s+(\w+)\s+(\d+)", visible_text)
    if not match:
        return fallback_date

    month_name = match.group(2)[:3]
    day = int(match.group(3))
    month_map = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    try:
        return fallback_date.replace(month=month_map.get(month_name, fallback_date.month), day=day)
    except ValueError:
        return fallback_date


def extract_classes_from_text(visible_text, fallback_date):
    """Extract IMI classes from the rendered MindBody schedule text."""
    current_date = extract_displayed_date(visible_text, fallback_date)
    lines = [line.strip() for line in visible_text.splitlines() if line.strip()]
    classes = []

    for i, line in enumerate(lines):
        if not re.match(r"^\d{1,2}:\d{2}\s*(?:AM|PM)$", line, re.IGNORECASE):
            continue

        if i + 3 >= len(lines):
            continue

        duration_match = re.match(r"^(\d+)\s*min$", lines[i + 1], re.IGNORECASE)
        if not duration_match:
            continue

        class_name = lines[i + 2]
        instructor_line = lines[i + 3]

        if class_name.lower() in {"show details", "book", "imi dance"}:
            continue

        start_dt = parse_time_to_datetime(line, current_date)
        if not start_dt:
            continue

        duration = int(duration_match.group(1))
        end_dt = start_dt + timedelta(minutes=duration)
        choreographer = parse_choreographer(instructor_line)
        service_id = (
            f"imi_{current_date.isoformat()}_"
            f"{line.replace(' ', '').replace(':', '')}_"
            f"{class_name.replace(' ', '_')[:40]}_"
            f"{choreographer['name'].replace(' ', '_')[:24]}"
        )

        classes.append(
            {
                "serviceId": service_id,
                "start": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "choreo": choreographer,
                "name": class_name,
                "location": LOCATION,
                "level": determine_level(class_name),
                "style": determine_style(class_name),
            }
        )

    return classes


async def scrape_imi_classes_async(start_date, end_date):
    all_classes = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        try:
            print("[INFO] Loading IMI schedule...")
            await page.goto(WIDGET_URL, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)

            days_to_check = min((end_date - start_date).days + 1, 14)
            processed_dates = set()

            for day_offset in range(days_to_check):
                target_date = start_date + timedelta(days=day_offset)

                if target_date < datetime.now().date():
                    continue

                try:
                    date_buttons = page.locator('button, [role="button"]')
                    count = await date_buttons.count()
                    for button_index in range(count):
                        button = date_buttons.nth(button_index)
                        text = (await button.inner_text(timeout=1000)).strip()
                        parts = [part.strip() for part in text.splitlines() if part.strip()]
                        if parts and parts[-1] == str(target_date.day):
                            await button.click()
                            await page.wait_for_timeout(2000)
                            break
                except Exception:
                    pass

                visible_text = await page.evaluate("document.body.innerText")
                displayed_date = extract_displayed_date(visible_text, target_date)

                if displayed_date != target_date or displayed_date in processed_dates:
                    continue

                processed_dates.add(displayed_date)

                if "no available classes" in visible_text.lower():
                    print(f"[INFO] No IMI classes on {displayed_date.strftime('%b %d')}")
                    continue

                day_classes = extract_classes_from_text(visible_text, displayed_date)
                if day_classes:
                    print(f"[INFO] Found {len(day_classes)} IMI classes on {displayed_date.strftime('%b %d')}")
                    all_classes.extend(day_classes)

        except Exception as e:
            print(f"[WARN] Error during IMI scraping: {e}")
        finally:
            await browser.close()

    seen_ids = set()
    unique_classes = []
    for cls in all_classes:
        if cls["serviceId"] in seen_ids:
            continue
        seen_ids.add(cls["serviceId"])
        unique_classes.append(cls)

    filtered_classes = []
    for cls in unique_classes:
        class_date = datetime.fromisoformat(cls["start"]).date()
        if start_date <= class_date <= end_date:
            filtered_classes.append(cls)

    print(f"[OK] Scraped {len(filtered_classes)} classes from IMI")
    return filtered_classes


def scrape_imi_classes(start_date, end_date):
    return asyncio.run(scrape_imi_classes_async(start_date, end_date))


def imi(start_date, end_date=None, *_legacy_args):
    """
    Fetch IMI Dance schedule data and sync to API.

    The previous scraper used IMI's old MindBody JSONP widget. IMI now uses the
    brandedweb-next schedule widget, so this scraper renders the current widget.
    """
    if end_date is None:
        end_date = start_date + timedelta(days=7)

    api_client = DanceClassAPI()
    classes = scrape_imi_classes(start_date, end_date)

    if not classes:
        return {"created": 0, "updated": 0, "errors": []}

    transformed = [
        transform_class_data(
            cls,
            "IMI",
            BOOKING_URL,
        )
        for cls in classes
    ]

    return api_client.sync_classes("imi", transformed)


if __name__ == "__main__":
    from datetime import date

    today = date.today()
    end = today + timedelta(days=7)
    result = imi(today, end)
    print(f"Result: {result}")
