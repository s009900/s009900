import os
import re
import sys
from github import Github

def extract_field(field_name, body):
    match = re.search(rf'### {re.escape(field_name)}[\s\S]*?###', body + '###')
    if not match:
        return ''
    content = match.group(0).split('\r\n', 1)[1].rsplit('###', 1)[0].strip()
    return content.replace('\r\n', ' ').strip()

def main():
    # Get environment variables
    github_token = os.environ['GITHUB_TOKEN']
    repo_name = os.environ['GITHUB_REPOSITORY']
    issue_number = int(os.environ['ISSUE_NUMBER'])
    
    # Initialize GitHub client
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    # Get all guestbook issues
    issues = repo.get_issues(labels=['guestbook'], state='all', sort='created', direction='desc')
    
    # Collect all entries
    all_entries = []
    for issue in issues:
        try:
            body = issue.body
            if not body:
                continue
                
            emoji = extract_field('Pick an emoji', body)
            name = extract_field('Your Name (or GitHub username)', body)
            message = extract_field('Your Message', body)
            link = extract_field('Link (optional)', body)
            
            if message and name:
                all_entries.append({
                    'emoji': emoji or '✨',
                    'name': name,
                    'link': link if link and link != "_No response_" else None,
                    'message': message,
                    'date': issue.created_at.strftime('%Y-%m-%d')
                })
        except Exception as e:
            print(f'Error processing issue #{issue.number}: {str(e)}', file=sys.stderr)
    
    # Sort entries by date (newest first)
    all_entries.sort(key=lambda x: x['date'], reverse=True)
    
    # Create the guestbook table
    guestbook_table = '### Recent Guestbook Entries\n\n'
    guestbook_table += '| Emoji | Name | Message | Date |\n'
    # Add table header separator
    guestbook_table += '|:-----:|:----:|:-------:|:----:|\n'
    # Add entries
    for entry in all_entries[:10]:  # Show up to 10 most recent entries
        name_display = f'[{entry["name"]}]({entry["link"]})' if entry['link'] else entry['name']
        guestbook_table += f'| {entry["emoji"]} | {name_display} | {entry["message"]} | {entry["date"]} |\n'
    # Update README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    guestbook_start = '<!-- Guestbook -->'
    guestbook_end = '<!-- /Guestbook -->'
    
    before = content.split(guestbook_start)[0]
    after = content.split(guestbook_end)[1]
    
    new_guestbook = f'''{guestbook_start}

## 📝 Guestbook

Leave your mark in my guestbook! Share a message, a joke, or just say hi. I'd love to hear from you! 😊

[Sign the Guestbook](https://github.com/s009900/s009900/issues/new?template=guestbook.yml&title=Guestbook%3A+Your+Name) ➠•  [View All Entries](https://github.com/s009900/s009900/issues?q=is%3Aissue+label%3Aguestbook+sort%3Acreated-desc)

{guestbook_table}

*Showing {min(10, len(all_entries))} of {len(all_entries)} entries. [View all](https://github.com/s009900/s009900/issues?q=is%3Aissue+label%3Aguestbook+sort%3Acreated-desc)*

{guestbook_end}'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(f'{before}{new_guestbook}{after}')
    
    # Configure git
    os.system('git config --global user.name "GitHub Actions"')
    os.system('git config --global user.email "actions@github.com"')
    
    # Commit changes
    os.system('git add README.md')
    os.system('git commit -m "Update guestbook with new entry"')
    os.system('git push')
    
    # Add a comment and close the issue
    issue.create_comment('🎉 Thank you for signing my guestbook! Your message has been added to my README.')
    issue.edit(state='closed')

if __name__ == '__main__':
    main()
