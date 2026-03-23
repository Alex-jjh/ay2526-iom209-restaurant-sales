# Step 3: Data Collection Guide for "The Bistro" Analysis

## Overview

This document provides detailed instructions for collecting external data to test the 8 hypotheses proposed in Step 2. The data should cover **January 2022 - December 2023** to match our sales dataset.

**Location:** Austin, Texas, USA

---

## A. ECONOMIC DIMENSION DATA

### A1. Inflation / Consumer Price Index (CPI)

| Item | Details |
|------|---------|
| **Data Source** | FRED (Federal Reserve Economic Data) - St. Louis Fed |
| **URL** | https://fred.stlouisfed.org/series/CPIAUCSL |
| **Variable Name** | CPIAUCSL - Consumer Price Index for All Urban Consumers |
| **Frequency** | Monthly |
| **Date Range Needed** | January 2022 - December 2023 (24 months) |
| **Download Format** | CSV |

**How to Download:**
1. Go to the URL above
2. Click "Edit Graph" → Set date range: 2022-01-01 to 2023-12-31
3. Click "Download" → Select CSV
4. Save as: `economic_cpi_2022_2023.csv`

**Alternative/Additional:**
- Austin-specific CPI: https://fred.stlouisfed.org/series/CUURA316SA0 (South region)
- Food CPI only: https://fred.stlouisfed.org/series/CPIUFDSL

---

### A2. Unemployment Rate

| Item | Details |
|------|---------|
| **Data Source** | FRED / Bureau of Labor Statistics |
| **URL (Texas)** | https://fred.stlouisfed.org/series/TXUR |
| **URL (Austin MSA)** | https://fred.stlouisfed.org/series/AUST448URN |
| **Variable Name** | Unemployment Rate (%) |
| **Frequency** | Monthly |
| **Date Range Needed** | January 2022 - December 2023 |
| **Download Format** | CSV |

**How to Download:**
1. Go to URL above
2. Set date range: 2022-01-01 to 2023-12-31
3. Download CSV
4. Save as: `economic_unemployment_austin_2022_2023.csv`

---

### A3. Consumer Confidence Index (Optional but Recommended)

| Item | Details |
|------|---------|
| **Data Source** | FRED / Conference Board |
| **URL** | https://fred.stlouisfed.org/series/UMCSENT |
| **Variable Name** | University of Michigan Consumer Sentiment |
| **Frequency** | Monthly |
| **Date Range Needed** | January 2022 - December 2023 |

**Save as:** `economic_consumer_sentiment_2022_2023.csv`

---

### A4. Tech Layoffs Data (For H2 - Austin Tech Sector)

| Item | Details |
|------|---------|
| **Data Source** | Layoffs.fyi |
| **URL** | https://layoffs.fyi/ |
| **Variable Name** | Company layoff announcements with dates |
| **Frequency** | Event-based |
| **Date Range Needed** | 2022-2023 |

**How to Get Data:**
1. Visit https://layoffs.fyi/
2. Filter by: Location = Austin or Company HQ in Austin
3. Filter companies: Dell, Meta, Google, Apple, Indeed, etc.
4. Export or manually record dates and company names

**Alternative Source:**
- WARN Notices (Texas): https://www.twc.texas.gov/businesses/warn-notices-texas
- Save as: `economic_tech_layoffs_austin_2022_2023.csv`

**Required Columns:**
| Date | Company | Location | Number_Laid_Off |
|------|---------|----------|-----------------|

---

## B. WEATHER DIMENSION DATA

### B1. Temperature Data (Austin, TX)

| Item | Details |
|------|---------|
| **Data Source** | NOAA - National Centers for Environmental Information |
| **URL** | https://www.ncdc.noaa.gov/cdo-web/search |
| **Station** | Austin-Bergstrom International Airport (USW00013904) |
| **Variables Needed** | TAVG (Average Temp), TMAX (Max Temp), TMIN (Min Temp) |
| **Frequency** | Daily (can aggregate to monthly) |
| **Date Range Needed** | January 2022 - December 2023 |
| **Download Format** | CSV |

**How to Download:**
1. Go to: https://www.ncdc.noaa.gov/cdo-web/search
2. Select: "Daily Summaries"
3. Date Range: 2022-01-01 to 2023-12-31
4. Search by: "Stations" → Search "Austin Bergstrom" or ZIP 78719
5. Add to Cart → Select variables: TAVG, TMAX, TMIN, PRCP
6. Select CSV format → Submit Order (free, requires email)
7. Save as: `weather_austin_daily_2022_2023.csv`

