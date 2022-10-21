import requests
from modAppliers import applyMods
from os import getenv

API_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# To run this, environment variable CLIENT_ID must be set to a client id and CLIENT_SECRET must be 
# set to a client secret (see osu api docs)
# Alternatively, run the website from https://jwerneth.pythonanywhere.com/
body = {
    "client_id": getenv("CLIENT_ID"),
    "client_secret": getenv("CLIENT_SECRET"),
    "grant_type": "client_credentials",
    "scope": "public"
}

response1 = requests.post(TOKEN_URL, data=body)
token = response1.json().get("access_token")

authHeaders = {"Authorization": f"Bearer {token}"}
authHeaders.update(headers)

params = {
    "mode": "osu",
    "limit": 100
}

statTypes = {
    "Circle Size": "cs",
    "Star Rating": "difficulty_rating", # Need to apply mods (this is hard)
    "Length": "total_length", # Need to apply mod
    "HP Drain": "drain",
    "OD": "accuracy",
    "Approach Rate": "ar",
    "BPM": "bpm",
    "PP": "pp",
    "Score": "score",
    "Date": "last_updated", # Need to somehow parse the day/time/year, etc
    "Slider:circle ratio": "custom" # Implement custom stuff
}

mapStats = {"Circle Size": "cs",
    "Star Rating": "difficulty_rating", # Need to apply mods (this is hard)
    "Length": "total_length", # Need to apply mod
    "HP Drain": "drain",
    "OD": "accuracy",
    "Approach Rate": "ar",
    "BPM": "bpm",
}

scoreStats = {
    "Score": "score",
    "PP": "pp"
}

modBits = {
    "EZ": 2,
    "HT": 256,
    "FL": 1024,
    "HR": 16,
    "NC": 64,
    "DT": 64,
}

def getDifficulty(id, mods, diff):
    modBitSet = 0
    for mod in mods:
        if mod in modBits:
            modBitSet += modBits[mod]
    
    if modBitSet == 0:
        return diff

    reqBody = {
        "mods": modBitSet,
    }
    # print(id, mods)
    responsejson = requests.post(f"{API_URL}/beatmaps/{id}/attributes", headers=authHeaders, params=reqBody)
    attributes = responsejson.json().get("attributes")
    print(responsejson)
    # print(attributes)
    return attributes["star_rating"]

def PlayerData(userId, statType):
    

    if not (statType in statTypes):
        return ["", []]

    responsejson = requests.get(f"{API_URL}/users/{userId}/scores/best", headers=authHeaders, params=params)
    scores = responsejson.json()
    
    if "error" in scores:
        return ["", []]
    
    statTuples = []

    for score in scores:
        bm = score.get("beatmap")
        stat = -1
        if statType in mapStats:
            stat = bm.get(mapStats[statType])
        elif statType in scoreStats:
            stat = score.get(scoreStats[statType])

        # Apply mods to the stat
        mods = score.get("mods")
        url = bm.get("url")
        if (statType == "Star Rating"):
            # print("BEATMAP: ", bm)
            stat = round(getDifficulty(bm.get("id"), mods, stat), 2)
            # print("SR:", stat)
        else:
            stat = round(applyMods(mods, statType, stat), 2)
        modStr = ""
        for mod in mods:
            modStr += mod + ", "
        if len(modStr) == 0:
            modStr = "NM"
        else:
            modStr = modStr[0:len(modStr) - 2]
        
        id = bm.get("id")
        title = score.get("beatmapset").get("title")
        statTuples.append((id, stat, title, modStr, url))

    statTuples.sort(key=lambda m: m[1])
    statTuples.reverse()
    for i in range(len(statTuples)):
        lst = list(statTuples[i])
        lst[1] = "{:,}".format(lst[1])
        statTuples[i] = (i + 1,) + tuple(lst)

    return [statType, statTuples]