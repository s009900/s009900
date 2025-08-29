import requests

USERNAME = "s009900"
FOLLOWERS_API = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
PLACEHOLDER_START = "<!--LAST_FOLLOWERS_START-->"
PLACEHOLDER_END = "<!--LAST_FOLLOWERS_END-->"
FOLLOWER_COUNT = 10  # Change this to show more/less followers

def get_followers():
    followers = []
    page = 1
    while True:
        resp = requests.get(FOLLOWERS_API + f"&page={page}")
        data = resp.json()
        if not data:
            break
        followers.extend(data)
        if len(data) < 100:
            break
        page += 1
    return followers

def render_followers_table(followers, count=FOLLOWER_COUNT):
    lines = []
    lines.append("| # | Avatar | Username |")
    lines.append("|---|--------|----------|")
    for idx, follower in enumerate(followers[-count:][::-1], 1):
        login = follower["login"]
        url = follower["html_url"]
        avatar = follower["avatar_url"]
        lines.append(f"| {idx} | <img src=\"{avatar}\" width=\"24\" /> | [{login}]({url}) |")
    return "\n".join(lines)

def update_readme(table_md):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find(PLACEHOLDER_START)
    end = content.find(PLACEHOLDER_END)
    if start == -1 or end == -1:
        # Add placeholder if not present
        content += f"\n## Last Followers\n{PLACEHOLDER_START}\n{table_md}\n{PLACEHOLDER_END}\n"
    else:
        content = (
            content[: start + len(PLACEHOLDER_START)]
            + "\n"
            + table_md
            + "\n"
            + content[end:]
        )
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    followers = get_followers()
    table_md = render_followers_table(followers, FOLLOWER_COUNT)
    update_readme(table_md)
