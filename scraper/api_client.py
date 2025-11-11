import requests
import os
from typing import List, Dict

class DanceClassAPI:
    def __init__(self):
        self.base_url = os.getenv('NUXT_API_URL', 'http://localhost:3000')
        self.api_key = os.getenv('SYNC_API_KEY')
        
        if not self.api_key:
            raise ValueError("SYNC_API_KEY environment variable not set")
    
    def sync_classes(self, source: str, classes: List[Dict]) -> Dict:
        """
        Sync classes to the database via API
        
        Args:
            source: Studio identifier (e.g., 'movement_nation_hurstville')
            classes: List of class dictionaries
            
        Returns:
            API response with created/updated/error counts
        """
        if not classes:
            print(f"⚠️  No classes to sync for {source}")
            return {"created": 0, "updated": 0, "errors": []}
        
        payload = {
            "source": source,
            "api_key": self.api_key,
            "classes": classes
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/sync/external-classes",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error for {source}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise

def transform_class_data(raw_class: Dict, studio_name: str, booking_base_url: str) -> Dict:
    """
    Transform scraped class data to API format
    
    Args:
        raw_class: Raw class data from scraping
        studio_name: Name of the studio
        booking_base_url: Base URL for booking links
        
    Returns:
        Transformed class data matching API schema
    """
    # Handle different booking URL patterns
    if "booking_url" in raw_class:
        external_url = raw_class["booking_url"]
    else:
        external_url = f"{booking_base_url}/book/{raw_class.get('serviceId', '')}"
    
    return {
        "external_id": str(raw_class.get("serviceId", raw_class.get("id", ""))),
        "name": raw_class["name"],
        "choreographer_name": raw_class["choreo"]["name"],
        "choreographer_instagram": raw_class["choreo"].get("instagram"),
        "studio_name": studio_name,
        "external_booking_url": external_url,
        "start_time": raw_class["start"],
        "end_time": raw_class["end"],
        "location": raw_class.get("location", "TBD"),
        "level": raw_class.get("level", []),
        "style": raw_class.get("style", []),
    }