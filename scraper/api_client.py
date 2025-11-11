import requests
import os
from typing import List, Dict

class DanceClassAPI:
    def __init__(self):
        self.base_url = os.getenv('NUXT_API_URL', 'http://localhost:3000')
        self.api_key = os.getenv('SYNC_API_KEY')
        
        if not self.base_url:
            raise ValueError("NUXT_API_URL environment variable is empty!")
        
        if not self.api_key:
            raise ValueError("SYNC_API_KEY environment variable not set")
    
    def sync_classes(self, source: str, classes: List[Dict]) -> Dict:
        """
        Sync classes to the database via API in batches
        """
        if not classes:
            print(f"⚠️  No classes to sync for {source}")
            return {"created": 0, "updated": 0, "errors": []}
        
        # Batch size - adjust if needed
        BATCH_SIZE = 10
        total_results = {
            "created": 0,
            "updated": 0,
            "errors": []
        }
        
        total_batches = (len(classes) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"   📊 Total classes: {len(classes)}, batches: {total_batches}")
        
        for i in range(0, len(classes), BATCH_SIZE):
            batch = classes[i:i + BATCH_SIZE]
            batch_num = (i // BATCH_SIZE) + 1
            
            print(f"   📦 Batch {batch_num}/{total_batches} ({len(batch)} classes)...", end=" ")
            
            payload = {
                "source": source,
                "api_key": self.api_key,
                "classes": batch
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/sync/external-classes",
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                
                batch_results = response.json()
                total_results["created"] += batch_results.get("created", 0)
                total_results["updated"] += batch_results.get("updated", 0)
                total_results["errors"].extend(batch_results.get("errors", []))
                
                print(f"✓ (+{batch_results.get('created', 0)} ~{batch_results.get('updated', 0)})")
                
            except requests.exceptions.RequestException as e:
                print(f"❌")
                print(f"      Error: {str(e)[:100]}")
                total_results["errors"].append(f"Batch {batch_num} failed: {e}")
                continue
        
        return total_results


def transform_class_data(raw_class: Dict, studio_name: str, booking_base_url: str) -> Dict:
    """Transform scraped class data to API format"""
    if "booking_url" in raw_class:
        external_url = raw_class["booking_url"]
    else:
        external_url = booking_base_url
    
    return {
        "external_id": str(raw_class.get("serviceId", "")),
        "name": raw_class["name"],
        "choreographer_name": raw_class["choreo"]["name"],
        "choreographer_instagram": raw_class["choreo"].get("instagram", ""),
        "studio_name": studio_name,
        "external_booking_url": external_url,
        "start_time": raw_class["start"],
        "end_time": raw_class["end"],
        "location": raw_class.get("location", "TBD"),
        "level": raw_class.get("level", []),
        "style": raw_class.get("style", []),
    }