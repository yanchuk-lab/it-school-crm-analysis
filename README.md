# IT School CRM Analytics Case Study

## The main idea
Perform a comprehensive analysis of product, sales, and marketing data to uncover business insights, understand customer behavior, and evaluate the effectiveness of marketing campaigns for an online programming school.

## Tasks
* **Data cleaning and preparation:** Processing and merging data from various sources (Calls, Contacts, Deals, Spend).
* **Descriptive statistics & Dashboard:** Calculating key business metrics and creating a dynamic dashboard to track KPIs.
* **Marketing Analysis:** Analyzing marketing spend and campaign performance (CPC, CAC, and conversion rates).
* **A/B Testing & Hypothesis:** Conducting statistical analysis to evaluate the impact of marketing changes and business growth points.
* **Data Visualization:** Building an interactive environment using **Python Dash** to visualize key findings.
* **Reporting:** Formulating actionable recommendations for business growth based on data-driven insights.

## Data cleaning
The project involved processing four primary datasets: `Calls`, `Contacts`, `Deals`, and `Spend`.
* **Filtering:** Removed irrelevant entries, duplicates, and "test" deals to ensure data integrity.
* **Missing values:** Handled null values using logical imputation (e.g., filling campaign info based on Source/Term tags).
* **Data Transformation:** Converted data types for time-series analysis and optimized memory usage (categorical types, datetime, etc.).

## Research data analysis
I addressed several critical business questions through deep-dive analysis:
* **Marketing Channels:** Identified top-performing channels and campaigns by clicks and cost-per-click (CPC).
* **Deal Attributes:** Evaluated how lead quality, source, and product type affect sales. 
    * *Insight:* **Evening classes** show a **41.6% conversion rate**, which is nearly double the rate of morning classes (22.1%).
* **Performance Trends:** Analyzed the relationship between deal creation and call activity over time.
* **Lost Reasons:** Identified key bottlenecks in the sales funnel where potential customers drop off.
* **Geography:** Discovered that **Berlin** is the absolute leader, generating 2.5x more unique leads than the second-largest city (Munich).

## Product Analytics & A/B Testing
* **Unit Economics:** Calculated LTV, CAC, and ROMI to identify business growth points.
* **Statistical Testing:** Performed a Z-test for micro-conversions.
    * *Conclusion:* Proven that a standard 2-week A/B test is currently impossible for specific segments due to insufficient traffic volume, meaning the Null Hypothesis ($H_0$) is accepted for short-term fluctuations.

## Dynamic Dashboard (Python Dash)
Developed a dynamic dashboard that allows stakeholders to:
* Track **Total Revenue**, **Conversion Rates**, and **Average Order Value (AOV)** in real-time.
* Filter data by Manager, City, Product type, and Date range.
* Visualize the sales funnel and geographic lead distribution.

## Conclusion
This project demonstrates the full data analysis lifecycle—from cleaning "dirty" CRM data to advanced visualization and statistical modeling.
* Successfully calculated and visualized key business metrics including conversion and ROMI.
* Provided actionable insights into marketing campaign effectiveness.
* Identified high-value products (Evening classes) and key geographic markets (Berlin).
* Highlighted the necessity of data-driven decision-making when planning marketing experiments (A/B testing).

---
**Tech Stack:** `Python (Pandas, NumPy, SciPy)`, `Plotly Dash`, `Matplotlib`, `Seaborn`, `Statsmodels`.
