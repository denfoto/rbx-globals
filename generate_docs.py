import requests
import yaml
import json
import time
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE = "https://api.github.com/repos/Roblox/creator-docs/contents/content/en-us/reference/engine"

FOLDERS = ["libraries", "globals", "enums", "datatypes"]

def get_files(folder):
    url = f"{BASE}/{folder}"
    return requests.get(url).json()

def get_yaml(url):
    return yaml.safe_load(requests.get(url).text)

def process(folder):
    data = {}
    files = get_files(folder)

    for f in files:
        if f["name"].endswith(".yaml"):
            name = f["name"].replace(".yaml", "")
            print(f"{folder}: {name}")

            try:
                data[name] = get_yaml(f["download_url"])
            except Exception as e:
                print("Error:", e)

            time.sleep(0.1)

    return data

for folder in FOLDERS:
    result = process(folder)

    filepath = os.path.join(SCRIPT_DIR, f"{folder}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    
    print(f"Saved {folder}.json")