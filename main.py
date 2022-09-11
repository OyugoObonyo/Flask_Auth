from app import create_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
 

app = create_app(Config)

app.run(port=5500, debug=True)