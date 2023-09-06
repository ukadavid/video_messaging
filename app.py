from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your routes from the respective blueprints
from routes.user_routes import user_bp
from routes.video_routes import video_bp
from routes.share_routes import share_bp

# Register your blueprints with the app
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(video_bp, url_prefix='/video')
app.register_blueprint(share_bp, url_prefix='/share')

if __name__ == '__main__':
    app.run()
