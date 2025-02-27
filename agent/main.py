from agent import agent
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from flask_cors import CORS  


load_dotenv()
PROD = os.getenv("PROD")

app = Flask(__name__)
CORS(app) 



@app.route("/biascheck", methods=["POST"])
def check_bias(request):
    content = request.get_json()
    
    return agent.print_response(f"check bias and rewrite if needed =>{content['text']}")

if __name__ == "__main__":
    app.run(debug=not PROD)

