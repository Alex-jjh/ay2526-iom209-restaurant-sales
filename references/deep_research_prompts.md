# Deep Research Prompts for Other Agents

以下是 6 个独立的 deep research prompt，可以分别发给不同的 research agent（如 ChatGPT Deep Research、Gemini Deep Research、Perplexity 等）。每个 prompt 都是自包含的，直接复制粘贴即可。

---

## Prompt 1: 如何识别和论证合成/人造数据集

```
I am working on a university coursework (IOM209 Business Intelligence) analyzing a restaurant sales dataset from Kaggle called "Restaurant Sales – Dirty Data for Cleaning Training". The dataset contains 17,534 transaction records from Jan 2022 to Dec 2023 for a fictional restaurant.

After running hypothesis tests (correlation, t-test, ANOVA, chi-square) across 8 hypotheses linking external factors (CPI, weather, unemployment, Google Trends) to menu ordering patterns, almost none of the hypotheses showed statistical significance. Specifically:
- Seasonal ANOVA for indulgent food: F=0.022, p=0.995 (essentially zero variation across seasons)
- Temperature vs hot/cold food preference: r=-0.065, p=0.762 (no correlation at all)
- Weekend vs weekday health level: χ²=0.479, p=0.923
- Day-of-week dessert patterns: χ²=2.366, p=0.883

Only 2 out of 13 tests were significant (CPI vs Steak r=-0.43, p=0.035; Plant-based trend vs Vegetarian Platter r=-0.43, p=0.035 but in the WRONG direction).

Please research and provide:

1. **Statistical methods to formally detect synthetic/simulated data** — What tests or diagnostic approaches can identify that a dataset was randomly generated rather than reflecting real consumer behavior? (e.g., uniformity tests, autocorrelation analysis, Benford's Law, distribution shape tests)

2. **Expected patterns in REAL restaurant sales data** — What does academic literature say about real-world seasonal, weekly, and economic patterns in restaurant ordering? Provide specific effect sizes so I can compare with my null results.

3. **How to frame "null results" positively in an academic presentation** — What is the academic best practice for presenting and interpreting non-significant findings? How do researchers discuss the difference between "no effect" and "insufficient data to detect an effect"?

4. **Specific characteristics of synthetic data that differ from real data** — Things like: uniform distribution across categories, lack of autocorrelation in time series, absence of day-of-week effects, no holiday spikes, etc.

Please provide Harvard-style citations for all academic sources. Focus on sources from statistics, data science, and consumer behavior journals.
```

---

## Prompt 2: 研究方法论的学术支撑

```
I am conducting a Business Intelligence analysis for a university coursework project. I need academic justification for the specific analytical methods I used to test hypotheses about how external factors influence restaurant menu ordering patterns.

My analysis methods include:
- **Pearson correlation** between monthly CPI (inflation index) and monthly order counts for specific menu items (e.g., Steak, Salmon, Pasta)
- **Independent samples t-test** comparing indulgent food order percentages between months with tech layoffs vs months without
- **One-way ANOVA** comparing indulgent food percentages across four seasons (Winter, Spring, Summer, Fall)
- **Chi-square test of independence** between day-of-week and dessert ordering frequency
- **Chi-square test** between weekend/weekday and health level of food ordered
- **Dual-axis time series visualization** overlaying external data (CPI, temperature, Google Trends) with sales metrics
- **Scatter plots with linear regression lines** for correlation visualization

Please research and provide:

1. **Academic justification for each method** — Why is Pearson correlation appropriate for testing economic impact on food choices? Why is ANOVA suitable for seasonal comparison? When is chi-square preferred over other tests for categorical data?

2. **Limitations of each method** with small sample sizes (I only have 24 monthly data points for correlation/ANOVA, though 17,534 individual transactions for chi-square)

3. **Alternative methods I could mention** as improvements — e.g., time series regression with lag effects, interrupted time series for event studies, logistic regression for binary outcomes

4. **Key references** from research methodology textbooks and papers that justify using these methods in consumer behavior / business intelligence contexts

Please provide all citations in Harvard referencing style. Prioritize well-known methodology textbooks (e.g., Field, Hair, Tabachnick) and consumer behavior research methods papers.
```

---

## Prompt 3: 经济因素对餐饮消费行为的影响（加强 H1/H2 的理论深度）

```
I am researching how economic factors (specifically inflation and unemployment/layoffs) affect restaurant dining behavior and menu item preferences for a Business Intelligence coursework.

Context: My analysis of a restaurant in Austin, Texas (2022-2023) found that:
- CPI (inflation) has a significant negative correlation with Steak orders (r=-0.43, p=0.035)
- Tech layoff months show marginally significant higher indulgent food ordering (p=0.088)
- Austin experienced 8.5% inflation in 2022 and major tech layoffs (Dell, Meta, Google had Austin offices)

Please conduct deep research on:

1. **The "trading down" effect in restaurants during inflation** — Academic evidence that consumers substitute premium items (steak, seafood) with cheaper alternatives (pasta, chicken) when prices rise. What are the documented effect sizes?

2. **The "lipstick effect" / "affordable luxury" theory applied to food** — Do consumers increase spending on small indulgences (desserts, specialty drinks) while cutting back on expensive mains during economic downturns?

3. **Austin, Texas tech sector economic impact 2022-2023** — Specific data on tech layoffs in Austin, their timing, and any documented impact on local consumer spending patterns.

4. **Consumer behavior theories explaining food choice under economic stress** — Prospect theory, mental accounting, hedonic adaptation as they apply to restaurant menu selection.

Provide Harvard-style citations. Prioritize peer-reviewed journal articles from 2015-2024, plus any relevant industry reports (National Restaurant Association, Deloitte, McKinsey).
```

---