**Alternative - Visual Crossing (Easier):**
| Item | Details |
|------|---------|
| **URL** | https://www.visualcrossing.com/weather-history/Austin,TX/us/2022-01-01/2023-12-31 |
| **Variables** | temp, tempmax, tempmin, humidity, precip |
| **Format** | CSV download available |

---

### B2. Precipitation Data

Included in the NOAA download above (PRCP variable).

**Variables to Include:**
- PRCP: Precipitation (inches)
- SNOW: Snowfall (rare in Austin, but include if available)

---

### B3. Monthly Aggregated Weather (Alternative)

| Item | Details |
|------|---------|
| **Data Source** | Weather Underground - History |
| **URL** | https://www.wunderground.com/history/monthly/us/tx/austin/KAUS/date/2022-1 |
| **Variables** | Monthly averages already calculated |

**Manual Collection:**
- Navigate month by month: change URL to `/date/2022-1`, `/date/2022-2`, etc.
- Record: Avg High, Avg Low, Avg Temp, Total Precip
- Save as: `weather_austin_monthly_2022_2023.csv`

**Required Format:**
| Year | Month | Avg_Temp_F | Max_Temp_F | Min_Temp_F | Precip_Inches |
|------|-------|------------|------------|------------|---------------|
| 2022 | 1 | 52 | 62 | 41 | 2.5 |
| 2022 | 2 | 55 | 66 | 45 | 1.8 |
| ... | ... | ... | ... | ... | ... |

---

## C. PSYCHOLOGICAL DIMENSION DATA

### C1. Google Trends - Health Consciousness

| Item | Details |
|------|---------|
| **Data Source** | Google Trends |
| **URL** | https://trends.google.com/trends/explore |
| **Variables** | Search interest (0-100 scale) |
| **Frequency** | Weekly or Monthly |
| **Date Range Needed** | January 2022 - December 2023 |
| **Location Filter** | United States (or Texas if enough data) |

**Search Terms to Download (one at a time or compare up to 5):**

**Health-Related Terms:**
1. "healthy eating"
2. "healthy recipes"
3. "diet plan"
4. "weight loss"
5. "salad recipes"

**Comfort Food Terms:**
6. "comfort food"
7. "comfort food recipes"
8. "mac and cheese recipe"
9. "chocolate cake recipe"

**Stress/Wellness Terms:**
10. "stress relief"
11. "anxiety"
12. "mental health"

**How to Download:**
1. Go to https://trends.google.com/trends/explore
2. Enter search term (e.g., "healthy eating")
3. Set location: United States
4. Set time range: 1/1/2022 - 12/31/2023
5. Click download icon (↓) → CSV
6. Save as: `google_trends_healthy_eating_2022_2023.csv`

**Repeat for each term, or compare multiple terms:**
- Save comparison as: `google_trends_health_vs_comfort_2022_2023.csv`

---

### C2. Consumer Confidence / Sentiment (Overlap with Economic)

Already covered in A3. This data also reflects psychological state.

---

### C3. Stress Proxy - Tax Season Indicator

No external data needed - we'll use calendar indicators:
- April 15 = Tax Day
- Create flag for March 15 - April 15 as "tax season"

---

## D. COMPETITIVE DIMENSION DATA

### D1. Food Trends - Google Trends

| Item | Details |
|------|---------|
| **Data Source** | Google Trends |
| **URL** | https://trends.google.com/trends/explore |
| **Variables** | Search interest for food trends |

**Search Terms for Food Trends:**
1. "plant based food"
2. "vegan restaurant"
3. "vegetarian recipes"
4. "impossible burger"
5. "oat milk"

**Save as:** `google_trends_plant_based_2022_2023.csv`

---

### D2. Restaurant Industry Data (Limited Public Access)

| Item | Details |
|------|---------|
| **Data Source** | National Restaurant Association |
| **URL** | https://restaurant.org/research-and-media/research/industry-statistics/ |
| **Access** | Limited - some reports free, detailed data requires membership |

**What You Might Find Free:**
- Monthly Restaurant Performance Index (RPI)
- Industry outlook reports

**Alternative - Yelp Data:**
| Item | Details |
|------|---------|
| **URL** | https://www.yelp.com/search?find_desc=Restaurants&find_loc=Austin%2C+TX |
| **Manual Collection** | Count new restaurant openings, review competitor menus |

---

### D3. Competitor Proxy Data (Recommended Approach)

Since direct competitor data is unavailable, use these proxies:

**Option 1: Chain Restaurant News**
- Monitor press releases from Chili's, Applebee's, TGI Friday's
- Look for Austin-area promotions or menu changes
- Save as: `competitor_events_2022_2023.csv`

**Option 2: Food Delivery Platform Trends**
| Item | Details |
|------|---------|
| **Source** | DoorDash/UberEats trending cuisines (manual observation) |
| **Limitation** | No historical data available |

