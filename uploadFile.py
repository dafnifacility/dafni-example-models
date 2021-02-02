import os
import requests

service_account_user = os.getenv("DAFNI_SERVICE_ACCOUNT_USER", "")
service_account_pass = os.getenv("DAFNI_SERVICE_ACCOUNT_PASSWORD", "")

print("log in to DAFNI")
login_resp = requests.post(
    "https://login.secure.dafni.rl.ac.uk/login/",
    json={"username": service_account_user, "password": service_account_pass},
)
response.raise_for_status()
print(response.text)
