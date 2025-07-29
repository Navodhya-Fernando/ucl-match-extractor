# 🏆 UCL Match Data Extractor

A simple Streamlit tool developed for a research project conducting a **comparative analysis between the new UEFA Champions League (UCL) format and the previous format**.

This tool helps extract key data points from UCL match reports and SofaScore sources, storing them in MongoDB for structured analysis.

## 🔧 Features

- Upload official UCL match report PDFs
- Manually input team data (cards, market value, injuries)
- Automatically calculates totals and saves to MongoDB
- Supports both “Old” and “New” UCL formats

## 🧱 Tech Stack

This tool is built using a lightweight full stack architecture:

| Layer         | Technology   | Purpose                                      |
|---------------|--------------|----------------------------------------------|
| Frontend (UI) | Streamlit    | Web interface for file upload and inputs     |
| Backend       | Python       | Business logic and PDF parsing               |
| Database      | MongoDB      | Storing extracted and structured match data  |

> Designed for simplicity, accuracy, and ease of use for academic data collection and analysis.

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run ucl_tool.py