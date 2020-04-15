import requests
from pprint import pprint

def get_change_id():
    return requests.get("https://poe.ninja/api/data/getstats").json()['next_change_id']

def get_data(league):
    flatten = lambda l: [item for sublist in l for item in sublist]

    arr = [
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=BaseType").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueWeapon").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueArmour").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueAccessory").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueJewel").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueFlask").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=UniqueMap").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=Map").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=Fossil").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=Scarab").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=Oil").json()["lines"],
        requests.get(f"https://poe.ninja/api/data/itemoverview?league={league}&type=Incubator").json()["lines"],
    ]

    return flatten(arr)

# def get_data():
#     data = requests.get(f"http://api.pathofexile.com/public-stash-tabs/?id={get_change_id()}").json()['stashes']
#     return data

