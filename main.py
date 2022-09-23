from app import create_app
from config import DevelopmentConfig

def main():
    app = create_app(config_class=DevelopmentConfig)
    app.run(port=5500)

main()