## Prompt 4: 天气和季节对食物偏好的影响（加强 H3/H4）

```
I am researching how weather (temperature) and seasonal patterns affect food and beverage preferences in restaurants, specifically for Austin, Texas (humid subtropical climate).

My analysis found NO significant correlation between monthly average temperature and hot/cold food ordering patterns (r=-0.065, p=0.762 for cold food; r=0.252, p=0.234 for hot food). Seasonal ANOVA for indulgent vs healthy food was also completely non-significant (F=0.022, p=0.995).

I suspect this is because my dataset is synthetic. However, I need to:

1. **Document what REAL weather-food relationships look like** — What does the academic literature say about temperature effects on food choice? What correlation strengths are typically found in real restaurant data?

2. **Specific studies on hot climate cities and food preferences** — Austin has summers reaching 97°F. How do restaurants in similar climates (Phoenix, Houston, Miami) see menu shifts?

3. **The thermoregulation theory of food choice** — Academic evidence for the biological mechanism: hot weather → body seeks cooling → preference for cold foods, salads, ice cream, cold beverages.

4. **Seasonal Affective Disorder (SAD) and comfort food** — Evidence that shorter days / colder weather increase cravings for carbohydrate-rich, high-calorie "comfort" foods.

5. **Austin-specific climate data context** — Average temperatures by month, extreme weather events in 2022-2023 (e.g., Winter Storm Uri aftermath), and how these might affect dining patterns.

Provide Harvard-style citations. Include both food science journals and consumer psychology journals.
```

---

## Prompt 5: 心理因素和社会趋势对食物选择的影响（加强 H5/H6/H7）

```
I am researching psychological and social factors that drive food preference changes in restaurants for a Business Intelligence coursework project.

My hypotheses and results:
- H5: January shows higher healthy eating (New Year's resolution effect) — NOT significant in my data (p=0.556)
- H6: Mondays and April (tax season) show elevated dessert/comfort food — NOT significant for day-of-week (p=0.883), but April dessert share was marginally lower (p=0.053)
- H7: Plant-based food trend correlates with vegetarian menu orders — Significant but NEGATIVE correlation (r=-0.43, p=0.035), meaning when Google Trends for "plant based food" went up, Vegetarian Platter orders went DOWN

Please research:

1. **The "New Year's Resolution Effect" on food choices** — Academic evidence for January health consciousness spikes. How long does it typically last? What percentage increase in healthy food orders do real restaurants see?

2. **The "Monday Blues" and emotional eating** — Is there documented evidence that people eat more comfort food on Mondays? What about "treat yourself Friday" effects?

3. **Tax season stress and consumer behavior** — Does April (US tax deadline) show measurable changes in spending patterns, particularly on comfort food or indulgences?

4. **The gap between food trend awareness and actual purchasing** — Why might Google Trends for "plant based food" increase while actual plant-based orders decrease? Research on the "intention-behavior gap" in food choices, "virtue signaling" in food trends, and the difference between online interest and offline purchasing.

5. **Social media food trends and restaurant ordering** — How do Instagram/TikTok food trends translate (or fail to translate) into actual restaurant orders? What is the typical lag time?

Provide Harvard-style citations. Focus on consumer psychology, behavioral economics, and food marketing journals.
```

---

## Prompt 6: Business Intelligence 工具和方法论（对应 Assessed Outcome A & B）

```
I am preparing a university presentation for IOM209 Business Intelligence that requires me to:
A. Explain BI concepts and how BI supports business decision-making
B. Evaluate the suitability of BI tools for organizational needs

My project uses Python (pandas, matplotlib, seaborn, scipy) to analyze restaurant sales data and test hypotheses about taste preference changes. The coursework originally mentioned Looker Studio but we used Python instead.

Please research:

1. **Definition and components of Business Intelligence** — What are the standard BI components (data warehousing, ETL, OLAP, dashboards, reporting, analytics)? How does our Python-based analysis pipeline map to these components?

2. **Python as a BI tool vs traditional BI platforms** — Compare Python (with pandas/matplotlib/seaborn) against Looker Studio, Tableau, and Power BI for:
   - Data cleaning and preparation
   - Statistical analysis capabilities
   - Visualization quality
   - Reproducibility and version control
   - Learning curve and accessibility
   - Suitability for a small restaurant business

3. **How BI supports restaurant decision-making** — Specific examples of how restaurants use BI for menu optimization, pricing strategy, seasonal planning, and customer segmentation. Include case studies if available.

4. **Data-driven decision making framework** — Academic models for how businesses should move from data → insight → action. Specifically the DIKW pyramid (Data-Information-Knowledge-Wisdom) and how our analysis demonstrates each level.

5. **Limitations of BI analysis** — What are the recognized limitations of using historical transaction data for predicting future consumer behavior? How should businesses combine quantitative BI with qualitative insights?

Provide Harvard-style citations. Include both academic sources and industry reports (Gartner, Forrester, McKinsey).
```

---

## 使用建议

| Prompt | 发给谁 | 预计用途 |
|--------|--------|---------|
| Prompt 1 | ChatGPT Deep Research / Perplexity | 解释为什么大部分假设不显著，在 PPT 里作为 limitation 讨论 |
| Prompt 2 | 任意 research agent | 方法论部分的学术支撑，PPT 里解释为什么选这些统计方法 |
| Prompt 3 | Gemini Deep Research | 加强经济维度的理论深度，H1/H2 是你们最强的结果 |
| Prompt 4 | 任意 research agent | 加强天气维度，用真实数据的 effect size 对比你们的 null results |
| Prompt 5 | ChatGPT Deep Research | 解释 H7 反向结果（最有趣的发现），加强心理维度 |
| Prompt 6 | 任意 research agent | 对应 Assessed Outcome A & B，BI 概念和工具评估 |
