# DeFi Analytics Data Platform: End-to-End Analytics Engineering Pipeline

![Dashboard Preview](https://raw.githubusercontent.com/SergeyKoverzen/defi-analytics-dbt-bigquery/main/assets/dashboard_preview.png)
*(Замените ссылку на ваш скриншот)*

## 🔗 Quick Links
- **Live Interactive Dashboard:** [📊 Looker Studio Report](https://datastudio.google.com/s/s_BfMsyFwoo)
- **Author:** Sergey Koverzen ([LinkedIn](https://www.linkedin.com/in/serhii-k-51680032a) | [GitHub](https://github.com/SergeyKoverzen))

---

## 📌 Project Overview
This project demonstrates a production-style Analytics Engineering workflow that transforms raw, unstructured Web3 API data into structured, business-ready analytical data marts.

Using a **Medallion Architecture (Bronze → Silver → Gold)**, the pipeline automates the extraction of DeFi market metrics (Total Value Locked, Protocol Categories, Chain Breakdown), handles nested JSON parsing, deduplicates snapshot data, and exposes materialized tables to Looker Studio.

---

## 🏗️ Data Architecture & Pipeline
