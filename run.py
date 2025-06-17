from app import create_app

# Create the Flask app instance using the app factory
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(host='0.0.0.0', port=5000, debug=True)