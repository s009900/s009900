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

def generate_colorful_background(width, height):
    """Generate a colorful gradient background."""
    # Create a grid of points
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    X, Y = np.meshgrid(x, y)
    
    # Create RGB channels with different gradients
    r = X  # Red increases with x
    g = Y  # Green increases with y
    b = 0.5 + 0.5*np.sin(10*X*Y)  # Blue has a wave pattern
    
    # Combine into an RGB image
    img = np.dstack((r, g, b))
    return (img * 255).astype(np.uint8)

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
        # Create a colorful background
        width, height = 1600, 800
        color_image = generate_colorful_background(width, height)
        
        # Create a mask from the color image (white = keep, black = mask out)
        mask = 255 - np.mean(color_image, axis=2).astype(np.uint8)
        
        # Generate word cloud with smaller text settings
        wc = WordCloud(
            width=width,
            height=height,
            background_color=None,
            mode='RGBA',
            mask=mask,
            max_words=300,  # Increased number of words
            contour_width=0,
            prefer_horizontal=0.9,
            min_font_size=6,   # Much smaller minimum font size
            max_font_size=80,  # Reduced maximum font size
            margin=2,          # Reduced margin between words
            random_state=42,
            collocations=False,
            normalize_plurals=True,
            relative_scaling=0.4,  # More variation in word sizes
            color_func=lambda *args, **kwargs: 'white'  # Words will be white, we'll color them later
        ).generate_from_frequencies(word_freq)
        
        # Create figure with black background
        plt.figure(figsize=(16, 8), facecolor='black', edgecolor='none')
        
        # Show the colorful background
        plt.imshow(color_image, alpha=0.9)
        
        # Generate word colors based on the background
        image_colors = ImageColorGenerator(color_image)
        
        # Plot the word cloud with colors from the background
        plt.imshow(wc.recolor(color_func=image_colors), alpha=0.8, interpolation='bilinear')
        
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
