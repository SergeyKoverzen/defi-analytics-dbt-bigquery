# DeFi Analytics Data Platform: End-to-End Analytics Engineering Pipeline

## 🔗 Quick Links
![Dashboard Preview](docs/TVL_Dashboard.pdf)   -AND-   **Live Interactive Dashboard:** [📊 Looker Studio Report](https://datastudio.google.com/s/s_BfMsyFwoo)

---

## 📌 Project Overview
This project demonstrates a production-style Analytics Engineering workflow that transforms raw, unstructured Web3 API data into structured, business-ready analytical data marts.

Using a **Medallion Architecture (Bronze → Silver → Gold)**, the pipeline automates the extraction of DeFi market metrics (Total Value Locked, Protocol Categories, Chain Breakdown), handles nested JSON parsing, deduplicates snapshot data, and exposes materialized tables to Looker Studio.

---

## 🏗️ Data Architecture & Pipeline

│
▼ [ External DeFi API ]


│
▼ (Python Ingestion Script)
[ BigQuery: Bronze Layer ]  ──>  bronze_protocols_raw (Raw JSON Payload)


│
▼ (dbt Models: JSON Parsing & Deduplication)
[ BigQuery: Silver Layer ]  ──>  stg_protocols (Cleaned & Structured SQL Views)


│
▼ (dbt Models: Aggregations & Data Marts)
[ BigQuery: Gold Layer ]    ──>  mart_protocols_summary (Materialized Data Mart)


│
▼ (BI Integration)
[ Looker Studio ]          ──>  Interactive Executive Dashboard ($570B+ TVL Analyzed)

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

├── dbt_project/             # dbt project configuration & models
│   ├── models/
│   │   ├── bronze/          # Raw data references
│   │   ├── silver/          # Staging models (parsing & deduplication)
│   │   └── gold/            # Analytical data marts (mart_protocols_summary)
│   └── dbt_project.yml
├── scripts/                 # Python ingestion scripts
│   └── fetch_to_bigquery.py
├── assets/                  # Dashboard screenshots and diagrams
└── README.md
