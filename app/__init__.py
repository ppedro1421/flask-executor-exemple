import logging
from flask import Flask
from flask_cors import CORS
from flask_executor import Executor

app = Flask(__name__)

CORS(app)

app.config['EXECUTOR_TYPE'] = 'process'
app.config['EXECUTOR_MAX_WORKERS'] = 5

file_handler = logging.FileHandler(filename="app.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
file_handler.setLevel(logging.INFO)
app.logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

executor = Executor(app)

from app.routes import bp

app.register_blueprint(bp)
