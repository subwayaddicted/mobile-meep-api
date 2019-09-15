from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def test():
    return jsonify(
        test_data='test_string'
    )
