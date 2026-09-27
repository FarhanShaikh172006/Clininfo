# services/firebase_service.py
import os
import json
from dotenv import load_dotenv

# Force reload environment variables on initialization
load_dotenv(override=True)

class FirebaseService:
    @staticmethod
    def get_config() -> dict:
        """
        Retrieves Firebase Web SDK configuration dictionary from environment.
        """
        config = {
            "apiKey": os.getenv("FIREBASE_API_KEY", ""),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
            "projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
            "appId": os.getenv("FIREBASE_APP_ID", ""),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "")
        }
        return config

    @staticmethod
    def get_config_json() -> str:
        """
        Returns JSON-encoded configuration string for safe Jinja template injection.
        """
        return json.dumps(FirebaseService.get_config())

    @staticmethod
    def validate_keys() -> bool:
        """
        Validates whether key required Firebase parameters are set.
        """
        config = FirebaseService.get_config()
        return bool(config.get("apiKey") and config.get("projectId"))