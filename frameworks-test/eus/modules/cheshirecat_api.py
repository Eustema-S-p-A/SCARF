import os
import json
import requests
import logging
import mimetypes
from typing import Dict, Any, Optional


class CheshireCatAPI:
    def __init__(self, base_url: str, api_key: str, username: str, password: str):
        logging.info("Starting CheshireCat API Client")
        self.base_url = base_url
        self.api_key = api_key
        self.username = username
        self.password = password
        self.jwt = self._get_jwt_token()
        self.headers = {
            'Authorization': f'Bearer {self.jwt}',
            'accept': 'application/json'
        }

    def _get_jwt_token(self) -> str:
        """Retrieve JWT token using username and password."""
        url = f"{self.base_url}/auth/token"
        payload = {"username": self.username, "password": self.password}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logging.info("JWT token retrieved successfully.")
            return response.json()["access_token"]
        except requests.RequestException as e:
            logging.error(f"Failed to obtain JWT token: {e}")
            raise

    def upload_document(self, file_path: str) -> Dict[str, Any]:
        """Upload a document to the Cheshire Cat system."""
        url = f"{self.base_url}/rabbithole/"
        file_name = os.path.basename(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        metadata = {
            "source": file_name,
            "title": file_name,
            "author": "Test author",
            "year": 2024
        }

        payload = {
            "chunk_size": 512,
            "chunk_overlap": 64,
            "metadata": json.dumps(metadata)
        }

        logging.info(f"Uploading document '{file_name}' to Cheshire Cat...")
        try:
            with open(file_path, 'rb') as file:
                files = {"file": (file_name, file, content_type)}
                response = self._post_request(url, payload=payload, files=files)
                if response.get('status_code') == 200:
                    logging.info(f"Document '{file_name}' uploaded successfully.")
                else:
                    logging.error(f"Failed to upload document '{file_name}'.")
                return response
        except requests.RequestException as e:
            logging.error(f"Document upload failed: {e}")
            return {'error': str(e)}

    def send_message(self, message: str) -> Dict[str, Any]:
        """Send a message to the Cheshire Cat system."""
        url = f"{self.base_url}/message"
        payload = {"text": message}

        logging.info(f"Sending message to Cheshire Cat: {message}")
        response = self._post_request(url, payload=payload)
        if response.get('status_code') == 200:
            logging.info(f"Message sent successfully: {message}")
        else:
            logging.error(f"Failed to send message: {message}")
        return {'text_response': response.get('data', {}).get('content', {}), 'full_response': response}

    def get_status(self) -> Dict[str, Any]:
        """Check the status of the Cheshire Cat system."""
        url = f"{self.base_url}/status"
        logging.info("Checking status of Cheshire Cat system...")
        return self._get_request(url)

    def _get_request(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Internal method to handle GET requests."""
        try:
            combined_headers = {**self.headers, **(headers or {})}
            response = requests.get(url, headers=combined_headers)
            response.raise_for_status()
            logging.info(f"GET request to {url} successful.")
            return {"status_code": response.status_code, "data": response.json()}
        except requests.RequestException as e:
            logging.error(f"GET request to {url} failed: {e}")
            return {'error': str(e)}

    def _post_request(self, url: str, payload: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Internal method to handle POST requests."""
        try:
            combined_headers = {**self.headers, **(headers or {})}
            if files:
                response = requests.post(url, headers=combined_headers, files=files, data=payload)
            else:
                response = requests.post(url, headers=combined_headers, json=payload)
            response.raise_for_status()
            logging.info(f"POST request to {url} successful.")
            return {"status_code": response.status_code, "data": response.json()}
        except requests.RequestException as e:
            logging.error(f"POST request to {url} failed: {e}")
            return {'error': str(e)}
