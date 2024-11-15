import requests
import time

KEYCLOAK_URL = 'http://localhost:8080/auth'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

def configure_keycloak():
    # Wait for Keycloak to start
    time.sleep(30)

    # Get admin access token
    token_response = requests.post(
        f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token",
        data={
            'grant_type': 'password',
            'client_id': 'admin-cli',
            'username': ADMIN_USERNAME,
            'password': ADMIN_PASSWORD
        }
    )
    admin_token = token_response.json()['access_token']

    headers = {'Authorization': f'Bearer {admin_token}',
               'Content-Type': 'application/json'}
    
    # TODO: Create realm, client, user, etc.
    # ...