import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_executor import Executor

EXECUTOR_TYPE = os.getenv('EXECUTOR_TYPE', 'thread')
EXECUTOR_MAX_WORKERS = os.getenv('EXECUTOR_MAX_WORKERS', 5)
LOGGER_THREAD_FORMATTER = '%(asctime)s - %(threadName)s - %(levelname)s: %(message)s'
LOGGER_PROCESS_FORMATTER = '%(asctime)s - %(processName)s - %(levelname)s: %(message)s'

app = Flask(__name__)

CORS(app)

app.config['EXECUTOR_TYPE'] = EXECUTOR_TYPE
app.config['EXECUTOR_MAX_WORKERS'] = EXECUTOR_MAX_WORKERS

formatter = LOGGER_THREAD_FORMATTER
if EXECUTOR_TYPE == 'process':
    formatter = LOGGER_PROCESS_FORMATTER

file_handler = logging.FileHandler(filename="app.log")
file_handler.setFormatter(logging.Formatter(formatter))
file_handler.setLevel(logging.INFO)
app.logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

executor = Executor(app)

from app.routes import bp

app.register_blueprint(bp)
