import os

import dotenv

dotenv.load_dotenv()

API_HOST = os.environ.get("API_HOST")
API_PORT = int(os.environ.get("API_PORT"))

CLASSIFIER_HOST = os.environ.get("CLASSIFIER_HOST")
CLASSIFIER_PORT = int(os.environ.get("CLASSIFIER_PORT"))
