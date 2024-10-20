import requests
import os
from pprint import pprint
from dotenv import load_dotenv
import json

import user_stories_automation as us_st


load_dotenv()

API_BASE_URL = "https://api.github.com"
FINE_GITHUB_API = os.getenv("FINE_GITHUB_TOKEN")
OWNER = os.getenv("OWNER")
REPO_NAME = os.getenv("REPO_NAME")

headers = {
    "Authorization": f"token {FINE_GITHUB_API}",
    "Accept": "application/vnd.github+json",
}

# Request the github repository
try:
    api_request = requests.get(
        API_BASE_URL + "/repos/{OWNER}/{REPO}",
        headers=headers
    )
except requests.exceptions.RequestException as err:
    raise SystemExit(err)

# Create an issue on the repository
payload = json.dumps({"title": us_st.issue_title, "body": us_st.issue_body})
print(payload)

try:
    new_issue = requests.post(
        API_BASE_URL + f"/repos/{OWNER}/{REPO_NAME}/issues",
        payload,
        headers=headers,
    )
except requests.exceptions.RequestException as err:
    raise SystemExit(err)

print(new_issue.status_code)


# List all default labels for the repository

try:
    list_request = requests.get(
        API_BASE_URL + f"/repos/{OWNER}/{REPO_NAME}/labels",
        headers=headers
    )
except requests.exceptions.RequestException as err:
    raise SystemExit(err)

list_default_labels = [label.get("name") for label in list_request.json()]
print(list_default_labels)

# Delete all default labels

for label in list_default_labels:
    try:
        deletion = requests.delete(
            API_BASE_URL + f"/repos/{OWNER}/{REPO_NAME}/labels/{label}",
            headers=headers
        )
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    print(f"{label} deletion status: {deletion.status_code}")


# Create new labels for the repository
for i in range(1, 14):
    payload = json.dumps(
        {
            "name": us_st.label_names[i],
            "description": us_st.label_descriptions[i],
            "color": us_st.label_colors[i]},
    )

    try:
        new_label = requests.post(
            API_BASE_URL + f"/repos/{OWNER}/{REPO_NAME}/labels",
            payload,
            headers=headers
        )
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    print(new_label.status_code)
