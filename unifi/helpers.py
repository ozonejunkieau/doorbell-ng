import requests

def get_cookie_and_token(protect_ip, username, password, verify_ssl=False):
    auth_url = f"https://{protect_ip}/api/auth/login"
    auth_request = requests.post(auth_url, data={"username": username, "password": password}, verify=verify_ssl)

    csrf_token = auth_request.headers.get("X-CSRF-Token")
    cookie = auth_request.headers.get("Set-Cookie")

    return cookie, csrf_token

def get_snap_jpeg(camera_ip, username, password, verify_ssl=False):
    auth_url = f"https://{camera_ip}/api/1.1/login"
    snap_url = f"https://{camera_ip}/snap.jpeg"

    with requests.Session() as s:
        auth = s.post(auth_url, json={"username": username, "password": password}, verify=verify_ssl)
        resp = s.get(snap_url)
    
    # Return binary blob as bytes
    return resp.content 