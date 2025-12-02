# Customer Experience Analytics for Fintech Apps

## 🎯 Project Overview

This project provides data-driven insights into customer satisfaction and pain points for mobile banking applications using advanced Natural Language Processing (NLP) techniques. We analyze user reviews from the Google Play Store to quantify sentiment and identify recurring themes across different banks.

**Target Banks:**

1. Commercial Bank of Ethiopia (CBE)

2. Bank of Abyssinia (BoA)

3. Dashen Bank

## 💡 Key Findings

The analysis of 1,200 clean reviews revealed that **Access & Reliability** (issues like login failures, app crashes, and bugs) is the most critical pain point across all three institutions, consistently driving the lowest positive sentiment scores.

| Theme | Universal Impact | 
| :--- | :--- | 
| **Access & Reliability** | **Primary Pain Point.** Lowest positive sentiment (e.g., Dashen Bank at 59.8%). Requires urgent technical stability fixes. | 
| **Transaction Performance** | **Primary Driver.** Highest positive sentiment (e.g., Bank of Abyssinia at 90.5%). Core functionality is successful. | 
| **User Experience (UX/UI)** | **Secondary Pain Point.** Moderate dissatisfaction due to "clunky" design and confusing navigation. | 

## 🛠️ Project Structure and Methodology

The project is executed via two main Python scripts across four analytical tasks:

| Task | Script | Description | 
| :--- | :--- | :--- | 
| **Task 1: Data Collection** | `scrape_reviews.py` | Scrapes 400 reviews from each of the three target apps (1,200 total), cleans the data (removes duplicates/missing values), and saves it to `clean_bank_reviews.csv`. | 
| **Tasks 2 & 3: Analysis** | `analysis_pipeline_final.py` | 1\. **Sentiment Analysis:** Uses **DistilBERT** (HuggingFace Transformers) to assign sentiment labels and scores to every review. 2. **Thematic Analysis:** Uses **TF-IDF** and rule-based keyword matching to assign reviews to 4 key themes (e.g., 'Access & Reliability'). 3. **Aggregation:** Calculates mean positive sentiment per theme and per bank. | 

## 🚀 Getting Started

Follow these steps to set up and run the entire analysis pipeline.

### 1. Prerequisites

You need **Python 3.8+** installed on your system.

### 2. Environment Setup

It is highly recommended to use a virtual environment (`venv`).

```bash
# 1. Create a virtual environment
python3 -m venv venv
# 2. Activate the environment (Linux/macOS)
source venv/bin/activate
# 2. Activate the environment (Windows)
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries, including the deep learning components for the sentiment model.

```bash
pip install transformers torch nltk scikit-learn pandas google-play-scraper 
```

### 4. Run the Pipeline
The process involves two main steps:
Step A: Data Scraping (Task 1)
This generates the primary input file (clean_bank_reviews.csv).

    ```bash
    python scrape_reviews.py
    ```

Step B: Analysis and Aggregation (Tasks 2 & 3)
This executes the NLP models and generates the final analytical output (sentiment_and_themes.csv).

        ```bash
        python analysis_pipeline_final.py
        ```

### 5. Final Output
The sentiment_and_themes.csv file contains the original review data augmented with the sentiment_label, sentiment_score, and identified_theme(s), providing the quantitative foundation for the final report.