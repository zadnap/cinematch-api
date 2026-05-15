import os
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL")

if not ML_SERVICE_URL:
    raise ValueError("Missing ML_SERVICE_URL environment variable")


class MLService:
    TIMEOUT = (5, 60)

    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    session.mount(
        "https://",
        HTTPAdapter(max_retries=retries)
    )

    @staticmethod
    def get_recommendations(user_id, top_k=100):
        try:
            response = MLService.session.get(
                f"{ML_SERVICE_URL}/recommend",
                params={
                    "user_id": user_id,
                    "top_k": top_k
                },
                timeout=MLService.TIMEOUT
            )

            response.raise_for_status()

            json_data = response.json()

            if "data" not in json_data:
                raise RuntimeError(
                    "ML service response missing data field"
                )

            return json_data["data"]

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "ML service timeout"
            )

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Cannot connect to ML service"
            )

        except requests.exceptions.HTTPError as e:
            raise RuntimeError(
                f"ML service HTTP error: {e}"
            )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"ML service request failed: {e}"
            )

        except ValueError:
            raise RuntimeError(
                "Invalid JSON response from ML service"
            )