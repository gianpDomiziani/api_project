import os
import sys
sys.path.append(os.path.dirname(__file__))
# === Logger START===
import json
import logging
import logging.config
with open('app/log_config.json', 'r') as f:
    log_dict = json.load(f)
logging.config.dictConfig(log_dict)
logger = logging.getLogger(__name__)
# === Logger END ===