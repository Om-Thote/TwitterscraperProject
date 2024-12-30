from flask import Flask, render_template
import subprocess  # To run external script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script')
def run_script():
    subprocess.run(["python", "twitter_trending.py"])  # Run the Selenium script
    return "Script executed successfully! Refresh to see results."

@app.route('/results')
def results():
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client["twitter_data"]
    collection = db["trends"]
    latest_data = collection.find_one({}, sort=[('_id', -1)])  # Fetch most recent record
    return render_template('results.html', data=latest_data)

if __name__ == '__main__':
    app.run(debug=True)
