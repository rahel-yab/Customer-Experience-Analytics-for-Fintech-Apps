import pandas as pd
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
# Download the list of common English stop words
nltk.download('stopwords') 
# Download VADER lexicon (if you decide to use VADER as a baseline)
nltk.download('vader_lexicon')

# Load data - the input for this task
df = pd.read_csv('clean_bank_reviews.csv')
print(f"Loaded {len(df)} clean reviews for analysis.")

# --- STEP 1: Sentiment Analysis (using DistilBERT) ---
print("\nStarting DistilBERT Sentiment Analysis...")
# Load the specified model
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Function to safely analyze sentiment (handles truncation for long reviews)
def get_sentiment(review_text):
    # Truncate to the max length the model can handle (512 tokens is standard)
    truncated_review = review_text[:512] 
    try:
        result = sentiment_pipeline(truncated_review)[0]
        return result['label'], result['score']
    except Exception as e:
        # Handle potential errors, assigning a neutral or placeholder
        print(f"Error analyzing review: {e}")
        return 'NEUTRAL', 0.5 

# Apply the function to the DataFrame
sentiment_results = df['review'].apply(
    lambda x: get_sentiment(x) if pd.notna(x) else ('NEUTRAL', 0.0)
).to_list()

df[['sentiment_label', 'sentiment_score']] = pd.DataFrame(sentiment_results)

print("Sentiment Analysis Complete.")
# Check KPI: Sentiment scores for 90%+ reviews (if all reviews were processed, this is 100%)
print(f"Processed {len(df)} reviews.")