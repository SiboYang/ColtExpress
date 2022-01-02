import requests

from assets.network_constants import LOBBYURL


def get_user_access_token(username, password):
    # TODO: Properly handle errors like:
    # bad user/ bad password
    # invalid return from server
    # Pass the errors back up to caller
    querystring = {"grant_type": "password", "username": username, "password": password, "": ["", ""]}
    headers = {'authorization': 'Basic YmdwLWNsaWVudC1uYW1lOmJncC1jbGllbnQtcHc='}
    return requests.post(LOBBYURL + "/oauth/token", headers=headers, params=querystring)


# TODO: Fix this hack. Do not call function in default
# Potential return: User already exists, then we can raise that message back to the signup screen
def signup_user(name, password, admin_token=None):
    if admin_token is None:
        admin_token = get_user_access_token("admin", "admin").json()['access_token']
    querystring = {"access_token": admin_token}
    payload = {
        "name": name,
        "password": password,
        "preferredColour": "01FFFF",
        "role": "ROLE_PLAYER"
    }
    headers = {'content-type': 'application/json'}
    return requests.put(f"{LOBBYURL}/api/users/{name}", json=payload, headers=headers, params=querystring)
