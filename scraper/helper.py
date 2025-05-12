import json
import os

# Global variable to control matching mode
# True: Match by first name only, False: Match by full name
MATCH_BY_FIRST_NAME = True

def get_or_create_choreographer(name, instagram=""):
    # Load existing choreographers
    choreographers_file = 'scraper/choreographers.json'
    
    if os.path.exists(choreographers_file):
        with open(choreographers_file, 'r') as file:
            choreographers = json.load(file)
    else:
        choreographers = []

    # Load manual Instagram handles
    manual_instagram_handles = {}
    manual_instagram_file = 'scraper/manual_instagram.txt'
    if os.path.exists(manual_instagram_file) and os.path.getsize(manual_instagram_file) > 0:
        with open(manual_instagram_file, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        choreo_name = parts[0].strip()
                        insta_handle = parts[1].strip()
                        manual_instagram_handles[choreo_name.lower()] = insta_handle

    # Look for existing choreographer and update instagram if provided
    for choreographer in choreographers:
        if MATCH_BY_FIRST_NAME:
            # Match by first name only
            if choreographer['name'].lower().split()[0] == name.lower().split()[0]:
                # Update Instagram if provided in the function call
                if instagram.strip():
                    choreographer['instagram'] = instagram.strip()
                    # Save updated choreographers
                    with open(choreographers_file, 'w') as file:
                        json.dump(choreographers, file, indent=4)
                
                # Check if there's a manual Instagram handle for this choreographer
                if choreographer['name'].lower() in manual_instagram_handles:
                    choreographer['instagram'] = manual_instagram_handles[choreographer['name'].lower()]
                    # Save updated choreographers
                    with open(choreographers_file, 'w') as file:
                        json.dump(choreographers, file, indent=4)
                
                return choreographer
        else:
            # Match by full name
            if choreographer['name'].lower() == name.lower():
                # Update Instagram if provided in the function call
                if instagram.strip():
                    choreographer['instagram'] = instagram.strip()
                    # Save updated choreographers
                    with open(choreographers_file, 'w') as file:
                        json.dump(choreographers, file, indent=4)
                
                # Check if there's a manual Instagram handle for this choreographer
                if choreographer['name'].lower() in manual_instagram_handles:
                    choreographer['instagram'] = manual_instagram_handles[choreographer['name'].lower()]
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
    
    # Check if there's a manual Instagram handle for this new choreographer
    if name.lower() in manual_instagram_handles:
        new_choreographer['instagram'] = manual_instagram_handles[name.lower()]
    
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
    elif 'heel' in name:
        return ['Heels']
    return ['Other']