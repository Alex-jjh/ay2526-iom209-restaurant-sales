# Deep Research Report: Synthetic Data Detection, Statistical Methods & BI Framework

## Source
Generated via deep research agent, covering 96 academic and industry references.

## Key Findings Summary

### 1. The Dataset is Almost Certainly Synthetic
- Real restaurant data shows temperature-coffee correlation r=0.741 (Penn State); our data: r=0.065
- Real seasonal food shifts: 40-42% (DoorDash); our ANOVA F=0.022, p=0.995
- Real weekend-weekday calorie difference: 82-222 kcal/day (USDA/UNC); our χ²=0.479, p=0.923
- Gap is 5-10× between real benchmarks and our null results
- Convergent null results across ALL dimensions = forensic evidence of fabrication (Al-Marzouki et al., 2005, BMJ)

### 2. Multiple Testing Problem
- 13 independent tests at α=0.05 → P(at least 1 false positive) ≈ 49%
- Even the CPI vs Steak result (r=-0.43, p=0.035) may be Type I error
- Bonferroni correction: adjusted α = 0.05/13 = 0.0038 → NO results survive

### 3. Power Analysis (n=24 monthly points)
- Can only detect r≥0.50 at 80% power
- Medium effect (r=0.30): power = 0.29 (severely underpowered)
- Small effect (r=0.20): power = 0.15
- ANOVA with ~6/group needs ~25/group for medium effects
- Chi-square with 17,534 transactions: adequate power

### 4. Synthetic Data Detection Methods
- Benford's Law: check leading digit distribution
- Autocorrelation (ACF/PACF): real data shows lag-7 spikes (weekly), synthetic shows flat
- Wald-Wolfowitz runs test: real data clusters, synthetic passes with p≈0.5
- Kolmogorov-Smirnov test: detect overly smooth distributions
- Kuiper's test: cyclic invariance, good for day-of-week patterns

### 5. Real-World Benchmarks for Presentation

| Dimension | Real-World Effect | Our Dataset | Gap |
|-----------|------------------|-------------|-----|
| Temp → Coffee | r = -0.741 | r = -0.065 | 11× |
| Seasonal comfort food | 40-42% shift | F = 0.022 | ~∞ |
| Weekend calories | +82-222 kcal/day | χ² = 0.479 | ~∞ |
| CPI → dining elasticity | 0.7-0.8 | r = -0.43 | Close |
| January health spike | +29.4% healthy purchases | p = 0.556 | ~∞ |
| Day-of-week effects | Significant in all studies | p = 0.883 | ~∞ |

### 6. Key Theories for Presentation
- **Trading Down Effect**: food-away-from-home elasticity 0.7-0.8 (Andreyeva et al., 2010)
- **Lipstick Effect / Foodluxxing**: small indulgences preserved during economic stress
- **Thermoregulation**: every 1°C increase → 85.9 kcal less food (Bernhard et al., 2015)
- **Intention-Behavior Gap**: plant-based stated vs actual Cohen's d = 1.78 (Blanke et al., 2022)
- **New Year Resolution**: +29.4% healthy purchases, collapses in ~7 weeks (Pope et al., 2014)
- **TOST Equivalence Testing**: reframe null results as "effects statistically equivalent to zero"

### 7. BI Framework
- DIKW Pyramid: Data → Information → Knowledge → Wisdom
- Python excels in statistical depth (5/5) and reproducibility (5/5)
- Power BI best for small restaurant: affordable (~£7.50/user/month), Excel-familiar
- 70% of restaurant leaders consider BI fundamental, only 27% apply rigorous methods

### 8. Presentation Strategy
1. Show the analysis was methodologically rigorous
2. Present real-world benchmarks to contextualize null results
3. Argue that detecting synthetic data IS a BI competency
4. Use TOST to formally demonstrate effects are "equivalent to zero"
5. Discuss what WOULD be found with real data (citing benchmarks)
6. CPI vs Steak is your strongest talking point, but caveat with multiple testing

