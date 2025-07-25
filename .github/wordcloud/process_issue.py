import json
import os
import sys
from pathlib import Path

def parse_issue_body(issue_body):
    """Parse the word from the issue body"""
    if not issue_body:
        return None
        
    # Look for the word after "### Word to Add"
    word_section = issue_body.split("### Word to Add")
    if len(word_section) < 2:
        return None
        
    # Get the first line after the section header
    lines = [line.strip() for line in word_section[1].split('\n') if line.strip()]
    if not lines:
        return None
        
    return lines[0].strip()

def update_words_json(word):
    """Update the words.json file with the new word"""
    if not word:
        return False
        
    words_path = Path('.github/wordcloud/words.json')
    
    # Create directory if it doesn't exist
    words_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize with default words if file doesn't exist
    if not words_path.exists():
        words = ["GitHub", "Open Source", "s009900", "Collaboration", "Code", "Fun", "Awesome"]
    else:
        try:
            with open(words_path, 'r') as f:
                words = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            words = []
    
    # Add the new word if it's not already there
    if word not in words:
        words.append(word)
        
        # Save the updated list
        with open(words_path, 'w') as f:
            json.dump(words, f, indent=2)
        
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_issue.py <issue_body>")
        sys.exit(1)
        
    issue_body = sys.argv[1]
    word = parse_issue_body(issue_body)
    
    if not word:
        print("No valid word found in the issue body")
        sys.exit(0)
        
    if update_words_json(word):
        print(f"Successfully added '{word}' to words.json")
    else:
        print(f"Word '{word}' already exists in words.json")

if __name__ == "__main__":
    main()
