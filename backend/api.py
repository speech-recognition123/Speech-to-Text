import os
from datetime import datetime
from pickle import load

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return make_response(
        jsonify(
            {
                "success": True,
                "timestamp": datetime.now().isoformat(),
            }
        ),
        200,
    )


@app.route("/predict", methods=["POST", "GET"])
def predict():
    path = request.json['path']
    text = request.json['text']
    duration = request.json['duration']


    file = {"path": path,
            "text": text,
            "duration": duration}
    # file = request.files["file"]
    pwd = os.getcwd()
    rnn_model_path = os.path.join(pwd, "../model/RNN_model.pickle")
    rnn_model = load(open(rnn_model_path, "rb"))
    prediction = rnn_model.predict(file)
    return make_response(jsonify({"success": True, "data": prediction}), 200)
    return jsonify(file)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
