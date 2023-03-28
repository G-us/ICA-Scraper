import json

# Function to parse JSON file
def parseJSONFile(filename):
    links = []
    with open(filename) as f:
        data = json.load(f)
        for i in data["links"]:
            links.append(i)
        return links
