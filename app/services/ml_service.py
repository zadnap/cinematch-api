import os
import requests

from dotenv import load_dotenv

load_dotenv()

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL")

class MLService:
    TIMEOUT = 10

    @staticmethod
    def get_recommendations(user_id, top_k=100):
        try:
            response = requests.get(
                f"{ML_SERVICE_URL}/recommend",
                params={
                    "user_id": user_id,
                    "top_k": top_k
                },
                timeout=MLService.TIMEOUT
            )

            response.raise_for_status()

            json_data = response.json()

            return json_data["data"]

        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"ML service request failed: {e}"
            )