import logging  # Add logging for debugging
from backend.app import create_app  # Use absolute import

app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # app.run(debug=False, host="your-ip-address", port=5000)  Host Locally
    app.run(debug=True)