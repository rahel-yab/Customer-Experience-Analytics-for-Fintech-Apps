import pandas as pd
from google_play_scraper import reviews_all, Sort

# --- Configuration ---
BANK_APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'Bank of America': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.dashen.dashensuperapp'
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


# --- Preprocessing Steps ---

# 1. Drop Duplicates
clean_df = raw_df.drop_duplicates(subset=['review', 'date', 'bank'])
print(f"Removed {len(raw_df) - len(clean_df)} duplicate reviews.")

# 2. Handle Missing Data
# The KPI is <5% errors/missing. We remove rows with missing critical data.
clean_df.dropna(subset=['review', 'rating'], inplace=True)
print(f"Removed rows with missing reviews or ratings.")

# 3. Normalize Date Format (to YYYY-MM-DD)
# The 'date' column is a datetime object after scraping (under the hood).
# Convert it to a datetime object, then format it as a string.
clean_df['date'] = pd.to_datetime(clean_df['date']).dt.strftime('%Y-%m-%d')
print("Dates normalized to YYYY-MM-DD format.")

# 4. Final KPI Check
total_reviews = len(clean_df)
print(f"\n--- KPI CHECK ---")
print(f"Total clean reviews collected: **{total_reviews}**")
if total_reviews >= 1200:
    print("✅ Volume KPI (1,200+) Met.")
else:
    print(f"⚠️ Volume KPI not met. Scraped {total_reviews}. You may need to run the scraper again or find more App IDs.")

# 5. Save Final Clean Data
# Ensure columns are exactly as required: review, rating, date, bank, source
final_columns = ['review', 'rating', 'date', 'bank', 'source']
clean_df[final_columns].to_csv('clean_bank_reviews.csv', index=False)
print("\n✅ Final Clean CSV saved as **clean_bank_reviews.csv**")