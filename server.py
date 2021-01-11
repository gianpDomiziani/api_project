import os
import sys
sys.path.append(os.path.abspath(__file__) + '../app')

from app import create_app
from app.config import default_config
from app.custom_logger import logger

app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask API ...")
    app.run(port=8080, debug=default_config['app_debug'])