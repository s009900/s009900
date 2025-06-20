import sys
import datetime

username = sys.argv[1]
title = sys.argv[2]
body = sys.argv[3]
issue_url = sys.argv[4]

entry = f'- **[@{username}]({issue_url})**: {title}\n  > {body.strip()}\n  _({datetime.date.today()})_\n\n'

with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_marker = '<!-- GUESTBOOK:START -->'
end_marker = '<!-- GUESTBOOK:END -->'

start_idx = lines.index(next(filter(lambda l: start_marker in l, lines)))
end_idx = lines.index(next(filter(lambda l: end_marker in l, lines)))

new_lines = (
    lines[:start_idx+1] +
    [entry] +
    lines[start_idx+1:end_idx] +
    lines[end_idx:]
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
