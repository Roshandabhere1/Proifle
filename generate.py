import requests
from jinja2 import Environment, FileSystemLoader
import os

GITHUB_USERNAME = "YOUR_USERNAME"
TOKEN = "YOUR_GITHUB_TOKEN"

def fetch_data():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

    headers = {"Authorization": f"token {TOKEN}"}

    user = requests.get(url, headers=headers).json()
    repos = requests.get(repos_url, headers=headers).json()

    # sort repos by stars
    repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:6]

    return user, repos

def generate_site():
    user, repos = fetch_data()

    env = Environment(loader=FileSystemLoader("template"))
    template = env.get_template("index.html.jinja")

    html = template.render(user=user, repos=repos)

    os.makedirs("dist", exist_ok=True)
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Site generated inside dist/ folder ✔️")

if __name__ == "__main__":
    generate_site()

