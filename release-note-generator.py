import requests
import json
import argparse
#import re

parser = argparse.ArgumentParser(description='Python3 script to generate release notes')
parser.add_argument('--owner', help='provide use id of repo owner', required=True)
parser.add_argument('--repo', help='provide name of github repo', required=True)
parser.add_argument('--token', help='provide github token', required=True)
parser.add_argument('--api', help='provide api website, default is api.github.com', default='api.github.com', required=False)
parser.add_argument('--branch', help='provide origin branch, default is set to main', default='main', required=False)
args = parser.parse_args()

WEBSITE = args.api
ORIGIN_BRANCH = args.branch
OWNER = args.owner
REPO = args.repo
GITHUB_TOKEN = args.token

PATH = "https://{}/repos/{}/{}".format(WEBSITE, OWNER, REPO)

headers = {
  "Content-Type" : "application/json",
  "Authorization" : "token " + GITHUB_TOKEN
}

# Model
change_list = {
  "breaking" : [],   # major
  "feature" : [],    # minor
  "bug" : []         # patch
}

changelog_header = {
  "breaking" : "Breaking Changes",            # major
  "feature" : "Features and Enhancements",    # minor
  "bug" : "Bug Fixes"                         # patch
}

semantic_version = {
  "breaking" : 0,   # major
  "feature" : 0,    # minor
  "bug" : 0         # patch
}

semantic_flag = {
  "breaking" : False,   # major
  "feature" : False,    # minor
  "bug" : False         # patch
}

# Find the tag for the latest release
response = requests.get(PATH + '/releases/latest', headers=headers)
resjson = json.loads(response.text)
tag_name = resjson["tag_name"]

# Parse semantic version of latest release
# Format : v1.2.3
tag_parts = tag_name.split(".")
semantic_version["breaking"] = int(tag_parts[0][1:]) # ignoring v
semantic_version["feature"] = int(tag_parts[1])
semantic_version["bug"] = int(tag_parts[2])

# List Pending PRs that are not merged in the latest release
# This is done by comparing the latest release with main / master
pending_pr_list = []
response = requests.get(PATH + '/compare/' + tag_name + '...' + ORIGIN_BRANCH, headers=headers)
resjson = json.loads(response.text)
for entry in resjson["commits"]:
  message = entry["commit"]["message"]
  # use regex
  if "Merge pull request" in message:
    pr_num = message.split("#")[1].split(" ")[0]
    pending_pr_list.append(pr_num)

# Find details of the PRs not part of latest release
for pr_num in pending_pr_list:
  changelog_entry = {"pr_num" : "", "title" : "", "assignees" : []}
  changelog_entry["pr_num"] = pr_num
  response = requests.get(PATH + '/pulls/' + pr_num)
  resjson = json.loads(response.text)
  entry = resjson
  # check label(s)
  header = ""
  for label in entry["labels"]:
    if label["name"] in ["breaking", "feature", "bug"]:
      header = label["name"]
      break
  changelog_entry["title"] = entry["title"]
  # check assignee(s)
  for assignee in entry["assignees"]:
    changelog_entry["assignees"].append(assignee["login"])
  change_list[header].append(changelog_entry)

# create changelog for release note
changelog = ""
for key, values in change_list.items():
  line = ""
  if len(values) <= 0:
    continue
  semantic_flag[key] = True
  line = line + "###" + " " + changelog_header[key]
  line = line + '\n'
  line = line + "---"
  line = line + '\n'
  for value in values:
    line = line + " - " + " " + value["title"] + " " + "#" + value["pr_num"]
    for assignee in value["assignees"]:
      line = line + ", @" + assignee
    line = line + "\n"
  changelog = changelog + line

# set the updated version
if semantic_flag["breaking"]:
  semantic_version["breaking"] = semantic_version["breaking"] + 1
  semantic_version["feature"] = 0
  semantic_version["bug"] = 0
elif semantic_flag["feature"]:
  semantic_version["feature"] = semantic_version["feature"] + 1
  semantic_version["bug"] = 0
elif semantic_flag["bug"]:
  semantic_version["bug"] = semantic_version["bug"] + 1
new_tag_name = "v{}.{}.{}".format(semantic_version["breaking"], semantic_version["feature"], semantic_version["bug"])

# Post the brand new release
payload = {
  "tag_name" : new_tag_name,
  "name": new_tag_name,
  "body": changelog
}

if payload["body"] == "":
  print("Error: No new PR merged since latest release")
  exit()

response = requests.post(PATH + '/releases', headers=headers, json=payload)
resjson = json.loads(response.text)
# In case of error, documentation is suggested in the response
if "documentation_url" in resjson:
  print(resjson)

# response should be in json format
