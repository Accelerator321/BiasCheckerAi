from agent import agent
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
from flask_cors import CORS  


load_dotenv()
PROD = os.getenv("PROD")

app = Flask(__name__)
CORS(app) 


@app.route("/biascheck", methods=["POST"])
def check_bias():
    content = request.get_json()
    
    return agent.print_response(f"check bias and rewrite if needed =>{content['text']}")

@app.route("/", methods=["GET"])
def home():
    return "Bias Checking API is running! Use the /biascheck endpoint with a POST request."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=not PROD)

