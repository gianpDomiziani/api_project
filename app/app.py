import json
import logging
import logging.config
with open('../log_config.json', 'r') as f:
    log_config = json.dumps(f.read())
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

from flask import Flask

app = Flask(__name__)
#Blueprints
from core.core_api import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
