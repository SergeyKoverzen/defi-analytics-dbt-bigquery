# DeFi Analytics Data Platform: End-to-End Analytics Engineering Pipeline

## 🔗 Quick Links
![Dashboard Preview](docs/TVL_Dashboard.pdf)   -AND-   **Live Interactive Dashboard:** [📊 Looker Studio Report](https://datastudio.google.com/s/s_BfMsyFwoo)

---

## 📌 Project Overview
This project demonstrates a production-style Analytics Engineering workflow that transforms raw, unstructured Web3 API data into structured, business-ready analytical data marts.

Initially, the raw datasets and transformations were prototyped and prepared on **Databricks** with a target connection for **Power BI** reporting. To build an agile, cloud-native Analytics Engineering stack, the architecture was fully materialized using a **Medallion Architecture (Bronze → Silver → Gold)** in **Google BigQuery** and **dbt**, serving a live dashboard in **Looker Studio**.

---

## 🌐 Data Sources & Extraction
- **Primary Data Source:** Open-source Web3 / DeFi aggregator **[DeFiLlama API](https://defillama.com/docs/api)** (`https://api.llama.fi/protocols`).
- **Data Attributes Extracted:** Protocol IDs, Names, Categories (DEXs, Lending, Liquid Staking, Yield, etc.), Main Chains, TVL (Total Value Locked), and historical metrics.
- **Ingestion Technique:** Python-driven REST API polling with rate limiting and retry handling.

---

## 🏗️ Data Architecture & Pipeline

```text
[ External DeFi API ]
         │
         ▼ (Initial Prototyping & Staging on Databricks / Power BI Ready)
[ Databricks / PySpark Environment ]
         │
         ▼ (Python Ingestion Script to Production DWH)
[ BigQuery: Bronze Layer ]  ──>  `bronze_protocols_raw` (Raw JSON Payload)
         │
         ▼ (dbt Models: JSON Parsing & Deduplication)
[ BigQuery: Silver Layer ]  ──>  `stg_protocols` (Cleaned & Structured SQL Views)
         │
         ▼ (dbt Models: Aggregations & Data Marts)
[ BigQuery: Gold Layer ]    ──>  `mart_protocols_summary` (Materialized Data Mart)
         │
         ▼ (BI Integration)
[ Looker Studio / Power BI ] ──> Interactive Executive Dashboards ($570B+ TVL Analyzed)

---

## ⚙️ Data Processing & Technical Implementation Details

### 0. Initial Prototyping (Databricks & Power BI Integration)

Processed initial raw API payloads using Databricks (PySpark / Spark SQL) to explore schema definitions and build prototype analytical tables.

Formatted data schemas for direct model integration with Power BI via DirectQuery / Import modes.

### 1. Bronze Layer (Raw Ingestion)

Script: scripts/fetch_to_bigquery.py

Fetches full protocol snapshots from DeFiLlama API using Python (requests, google-cloud-bigquery).

Appends unparsed JSON records (raw_json) directly into BigQuery Bronze table with metadata fields (fetch_timestamp in UTC ISO format).

### 2. Silver Layer (Parsing, Cleaning & Deduplication — dbt / SQL)

- **Model:** `dbt_project/models/silver/stg_protocols.sql`
- **JSON Parsing:** Uses BigQuery's native `JSON_VALUE()` functions to extract nested attributes (`protocol_id`, `name`, `category`, `chain`, `tvl`).
- **Data Deduplication:** Due to frequent API polling, multiple snapshots of the same protocol accumulate over time. The Silver layer cleans duplicates using SQL Window Functions:

    ```sql
  QUALIFY ROW_NUMBER() OVER (
      PARTITION BY protocol_id 
      ORDER BY fetch_timestamp DESC
  ) = 1

### 3. Gold Layer (Analytics Marts & Aggregations)

- Model: dbt_project/models/gold/mart_protocols_summary.sql

- Analytical Transformations: Groups and materializes key KPIs: Total Value Locked (TVL) per Blockchain (main_chain), Total TVL & Protocol Count per Category (category), and average TVL metrics.

- Optimized for BI: Materialized as physical tables in BigQuery for high-performance querying and fast response times in BI tools.

### 4. BI & Visualisation Layer (Looker Studio)

- Executive Metrics: High-level scorecard showing Total Market TVL ($570.7B+).

- Liquidity Concentration: Pie chart highlighting dominant blockchains (Multi-Chain & Ethereum capturing ~80%+ liquidity).

- Sector Analysis: Bar charts and data tables breaking down TVL and protocol counts across categories (DEXs, Lending, Liquid Staking, Yield).
  
  ---
  
## ⚙️ Key Technical Features & Implementation Details

### 1. Bronze Layer (Raw Ingestion)
- Fetches protocol metrics from Web3 endpoints using Python (`requests`, `google-cloud-bigquery`).
- Stores append-only raw JSON records (`raw_json`) with ingestion metadata (`fetch_timestamp`).

### 2. Silver Layer (Parsing & Deduplication)
- **JSON Attribute Extraction:** Uses native BigQuery `JSON_VALUE` within dbt staging models to unnest attributes like `protocol_id`, `protocol_name`, `category`, `chain`, and `tvl`.
- **Data Quality & Deduplication:** Implements `ROW_NUMBER() OVER (PARTITION BY protocol_id ORDER BY fetch_timestamp DESC)` to eliminate duplicate API polling snapshots and retain only the latest data state.

### 3. Gold Layer (Analytics Marts)
- **Analytical Transformations:** Groups and materializes key KPIs: Total Value Locked (TVL), Average TVL per category, Protocol counts, and Chain liquidity shares.
- **Optimized for BI:** Materialized as tables in BigQuery for fast query response times in BI tools.

### 4. BI & Visualisation (Looker Studio)
- **Executive Metrics:** High-level scorecard showing Total Market TVL (**$570.7B+**).
- **Liquidity Concentration:** Pie chart highlighting dominant blockchains (Multi-Chain & Ethereum capturing ~80%+ liquidity).
- **Sector Analysis:** Bar chart and data tables breaking down TVL and protocol count across categories (DEXs, Lending, Liquid Staking, Yield).

---

## 📊 Business & Analytical Insights

1. **High Capital Centralization:** Over **80%** of total lockable capital ($570B+) is concentrated in Multi-Chain architecture and Ethereum, leaving alternative L1s in niche markets.
2. **Core DeFi Primitives:** Decentralized Exchanges (DEXs), Yield Aggregators, and Lending protocols account for the vast majority of active protocols and capital efficiency.
3. **Analytics Engineering Value:** By implementing automated deduplication and data modeling at the DWH layer (BigQuery + dbt), dashboard loading times and data accuracy were significantly improved compared to querying raw JSON directly.

---

## 🛠️ Tech Stack & Tools
- **Data Warehouse:** Google BigQuery
- **Data Transformation:** dbt (data build tool)
- **Data Processing / Scripting:** Python (Pandas, BigQuery API)
- **BI / Data Visualization:** Looker Studio
- **Data Architecture:** Medallion Architecture (Bronze, Silver, Gold)
- **Version Control:** Git / GitHub

---

## 📁 Repository Structure

```text
├── dbt_project/              # dbt project configuration & models
│   ├── models/
│   │   ├── bronze/           # Raw data references
│   │   ├── silver/           # Staging models (parsing & deduplication)
│   │   └── gold/             # Analytical data marts (mart_protocols_summary)
│   └── dbt_project.yml
├── scripts/                  # Python ingestion scripts
│   └── fetch_to_bigquery.py
├── docs/                   # Dashboard screenshots and diagrams
└── README.md
