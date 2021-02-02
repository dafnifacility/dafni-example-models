import os
import requests
from pathlib import Path

service_account_user = os.getenv("DAFNI_SERVICE_ACCOUNT_USER", "")
service_account_pass = os.getenv("DAFNI_SERVICE_ACCOUNT_PASSWORD", "")
NIMS_url = "https://dafni-nims-api.secure.dafni.rl.ac.uk"
model_definition = Path("./simple-example--fibonacci-model/model_definition.yaml")
image = Path("./simple-example.tar.gz")

print("log in to DAFNI")
login_resp = requests.post(
    "https://login.secure.dafni.rl.ac.uk/login/",
    json={"username": service_account_user, "password": service_account_pass},
    headers={
        "Content-Type": "application/json",
    },
    allow_redirects=False,
)

jwt = f"JWT {login_resp.cookies['__Secure-dafnijwt']}"
print(jwt)

print("validate Model Definition")
validation_headers = {"Authorization": jwt, "Content-Type": "application/yaml"}
with model_definition.open("rb") as md:
    validation_resp = requests.put(
        f"{NIMS_url}/models/definition/validate/",
        headers=validation_headers,
        data=md,
    )
    validation_resp.raise_for_status()
    if not validation_resp.json()["valid"]:
        print(validation_resp.json()["errors"])
        exit

print("Get Urls")
auth_header = {"Authorization": jwt}
urls_resp = requests.post(
    f"{NIMS_url}/models/upload/",
    headers=auth_header,
    json={"image": True, "definition": True},
)
urls = urls_resp.json()["urls"]
model_id = urls_resp.json()["id"]
definition_url = urls["definition"]
image_url = urls["image"]

upload_headers = {"Authorization": jwt, "Content-Type": "multipart/form-data"}
print("Upload model definition")
with model_definition.open("rb") as md:
    definition_upload_resp = requests.put(
        definition_url, headers=upload_headers, data=md
    )
    print(definition_upload_resp.text)
print("Upload image")
with image.open("rb") as im:
    image_upload_resp = requests.put(image_url, headers=upload_headers, data=im)
    print(image_upload_resp.text)

print("Start Model Ingest")
start_ingest_resp = requests.post(
    f"{NIMS_url}/models/upload/{model_id}/ingest/",
    headers=auth_header,
    json={"version_message": "testing python script"},
)
