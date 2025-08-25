import threading
import subprocess
import time
from flask import Flask, render_template, send_from_directory, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ======================================================
# Headline Recommender (with location alerts)
# ======================================================
class HeadlineRecommender:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.load_data()

    def load_data(self):
        try:
            self.data = pd.read_csv(self.csv_file)
            if not {"Headline", "Link", "Date"}.issubset(self.data.columns):
                raise ValueError("CSV file missing required columns.")
            
            # TF-IDF Vectorization
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.headline_vectors = self.vectorizer.fit_transform(self.data['Headline'].astype(str))
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = pd.DataFrame(columns=["Headline", "Link", "Date"])
            self.vectorizer = None
            self.headline_vectors = None

    def recommend(self, keyword, location=None):
        if self.vectorizer is None or self.data.empty:
            return {"error": "No data available. Try again later."}

        keyword_vector = self.vectorizer.transform([keyword])
        similarities = cosine_similarity(keyword_vector, self.headline_vectors).flatten()
        most_similar_idx = similarities.argmax()

        result = {
            "Headline": self.data.iloc[most_similar_idx]['Headline'],
            "Link": self.data.iloc[most_similar_idx]['Link'],
            "Date": self.data.iloc[most_similar_idx]['Date'],
            "Similarity Score": float(similarities[most_similar_idx])
        }

        # Location-based alert
        if location:
            loc = location.lower()
            headline_text = str(result["Headline"]).lower()
            if loc in headline_text:
                result["Alert"] = f"⚠️ Cyber incident detected near {location}!"
            else:
                result["Alert"] = f"✅ No direct incident reported near {location}."

        return result


# ======================================================
# Flask App
# ======================================================
app = Flask(__name__)
recommender = HeadlineRecommender("news.csv")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def home():
    try:
        file_path = "news.csv"
        data = pd.read_csv(file_path)
        records = data[["Headline", "Link", "Date"]].to_dict(orient="records")
        return render_template("index.html", records=records)
    except Exception as e:
        print(f"Error: {e}")
        return "Error loading data"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        keyword = data.get("keyword")
        location = data.get("location")

        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400

        recommendation = recommender.recommend(keyword, location)
        return jsonify(recommendation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================================
# Scraping Task (runs scraping.py)
# ======================================================
def run_scraping_task():
    while True:
        print("Running scraping.py to refresh news...")
        try:
            subprocess.run(["python", "scraping.py"], check=True)
            print("✅ scraping.py executed successfully.")
            
            # Reload recommender with updated news
            recommender.load_data()
            print("🔄 Recommender reloaded with new headlines.")
        except Exception as e:
            print(f"Error running scraping.py: {e}")
        time.sleep(300)  # run every 5 minutes


# ======================================================
# Main Entry Point
# ======================================================
if __name__ == "__main__":
    scraping_thread = threading.Thread(target=run_scraping_task)
    scraping_thread.daemon = True
    scraping_thread.start()
    print("🚀 Starting Flask app...")
    app.run(debug=False,use_reloader=False)
