from flask import Flask
app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello, World as test message!'