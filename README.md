# DeFi Analytics Data Platform: End-to-End Analytics Engineering Pipeline

![Dashboard Preview](docs/TVL_Dashboard.pdf)

## 🔗 Quick Links
- **Live Interactive Dashboard:** [📊 Looker Studio Report](https://datastudio.google.com/s/s_BfMsyFwoo)

---

## 📌 Project Overview
This project demonstrates a production-style Analytics Engineering workflow that transforms raw, unstructured Web3 API data into structured, business-ready analytical data marts.

Using a **Medallion Architecture (Bronze → Silver → Gold)**, the pipeline automates the extraction of DeFi market metrics (Total Value Locked, Protocol Categories, Chain Breakdown), handles nested JSON parsing, deduplicates snapshot data, and exposes materialized tables to Looker Studio.

---

## 🏗️ Data Architecture & Pipeline
