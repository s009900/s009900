import os
import sys
import json
import logging
import datetime
import numpy as np
from pathlib import Path
from collections import Counter
import matplotlib
# Use 'Agg' backend for non-interactive environments (like GitHub Actions)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_words(json_path):
    """Load words from JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                logging.warning("JSON file does not contain a list. Converting to list format.")
                data = list(data.values()) if isinstance(data, dict) else [data]
            return data
    except FileNotFoundError:
        logging.warning(f"Words file not found at {json_path}, using default words.")
        return ["GitHub", "Open Source", "Welcome"]
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {json_path}: {e}")
        return ["GitHub", "Open Source", "Welcome"]

def generate_color_palette():
    """Generate a vibrant color palette for the word cloud."""
    return [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
    ]

def generate_word_cloud():
    """Generate and save a word cloud image."""
    # Get the directory of the current script
    script_dir = Path(__file__).parent
    
    # Define paths
    words_path = script_dir / 'words.json'
    output_dir = script_dir.parent.parent / 'assets'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'wordcloud.png'
    
    # Load words
    words = load_words(words_path)
    logging.info(f"Loaded {len(words)} words")
    
    # If no words are found, use default words
    if not words:
        logging.warning("No words found, using default words")
        words = ["GitHub", "Open Source", "Welcome"]
    
    # Count word frequencies
    word_freq = Counter(words)
    logging.info(f"Word frequencies: {dict(word_freq.most_common(5))}...")
    
    # Generate word cloud
    try:
        # Set dimensions
        width, height = 1600, 800
        
        # Generate word cloud with varied text sizes
        wc = WordCloud(
            width=width,
            height=height,
            background_color='white',
            mode='RGB',
            max_words=250,
            prefer_horizontal=0.9,
            min_font_size=8,     # Smallest words
            max_font_size=150,   # Largest words
            margin=4,            # Slight margin between words
            random_state=42,     # For reproducibility
            collocations=False,
            normalize_plurals=True,
            relative_scaling=0.8,  # More variation in word sizes
            color_func=lambda *args, **kwargs: np.random.choice(generate_color_palette())  # Random colors from our palette
        ).generate_from_frequencies(word_freq)
        
        # Create figure with white background
        plt.figure(figsize=(16, 8), facecolor='white', edgecolor='none')
        
        # Plot the word cloud
        plt.imshow(wc, interpolation='bilinear')
        
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save with metadata for cache busting
        metadata = {
            'Title': 'GitHub Word Cloud',
            'Author': 'GitHub Action',
            'Description': 'Word cloud generated from GitHub issues',
            'Generated': datetime.datetime.utcnow().isoformat()
        }
        
        # Save the figure with metadata
        plt.savefig(
            output_path,
            bbox_inches='tight',
            pad_inches=0,
            dpi=150,
            facecolor='black',
            metadata=metadata
        )
        plt.close()
        
        logging.info(f"Word cloud saved to {output_path}")
        return True
        
    except Exception as e:
        logging.error(f"Error generating word cloud: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the script."""
    logging.info("Starting word cloud generation...")
    
    try:
        success = generate_word_cloud()
        if not success:
            logging.error("Word cloud generation failed")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
