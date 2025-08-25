🔐 AI-Driven Cyber Incident Monitoring

Technologies: Python · Flask · HTML/CSS/JS · Scikit-learn · BeautifulSoup · Pandas

📌 Project Overview

This project is an AI-powered real-time cyber incident monitoring system that fetches the latest cybersecurity-related news articles from the web, processes them using NLP techniques, and provides predictive insights about possible cyber threats happening near the user’s interest area.

It integrates:

🌐 Web Scraping (automated news collection)

🖥️ Dynamic  Frontend for visualization

🤖 Machine Learning (Scikit-learn + NLP) for predictive analysis

⚡ Flask Backend to serve live data and recommendations

📍 Location-Based Threat Alerts that warn users if incidents are happening near them

🚀 Features

✅ Real-time Web Scraping – Fetches cybersecurity news automatically from Google News every 5 minutes.


✅ AI-Powered Predictions – Uses TF-IDF Vectorization + Cosine Similarity to match user queries with the most relevant cyber incidents.


✅ Interactive Search – User can enter keywords (e.g., phishing, ransomware, DDoS) and instantly see related cybercrime predictions.


✅ Dynamic Dashboard –  frontend updates with the latest incidents.


✅ Automated Storage – News articles are saved in news.csv for continuous training and predictions.


✅ 📍 Location-Based Alerts – Detects user’s city/country (via browser geolocation) and alerts them if a cyber incident is reported in or near their region.

🛠️ Tech Stack

Backend: Python, Flask, Threading (for continuous scraping)

Frontend:HTML/CSS

Data Processing: Pandas, BeautifulSoup (scraping & cleaning)

AI/ML: Scikit-learn,(TF-IDF + Cosine Similarity)

Location Services: HTML5 Geolocation API + OpenStreetMap Reverse Geocoding
