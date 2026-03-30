import os

import requests


def verify_token_with_auth_service(token):
    base_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000").rstrip("/")
    verify_url = f"{base_url}/api/auth/verify/"

    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(verify_url, headers=headers, timeout=5)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    if "name" not in data or "roll_number" not in data:
        return None

    return {
        "name": data["name"],
        "roll_number": data["roll_number"],
    }
