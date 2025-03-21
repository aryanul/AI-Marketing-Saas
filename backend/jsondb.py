import json
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"id": {}}

def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)