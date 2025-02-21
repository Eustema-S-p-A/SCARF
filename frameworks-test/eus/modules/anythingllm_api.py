import os
import requests
import logging
import mimetypes
from typing import Dict, Any, Optional


class AnythingLLMAPI:
    def __init__(self, base_url: str, api_key: str, workspace_slug: str):
        logging.info("Starting AnythingLLM API Client")
        self.base_url = base_url
        self.api_key = api_key
        self.workspace_slug = workspace_slug
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'accept': 'application/json'
        }
        self.verify_auth()

    def verify_auth(self) -> Dict[str, Any]:
        """Verify authentication using the API key."""
        url = f"{self.base_url}/api/v1/auth"
        logging.info("Verifying authentication with AnythingLLM...")
        response = self._get_request(url)
        if response.get('status_code') == 200:
            logging.info("Authentication verified successfully.")
        else:
            logging.error("Authentication failed.")
        return response

    def upload_document(self, file_path: str) -> Dict[str, Any]:
        """Upload a document to the workspace for processing."""
        url = f"{self.base_url}/api/v1/document/upload"
        file_name = os.path.basename(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        logging.info(f"Uploading document '{file_name}' to AnythingLLM...")
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (file_name, file, content_type)}
                response = self._post_request(url, files=files)
                if response.get('status_code') == 200 and response.get('data', {}).get('success'):
                    logging.info(f"Document '{file_name}' uploaded successfully.")
                else:
                    logging.error(f"Failed to upload document '{file_name}': {response.get('data', {}).get('error', 'Unknown error')}")
                return response
        except requests.RequestException as e:
            logging.error(f"Document upload failed: {e}")
            return {'error': str(e)}

    def send_message(self, message: str, mode: str = "chat", session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to the workspace."""
        url = f"{self.base_url}/api/v1/workspace/{self.workspace_slug}/chat"
        payload = {
            "message": message,
            "mode": mode,
            "sessionId": session_id if session_id else "default-session"
        }

        logging.info(f"Sending message to AnythingLLM: {message}")
        response = self._post_request(url, payload=payload)
        if response.get('status_code') == 200:
            logging.info(f"Message sent successfully: {message}")
        else:
            logging.error(f"Failed to send message: {message}")
        return {'text_response': response.get('data', {}).get('textResponse', {}), 'full_response': response}

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
                response = requests.post(url, headers=combined_headers, files=files)
            else:
                response = requests.post(url, headers=combined_headers, json=payload)
            response.raise_for_status()
            logging.info(f"POST request to {url} successful.")
            return {"status_code": response.status_code, "data": response.json()}
        except requests.RequestException as e:
            logging.error(f"POST request to {url} failed: {e}")
            return {'error': str(e)}
        except ValueError as e:
            logging.error(f"Failed to parse JSON response from {url}: {e}")
            return {'error': f"Failed to parse response: {e}"}
