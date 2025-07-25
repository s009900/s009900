from wordcloud import WordCloud
import json
import os
import sys
import logging
from collections import Counter
import matplotlib

# Use 'Agg' backend for non-interactive environments (like GitHub Actions)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
WORDS_JSON = os.path.abspath(os.path.join(SCRIPT_DIR, 'words.json'))
OUTPUT_DIR = os.path.abspath(os.path.join(REPO_ROOT, 'assets'))
OUTPUT_IMAGE = os.path.join(OUTPUT_DIR, 'wordcloud.png')

def load_words():
    try:
        logger.info(f"Loading words from: {WORDS_JSON}")
        with open(WORDS_JSON, 'r', encoding='utf-8') as f:
            words = json.load(f)
            logger.info(f"Successfully loaded {len(words)} words")
            return words
    except FileNotFoundError:
        logger.warning(f"Words file not found at {WORDS_JSON}")
        return ["GitHub", "Open Source", "Welcome"]
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {WORDS_JSON}: {str(e)}")
        return ["Error", "Invalid", "JSON"]
    except Exception as e:
        logger.error(f"Unexpected error loading words: {str(e)}")
        return ["Error", "Loading", "Failed"]

def generate_wordcloud():
    try:
        logger.info("Starting word cloud generation...")
        
        # Load words
        words = load_words()
        if not words:
            words = ["GitHub", "Open Source", "Welcome"]
            logger.warning("No words found, using default words")
        
        logger.info(f"Generating word cloud from {len(words)} words")
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Generate word cloud with improved settings
        wc = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=200,
            contour_width=1,
            contour_color='steelblue',
            prefer_horizontal=0.9,
            min_font_size=10,
            max_font_size=200,
            relative_scaling=0.5
        ).generate_from_frequencies(word_freq)
        
        # Create output directory if it doesn't exist
        logger.info(f"Ensuring output directory exists: {OUTPUT_DIR}")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Save the image
        logger.info("Creating figure and saving word cloud...")
        plt.figure(figsize=(16, 8), facecolor='white')
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        logger.info(f"Saving word cloud to: {OUTPUT_IMAGE}")
        plt.savefig(
            OUTPUT_IMAGE,
            bbox_inches='tight',
            pad_inches=0,
            dpi=150,
            optimize=True
        )
        plt.close()
        
        # Verify the file was created
        if os.path.exists(OUTPUT_IMAGE):
            size_kb = os.path.getsize(OUTPUT_IMAGE) / 1024
            logger.info(f"Successfully generated word cloud: {size_kb:.1f} KB")
            return True
        else:
            logger.error("Failed to save word cloud image")
            return False
            
    except Exception as e:
        logger.error(f"Error generating word cloud: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = generate_wordcloud()
    sys.exit(0 if success else 1)
