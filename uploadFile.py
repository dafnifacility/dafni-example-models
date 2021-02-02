import os
import requests
import argparse
from pathlib import Path

NIMS_url = "https://dafni-nims-api.secure.dafni.rl.ac.uk"

def login(username: str, password: str) -> str:
    login_resp = requests.post(
        "https://login.secure.dafni.rl.ac.uk/login/",
        json={"username": username, "password": password},
        headers={
            "Content-Type": "application/json",
        },
        allow_redirects=False,
    )
    return f"JWT {login_resp.cookies['__Secure-dafnijwt']}"


def validate_model_definition(
    jwt: str, model_definition: Path
) -> tuple[bool, list[str]]:
    validation_headers = {"Authorization": jwt, "Content-Type": "application/yaml"}
    with model_definition.open("rb") as md:
        validation_resp = requests.put(
            f"{NIMS_url}/models/definition/validate/",
            headers=validation_headers,
            data=md,
        )
        validation_resp.raise_for_status()
        if not validation_resp.json()["valid"]:
            return False, validation_resp.json()["errors"]
    return True, []


def get_model_upload_urls(jwt: str, image: bool = True, definition: bool = True) -> tuple[str, dict]:
    auth_header = {"Authorization": jwt}
    urls_resp = requests.post(
        f"{NIMS_url}/models/upload/",
        headers=auth_header,
        json={"image": True, "definition": True},
    )
    upload_id = urls_resp.json()["id"]
    urls = urls_resp.json()["urls"]
    return upload_id, urls

def upload_file_to_minio(jwt: str, url: str, file_path: Path) -> None:
    upload_headers = {"Authorization": jwt, "Content-Type": "multipart/form-data"}
    with file_path.open("rb") as file_data:
        requests.put(
            url, headers=upload_headers, data=file_data
        )

def start_model_ingest(jwt: str, upload_id: str, version_message: str):
    auth_header = {"Authorization": jwt}
    requests.post(
        f"{NIMS_url}/models/upload/{upload_id}/ingest/",
        headers=auth_header,
        json={"version_message": version_message},
    )

def start_model_version_ingest(jwt: str, model_id: str, upload_id: str, version_message: str):
    auth_header = {"Authorization": jwt}
    requests.post(
        f"{NIMS_url}/models/{model_id}/upload/{upload_id}/ingest/",
        headers=auth_header,
        json={"version_message": version_message},
    )

service_account_user = os.getenv("DAFNI_SERVICE_ACCOUNT_USER", "")
service_account_pass = os.getenv("DAFNI_SERVICE_ACCOUNT_PASSWORD", "")
model_definition = Path("./simple-example--fibonacci-model/model_definition.yaml")
image = Path("./simple-example.tar.gz")

print("log in to DAFNI")
# jwt = login(service_account_user, service_account_pass)
jwt = login("model-uploader", "&9OtXc94@%ThKeVQ")
print(jwt)

print("validate Model Definition")
valid, errors = validate_model_definition(jwt, model_definition)
if not valid: 
    print(errors)
    exit

print("Get Urls")
upload_id, urls = get_model_upload_urls(jwt)
definition_url = urls["definition"]
image_url = urls["image"]

print("Upload model definition")
upload_file_to_minio(jwt, definition_url, model_definition)
print("Upload image")
upload_file_to_minio(jwt, image_url, image)

print("Start Model Ingest")
start_model_version_ingest(jwt, "abdffa58-f0ee-482a-b09f-87d3dc16f31a", upload_id, "Testing new version python script")
