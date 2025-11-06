from movement.movement import movement
from imi.imi import imi
from xo.xo import xo
from ix.ix import ix
from pdc.pdc import pdc
from duti.duti import duti
from endless.endless import endless
from kcc.kcc import kcc
from colab.colab import colab
import datetime

# Calculate date range
today = datetime.date.today()
today_weekday = today.weekday()
previous_monday = today - datetime.timedelta(days=today_weekday)
upcoming_sunday = today + datetime.timedelta(days=(7 + 6 - today_weekday + 1))

print("=" * 70)
print(f"🎯 Starting Dance Class Sync")
print(f"📅 Date range: {previous_monday} to {upcoming_sunday}")
print("=" * 70)

# Configuration for each studio
studios = [
    {
        "name": "Movement Nation",
        "func": movement,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "IMI Dance",
        "func": imi,
        "args": (
            "jQuery36406886794353924179_1715325689640",
            today,
            "1715325689641"
        )
    },
    {
        "name": "CrossOver (XO)",
        "func": xo,
        "args": ()
    },
    {
        "name": "IX Dance",
        "func": ix,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "PDC",
        "func": pdc,
        "args": (previous_monday, upcoming_sunday)
    },
    {
        "name": "Duti Dance",
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
        "name": "Colab Dance",
        "func": colab,
        "args": (previous_monday, upcoming_sunday)
    },
]

# Sync each studio
total_created = 0
total_updated = 0
total_errors = 0
successful_studios = 0
failed_studios = []

for studio_config in studios:
    studio_name = studio_config["name"]
    print(f"\n{'─' * 70}")
    print(f"🏢 Syncing {studio_name}...")
    print(f"{'─' * 70}")
    
    try:
        result = studio_config["func"](*studio_config["args"])
        
        if result:
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
print("📊 SYNC SUMMARY")
print("=" * 70)
print(f"✅ Successful studios: {successful_studios}/{len(studios)}")
print(f"📝 Total created: {total_created}")
print(f"🔄 Total updated: {total_updated}")
print(f"⚠️  Total errors: {total_errors}")

if failed_studios:
    print(f"\n❌ Failed studios: {', '.join(failed_studios)}")

print("\n✅ Scraping completed!")
print("=" * 70)