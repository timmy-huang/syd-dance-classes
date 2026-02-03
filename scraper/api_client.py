import requests
import os
import json
from typing import List, Dict

# Test mode - set via environment variable or imported from main
TEST_MODE = os.getenv('SCRAPER_TEST_MODE', 'false').lower() == 'true'

class DanceClassAPI:
    def __init__(self):
        # In test mode, skip API initialization
        if TEST_MODE:
            self.base_url = None
            self.api_key = None
            self.test_mode = True
            return
        
        self.test_mode = False
        self.base_url = os.getenv('NUXT_API_URL', 'http://localhost:3000')
        self.api_key = os.getenv('SYNC_API_KEY')
        
        if not self.base_url:
            raise ValueError("NUXT_API_URL environment variable is empty!")
        
        if not self.api_key:
            raise ValueError("SYNC_API_KEY environment variable not set")
    
    def delete_all_external_classes(self) -> Dict:
        """
        Delete all external classes from the database via API
        """
        # In test mode, skip deletion
        if self.test_mode:
            return {"deleted": 0, "message": "Test mode - skipped deletion"}
        
        payload = {
            "api_key": self.api_key
        }
        
        try:
            response = requests.delete(
                f"{self.base_url}/api/sync/external-classes",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to delete external classes: {e}")
    
    def sync_classes(self, source: str, classes: List[Dict]) -> Dict:
        """
        Sync classes to the database via API in batches
        In test mode, returns the classes data without syncing
        """
        if not classes:
            print(f"⚠️  No classes to sync for {source}")
            return {"created": 0, "updated": 0, "errors": [], "classes": []}
        
        # In test mode, return the classes data without syncing
        if self.test_mode:
            print(f"   🧪 Test mode: Collected {len(classes)} classes for {source}")
            return {
                "created": len(classes),
                "updated": 0,
                "errors": [],
                "classes": classes  # Include raw classes data for test output
            }
        
        # Batch size - adjust if needed
        BATCH_SIZE = 8
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
                
                # Check for HTTP errors
                if not response.ok:
                    print(f"❌")
                    print(f"      HTTP {response.status_code}: {response.reason}")
                    
                    # Try to get error details from response
                    try:
                        error_data = response.json()
                        print(f"      Error details: {json.dumps(error_data, indent=2)}")
                        total_results["errors"].append(f"Batch {batch_num}: {error_data}")
                    except:
                        # Response is not JSON (might be HTML error page)
                        print(f"      Response body: {response.text[:500]}")
                        total_results["errors"].append(f"Batch {batch_num}: HTTP {response.status_code}")
                    
                    # Save problematic batch for debugging
                    self._save_debug_batch(source, batch_num, batch, response)
                    continue
                
                # Parse successful response
                batch_results = response.json()
                total_results["created"] += batch_results.get("created", 0)
                total_results["updated"] += batch_results.get("updated", 0)
                total_results["errors"].extend(batch_results.get("errors", []))
                
                # Show batch-level errors if any
                if batch_results.get("errors"):
                    print(f"⚠️  (+{batch_results.get('created', 0)} ~{batch_results.get('updated', 0)} !{len(batch_results.get('errors', []))})")
                    for error in batch_results.get("errors", []):
                        print(f"      - {error}")
                else:
                    print(f"✓ (+{batch_results.get('created', 0)} ~{batch_results.get('updated', 0)})")
                
            except requests.exceptions.Timeout:
                print(f"❌")
                print(f"      Error: Request timeout (>30s)")
                total_results["errors"].append(f"Batch {batch_num}: Timeout")
                self._save_debug_batch(source, batch_num, batch, None)
                continue
                
            except requests.exceptions.ConnectionError as e:
                print(f"❌")
                print(f"      Error: Connection failed - {str(e)[:100]}")
                total_results["errors"].append(f"Batch {batch_num}: Connection error")
                continue
                
            except requests.exceptions.RequestException as e:
                print(f"❌")
                print(f"      Error: {str(e)[:200]}")
                total_results["errors"].append(f"Batch {batch_num}: {str(e)[:100]}")
                
                # Try to save debug info
                if hasattr(e, 'response') and e.response is not None:
                    self._save_debug_batch(source, batch_num, batch, e.response)
                continue
            
            except json.JSONDecodeError as e:
                print(f"❌")
                print(f"      Error: Invalid JSON response")
                total_results["errors"].append(f"Batch {batch_num}: Invalid JSON")
                continue
        
        return total_results
    
    def _save_debug_batch(self, source: str, batch_num: int, batch: List[Dict], response):
        """Save problematic batch data for debugging"""
        try:
            debug_dir = "scraper/debug"
            os.makedirs(debug_dir, exist_ok=True)
            
            debug_file = f"{debug_dir}/{source}_batch_{batch_num}_error.json"
            
            debug_data = {
                "source": source,
                "batch_num": batch_num,
                "batch_data": batch,
                "response_status": response.status_code if response else None,
                "response_body": response.text[:1000] if response else None
            }
            
            with open(debug_file, 'w') as f:
                json.dump(debug_data, f, indent=2, default=str)
            
            print(f"      💾 Debug data saved to: {debug_file}")
            
        except Exception as e:
            print(f"      ⚠️  Could not save debug data: {e}")


def transform_class_data(raw_class: Dict, studio_name: str, booking_base_url: str) -> Dict:
    """Transform scraped class data to API format"""
    
    # Validate required fields
    if not raw_class.get("serviceId"):
        raise ValueError(f"Missing serviceId for class: {raw_class.get('name', 'Unknown')}")
    
    if not raw_class.get("name"):
        raise ValueError(f"Missing name for class with serviceId: {raw_class.get('serviceId')}")
    
    if not raw_class.get("choreo", {}).get("name"):
        raise ValueError(f"Missing choreographer name for class: {raw_class.get('name')}")
    
    if not raw_class.get("start"):
        raise ValueError(f"Missing start time for class: {raw_class.get('name')}")
    
    if not raw_class.get("end"):
        raise ValueError(f"Missing end time for class: {raw_class.get('name')}")
    
    # Handle booking URL
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