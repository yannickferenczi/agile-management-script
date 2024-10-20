#! python
import requests
import os
from pprint import pprint
from dotenv import load_dotenv
import argparse
import pathlib


load_dotenv()

print(pathlib.Path().resolve())


API_BASE_URL = "https://api.github.com"
FINE_GITHUB_API = os.getenv("FINE_GITHUB_TOKEN")

# Create arguments that can be passed in the CLI
parser = argparse.ArgumentParser()
parser.add_argument(
    "--name",
    type=str,
    dest="name",
    required=True
)
parser.add_argument(
    "--private",
    dest="is_private",
    action="store_true"
)
args = parser.parse_args()

# Variables
repo_name = args.name
is_private = args.is_private
repo_description = "Let's try to put a description here to see what impact it will have while creating the new repository."

if is_private:
    repo_payload = '{"name": "' + repo_name + '", "private": true }'
else:
    repo_payload = '{"name": "' + repo_name + '", "private": false }'

headers = {
    "Authorization": f"token {FINE_GITHUB_API}",
    "Accept": "application/vnd.github+json"
}

# Try to call the API to create the remote repository from template on Github
try:
    api_request = requests.post(
        API_BASE_URL + f"/repos/{os.getenv("OWNER")}/start-project-template/generate",
        data=repo_payload,
        headers=headers
    )
    api_request.raise_for_status()
    # pprint(api_request.json())
except requests.exceptions.RequestException as err:
    raise SystemExit(err)

# Try to clone the remote repository locally
try:
    REPO_PATH = pathlib.Path().resolve()
    os.chdir(REPO_PATH)
    os.system("mkdir " + repo_name)
    os.chdir(os.path.join(REPO_PATH, repo_name))
    os.system('git clone https://github.com/' + os.getenv("OWNER") + '/' + repo_name + '.git')
    # os.system("git init")
    # os.system(f'echo # {repo_name} >> README.md')
    # os.system('git add . && git commit -m "Initial commit"')
    # os.system('git branch -M main')
    # os.system('git remote add origin https://github.com/yannickferenczi/' + repo_name)
    # os.system('git push -u origin main')
except FileExistsError as err:
    raise SystemExit(err)

# Try to create a repo project
project_description = """This is an agile project manager to help its 
stakeholders focus on the scope of the project, keep track of time, and 
therefore finish a complete project before the deadline."""
project_payload = {
    "name": "Scrum Project Manager",
    "description": project_description
}
project_payload = "Project Test"
try:
    api_request = requests.get(
        API_BASE_URL + f"/users/{os.getenv("OWNER")}/projects",
        headers=headers
    )
    api_request.raise_for_status()
    # pprint(api_request.json())
except requests.exceptions.RequestException as err:
    raise SystemExit(err)
print(api_request.json())
