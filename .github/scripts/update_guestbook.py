import sys
import datetime

def main():
    try:
        username = sys.argv[1]
        title = sys.argv[2]
        body = sys.argv[3]
        issue_url = sys.argv[4]
        
        # Format the date
        today = datetime.date.today().strftime('%Y-%m-%d')
        
        # Create a table row for the entry
        entry = f"| **{username}** | {body.strip()} | {today} |\n"
        
        # Read the README
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Define the markers
        start_marker = '<!-- GUESTBOOK:START -->'
        end_marker = '<!-- GUESTBOOK:END -->'
        
        # Find the position of the markers
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            print("Error: Could not find guestbook markers in README.md")
            sys.exit(1)
        
        # Get the content before and after the guestbook section
        before = content[:start_idx + len(start_marker)]
        after = content[end_idx:]
        
        # Get the current guestbook content
        guestbook_content = content[start_idx + len(start_marker):end_idx].strip()
        
        # If this is the first entry, replace the default message
        if "No entries yet" in guestbook_content:
            guestbook_content = ""
        
        # Add the new entry to the guestbook
        guestbook_content = f"\n{entry}" + guestbook_content
        
        # Write the updated content back to the README
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(before)
            f.write("\n")
            f.write("| Name | Message | Date |\n")
            f.write("|------|---------|------|\n")
            f.write(guestbook_content.strip())
            f.write("\n")
            f.write(after)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
