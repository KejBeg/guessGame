
# Import to use for production deployment
from waitress import serve

# Import the app
from app import app

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80, threads=2)