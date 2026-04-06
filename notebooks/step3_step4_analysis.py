# %% [markdown]
# # Step 3 & 4: External Data Integration, Visualization & Hypothesis Testing
#
# This notebook:
# 1. **Step 3** — Documents and visualizes all external data sources
# 2. **Step 4** — Merges external data with sales data and tests H1–H8
#
# ---

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 11
sns.set_style('whitegrid')

# %% [markdown]
# ## 1. Load Sales Data (from Step 2)

# %%
df = pd.read_csv('../data/step2/restaurant_sales_data_step2.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['YearMonth'] = df['Order Date'].dt.to_period('M')
print(f"Sales data: {len(df):,} records, {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
print(f"Columns: {list(df.columns)}")
df.head(3)

# %% [markdown]
# ---
# ## 2. Step 3 — Load & Document External Data Sources
#
# ### 2.1 Economic Data

# %%
# --- CPI (Consumer Price Index) ---
cpi = pd.read_csv('../data/external/economic_cpi_2022_2023.csv')
cpi['observation_date'] = pd.to_datetime(cpi['observation_date'])
cpi.rename(columns={'CPIAUCSL': 'CPI'}, inplace=True)
cpi['YearMonth'] = cpi['observation_date'].dt.to_period('M')
# Calculate month-over-month inflation rate
cpi['CPI_MoM_Pct'] = cpi['CPI'].pct_change() * 100
# Year-over-year (approximate using 12-month lag)
cpi['CPI_YoY_Pct'] = cpi['CPI'].pct_change(periods=12) * 100

print("=== CPI Data ===")
print(f"Source: FRED (CPIAUCSL) | Range: {cpi['observation_date'].min().date()} – {cpi['observation_date'].max().date()}")
print(f"Records: {len(cpi)} months")
display(cpi.head())

# %%
# --- Food CPI ---
food_cpi = pd.read_csv('../data/external/food_cpi_2022_2023.csv')
food_cpi['observation_date'] = pd.to_datetime(food_cpi['observation_date'])
food_cpi.rename(columns={'CPIUFDSL': 'Food_CPI'}, inplace=True)
food_cpi['YearMonth'] = food_cpi['observation_date'].dt.to_period('M')
food_cpi['Food_CPI_MoM_Pct'] = food_cpi['Food_CPI'].pct_change() * 100

print("=== Food CPI Data ===")
print(f"Source: FRED (CPIUFDSL) | Range: {food_cpi['observation_date'].min().date()} – {food_cpi['observation_date'].max().date()}")
display(food_cpi.head())

# %%
# --- Unemployment Rate (Austin MSA) ---
unemp = pd.read_csv('../data/external/economic_unemployment_austin_2022_2023.csv')
unemp['observation_date'] = pd.to_datetime(unemp['observation_date'])
unemp.rename(columns={'AUST448URN': 'Unemployment_Rate'}, inplace=True)
unemp['YearMonth'] = unemp['observation_date'].dt.to_period('M')

print("=== Unemployment Rate (Austin MSA) ===")
print(f"Source: FRED (AUST448URN) | Range: {unemp['observation_date'].min().date()} – {unemp['observation_date'].max().date()}")
display(unemp.head())

# %%
# --- Consumer Sentiment ---
sentiment = pd.read_csv('../data/external/economic_consumer_sentiment_2022_2023.csv')
sentiment['observation_date'] = pd.to_datetime(sentiment['observation_date'])
sentiment.rename(columns={'UMCSENT': 'Consumer_Sentiment'}, inplace=True)
sentiment['YearMonth'] = sentiment['observation_date'].dt.to_period('M')

print("=== Consumer Sentiment ===")
print(f"Source: FRED (UMCSENT - U. Michigan) | Range: {sentiment['observation_date'].min().date()} – {sentiment['observation_date'].max().date()}")
display(sentiment.head())


# %%
# --- Tech Layoffs (Austin) ---
layoffs = pd.read_csv('../data/external/economic_tech_layoffs_austin_2022_2023.csv')
layoffs['Date'] = pd.to_datetime(layoffs['Date'], format='mixed', dayfirst=False)
layoffs['YearMonth'] = layoffs['Date'].dt.to_period('M')
# Aggregate monthly layoff count
layoffs_monthly = layoffs.groupby('YearMonth').agg(
    Layoff_Events=('Company', 'count'),
    Total_Laid_Off=('No. Laid Off', lambda x: pd.to_numeric(x, errors='coerce').sum())
).reset_index()

print("=== Tech Layoffs (Austin) ===")
print(f"Source: layoffs.fyi | Records: {len(layoffs)} events")
print(f"Companies: {layoffs['Company'].nunique()} unique")
display(layoffs.head())

# %% [markdown]
# ### 2.2 Weather Data

# %%
# --- Weather (Austin daily) ---
weather = pd.read_csv('../data/external/weather_austin_daily_2022_2023.csv')
weather['DATE'] = pd.to_datetime(weather['DATE'], format='mixed', dayfirst=False)
weather.rename(columns={'TAVG': 'Avg_Temp_F', 'PRCP': 'Precip_In', 'AWND': 'Avg_Wind_Speed'}, inplace=True)
weather['YearMonth'] = weather['DATE'].dt.to_period('M')

# Monthly aggregation
weather_monthly = weather.groupby('YearMonth').agg(
    Monthly_Avg_Temp=('Avg_Temp_F', 'mean'),
    Monthly_Max_Temp=('Avg_Temp_F', 'max'),
    Monthly_Min_Temp=('Avg_Temp_F', 'min'),
    Monthly_Precip=('Precip_In', 'sum'),
    Hot_Days=('Avg_Temp_F', lambda x: (x >= 85).sum()),
    Cold_Days=('Avg_Temp_F', lambda x: (x <= 50).sum())
).round(1).reset_index()

print("=== Weather Data (Austin) ===")
print(f"Source: NOAA | Range: {weather['DATE'].min().date()} – {weather['DATE'].max().date()}")
print(f"Records: {len(weather)} days")
display(weather_monthly.head())

# %% [markdown]
# ### 2.3 Google Trends Data (Psychological & Competitive)

# %%
# Load all trend files
def load_trend(filepath, col_name):
    t = pd.read_csv(filepath)
    orig_col = [c for c in t.columns if c != 'Week'][0]
    t.rename(columns={orig_col: col_name}, inplace=True)
    t['Week'] = pd.to_datetime(t['Week'], format='mixed', dayfirst=True)
    t[col_name] = pd.to_numeric(t[col_name], errors='coerce')
    t['YearMonth'] = t['Week'].dt.to_period('M')
    return t

trend_healthy = load_trend('../data/external/trend_healthyeating.csv', 'Trend_HealthyEating')
trend_comfort = load_trend('../data/external/trend_comfortfood.csv', 'Trend_ComfortFood')
trend_plant = load_trend('../data/external/trend_plantbasedfood.csv', 'Trend_PlantBased')
trend_stress = load_trend('../data/external/trend_stress.csv', 'Trend_Stress')

# Monthly averages
trends_monthly = trend_healthy.groupby('YearMonth')['Trend_HealthyEating'].mean().reset_index()
trends_monthly = trends_monthly.merge(
    trend_comfort.groupby('YearMonth')['Trend_ComfortFood'].mean().reset_index(), on='YearMonth', how='outer')
trends_monthly = trends_monthly.merge(
    trend_plant.groupby('YearMonth')['Trend_PlantBased'].mean().reset_index(), on='YearMonth', how='outer')
trends_monthly = trends_monthly.merge(
    trend_stress.groupby('YearMonth')['Trend_Stress'].mean().reset_index(), on='YearMonth', how='outer')

print("=== Google Trends Data ===")
print(f"Source: Google Trends (US) | Frequency: Weekly → aggregated monthly")
print(f"Terms: healthy eating, comfort food, plant based food, stress")
display(trends_monthly.head())

# %% [markdown]
# ### 2.4 Visualize All External Data Sources (Step 3 Requirement)

# %%
fig, axes = plt.subplots(3, 2, figsize=(16, 14))
fig.suptitle('Step 3: External Data Sources Overview (Jan 2022 – Dec 2023)', fontsize=16, fontweight='bold', y=1.01)

# CPI
ax = axes[0, 0]
ax.plot(cpi['observation_date'], cpi['CPI'], 'b-o', markersize=4, label='CPI (All Urban)')
ax.plot(food_cpi['observation_date'], food_cpi['Food_CPI'], 'r-s', markersize=4, label='Food CPI')
ax.set_title('A1. Consumer Price Index')
ax.set_ylabel('Index Value')
ax.legend(fontsize=9)
ax.tick_params(axis='x', rotation=45)

# Unemployment
ax = axes[0, 1]
ax.plot(unemp['observation_date'], unemp['Unemployment_Rate'], 'g-o', markersize=4)
ax.set_title('A2. Unemployment Rate (Austin MSA)')
ax.set_ylabel('Rate (%)')
ax.axhline(y=unemp['Unemployment_Rate'].mean(), color='gray', linestyle='--', alpha=0.5, label=f"Mean: {unemp['Unemployment_Rate'].mean():.1f}%")
ax.legend(fontsize=9)
ax.tick_params(axis='x', rotation=45)

# Consumer Sentiment
ax = axes[1, 0]
ax.plot(sentiment['observation_date'], sentiment['Consumer_Sentiment'], 'm-o', markersize=4)
ax.set_title('A3. Consumer Sentiment (U. Michigan)')
ax.set_ylabel('Index')
ax.tick_params(axis='x', rotation=45)

# Weather
ax = axes[1, 1]
wm_dates = weather_monthly['YearMonth'].astype(str)
ax.bar(range(len(wm_dates)), weather_monthly['Monthly_Avg_Temp'], color='coral', alpha=0.7, label='Avg Temp (°F)')
ax.bar(range(len(wm_dates)), weather_monthly['Hot_Days'], color='red', alpha=0.4, label='Hot Days (≥85°F)')
ax.set_title('B1. Austin Monthly Temperature')
ax.set_ylabel('Temperature (°F) / Count')
ax.set_xticks(range(0, len(wm_dates), 3))
ax.set_xticklabels([wm_dates.iloc[i] for i in range(0, len(wm_dates), 3)], rotation=45)
ax.legend(fontsize=9)

# Google Trends - Psychological
ax = axes[2, 0]
tm = trends_monthly.copy()
tm['date_str'] = tm['YearMonth'].astype(str)
ax.plot(range(len(tm)), tm['Trend_HealthyEating'], 'g-', label='Healthy Eating')
ax.plot(range(len(tm)), tm['Trend_ComfortFood'], 'r-', label='Comfort Food')
ax.plot(range(len(tm)), tm['Trend_Stress'], 'purple', linestyle='-', label='Stress')
ax.set_title('C. Google Trends – Psychological Proxies')
ax.set_ylabel('Search Interest (0-100)')
ax.set_xticks(range(0, len(tm), 3))
ax.set_xticklabels([tm['date_str'].iloc[i] for i in range(0, len(tm), 3)], rotation=45)
ax.legend(fontsize=9)

# Google Trends - Competitive
ax = axes[2, 1]
ax.plot(range(len(tm)), tm['Trend_PlantBased'], 'green', linestyle='-', marker='o', markersize=3, label='Plant-Based Food')
ax.set_title('D. Google Trends – Competitive (Plant-Based Trend)')
ax.set_ylabel('Search Interest (0-100)')
ax.set_xticks(range(0, len(tm), 3))
ax.set_xticklabels([tm['date_str'].iloc[i] for i in range(0, len(tm), 3)], rotation=45)
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('../references/step3_external_data_overview.png', dpi=150, bbox_inches='tight')
plt.show()
print("✓ All external data sources documented and visualized.")


# %% [markdown]
# ---
# ## 3. Data Blending — Merge Sales with External Data
#
# Aggregate sales data monthly, then merge with all external sources.

# %%
# --- Monthly sales aggregation ---
monthly_sales = df.groupby('YearMonth').agg(
    Total_Orders=('Order ID', 'nunique'),
    Total_Revenue=('Order Total', 'sum'),
    Avg_Order_Value=('Order Total', 'mean'),
    Total_Quantity=('Quantity', 'sum')
).reset_index()

# Health level shares
for hl in ['Healthy', 'Indulgent', 'Moderate']:
    sub = df[df['Health_Level'] == hl].groupby('YearMonth')['Order ID'].count().reset_index()
    sub.columns = ['YearMonth', f'{hl}_Orders']
    monthly_sales = monthly_sales.merge(sub, on='YearMonth', how='left')

# Temperature preference shares
for temp in ['Hot', 'Cold']:
    sub = df[df['Temperature'] == temp].groupby('YearMonth')['Order ID'].count().reset_index()
    sub.columns = ['YearMonth', f'{temp}_Orders']
    monthly_sales = monthly_sales.merge(sub, on='YearMonth', how='left')

# Price tier shares
for tier in df['Price_Tier'].dropna().unique():
    safe_name = tier.replace(' ', '_').replace('<', 'lt').replace('>', 'gt').replace('$', '').replace('(', '').replace(')', '')
    sub = df[df['Price_Tier'] == tier].groupby('YearMonth')['Order ID'].count().reset_index()
    sub.columns = ['YearMonth', f'Tier_{safe_name}_Orders']
    monthly_sales = monthly_sales.merge(sub, on='YearMonth', how='left')

# Category shares
for cat in df['Category'].unique():
    sub = df[df['Category'] == cat].groupby('YearMonth')['Order ID'].count().reset_index()
    sub.columns = ['YearMonth', f'Cat_{cat.replace(" ", "_")}_Orders']
    monthly_sales = monthly_sales.merge(sub, on='YearMonth', how='left')

# Specific items for hypothesis testing
key_items = ['Salmon', 'Steak', 'Pasta Alfredo', 'French Fries', 'Vegetarian Platter',
             'Grilled Vegetables', 'Chocolate Cake', 'Ice Cream', 'Fruit Salad', 'Side Salad']
for item in key_items:
    sub = df[df['Item'] == item].groupby('YearMonth')['Order ID'].count().reset_index()
    sub.columns = ['YearMonth', f'Item_{item.replace(" ", "_")}_Orders']
    monthly_sales = monthly_sales.merge(sub, on='YearMonth', how='left')

# Calculate percentage shares
monthly_sales['Healthy_Pct'] = monthly_sales['Healthy_Orders'] / monthly_sales['Total_Orders'] * 100
monthly_sales['Indulgent_Pct'] = monthly_sales['Indulgent_Orders'] / monthly_sales['Total_Orders'] * 100
monthly_sales['Hot_Pct'] = monthly_sales['Hot_Orders'] / monthly_sales['Total_Orders'] * 100
monthly_sales['Cold_Pct'] = monthly_sales['Cold_Orders'] / monthly_sales['Total_Orders'] * 100

# Weekend vs weekday
weekend = df[df['Is_Weekend'] == True].groupby('YearMonth')['Order ID'].count().reset_index()
weekend.columns = ['YearMonth', 'Weekend_Orders']
monthly_sales = monthly_sales.merge(weekend, on='YearMonth', how='left')

# Trend items
trend_items = df[df['Is_Trend_Item'] == True].groupby('YearMonth')['Order ID'].count().reset_index()
trend_items.columns = ['YearMonth', 'Trend_Item_Orders']
monthly_sales = monthly_sales.merge(trend_items, on='YearMonth', how='left')

print(f"Monthly sales aggregated: {len(monthly_sales)} months, {len(monthly_sales.columns)} features")

# %%
# --- Merge all external data ---
merged = monthly_sales.copy()
merged = merged.merge(cpi[['YearMonth', 'CPI', 'CPI_MoM_Pct']], on='YearMonth', how='left')
merged = merged.merge(food_cpi[['YearMonth', 'Food_CPI']], on='YearMonth', how='left')
merged = merged.merge(unemp[['YearMonth', 'Unemployment_Rate']], on='YearMonth', how='left')
merged = merged.merge(sentiment[['YearMonth', 'Consumer_Sentiment']], on='YearMonth', how='left')
merged = merged.merge(weather_monthly, on='YearMonth', how='left')
merged = merged.merge(trends_monthly, on='YearMonth', how='left')
merged = merged.merge(layoffs_monthly, on='YearMonth', how='left')
merged[['Layoff_Events', 'Total_Laid_Off']] = merged[['Layoff_Events', 'Total_Laid_Off']].fillna(0)

print(f"Merged dataset: {len(merged)} months × {len(merged.columns)} columns")
display(merged.head())

# Save merged dataset
merged.to_csv('../data/step2/merged_analysis_dataset.csv', index=False)
print("✓ Saved: data/step2/merged_analysis_dataset.csv")


# %% [markdown]
# ---
# ## 4. Step 4 — Hypothesis Testing
#
# ### H1: Higher inflation → ↓ premium protein (Salmon, Steak), ↑ carb-based (Pasta)
#
# **Method:** Pearson correlation + scatter plots between CPI and item order shares

# %%
# H1: Inflation vs Premium Protein & Carb items
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('H1: Inflation Impact on Menu Preferences', fontsize=15, fontweight='bold')

# Premium items: Salmon, Steak
premium_items = ['Item_Salmon_Orders', 'Item_Steak_Orders']
carb_items = ['Item_Pasta_Alfredo_Orders', 'Item_French_Fries_Orders']

for i, item_col in enumerate(premium_items):
    ax = axes[0, i]
    valid = merged[[item_col, 'CPI']].dropna()
    r, p = stats.pearsonr(valid['CPI'], valid[item_col])
    ax.scatter(valid['CPI'], valid[item_col], c='steelblue', alpha=0.7, edgecolors='navy')
    z = np.polyfit(valid['CPI'], valid[item_col], 1)
    ax.plot(valid['CPI'], np.polyval(z, valid['CPI']), 'r--', alpha=0.7)
    item_name = item_col.replace('Item_', '').replace('_Orders', '').replace('_', ' ')
    ax.set_title(f'{item_name} vs CPI\nr={r:.3f}, p={p:.3f}', fontsize=11)
    ax.set_xlabel('CPI')
    ax.set_ylabel('Monthly Orders')

for i, item_col in enumerate(carb_items):
    ax = axes[1, i]
    valid = merged[[item_col, 'CPI']].dropna()
    r, p = stats.pearsonr(valid['CPI'], valid[item_col])
    ax.scatter(valid['CPI'], valid[item_col], c='coral', alpha=0.7, edgecolors='darkred')
    z = np.polyfit(valid['CPI'], valid[item_col], 1)
    ax.plot(valid['CPI'], np.polyval(z, valid['CPI']), 'r--', alpha=0.7)
    item_name = item_col.replace('Item_', '').replace('_Orders', '').replace('_', ' ')
    ax.set_title(f'{item_name} vs CPI\nr={r:.3f}, p={p:.3f}', fontsize=11)
    ax.set_xlabel('CPI')
    ax.set_ylabel('Monthly Orders')

# Overall healthy vs indulgent share vs CPI
ax = axes[0, 2]
valid = merged[['CPI', 'Healthy_Pct', 'Indulgent_Pct']].dropna()
ax.plot(valid['CPI'], valid['Healthy_Pct'], 'g-o', markersize=4, label='Healthy %')
ax.plot(valid['CPI'], valid['Indulgent_Pct'], 'r-s', markersize=4, label='Indulgent %')
ax.set_title('Health Level Share vs CPI')
ax.set_xlabel('CPI')
ax.set_ylabel('Order Share (%)')
ax.legend()

# Time series: CPI vs premium share
ax = axes[1, 2]
premium_share = (merged['Item_Salmon_Orders'].fillna(0) + merged['Item_Steak_Orders'].fillna(0)) / merged['Total_Orders'] * 100
ax2 = ax.twinx()
dates = range(len(merged))
ax.plot(dates, merged['CPI'], 'b-', label='CPI', linewidth=2)
ax2.plot(dates, premium_share, 'r-', label='Premium Protein %', linewidth=2)
ax.set_ylabel('CPI', color='blue')
ax2.set_ylabel('Premium Protein Share (%)', color='red')
ax.set_title('CPI vs Premium Protein Share Over Time')
ax.set_xticks(range(0, len(merged), 4))
ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
ax.legend(loc='upper left', fontsize=9)
ax2.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('../references/h1_inflation_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

# Statistical summary
print("=" * 70)
print("H1 STATISTICAL SUMMARY: Inflation → Menu Preferences")
print("=" * 70)
for col in premium_items + carb_items:
    valid = merged[[col, 'CPI']].dropna()
    r, p = stats.pearsonr(valid['CPI'], valid[col])
    item_name = col.replace('Item_', '').replace('_Orders', '').replace('_', ' ')
    sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else "ns"
    print(f"  {item_name:20s} vs CPI: r = {r:+.3f}, p = {p:.4f} {sig}")


# %% [markdown]
# ### H2: Tech layoffs → ↑ comfort food, ↓ healthy options
#
# **Method:** Event study / Before-After comparison around layoff periods

# %%
# H2: Tech Layoffs vs Comfort Food
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('H2: Tech Layoffs Impact on Comfort Food Ordering', fontsize=15, fontweight='bold')

# Layoff events timeline vs indulgent orders
ax = axes[0]
ax2 = ax.twinx()
dates = range(len(merged))
ax.bar(dates, merged['Layoff_Events'], color='red', alpha=0.4, label='Layoff Events')
ax2.plot(dates, merged['Indulgent_Pct'], 'b-o', markersize=4, label='Indulgent %')
ax.set_ylabel('Layoff Events', color='red')
ax2.set_ylabel('Indulgent Order %', color='blue')
ax.set_title('Layoff Events vs Indulgent Orders')
ax.set_xticks(range(0, len(merged), 4))
ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
ax.legend(loc='upper left', fontsize=9)
ax2.legend(loc='upper right', fontsize=9)

# Dessert category during layoff vs non-layoff months
ax = axes[1]
merged['Has_Layoffs'] = merged['Layoff_Events'] > 0
dessert_col = 'Cat_Desserts_Orders'
if dessert_col in merged.columns:
    merged['Dessert_Pct'] = merged[dessert_col] / merged['Total_Orders'] * 100
    layoff_dessert = merged[merged['Has_Layoffs']]['Dessert_Pct']
    no_layoff_dessert = merged[~merged['Has_Layoffs']]['Dessert_Pct']
    
    bp = ax.boxplot([no_layoff_dessert.dropna(), layoff_dessert.dropna()],
                    labels=['No Layoffs', 'Layoff Months'], patch_artist=True)
    bp['boxes'][0].set_facecolor('lightgreen')
    bp['boxes'][1].set_facecolor('salmon')
    ax.set_ylabel('Dessert Order Share (%)')
    ax.set_title('Dessert Share: Layoff vs Non-Layoff Months')
    
    t_stat, t_p = stats.ttest_ind(no_layoff_dessert.dropna(), layoff_dessert.dropna())
    ax.text(0.5, 0.95, f't={t_stat:.2f}, p={t_p:.3f}', transform=ax.transAxes,
            ha='center', va='top', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat'))

# Healthy vs Indulgent during layoff months
ax = axes[2]
if 'Has_Layoffs' in merged.columns:
    categories = ['No Layoffs', 'Layoff Months']
    healthy_means = [merged[~merged['Has_Layoffs']]['Healthy_Pct'].mean(),
                     merged[merged['Has_Layoffs']]['Healthy_Pct'].mean()]
    indulgent_means = [merged[~merged['Has_Layoffs']]['Indulgent_Pct'].mean(),
                       merged[merged['Has_Layoffs']]['Indulgent_Pct'].mean()]
    
    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, healthy_means, width, label='Healthy %', color='lightgreen')
    ax.bar(x + width/2, indulgent_means, width, label='Indulgent %', color='salmon')
    ax.set_ylabel('Order Share (%)')
    ax.set_title('Health Level: Layoff vs Non-Layoff')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    for i, (h, ind) in enumerate(zip(healthy_means, indulgent_means)):
        ax.text(i - width/2, h + 0.3, f'{h:.1f}%', ha='center', fontsize=9)
        ax.text(i + width/2, ind + 0.3, f'{ind:.1f}%', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('../references/h2_layoffs_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H2 STATISTICAL SUMMARY: Tech Layoffs → Comfort Food")
print("=" * 70)
if 'Has_Layoffs' in merged.columns:
    for label, col in [('Indulgent %', 'Indulgent_Pct'), ('Healthy %', 'Healthy_Pct'), ('Dessert %', 'Dessert_Pct')]:
        if col in merged.columns:
            g1 = merged[~merged['Has_Layoffs']][col].dropna()
            g2 = merged[merged['Has_Layoffs']][col].dropna()
            t, p = stats.ttest_ind(g1, g2)
            print(f"  {label:15s}: No-Layoff={g1.mean():.1f}%, Layoff={g2.mean():.1f}%, t={t:.2f}, p={p:.3f}")


# %% [markdown]
# ### H3: Higher temperature → ↑ cold food/drink, ↓ hot food
#
# **Method:** Correlation + time series overlay

# %%
# H3: Temperature vs Hot/Cold food preferences
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('H3: Temperature Impact on Hot vs Cold Food Preferences', fontsize=15, fontweight='bold')

# Scatter: Temp vs Cold orders %
ax = axes[0, 0]
valid = merged[['Monthly_Avg_Temp', 'Cold_Pct']].dropna()
r, p = stats.pearsonr(valid['Monthly_Avg_Temp'], valid['Cold_Pct'])
ax.scatter(valid['Monthly_Avg_Temp'], valid['Cold_Pct'], c='deepskyblue', edgecolors='navy', s=60)
z = np.polyfit(valid['Monthly_Avg_Temp'], valid['Cold_Pct'], 1)
ax.plot(valid['Monthly_Avg_Temp'], np.polyval(z, valid['Monthly_Avg_Temp']), 'r--')
ax.set_title(f'Cold Food/Drink % vs Avg Temperature\nr={r:.3f}, p={p:.4f}')
ax.set_xlabel('Monthly Avg Temperature (°F)')
ax.set_ylabel('Cold Item Order Share (%)')

# Scatter: Temp vs Hot orders %
ax = axes[0, 1]
valid = merged[['Monthly_Avg_Temp', 'Hot_Pct']].dropna()
r, p = stats.pearsonr(valid['Monthly_Avg_Temp'], valid['Hot_Pct'])
ax.scatter(valid['Monthly_Avg_Temp'], valid['Hot_Pct'], c='coral', edgecolors='darkred', s=60)
z = np.polyfit(valid['Monthly_Avg_Temp'], valid['Hot_Pct'], 1)
ax.plot(valid['Monthly_Avg_Temp'], np.polyval(z, valid['Monthly_Avg_Temp']), 'r--')
ax.set_title(f'Hot Food % vs Avg Temperature\nr={r:.3f}, p={p:.4f}')
ax.set_xlabel('Monthly Avg Temperature (°F)')
ax.set_ylabel('Hot Item Order Share (%)')

# Time series: Temperature vs Cold/Hot share
ax = axes[1, 0]
ax2 = ax.twinx()
dates = range(len(merged))
ax.plot(dates, merged['Monthly_Avg_Temp'], 'orange', linewidth=2, label='Avg Temp (°F)')
ax2.plot(dates, merged['Cold_Pct'], 'b-o', markersize=3, label='Cold %')
ax2.plot(dates, merged['Hot_Pct'], 'r-s', markersize=3, label='Hot %')
ax.set_ylabel('Temperature (°F)', color='orange')
ax2.set_ylabel('Order Share (%)')
ax.set_title('Temperature vs Hot/Cold Preferences Over Time')
ax.set_xticks(range(0, len(merged), 4))
ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
ax.legend(loc='upper left', fontsize=9)
ax2.legend(loc='upper right', fontsize=9)

# Specific cold items vs temperature
ax = axes[1, 1]
cold_items = ['Item_Ice_Cream_Orders', 'Item_Fruit_Salad_Orders', 'Item_Side_Salad_Orders']
for col in cold_items:
    if col in merged.columns:
        valid = merged[['Monthly_Avg_Temp', col]].dropna()
        r, p = stats.pearsonr(valid['Monthly_Avg_Temp'], valid[col])
        item_name = col.replace('Item_', '').replace('_Orders', '').replace('_', ' ')
        ax.scatter(valid['Monthly_Avg_Temp'], valid[col], alpha=0.6, label=f'{item_name} (r={r:.2f})')
ax.set_xlabel('Monthly Avg Temperature (°F)')
ax.set_ylabel('Monthly Orders')
ax.set_title('Cold Items vs Temperature')
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('../references/h3_temperature_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H3 STATISTICAL SUMMARY: Temperature → Hot/Cold Preferences")
print("=" * 70)
for label, col in [('Cold %', 'Cold_Pct'), ('Hot %', 'Hot_Pct')]:
    valid = merged[['Monthly_Avg_Temp', col]].dropna()
    r, p = stats.pearsonr(valid['Monthly_Avg_Temp'], valid[col])
    sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else "ns"
    print(f"  Temp vs {label:8s}: r = {r:+.3f}, p = {p:.4f} {sig}")


# %% [markdown]
# ### H4: Winter quarters → ↑ indulgent, ↓ healthy
#
# **Method:** ANOVA by season / seasonal decomposition

# %%
# H4: Seasonal patterns in health level preferences
# Add season to merged data
def get_season(ym):
    m = ym.month
    if m in [12, 1, 2]: return 'Winter'
    elif m in [3, 4, 5]: return 'Spring'
    elif m in [6, 7, 8]: return 'Summer'
    else: return 'Fall'

merged['Season'] = merged['YearMonth'].apply(get_season)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('H4: Seasonal Patterns in Food Preferences', fontsize=15, fontweight='bold')

# Grouped bar: Health level by season
ax = axes[0]
season_order = ['Winter', 'Spring', 'Summer', 'Fall']
season_health = merged.groupby('Season')[['Healthy_Pct', 'Indulgent_Pct']].mean().reindex(season_order)
x = np.arange(len(season_order))
width = 0.35
bars1 = ax.bar(x - width/2, season_health['Healthy_Pct'], width, label='Healthy %', color='lightgreen')
bars2 = ax.bar(x + width/2, season_health['Indulgent_Pct'], width, label='Indulgent %', color='salmon')
ax.set_ylabel('Order Share (%)')
ax.set_title('Health Level by Season')
ax.set_xticks(x)
ax.set_xticklabels(season_order)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{bar.get_height():.1f}%', ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{bar.get_height():.1f}%', ha='center', fontsize=9)

# ANOVA test
ax = axes[1]
groups_indulgent = [merged[merged['Season'] == s]['Indulgent_Pct'].dropna().values for s in season_order]
f_stat, f_p = stats.f_oneway(*groups_indulgent)
bp = ax.boxplot(groups_indulgent, labels=season_order, patch_artist=True)
colors_box = ['lightblue', 'lightgreen', 'lightyellow', 'peachpuff']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
ax.set_ylabel('Indulgent Order Share (%)')
ax.set_title(f'Indulgent % by Season (ANOVA)\nF={f_stat:.2f}, p={f_p:.4f}')

# Dessert + comfort food by season
ax = axes[2]
if 'Dessert_Pct' in merged.columns:
    season_dessert = merged.groupby('Season')['Dessert_Pct'].mean().reindex(season_order)
    ax.bar(season_order, season_dessert, color=['lightblue', 'lightgreen', 'lightyellow', 'peachpuff'])
    ax.set_ylabel('Dessert Order Share (%)')
    ax.set_title('Dessert Share by Season')
    for i, v in enumerate(season_dessert):
        ax.text(i, v + 0.1, f'{v:.1f}%', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('../references/h4_seasonal_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H4 STATISTICAL SUMMARY: Seasonal Patterns")
print("=" * 70)
for label, col in [('Indulgent %', 'Indulgent_Pct'), ('Healthy %', 'Healthy_Pct')]:
    groups = [merged[merged['Season'] == s][col].dropna().values for s in season_order]
    f, p = stats.f_oneway(*groups)
    print(f"  ANOVA {label}: F = {f:.3f}, p = {p:.4f}")
    for s in season_order:
        m = merged[merged['Season'] == s][col].mean()
        print(f"    {s:8s}: {m:.1f}%")


# %% [markdown]
# ### H5: January health consciousness peak; weekends more indulgent
#
# **Method:** T-test / proportion comparison

# %%
# H5: January health peak + Weekend indulgence
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('H5: Health Consciousness Cycles (January Peak & Weekend Indulgence)', fontsize=15, fontweight='bold')

# Monthly healthy % — highlight January
ax = axes[0]
monthly_healthy = merged[['YearMonth', 'Healthy_Pct']].copy()
monthly_healthy['Month'] = monthly_healthy['YearMonth'].apply(lambda x: x.month)
monthly_healthy['Is_Jan'] = monthly_healthy['Month'] == 1
colors_bar = ['green' if is_jan else 'lightgray' for is_jan in monthly_healthy['Is_Jan']]
ax.bar(range(len(monthly_healthy)), monthly_healthy['Healthy_Pct'], color=colors_bar)
ax.axhline(y=monthly_healthy['Healthy_Pct'].mean(), color='red', linestyle='--', label=f"Annual Avg: {monthly_healthy['Healthy_Pct'].mean():.1f}%")
ax.set_ylabel('Healthy Order Share (%)')
ax.set_title('Monthly Healthy % (January highlighted)')
ax.set_xticks(range(0, len(monthly_healthy), 3))
ax.set_xticklabels([str(monthly_healthy['YearMonth'].iloc[i]) for i in range(0, len(monthly_healthy), 3)], rotation=45)
ax.legend(fontsize=9)

# January vs rest t-test
jan_healthy = monthly_healthy[monthly_healthy['Is_Jan']]['Healthy_Pct']
non_jan_healthy = monthly_healthy[~monthly_healthy['Is_Jan']]['Healthy_Pct']
t_jan, p_jan = stats.ttest_ind(jan_healthy, non_jan_healthy)
ax.text(0.02, 0.95, f'Jan vs Rest: t={t_jan:.2f}, p={p_jan:.3f}', transform=ax.transAxes,
        va='top', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat'))

# Weekend vs Weekday analysis (from raw data)
ax = axes[1]
df['Is_Weekend_Bool'] = df['Is_Weekend'].astype(str).str.lower() == 'true'
weekend_health = df.groupby('Is_Weekend_Bool')['Health_Level'].value_counts(normalize=True).unstack().fillna(0) * 100
if 'Healthy' in weekend_health.columns and 'Indulgent' in weekend_health.columns:
    x = np.arange(2)
    width = 0.3
    ax.bar(x - width, weekend_health['Healthy'], width, label='Healthy %', color='lightgreen')
    ax.bar(x, weekend_health['Indulgent'], width, label='Indulgent %', color='salmon')
    ax.bar(x + width, weekend_health.get('Moderate', [0, 0]), width, label='Moderate %', color='lightyellow')
    ax.set_xticks(x)
    ax.set_xticklabels(['Weekday', 'Weekend'])
    ax.set_ylabel('Order Share (%)')
    ax.set_title('Health Level: Weekday vs Weekend')
    ax.legend(fontsize=9)

# Google Trends: healthy eating monthly pattern
ax = axes[2]
trend_healthy_monthly = trend_healthy.copy()
trend_healthy_monthly['Month'] = trend_healthy_monthly['Week'].dt.month
monthly_trend_avg = trend_healthy_monthly.groupby('Month')['Trend_HealthyEating'].mean()
colors_trend = ['green' if m == 1 else 'lightblue' for m in monthly_trend_avg.index]
ax.bar(monthly_trend_avg.index, monthly_trend_avg.values, color=colors_trend)
ax.set_xlabel('Month')
ax.set_ylabel('Google Trends: "Healthy Eating"')
ax.set_title('Healthy Eating Search Interest by Month')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.tight_layout()
plt.savefig('../references/h5_health_consciousness.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H5 STATISTICAL SUMMARY: Health Consciousness Cycles")
print("=" * 70)
print(f"  January Healthy %: {jan_healthy.mean():.1f}% vs Rest: {non_jan_healthy.mean():.1f}%")
print(f"  T-test: t = {t_jan:.3f}, p = {p_jan:.4f}")
# Weekend chi-square
ct = pd.crosstab(df['Is_Weekend_Bool'], df['Health_Level'])
chi2, chi_p, dof, expected = stats.chi2_contingency(ct)
print(f"  Weekend vs Weekday Health Level: χ² = {chi2:.3f}, p = {chi_p:.4f}, dof = {dof}")


# %% [markdown]
# ### H6: Mondays & April (tax season) → ↑ dessert/comfort food
#
# **Method:** ANOVA by day-of-week + monthly comparison

# %%
# H6: Stress-driven eating — Monday effect & April tax season
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('H6: Stress & Emotional Eating (Monday Effect + Tax Season)', fontsize=15, fontweight='bold')

# Day-of-week dessert share
ax = axes[0]
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_dessert = df[df['Category'] == 'Desserts']
dow_dessert_pct = df_dessert.groupby('Day of Week')['Order ID'].count() / df.groupby('Day of Week')['Order ID'].count() * 100
dow_dessert_pct = dow_dessert_pct.reindex(dow_order)
colors_dow = ['red' if d == 'Monday' else 'lightblue' for d in dow_order]
ax.bar(dow_order, dow_dessert_pct, color=colors_dow)
ax.axhline(y=dow_dessert_pct.mean(), color='gray', linestyle='--', label=f'Avg: {dow_dessert_pct.mean():.1f}%')
ax.set_ylabel('Dessert Order Share (%)')
ax.set_title('Dessert Share by Day of Week')
ax.tick_params(axis='x', rotation=45)
ax.legend(fontsize=9)

# April vs other months — dessert + comfort food
ax = axes[1]
merged['Month_Num'] = merged['YearMonth'].apply(lambda x: x.month)
monthly_dessert = merged.groupby('Month_Num')['Dessert_Pct'].mean() if 'Dessert_Pct' in merged.columns else None
if monthly_dessert is not None:
    colors_month = ['red' if m == 4 else 'lightblue' for m in range(1, 13)]
    ax.bar(range(1, 13), monthly_dessert.reindex(range(1, 13)), color=colors_month)
    ax.axhline(y=monthly_dessert.mean(), color='gray', linestyle='--', label=f'Avg: {monthly_dessert.mean():.1f}%')
    ax.set_xlabel('Month')
    ax.set_ylabel('Dessert Order Share (%)')
    ax.set_title('Dessert Share by Month (April highlighted)')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax.legend(fontsize=9)

# Google Trends stress vs dessert orders
ax = axes[2]
if 'Trend_Stress' in merged.columns and 'Dessert_Pct' in merged.columns:
    valid = merged[['Trend_Stress', 'Dessert_Pct']].dropna()
    r, p = stats.pearsonr(valid['Trend_Stress'], valid['Dessert_Pct'])
    ax.scatter(valid['Trend_Stress'], valid['Dessert_Pct'], c='purple', alpha=0.7, edgecolors='black')
    z = np.polyfit(valid['Trend_Stress'], valid['Dessert_Pct'], 1)
    ax.plot(valid['Trend_Stress'], np.polyval(z, valid['Trend_Stress']), 'r--')
    ax.set_xlabel('Google Trends: "Stress" (0-100)')
    ax.set_ylabel('Dessert Order Share (%)')
    ax.set_title(f'Stress Search vs Dessert Orders\nr={r:.3f}, p={p:.4f}')

plt.tight_layout()
plt.savefig('../references/h6_stress_eating.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H6 STATISTICAL SUMMARY: Stress & Emotional Eating")
print("=" * 70)
# Monday vs other days
monday_dessert = df_dessert[df_dessert['Day of Week'] == 'Monday'].shape[0] / df[df['Day of Week'] == 'Monday'].shape[0] * 100
other_dessert = df_dessert[df_dessert['Day of Week'] != 'Monday'].shape[0] / df[df['Day of Week'] != 'Monday'].shape[0] * 100
print(f"  Monday Dessert %: {monday_dessert:.1f}% vs Other Days: {other_dessert:.1f}%")

# ANOVA by day of week
dow_groups = [df_dessert[df_dessert['Day of Week'] == d].shape[0] / df[df['Day of Week'] == d].shape[0] * 100 for d in dow_order]
# Use chi-square on raw counts
ct_dow = pd.crosstab(df['Day of Week'], df['Category'] == 'Desserts')
chi2_dow, p_dow, _, _ = stats.chi2_contingency(ct_dow)
print(f"  Day-of-Week Dessert χ²: {chi2_dow:.3f}, p = {p_dow:.4f}")

# April vs rest
april_data = merged[merged['Month_Num'] == 4]['Dessert_Pct'] if 'Dessert_Pct' in merged.columns else pd.Series()
non_april = merged[merged['Month_Num'] != 4]['Dessert_Pct'] if 'Dessert_Pct' in merged.columns else pd.Series()
if len(april_data) > 0 and len(non_april) > 0:
    t_apr, p_apr = stats.ttest_ind(april_data.dropna(), non_april.dropna())
    print(f"  April Dessert %: {april_data.mean():.1f}% vs Rest: {non_april.mean():.1f}%, t={t_apr:.2f}, p={p_apr:.3f}")


# %% [markdown]
# ### H7: Plant-based trend → ↑ Vegetarian Platter & Grilled Vegetables
#
# **Method:** Trend analysis / correlation with Google Trends

# %%
# H7: Plant-based food trend
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('H7: Plant-Based Trend Impact on Vegetarian Menu Items', fontsize=15, fontweight='bold')

# Time series: plant-based trend vs veggie items
ax = axes[0]
ax2 = ax.twinx()
dates = range(len(merged))
ax.plot(dates, merged['Trend_PlantBased'], 'g-', linewidth=2, label='Plant-Based Trend')
veg_orders = merged['Item_Vegetarian_Platter_Orders'].fillna(0) + merged['Item_Grilled_Vegetables_Orders'].fillna(0)
ax2.plot(dates, veg_orders, 'b-o', markersize=3, label='Veg Platter + Grilled Veg Orders')
ax.set_ylabel('Google Trends (0-100)', color='green')
ax2.set_ylabel('Monthly Orders', color='blue')
ax.set_title('Plant-Based Trend vs Vegetarian Items')
ax.set_xticks(range(0, len(merged), 4))
ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
ax.legend(loc='upper left', fontsize=9)
ax2.legend(loc='upper right', fontsize=9)

# Scatter: trend vs Vegetarian Platter
ax = axes[1]
vp_col = 'Item_Vegetarian_Platter_Orders'
if vp_col in merged.columns and 'Trend_PlantBased' in merged.columns:
    valid = merged[[vp_col, 'Trend_PlantBased']].dropna()
    r, p = stats.pearsonr(valid['Trend_PlantBased'], valid[vp_col])
    ax.scatter(valid['Trend_PlantBased'], valid[vp_col], c='green', alpha=0.7, edgecolors='darkgreen', s=60)
    z = np.polyfit(valid['Trend_PlantBased'], valid[vp_col], 1)
    ax.plot(valid['Trend_PlantBased'], np.polyval(z, valid['Trend_PlantBased']), 'r--')
    ax.set_xlabel('Google Trends: "Plant Based Food"')
    ax.set_ylabel('Vegetarian Platter Orders')
    ax.set_title(f'Vegetarian Platter vs Plant-Based Trend\nr={r:.3f}, p={p:.4f}')

# Trend item share over time
ax = axes[2]
if 'Trend_Item_Orders' in merged.columns:
    trend_pct = merged['Trend_Item_Orders'] / merged['Total_Orders'] * 100
    ax.plot(dates, trend_pct, 'g-o', markersize=4)
    z = np.polyfit(dates, trend_pct.fillna(0), 1)
    ax.plot(dates, np.polyval(z, dates), 'r--', label=f'Trend line (slope={z[0]:.3f})')
    ax.set_ylabel('Trend Item Share (%)')
    ax.set_title('Trend Items Share Over Time')
    ax.set_xticks(range(0, len(merged), 4))
    ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig('../references/h7_plantbased_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H7 STATISTICAL SUMMARY: Plant-Based Trend")
print("=" * 70)
for col_name, label in [(vp_col, 'Vegetarian Platter'), ('Item_Grilled_Vegetables_Orders', 'Grilled Vegetables')]:
    if col_name in merged.columns and 'Trend_PlantBased' in merged.columns:
        valid = merged[[col_name, 'Trend_PlantBased']].dropna()
        r, p = stats.pearsonr(valid['Trend_PlantBased'], valid[col_name])
        sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else "ns"
        print(f"  {label:25s} vs Plant-Based Trend: r = {r:+.3f}, p = {p:.4f} {sig}")


# %% [markdown]
# ### H8: Competitor promotions → shift to value-tier items
#
# **Method:** Proxy analysis using price tier trends + consumer sentiment

# %%
# H8: Value-tier shift (proxy: consumer sentiment as competition pressure indicator)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('H8: Competitive Pressure & Value-Tier Shift', fontsize=15, fontweight='bold')

# Price tier distribution over time
ax = axes[0]
tier_cols = [c for c in merged.columns if c.startswith('Tier_')]
if tier_cols:
    tier_pcts = merged[tier_cols].div(merged['Total_Orders'], axis=0) * 100
    tier_pcts.columns = [c.replace('Tier_', '').replace('_Orders', '').replace('_', ' ') for c in tier_cols]
    tier_pcts.plot(kind='area', stacked=True, ax=ax, alpha=0.7)
    ax.set_ylabel('Order Share (%)')
    ax.set_title('Price Tier Distribution Over Time')
    ax.set_xticks(range(0, len(merged), 4))
    ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
    ax.legend(fontsize=8, loc='upper right')

# Consumer sentiment vs value tier
ax = axes[1]
budget_col = [c for c in tier_cols if 'Budget' in c or 'lt' in c]
if budget_col and 'Consumer_Sentiment' in merged.columns:
    budget_pct = merged[budget_col[0]] / merged['Total_Orders'] * 100
    valid_idx = budget_pct.notna() & merged['Consumer_Sentiment'].notna()
    r, p = stats.pearsonr(merged.loc[valid_idx, 'Consumer_Sentiment'], budget_pct[valid_idx])
    ax.scatter(merged.loc[valid_idx, 'Consumer_Sentiment'], budget_pct[valid_idx], c='orange', edgecolors='brown', s=60)
    z = np.polyfit(merged.loc[valid_idx, 'Consumer_Sentiment'], budget_pct[valid_idx], 1)
    ax.plot(merged.loc[valid_idx, 'Consumer_Sentiment'], np.polyval(z, merged.loc[valid_idx, 'Consumer_Sentiment']), 'r--')
    ax.set_xlabel('Consumer Sentiment Index')
    ax.set_ylabel('Budget Tier Order Share (%)')
    ax.set_title(f'Consumer Sentiment vs Budget Tier\nr={r:.3f}, p={p:.4f}')

# Drinks category value shift (H8 specific: drink category)
ax = axes[2]
drinks_col = 'Cat_Drinks_Orders'
if drinks_col in merged.columns:
    drinks_pct = merged[drinks_col] / merged['Total_Orders'] * 100
    ax2 = ax.twinx()
    dates = range(len(merged))
    ax.plot(dates, drinks_pct, 'b-o', markersize=3, label='Drinks Share %')
    if 'Consumer_Sentiment' in merged.columns:
        ax2.plot(dates, merged['Consumer_Sentiment'], 'r-', label='Consumer Sentiment')
    ax.set_ylabel('Drinks Share (%)', color='blue')
    ax2.set_ylabel('Consumer Sentiment', color='red')
    ax.set_title('Drinks Category vs Consumer Sentiment')
    ax.set_xticks(range(0, len(merged), 4))
    ax.set_xticklabels([str(merged['YearMonth'].iloc[i]) for i in range(0, len(merged), 4)], rotation=45)
    ax.legend(loc='upper left', fontsize=9)
    ax2.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('../references/h8_competitive_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("=" * 70)
print("H8 STATISTICAL SUMMARY: Competitive Pressure & Value Shift")
print("=" * 70)
print("  Note: Direct competitor data unavailable. Using proxy indicators.")
if budget_col and 'Consumer_Sentiment' in merged.columns:
    budget_pct = merged[budget_col[0]] / merged['Total_Orders'] * 100
    valid_idx = budget_pct.notna() & merged['Consumer_Sentiment'].notna()
    r, p = stats.pearsonr(merged.loc[valid_idx, 'Consumer_Sentiment'], budget_pct[valid_idx])
    print(f"  Consumer Sentiment vs Budget Tier: r = {r:+.3f}, p = {p:.4f}")

# Year-over-year value tier shift
for col in tier_cols:
    tier_name = col.replace('Tier_', '').replace('_Orders', '').replace('_', ' ')
    y2022 = merged[merged['YearMonth'].apply(lambda x: x.year) == 2022][col].sum()
    y2023 = merged[merged['YearMonth'].apply(lambda x: x.year) == 2023][col].sum()
    total_2022 = merged[merged['YearMonth'].apply(lambda x: x.year) == 2022]['Total_Orders'].sum()
    total_2023 = merged[merged['YearMonth'].apply(lambda x: x.year) == 2023]['Total_Orders'].sum()
    pct_2022 = y2022 / total_2022 * 100 if total_2022 > 0 else 0
    pct_2023 = y2023 / total_2023 * 100 if total_2023 > 0 else 0
    change = pct_2023 - pct_2022
    print(f"  {tier_name:25s}: 2022={pct_2022:.1f}% → 2023={pct_2023:.1f}% (Δ={change:+.1f}pp)")


# %% [markdown]
# ---
# ## 5. Comprehensive Correlation Heatmap

# %%
# Correlation heatmap: all key variables
corr_cols = ['CPI', 'Food_CPI', 'Unemployment_Rate', 'Consumer_Sentiment',
             'Monthly_Avg_Temp', 'Trend_HealthyEating', 'Trend_ComfortFood',
             'Trend_PlantBased', 'Trend_Stress', 'Layoff_Events',
             'Healthy_Pct', 'Indulgent_Pct', 'Hot_Pct', 'Cold_Pct']
if 'Dessert_Pct' in merged.columns:
    corr_cols.append('Dessert_Pct')

corr_data = merged[corr_cols].dropna()
corr_matrix = corr_data.corr()

fig, ax = plt.subplots(figsize=(14, 11))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax,
            annot_kws={'size': 8})
ax.set_title('Correlation Matrix: External Factors vs Menu Preferences', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('../references/correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ---
# ## 6. Summary of Hypothesis Testing Results

# %%
print("=" * 80)
print("HYPOTHESIS TESTING RESULTS SUMMARY")
print("=" * 80)
print()

results = []

# H1
for col in ['Item_Salmon_Orders', 'Item_Steak_Orders', 'Item_Pasta_Alfredo_Orders', 'Item_French_Fries_Orders']:
    valid = merged[[col, 'CPI']].dropna()
    r, p = stats.pearsonr(valid['CPI'], valid[col])
    item_name = col.replace('Item_', '').replace('_Orders', '').replace('_', ' ')
    results.append({'Hypothesis': 'H1', 'Test': f'CPI vs {item_name}', 'r': r, 'p': p})

# H2
if 'Has_Layoffs' in merged.columns:
    g1 = merged[~merged['Has_Layoffs']]['Indulgent_Pct'].dropna()
    g2 = merged[merged['Has_Layoffs']]['Indulgent_Pct'].dropna()
    t, p = stats.ttest_ind(g1, g2)
    results.append({'Hypothesis': 'H2', 'Test': 'Layoff vs Indulgent %', 'r': t, 'p': p})

# H3
for col in ['Cold_Pct', 'Hot_Pct']:
    valid = merged[['Monthly_Avg_Temp', col]].dropna()
    r, p = stats.pearsonr(valid['Monthly_Avg_Temp'], valid[col])
    results.append({'Hypothesis': 'H3', 'Test': f'Temp vs {col}', 'r': r, 'p': p})

# H4
groups = [merged[merged['Season'] == s]['Indulgent_Pct'].dropna().values for s in ['Winter', 'Spring', 'Summer', 'Fall']]
f, p = stats.f_oneway(*groups)
results.append({'Hypothesis': 'H4', 'Test': 'Season ANOVA (Indulgent %)', 'r': f, 'p': p})

# H5
results.append({'Hypothesis': 'H5', 'Test': 'Jan vs Rest (Healthy %)', 'r': t_jan, 'p': p_jan})
results.append({'Hypothesis': 'H5', 'Test': 'Weekend χ² (Health Level)', 'r': chi2, 'p': chi_p})

# H6
results.append({'Hypothesis': 'H6', 'Test': 'Day-of-Week Dessert χ²', 'r': chi2_dow, 'p': p_dow})

# H7
if vp_col in merged.columns and 'Trend_PlantBased' in merged.columns:
    valid = merged[[vp_col, 'Trend_PlantBased']].dropna()
    r, p = stats.pearsonr(valid['Trend_PlantBased'], valid[vp_col])
    results.append({'Hypothesis': 'H7', 'Test': 'Plant Trend vs Veg Platter', 'r': r, 'p': p})

# H8
if budget_col and 'Consumer_Sentiment' in merged.columns:
    budget_pct = merged[budget_col[0]] / merged['Total_Orders'] * 100
    valid_idx = budget_pct.notna() & merged['Consumer_Sentiment'].notna()
    r, p = stats.pearsonr(merged.loc[valid_idx, 'Consumer_Sentiment'], budget_pct[valid_idx])
    results.append({'Hypothesis': 'H8', 'Test': 'Sentiment vs Budget Tier', 'r': r, 'p': p})

results_df = pd.DataFrame(results)
results_df['Significance'] = results_df['p'].apply(
    lambda x: '***' if x < 0.01 else '**' if x < 0.05 else '*' if x < 0.1 else 'ns')
results_df['Supported?'] = results_df['p'].apply(lambda x: 'Yes' if x < 0.1 else 'Partially' if x < 0.2 else 'No')

display(results_df)
results_df.to_csv('../references/hypothesis_test_results.csv', index=False)
print("\n✓ Results saved to references/hypothesis_test_results.csv")

# %% [markdown]
# ---
# ## 7. Key Findings & Business Recommendations
#
# Based on the analysis above, the key findings for The Bistro owner are:
#
# 1. **Economic Impact (H1/H2):** CPI changes show correlation with menu item ordering patterns.
#    During high-inflation months, there may be shifts toward value-tier items.
#
# 2. **Weather Drives Preferences (H3/H4):** Temperature is a strong predictor of hot vs cold
#    food choices. Seasonal patterns in indulgent vs healthy ordering are observable.
#
# 3. **Health Consciousness Cycles (H5):** January shows elevated healthy eating interest
#    (New Year's resolution effect). Weekend dining tends toward more indulgent choices.
#
# 4. **Stress Eating (H6):** Day-of-week and monthly patterns in dessert ordering may reflect
#    stress-driven consumption (Monday blues, tax season).
#
# 5. **Plant-Based Trend (H7):** Google Trends for plant-based food shows correlation with
#    vegetarian menu item orders, suggesting The Bistro benefits from this macro trend.
#
# 6. **Competitive Pressure (H8):** Limited by data availability. Consumer sentiment serves
#    as a proxy; lower sentiment may push customers toward budget options.
#
# ### Recommendations for 2024:
# - **Seasonal menu rotation:** Emphasize cold items in summer, comfort food in winter
# - **January health promotions:** Capitalize on New Year health consciousness
# - **Monday specials:** Offer dessert deals to boost weekday traffic
# - **Expand plant-based options:** Align with growing trend
# - **Value-tier strategy:** Maintain affordable options as inflation hedge
# - **Competitor monitoring:** Implement systematic tracking (currently a data gap)

