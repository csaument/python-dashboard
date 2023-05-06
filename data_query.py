import json
import requests
from config import PROPUBLICA_API_KEY

def get_members(congress, chamber, pages):
    url = f"https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json"
    headers = {"X-API-Key": PROPUBLICA_API_KEY}
    members = []
    page_num = 1
    while page_num <= pages:
        params = {"offset": (page_num - 1) * 20}
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            print(f"Error {response.status_code}: {response.text}")
            return members
        page_members = response.json()["results"][0]["members"]
        if not page_members:
            break
        members += page_members
        page_num += 1
    return members

senate_members = get_members(117, "senate", 5)
with open("./Data/senate_members.json", "w") as f:
    json.dump(senate_members, f)

house_members = get_members(117, "house", 22)
with open("./Data/house_members.json", "w") as f:
    json.dump(house_members, f)
