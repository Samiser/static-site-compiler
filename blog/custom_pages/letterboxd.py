import json
import requests

def authenticate_letterboxd(username, password):
    # Your API endpoint
    url = "https://api.letterboxd.com/api/v0/auth/token"

    # Your API headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    # Your API body
    body = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=body)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Otherwise return the access token
    return response.json()['access_token']
