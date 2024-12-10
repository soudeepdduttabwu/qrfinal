from app import create_app
import os

# Choose configuration based on environment
if os.environ.get('FLASK_ENV') == 'production':
    from config.production import ProductionConfig
    config = ProductionConfig
else:
    from config.development import DevelopmentConfig
    config = DevelopmentConfig

app = create_app(config)

if __name__ == "__main__":
    # Use environment variables or default values
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host=host, 
        port=port, 
        debug=app.config['DEBUG']
    )