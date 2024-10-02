from flask import Flask
from flask_executor import Executor

app = Flask(__name__)

app.config['EXECUTOR_TYPE'] = 'process'
app.config['EXECUTOR_MAX_WORKERS'] = 5

executor = Executor(app)

from app.routes import bp

app.register_blueprint(bp)
