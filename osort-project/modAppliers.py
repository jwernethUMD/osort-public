# Calculate values after mods are applied locally when possible for speed

def applyHR(statName, stat):
    match statName:
        case "Circle Size":
            return min(stat * 1.3, 10)
        case "HP Drain":
            return min(stat * 1.4, 10)
        case "OD":
            return min(stat * 1.4, 10)
        case "Approach Rate":
            return min(stat * 1.4, 10)
        case _:
            return stat

def applyDT(statName, stat):
    match statName:
        case "HP Drain":
            return stat
        case "OD":
            return (2.0 / 3.0) * stat + (40.0 / 9.0)
        case "Approach Rate":
            if (stat > 5):
                return ((stat * 2) + 13) / 3.0
            else:
                return (0.5449 * stat) + 4.950 # Equation from linear regression
        case "BPM":
            return stat * 1.5
        case "Length":
            return stat * (2.0 / 3.0)
        case _:
            return stat
        
def applyEZ(statName, stat):
    match statName:
        case "Circle Size":
            return stat / 2.0
        case "HP Drain":
            return stat / 2.0
        case "OD":
            return stat / 2.0
        case "Approach Rate":
            return stat / 2.0
        case _:
            return stat

def applyHT(statName, stat):
    match statName:
        case "HP Drain":
            return stat
        case "OD":
            return ((4.0 / 3.0) * stat) - (40.0 / 9.0)
        case "Approach Rate":
            return ((4.0 / 3.0) * stat) - 5
        case "BPM":
            return stat * 0.75
        case "Length":
            return stat * (4.0 / 3.0)
        case _:
            return stat

def applyMods(mods, statName, stat):
    result = stat
    for mod in mods:
        match mod:
            case "HR":
                result = applyHR(statName, result)
            case "DT":
                result = applyDT(statName, result)
            case "NC":
                result = applyDT(statName, result)
            case "EZ":
                result = applyEZ(statName, result)
            case "HT":
                result = applyHT(statName, result)
            case _:
                result = result

    return result