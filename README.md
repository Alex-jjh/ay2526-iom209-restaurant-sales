# IOM209 Coursework — Restaurant Sales Analysis

## Project Overview

This project analyzes sales data from **"The Bistro"**, a fictional casual dining restaurant located in **Austin, Texas, USA**, to investigate how external factors (economic, weather, psychological, competitive) influence consumer taste preferences and food ordering behavior.

- **Dataset**: ~17,534 transaction records (Jan 2022 – Dec 2023)
- **Menu**: 26 items across 5 categories (Main Dishes, Starters, Side Dishes, Desserts, Drinks)
- **8 Hypotheses** tested across 4 dimensions

## Repository Structure

```
├── data/
│   ├── raw/
│   │   ├── restaurant_sales_data.csv          # Original raw sales data
│   │   └── the_bistro_data.xlsx               # Excel version of raw data
│   ├── cleaned/
│   │   ├── restaurant_sales_data_cleaned.csv  # After Step 1 cleaning
│   │   └── restaurant_sales_data_enriched.csv # With menu classification merged
│   ├── step2/
│   │   └── restaurant_sales_data_step2.csv    # Enriched + weather/trend features
│   └── external/
│       ├── economic_cpi_2022_2023.csv
│       ├── economic_unemployment_austin_2022_2023.csv
│       ├── economic_consumer_sentiment_2022_2023.csv
│       ├── economic_tech_layoffs_austin_2022_2023.csv
│       ├── food_cpi_2022_2023.csv
│       ├── weather_austin_daily_2022_2023.csv
│       ├── trend_comfortfood.csv
│       ├── trend_healthyeating.csv
│       ├── trend_plantbasedfood.csv
│       └── trend_stress.csv
├── notebooks/
│   ├── analysis.ipynb                         # Initial EDA (Chinese comments)
│   ├── step1_restaurant_context.ipynb         # Step 1: Restaurant context & data cleaning
│   └── step2_theoretical_framework.ipynb      # Step 2: Theoretical framework & hypotheses
├── references/
│   ├── menu_classification_reference.csv      # Menu item classification table
│   ├── step2_hypotheses.csv                   # 8 hypotheses (H1–H8)
│   ├── step2_causes_summary.csv               # Cause–mechanism–reference mapping
│   ├── step2_references.csv                   # Academic references
│   ├── step2_theoretical_framework.xlsx       # Excel export of Step 2
│   └── data_collection_guide.md               # Guide for collecting external data
└── README.md
```

## Analysis Steps

| Step | Notebook | Description |
|------|----------|-------------|
| 1 | `step1_restaurant_context.ipynb` | Define restaurant context (location, target customer, menu profile), clean raw data, add time features and menu classification |
| 2 | `step2_theoretical_framework.ipynb` | Identify 4 dimensions × 8 causes of taste preference changes, build theoretical framework with academic references, formulate testable hypotheses |
| 3 | (Data collection) | Collect external data (CPI, unemployment, weather, Google Trends) per `data_collection_guide.md` |
| EDA | `analysis.ipynb` | Exploratory data analysis on raw sales data |

## Hypotheses

| ID | Dimension | Hypothesis |
|----|-----------|------------|
| H1 | Economic | Higher inflation → ↓ premium protein orders, ↑ carb-based orders |
| H2 | Economic | Tech layoffs → ↑ comfort food, ↓ healthy options |
| H3 | Weather | Higher temperature → ↑ cold food/drink, ↓ hot food |
| H4 | Weather | Winter quarters → ↑ indulgent, ↓ healthy |
| H5 | Psychological | January health consciousness peak; weekends more indulgent |
| H6 | Psychological | Mondays & April (tax season) → ↑ dessert/comfort food |
| H7 | Competitive | Plant-based trend → ↑ Vegetarian Platter & Grilled Vegetables |
| H8 | Competitive | Competitor promotions → shift to value-tier items |

## Tech Stack

- Python 3.x (pandas, numpy, matplotlib, seaborn)
- Jupyter Notebook

## Data Sources

- **Economic**: FRED (CPI, Unemployment, Consumer Sentiment)
- **Weather**: NOAA / Visual Crossing (Austin daily weather)
- **Trends**: Google Trends (healthy eating, comfort food, plant-based, stress)
- **Layoffs**: layoffs.fyi / TWC WARN notices

## Note

The sales dataset is synthetic/simulated for academic coursework purposes.
