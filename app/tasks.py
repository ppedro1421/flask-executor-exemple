from app import app
import time

def background_task(task_id):
    time.sleep(10)
    app.logger.info("Task %s completed", task_id)
