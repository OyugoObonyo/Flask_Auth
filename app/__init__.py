from flask import Flask
from dotenv import load_dotenv

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class)
    load_dotenv()

    return app
    
