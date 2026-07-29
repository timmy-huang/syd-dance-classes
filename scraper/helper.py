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
    compact = name.lower().replace(" ", "").replace("-", "").replace("_", "")

    style_rules = [
        ('Hip Hop', ('hiphop',)),
        ('K-Pop', ('kpop', 'k-pop')),
        ('Heels', ('heel',)),
        ('Contemporary', ('contemporary', 'contemp', 'lyrical')),
        ('Jazz', ('jazz',)),
        ('Ballet', ('ballet',)),
        ('Popping', ('popping',)),
        ('Locking', ('locking',)),
        ('Breaking', ('breaking', 'breakdance', 'breakin', 'bboy', 'bgirl')),
        ('Waacking', ('waacking', 'whacking')),
        ('House', ('house',)),
        ('Afro', ('afro', 'afrobeats', 'amapiano')),
        ('Dancehall', ('dancehall',)),
        ('Reggaeton', ('reggaeton',)),
        ('Vogue', ('vogue',)),
        ('Girl Style', ('girlstyle', 'girlsstyle', 'girlschoreo', 'girlchoreo')),
        ('Commercial', ('commercial', 'jazzfunk', 'streetjazz')),
        ('Stretch / Conditioning', ('stretch', 'conditioning', 'strength', 'pilates', 'flexibility', 'mobility', 'floorwork')),
    ]

    for style, tokens in style_rules:
        if any(token in compact for token in tokens):
            return [style]

    if 'choreo' in compact or 'choreography' in compact or 'routine' in compact:
        return ['Choreography']

    return ['Other']
