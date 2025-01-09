from perceval.backends.core.github import GitHub as Github  # pip install perceval

from dotenv import load_dotenv # pip install python-dotenv
import json
import os

'''
Como usar o token:
criar um arquivo config.env, inserir
GITHUB_TOKEN=<personal_access_token>
'''

load_dotenv('config.env')
# Retrieve the token from the environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set it in config.env")


# Define the repository details
OWNER = "tensorflow"
REPO = "tensorflow"
print("token: ", GITHUB_TOKEN)
# exit()

# Initialize the Github backend
# github = Github(owner=OWNER, repository=REPO, api_token=GITHUB_TOKEN)
github = Github(owner=OWNER, repository=REPO, sleep_for_rate=True, api_token=[GITHUB_TOKEN])#, api_token=GITHUB_TOKEN)

# Fetch pull requests
pr_data = []
count = 0
i = 0
max_prs = 1000  # Limit to the first 2000 PRs

print(f"Fetching pull requests for {OWNER}/{REPO}...")
for pr in github.fetch(category="pull_request"):
    i += 1
    # print(pr)
    if pr['data']['state'] == 'closed' and not pr['data']['merged']: #only rejected PRs
        pr_data.append(pr)
        count += 1
        if count >= max_prs:
            break
    if i % 10 == 0:  # Status update every 100 PRs
        print(f"Fetched {i} PRs, has data on {count}...")

# Save data to a JSON file
output_file = f"{OWNER}_{REPO}_prs.json"
with open(output_file, "w") as f:
    json.dump(pr_data, f, indent=4)

print(f"Saved {len(pr_data)} pull requests to {output_file}.")
