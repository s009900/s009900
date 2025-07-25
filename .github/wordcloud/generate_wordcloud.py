import os
import sys
import json
import logging
import datetime
from pathlib import Path
from collections import Counter
import matplotlib
# Use 'Agg' backend for non-interactive environments (like GitHub Actions)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def setup_logging():
    """Set up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_script_dir():
    """Get the directory where this script is located."""
    return Path(__file__).parent.absolute()

def load_words():
    """Load words from the JSON file."""
    script_dir = get_script_dir()
    words_file = script_dir / 'words.json'
    
    try:
        with open(words_file, 'r', encoding='utf-8') as f:
            words = json.load(f)
            if not isinstance(words, list):
                logging.warning("words.json does not contain a list, initializing with empty list")
                return []
            return words
    except FileNotFoundError:
        logging.warning("words.json not found, using default words")
        return ["GitHub", "Open Source", "Welcome"]
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding words.json: {e}")
        return ["Error", "Check", "words.json"]

def generate_wordcloud():
    """Generate and save a word cloud image."""
    # Set up paths
    script_dir = get_script_dir()
    output_dir = script_dir.parent.parent / 'assets'  # Goes up two levels to reach repo root
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'wordcloud.png'
    
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Output file: {output_file}")
    
    # Load words
    words = load_words()
    logging.info(f"Loaded {len(words)} words")
    
    if not words:
        words = ["GitHub", "Open Source", "Welcome"]
    
    # Count word frequencies
    word_freq = Counter(words)
    logging.info(f"Word frequencies: {dict(word_freq.most_common(5))}...")
    
    # Generate word cloud
    try:
        # Create a color function for better visibility
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            return colors[random_state.randint(0, len(colors) - 1)]
        
        # Generate word cloud with improved settings
        wc = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            colormap='viridis',
            max_words=100,  # Reduced for better visibility
            contour_width=1,
            contour_color='#333333',
            prefer_horizontal=0.9,
            min_font_size=30,  # Increased minimum font size
            max_font_size=400,  # Increased maximum font size
            margin=10,
            random_state=42,
            collocations=False,
            normalize_plurals=True,
            relative_scaling=0.5,
            color_func=color_func
        ).generate_from_frequencies(word_freq)
        
        # Create figure
        plt.figure(figsize=(16, 9), dpi=100)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save the figure with high quality settings
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.1, dpi=300, format='png', 
                   metadata={'Creation Time': str(datetime.datetime.now())})
        plt.close()
        
        # Verify the file was created
        if output_file.exists():
            file_size = output_file.stat().st_size / 1024  # Size in KB
            logging.info(f"Successfully generated word cloud: {output_file} ({file_size:.1f} KB)")
            return True
        else:
            logging.error("Failed to generate word cloud: Output file not created")
            return False
            
    except Exception as e:
        logging.error(f"Error generating word cloud: {e}", exc_info=True)
        return False

def main():
    """Main function to run the script."""
    setup_logging()
    logging.info("Starting word cloud generation...")
    
    try:
        success = generate_wordcloud()
        if not success:
            logging.error("Word cloud generation failed")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
