# Choreographer management is now handled by the backend API
# This file only contains utility functions for determining level and style

def determine_level(name: str) -> list:
    name = name.lower()
    ret = []
    if 'kid' in name or 'youth' in name or 'under 15' in name or 'jr academy' in name:
        ret.append('youth')
    if 'int' in name:
        ret.append('intermediate')
    if 'beg' in name:
        ret.append('beginner')
    if 'adv' in name or 'open' in name:
        ret.append('advanced')
    if 'pop-up' in name or 'pop up' in name:
        ret.append('pop-up')
    if ret == []:
        ret.append('advanced')
    return ret

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