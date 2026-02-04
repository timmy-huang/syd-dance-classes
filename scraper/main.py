import datetime
import json
import os
import requests

# ============================================================
# TEST MODE - Set to True to save locally instead of API sync
# ============================================================
TEST_MODE = False
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), ".test_output")

# ============================================================
# TELEGRAM NOTIFICATIONS
# ============================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram_notification(message: str) -> bool:
    """Send a notification via Telegram bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram not configured (missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID)")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"⚠️  Failed to send Telegram notification: {e}")
        return False

# Set environment variable BEFORE importing scrapers so api_client picks it up
if TEST_MODE:
    os.environ['SCRAPER_TEST_MODE'] = 'true'

from movement.movement import movement_hurstville, movement_parramatta
from imi.imi import imi
from xo.xo import xo
from ix.ix import ix
from pdc.pdc import pdc
from duti.duti import duti
from endless.endless import endless
from kcc.kcc import kcc
from colab.colab import colab
from sdc.sdc import sdc
from api_client import DanceClassAPI

# Calculate date range
today = datetime.date.today()
today_weekday = today.weekday()
previous_monday = today - datetime.timedelta(days=today_weekday)
upcoming_sunday = today + datetime.timedelta(days=(7 + 6 - today_weekday + 1))

print("=" * 70)
if TEST_MODE:
    print(f"🧪 Starting Dance Class Sync (TEST MODE - Local Save)")
else:
    print(f"🎯 Starting Dance Class Sync")
print(f"📅 Date range: {previous_monday} to {upcoming_sunday}")
print("=" * 70)

# Initialize API client or test output directory
api_client = None
if TEST_MODE:
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    print(f"\n📁 Test output directory: {TEST_OUTPUT_DIR}")
    all_test_classes = {}  # Collect all classes for combined output
else:
    api_client = DanceClassAPI()
    # Delete all existing external classes before syncing
    print("\n🗑️  Deleting all existing external classes...")
    try:
        delete_result = api_client.delete_all_external_classes()
        print(f"✅ Deleted {delete_result.get('deleted', 0)} external classes")
    except Exception as e:
        print(f"❌ Error deleting external classes: {e}")
        print("⚠️  Continuing with sync anyway...")

# Configuration for each studio
studios = [
    {
        "name": "Movement Nation Hurstville",
        "func": movement_hurstville,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "Movement Nation Parramatta",
        "func": movement_parramatta,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "IMI",
        "func": imi,
        "args": (
            "jQuery36406886794353924179_1715325689640",
            today,
            "1715325689641"
        )
    },
    {
        "name": "Crossover",
        "func": xo,
        "args": ()
    },
    {
        "name": "IX",
        "func": ix,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "PDC",
        "func": pdc,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "DUTI",
        "func": duti,
        "args": (
            "jQuery364011093063789286006_1740274810344",
            today,
            "1740274810346"
        )
    },
    {
        "name": "Endless Dance",
        "func": endless,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "KCC",
        "func": kcc,
        "args": (
            "jQuery36407072146344659085_1747063164353",
            today,
            "1747063164355"
        )
    },
    {
        "name": "Co-Lab Quarters",
        "func": colab,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "Sydney Dance Company",
        "func": sdc,
        "args": (previous_monday, upcoming_sunday)
    },
]

# Sync each studio
total_created = 0
total_updated = 0
total_errors = 0
total_classes = 0
successful_studios = 0
failed_studios = []

for studio_config in studios:
    studio_name = studio_config["name"]
    print(f"\n{'─' * 70}")
    if TEST_MODE:
        print(f"🏢 Scraping {studio_name}...")
    else:
        print(f"🏢 Syncing {studio_name}...")
    print(f"{'─' * 70}")
    
    try:
        result = studio_config["func"](*studio_config["args"])
        
        if result:
            if TEST_MODE:
                # In test mode, result contains the raw classes data
                classes_data = result.get("classes", [])
                total_classes += len(classes_data)
                successful_studios += 1
                
                # Save individual studio file
                studio_filename = studio_name.lower().replace(" ", "_").replace("-", "_")
                studio_file = os.path.join(TEST_OUTPUT_DIR, f"{studio_filename}.json")
                with open(studio_file, 'w', encoding='utf-8') as f:
                    json.dump(classes_data, f, indent=2, ensure_ascii=False, default=str)
                
                # Add to combined output
                all_test_classes[studio_name] = classes_data
                
                print(f"✅ {studio_name} complete:")
                print(f"   📊 Classes found: {len(classes_data)}")
                print(f"   💾 Saved to: {studio_file}")
            else:
                total_created += result.get("created", 0)
                total_updated += result.get("updated", 0)
                total_errors += len(result.get("errors", []))
                successful_studios += 1
                
                print(f"✅ {studio_name} complete:")
                print(f"   📝 Created: {result.get('created', 0)}")
                print(f"   🔄 Updated: {result.get('updated', 0)}")
                if result.get('errors'):
                    print(f"   ⚠️  Errors: {len(result['errors'])}")
        else:
            print(f"⚠️  {studio_name} returned no result")
            
    except Exception as e:
        print(f"❌ Error syncing {studio_name}: {e}")
        failed_studios.append(studio_name)
        continue

# Summary
print("\n" + "=" * 70)
if TEST_MODE:
    print("📊 TEST MODE SUMMARY")
else:
    print("📊 SYNC SUMMARY")
print("=" * 70)
print(f"✅ Successful studios: {successful_studios}/{len(studios)}")

if TEST_MODE:
    print(f"📊 Total classes scraped: {total_classes}")
    
    # Save combined output file
    combined_file = os.path.join(TEST_OUTPUT_DIR, "_all_classes.json")
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump({
            "date_range": {
                "start": str(previous_monday),
                "end": str(upcoming_sunday)
            },
            "total_classes": total_classes,
            "studios": all_test_classes
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"💾 Combined output: {combined_file}")
else:
    print(f"📝 Total created: {total_created}")
    print(f"🔄 Total updated: {total_updated}")
    print(f"⚠️  Total errors: {total_errors}")

if failed_studios:
    print(f"\n❌ Failed studios: {', '.join(failed_studios)}")
    
    # Send Telegram notification for failed studios
    failure_message = (
        f"🚨 <b>Dance Class Scraper Alert</b>\n\n"
        f"❌ <b>{len(failed_studios)} studio(s) failed:</b>\n"
        f"• {chr(10).join(failed_studios)}\n\n"
        f"📅 Date range: {previous_monday} to {upcoming_sunday}\n"
        f"✅ Successful: {successful_studios}/{len(studios)}"
    )
    if send_telegram_notification(failure_message):
        print("📱 Telegram notification sent")

print("\n✅ Scraping completed!")
print("=" * 70)