from app import create_app

from datetime import datetime

# Create the Flask app instance
app = create_app()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)  # Enable debugging mode for development
