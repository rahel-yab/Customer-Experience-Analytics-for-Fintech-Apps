import pandas as pd
from google_play_scraper import reviews_all, Sort

# --- Configuration ---
BANK_APPS = {
    'Bank_A': 'com.package.id.for.bankA', # REPLACE WITH ACTUAL ID
    'Bank_B': 'com.package.id.for.bankB', # REPLACE WITH ACTUAL ID
    'Bank_C': 'com.package.id.for.bankC'  # REPLACE WITH ACTUAL ID
}
MIN_REVIEWS_PER_BANK = 400

# --- Scraping Function ---
def scrape_reviews(bank_name, app_id):
    """Scrapes reviews for a single app."""
    print(f"--- Starting scraping for {bank_name} ({app_id}) ---")
    
    # Use reviews_all to attempt to get as many as possible
    # Setting the limit ensures you stop once you've passed the minimum, 
    # but the scraper will naturally stop when reviews run out.
    result = reviews_all(
        app_id,
        sleep_milliseconds=0, # Set a pause if you run into rate limits (e.g., 500)
        lang='en', 
        country='us',
        sort=Sort.NEWEST # Start with the newest reviews
    )
    
    # Take the required minimum or all if fewer were found
    reviews_to_keep = result[:MIN_REVIEWS_PER_BANK]
    print(f"Successfully scraped {len(reviews_to_keep)} reviews for {bank_name}.")
    
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(reviews_to_keep)
    
    # Add metadata columns
    df['bank'] = bank_name
    df['source'] = 'Google Play Store'
    
    # Keep only required columns and rename them
    df = df[['content', 'score', 'at', 'bank', 'source']]
    df.columns = ['review', 'rating', 'date', 'bank', 'source']
    
    return df

# --- Main Execution ---
all_data = []
for bank_name, app_id in BANK_APPS.items():
    df = scrape_reviews(bank_name, app_id)
    all_data.append(df)

# Combine all bank data into one DataFrame
raw_df = pd.concat(all_data, ignore_index=True)

# Save the raw data before full cleaning (optional, but good practice)
raw_df.to_csv('01_raw_reviews.csv', index=False)
print("\n--- Raw data saved. Starting Preprocessing... ---")