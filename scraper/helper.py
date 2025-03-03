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

    # Look for existing choreographer and update instagram if provided
    for choreographer in choreographers:
        if choreographer['name'].lower() == name.lower():
            if instagram.strip():  # If instagram parameter is not empty
                choreographer['instagram'] = instagram.strip()
                # Save updated choreographers
                with open(choreographers_file, 'w') as file:
                    json.dump(choreographers, file, indent=4)
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

def determine_level(name: str) -> list:
    name = name.lower()
    if 'int/adv' in name:
        return ['intermediate', 'advanced']
    elif 'beg' in name:
        return ['beginner']
    elif 'intermediate' in name:
        return ['intermediate']
    else:
        return ['advanced']

def determine_style(name: str) -> list:
    name = name.lower().replace(" ", "").replace("-", "")
    if 'hiphop' in name:
        return ['Hip Hop']
    elif 'contemporary' in name:
        return ['Contemporary']
    elif 'kpop' in name:
        return ['Kpop']
    elif 'choreo' in name:
        return ['Choreography']
    return ['Other']