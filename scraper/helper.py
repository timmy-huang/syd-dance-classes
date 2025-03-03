import json
import os

def get_or_create_choreographer(name, instagram=""):
    # Load existing choreographers
    choreographers_file = 'scraper/choreographers.json'
    
    if os.path.exists(choreographers_file):
        with open(choreographers_file, 'r') as file:
            choreographers = json.load(file)
    else:
        choreographers = []

    # Look for existing choreographer
    for choreographer in choreographers:
        if choreographer['name'].lower() == name.lower():
            return choreographer

    # Create new choreographer
    new_choreographer = {
        'id': str(len(choreographers)),  # Simple ID generation
        'name': name.strip(),
        'instagram': instagram.strip()
    }
    
    choreographers.append(new_choreographer)

    # Save updated choreographers
    with open(choreographers_file, 'w') as file:
        json.dump(choreographers, file, indent=4)

    return new_choreographer
