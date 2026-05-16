# 👁️‍🗨️ Digital Resonance

**COMM7780 Final Project: Big Data Analytics for Media and Communication**

## 📌 Project Overview

**Digital Resonance** is a real-time, LLM-powered public opinion monitoring dashboard. Moving beyond static data reports, this project dynamically scrapes unstructured text data (e.g., comments, reviews) from media platforms and leverages the **NVIDIA Llama 3.1 70B** model to decode chaotic digital footprints into actionable sociological and commercial insights.

It is designed as a Proof of Concept (PoC) for a "One-Person Company" (SaaS model), empowering solopreneurs, indie developers, and solo creators with automated PR and deep data analysis capabilities.

## ✨ Key Features

- 🎮 **Steam Gamer "Tsundere" Radar:** Cross-references playtime with negative reviews to uncover complex emotional connections (the "Tsundere" phenomenon) in hardcore gaming communities.
- 📺 **YouTube Comment X-Ray:** Instantly extracts top-tier comments and identifies emotional contagion, factional divides, and echo chambers.
- 🧠 **Deep LLM Insights:** Shifts from basic string matching to deep semantic and sociological analysis using advanced prompt engineering.
- 📊 **Cyberpunk Interactive UI:** Built with Streamlit and Plotly, featuring a custom dark mode aesthetic and dynamic, interactive charts.

## 🛠️ Tech Stack

- **Frontend & App Framework:** Streamlit (with custom CSS injection)
- **Data Processing & Visualization:** Pandas, Plotly
- **LLM Engine:** NVIDIA API (`Meta Llama 3.1 70B Instruct`)
- **Data Sources:** Steamworks Web API, YouTube Data API v3
- **Deployment:** Debian Linux VPS, Nginx (Reverse Proxy with WebSocket support), Systemd

## 🚀 How to Run Locally

If you wish to run this dashboard on your local machine, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/SuPeRK0123/Course_Project.git
cd Course_Project
```

### 2. Install dependencies

```bash
pip install streamlit requests pandas plotly
```

### 3. Configure API Keys

Open pages/1_🎮_Steam_Radar.py and pages/2_📺_YouTube_Xray.py.
Replace the placeholder strings at the top of the files with your actual API keys:

```python
NVIDIA_API_KEY = "your_nvidia_api_key_here"
YOUTUBE_API_KEY = "your_youtube_api_key_here"
```
(Note: Steam API does not require a key for public reviews).

### 4. Launch the Dashboard

```bash
streamlit run app.py
```
The application will be available at http://localhost:8501.

## 📂 Repository Structure
```text
├── pages/
│   ├── 1_🎮_Steam_Radar.py   # Steam data scraping & LLM analysis module
│   └── 2_📺_YouTube_Xray.py  # YouTube data scraping & LLM analysis module
├── app.py                    # Main entry point and project vision statement
└── README.md                 # Project documentation
```
