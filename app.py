from flask import Flask, request, jsonify
import json
import time
from pathlib import Path

app = Flask(__name__)

# Paths for Kaggle interaction
input_path = Path("input.json")
output_path = Path("output.json")

@app.route('/extract', methods=['POST'])
def extract_info():
    user_text = request.json.get("text", "")

    # Save user input to Kaggle's input file
    input_path.write_text(user_text)

    # Wait for Kaggle to process and write the output
    for _ in range(30):
        time.sleep(2)
        if output_path.exists() and output_path.read_text().strip():
            try:
                response = json.loads(output_path.read_text())
                output_path.write_text("")  # Clear the output after sending response
                return jsonify(response)
            except json.JSONDecodeError:
                return jsonify({"error": "Malformed response from Kaggle"})

    return jsonify({"error": "Timeout while waiting for Kaggle response"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
