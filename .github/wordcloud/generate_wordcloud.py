from wordcloud import WordCloud
import json
import os
from collections import Counter
import matplotlib.pyplot as plt

def load_words():
    try:
        with open('.github/wordcloud/words.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_words(words):
    with open('.github/wordcloud/words.json', 'w') as f:
        json.dump(words, f)

def generate_wordcloud():
    # Load words
    words = load_words()
    if not words:
        words = ["GitHub", "Open Source", "Welcome"]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Generate word cloud
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
        contour_width=1,
        contour_color='steelblue'
    ).generate_from_frequencies(word_freq)
    
    # Save the image
    plt.figure(figsize=(16, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    
    # Create output directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Save the figure
    plt.savefig('assets/wordcloud.png', bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_wordcloud()
