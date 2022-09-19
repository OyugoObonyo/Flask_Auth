from app import create_app
from config import DevelopmentConfig

app = create_app(config_class=DevelopmentConfig)

app.run(port=5500)