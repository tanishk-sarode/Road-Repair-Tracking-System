import logging  # Add logging for debugging
from backend.app import create_app  # Use absolute import

app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # app.run(debug=True, host="127.0.0.1", port=5000)  # Explicitly set host and port
    app.run(debug=True)