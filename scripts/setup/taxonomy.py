import os
import json
from ebird.api import get_taxonomy
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EBIRD_API_KEY")

local_file = "life-list/taxonomy.json"

def fetch_and_save_taxonomy():
    taxonomy = get_taxonomy(api_key)
    with open(local_file, "w") as f:
        json.dump(taxonomy, f, indent=2)

    print("Taxonomy downloaded and saved locally.")

if not os.path.exists(local_file):
    fetch_and_save_taxonomy()
else:
    print(f"Local taxonomy file '{local_file}' already exists. Delete it to refresh.")