**Recommended Format for Manual Collection:**
| Date | Competitor | Event_Type | Description |
|------|------------|------------|-------------|
| 2022-03-01 | Chili's | Promotion | $10 lunch special |
| 2022-06-15 | Applebee's | New_Menu | Added plant-based burger |

---

## DATA FILES CHECKLIST

Please collect and save the following files:

### Required (High Priority)

| # | Filename | Source | Status |
|---|----------|--------|--------|
| 1 | `economic_cpi_2022_2023.csv` | FRED | ⬜ |
| 2 | `economic_unemployment_austin_2022_2023.csv` | FRED | ⬜ |
| 3 | `weather_austin_daily_2022_2023.csv` | NOAA | ⬜ |
| 4 | `google_trends_healthy_eating_2022_2023.csv` | Google Trends | ⬜ |
| 5 | `google_trends_comfort_food_2022_2023.csv` | Google Trends | ⬜ |

### Recommended (Medium Priority)

| # | Filename | Source | Status |
|---|----------|--------|--------|
| 6 | `economic_consumer_sentiment_2022_2023.csv` | FRED | ⬜ |
| 7 | `economic_tech_layoffs_austin_2022_2023.csv` | Layoffs.fyi | ⬜ |
| 8 | `google_trends_plant_based_2022_2023.csv` | Google Trends | ⬜ |
| 9 | `google_trends_stress_anxiety_2022_2023.csv` | Google Trends | ⬜ |

### Optional (Nice to Have)

| # | Filename | Source | Status |
|---|----------|--------|--------|
| 10 | `competitor_events_2022_2023.csv` | Manual | ⬜ |
| 11 | `weather_austin_monthly_2022_2023.csv` | Weather Underground | ⬜ |

---

## DATA FORMAT REQUIREMENTS

### Date Format
All dates should be in **YYYY-MM-DD** format (e.g., 2022-01-15)

### Column Naming Convention
- Use underscores instead of spaces: `Avg_Temp` not `Avg Temp`
- Be consistent with capitalization

### Expected File Structures

**Economic CPI:**
```
DATE,CPIAUCSL
2022-01-01,281.148
2022-02-01,283.716
...
```

**Weather Daily:**
```
DATE,TAVG,TMAX,TMIN,PRCP
2022-01-01,45,55,35,0.0
2022-01-02,48,58,38,0.1
...
```

**Google Trends:**
```
Week,healthy_eating
2022-01-02,65
2022-01-09,72
...
```

---

## LIMITATIONS TO ACKNOWLEDGE IN REPORT

### Economic Data
- CPI is national, not Austin-specific (South region CPI available but less granular)
- Tech layoff data may be incomplete for smaller companies

### Weather Data
- Austin airport station may not perfectly represent downtown dining area
- Extreme weather events (ice storms) may need special handling

### Psychological Data
- Google Trends shows search interest, not actual consumer behavior
- Regional filtering may have limited data for some terms
- Cannot directly measure individual stress levels

### Competitive Data
- **Major Limitation:** No public data on competitor pricing, promotions, or menu changes
- Proxy data (Google Trends for cuisines) only partially captures competitive dynamics
- **Recommendation for The Bistro:** Implement systematic competitor monitoring program:
  - Weekly competitor menu reviews
  - Track promotional calendars
  - Monitor social media mentions
  - Survey customers about competitor visits

---

## QUICK START GUIDE

### Step 1: FRED Data (10 minutes)
1. Go to https://fred.stlouisfed.org
2. Search and download: CPIAUCSL, AUST448URN, UMCSENT
3. Set date range 2022-01-01 to 2023-12-31 for each

### Step 2: Weather Data (15-30 minutes)
1. Go to https://www.ncdc.noaa.gov/cdo-web/search
2. Or use Visual Crossing for faster download
3. Get Austin daily data for 2022-2023

### Step 3: Google Trends (15 minutes)
1. Go to https://trends.google.com/trends/explore
2. Download each term separately
3. Combine into analysis file

### Step 4: Place Files
Put all downloaded CSV files in the project folder:
```
/workplace/alexjia/iom209-cw/
├── economic_cpi_2022_2023.csv
├── economic_unemployment_austin_2022_2023.csv
├── weather_austin_daily_2022_2023.csv
├── google_trends_*.csv
└── ...
```

---

## CONTACT FOR HELP

If you encounter issues downloading:
- NOAA requires free account registration
- Some FRED series may have different date ranges
- Google Trends data may need adjustment for geographic specificity

Once you have collected the data, let me know and I'll create the Step 3 notebook to document and visualize all data sources!
