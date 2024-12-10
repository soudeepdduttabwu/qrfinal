from flask import Flask
from flask_cors import CORS
import os

def create_app(config_class=None):
    """
    Application factory for creating Flask app instances
    """
    # Default to development config if not specified
    if config_class is None:
        from config.development import DevelopmentConfig
        config_class = DevelopmentConfig

    # Create app instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "allow_headers": [
                "Content-Type", 
                "Authorization", 
                "Access-Control-Allow-Credentials"
            ],
            "supports_credentials": True
        }
    })

    # Import and initialize components
    from .database import DatabaseManager
    from .qr_utils import QRCodeScanner
    from .camera import VideoCamera
    from .routes import routes, RouteHandler

    # Create utility instances
    database_manager = DatabaseManager(app.config)
    qr_scanner = QRCodeScanner()
    camera = VideoCamera(app.config.CAMERA_INDEX)

    # Setup route handler
    route_handler = RouteHandler(
        app.config, 
        camera, 
        qr_scanner, 
        database_manager
    )
    route_handler.setup_routes(routes)
    app.register_blueprint(routes)

    return app