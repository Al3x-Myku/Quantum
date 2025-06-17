from flask import Flask, jsonify
from config import config_by_name

def create_app(config_name='development'):
    """
    Application factory function.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    with app.app_context():
        # Import and register routes
        from . import routes

        # Register a global error handler for 500 Internal Server Error
        @app.errorhandler(500)
        def internal_server_error(error):
            app.logger.error(f"Server Error: {error}")
            return jsonify(error="An unexpected internal server error occurred."), 500

    return app