import requests
import os

USERNAME = "s009900"
FOLLOWERS_API = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
PLACEHOLDER_START = "<!--LAST_FOLLOWERS_START-->"
PLACEHOLDER_END = "<!--LAST_FOLLOWERS_END-->"

def get_followers():
    followers = []
    page = 1
    while True:
        resp = requests.get(FOLLOWERS_API + f"&page={page}")
        data = resp.json()
        if not data:
            break
        followers.extend(data)
        page += 1
        if len(data) < 100:
            break
    return followers

def render_followers(followers, count=5):
    lines = []
    for idx, follower in enumerate(followers[-count:][::-1], 1):
        login = follower["login"]
        url = follower["html_url"]
        avatar = follower["avatar_url"]
        lines.append(f'{idx}. <a href="{url}"><img src="{avatar}" width="20" /> {login}</a>')
    return "\n".join(lines)

def update_readme(followers_md):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find(PLACEHOLDER_START)
    end = content.find(PLACEHOLDER_END)
    if start == -1 or end == -1:
        # Add placeholder if not present
        content += f"\n{PLACEHOLDER_START}\n{followers_md}\n{PLACEHOLDER_END}\n"
    else:
        content = content[:start + len(PLACEHOLDER_START)] + "\n" + followers_md + "\n" + content[end:]
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    followers = get_followers()
    followers_md = render_followers(followers, count=5)
    update_readme(followers_md)
