# 🎾 Tennis Data Warehouse Project (LDS24)

Welcome to the Tennis DW project — a complete ETL, OLAP, and Dashboard system simulating a **Decision Support System (DSS)** for a **Tennis Sports Federation**. This project processes match-level data from tournaments, integrates geospatial data, and enables advanced analytical queries using a **Snowflake Data Warehouse Schema**, **SSIS pipelines**, and **OLAP Cube with MDX**.

📍 [Original dataset source](https://github.com/JeffSackmann/tennis_atp)

---

## 📈 Project Scope

This repository includes all work related to:
- Building a Data Warehouse using a **Snowflake schema**
- Populating the DW using **Python scripts** and **SSIS**
- Creating a **Data Cube**
- Executing **MDX queries**
- Designing **Dashboards** for geographical and financial insights

---

## 🔍 Questions Explored

✅ **Nemesis Analysis**  
_Which player did each player lose to most often every year?_  
> Powered by SSIS-based transformation.

✅ **Age-Outlier Matches**  
_Which players participated in matches with a large age difference (outliers)?_

✅ **Most Losing Players by Continent**  
_Using MDX: Who lost the most matches in each continent?_

✅ **Player Participation per Tournament**  
_Using MDX: How many players participated in each tournament?_

✅ **Profit Analysis**  
_Quarterly profit change per tournament, year-over-year (YOY)._

✅ **Dashboards**  
- **Geo Dashboard:** Winner vs. Loser rank points by region  
- **Finance Dashboard:** Tournament-level profit breakdowns

---

## 🧱 Data Architecture

**Snowflake Schema Design**  
- **Fact Table:** Matches with keys to all dimensions  
- **Dimensions:** Player, Date, Tournament, Geography  

**ETL Process:**  
- Stage & clean data with Python  
- Load 20% into `_SSIS` tables  
- Full load using optimized method (based on performance benchmarks)

**Tools Used:**
- Microsoft SQL Server Management Studio (SSMS)
- SQL Server Integration Services (SSIS)
- Python for data preparation
- Excel + Power BI for Dashboards
- MDX for OLAP querying

---

## 🗂️ Dataset Files

- `fact.csv`: Match-level performance and financial data  
- `sample_tourney.json`: Tournaments metadata  
- `countries.xml`: Player's country and continent

---

## 📌 How to Use This Project

1. Clone the repo
2. Setup the DW schema in SQL Server
3. Use Python scripts to preprocess data and create dimension/fact files
4. Use SSIS to populate `_SSIS` tables
5. Deploy the OLAP Cube and run MDX queries
6. Load dashboards with your preferred BI tool (e.g., Power BI or Tableau)

---

## ⭐ Like the project?

If you find this useful or inspiring, consider **starring** the repo! ⭐  
Your support helps maintain and expand projects like this.

---

## 📧 Contacts

Project by:  
- Cristiano Landi  
- Anna Monreale  

University of Pisa | LDS24 Straordinario  
