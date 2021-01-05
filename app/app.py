#import json
#import logging
#import logging.config
#with open('../log_config.json', 'r') as f:
#    log_config = json.load(f)
#logging.config.dictConfig(log_config)
#logger = logging.getLogger(__name__)

from flask import Flask

app = Flask(__name__)
#Blueprints
from core_api import bp 
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
