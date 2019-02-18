from flask import Flask
from flask_cors import CORS
from APIs.counter_api import count_vehicles_app

app = Flask(__name__)
CORS(app)

app.register_blueprint(count_vehicles_app)


@app.route('/')
def welcome():
    return 'Traffic Counter api'


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
