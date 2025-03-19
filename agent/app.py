from flask import Flask, request, jsonify,render_template
from dotenv import load_dotenv
from agent import bias_checker
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app) 

@app.get("/")
def home():
    return render_template("index.html")
@app.post("/analyse")
def analyse():
    try:
        body = request.get_json()
        query = body["query"]
        res = bias_checker(query)
        return jsonify(res)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"err": "internal server error"})

if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port, debug = not int(os.getenv("PROD", 0))) 
