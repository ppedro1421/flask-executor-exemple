import os
from dotenv import load_dotenv
from app import app

load_dotenv(override=True)

if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG', True)
    )
