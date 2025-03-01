from agent import check_bias
from dotenv import load_dotenv
import os
from flask import Flask, json, jsonify, request
from flask_cors import CORS

load_dotenv()
PROD = os.getenv("PROD")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/biascheck", methods=["POST"])
def checker():
  body = request.get_json()
  # print(body)
  try:

    response = check_bias(body["url"])

    return jsonify(response), 200

  except Exception as e:
    print(e)
    return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
  return "Bias Checking API is running! Use the /biascheck endpoint with a POST request."


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=not PROD)
  # app.run(debug=not PROD)
