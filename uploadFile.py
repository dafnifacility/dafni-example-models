import os
import requests
import argparse
from pathlib import Path
from dafni_cli.login import login
from dafni_cli.nims import (
    validate_model_definition,
    get_model_upload_urls,
    upload_file_to_minio,
    start_model_ingest,
    start_model_version_ingest,
)


parser = argparse.ArgumentParser(description="Uploading Model to DAFNI")
parser.add_argument(
    "--model-definition", help="The path to the model definition file", required=True
)
parser.add_argument("--image", help="The path to the image file", required=True)
parser.add_argument("--username", help="Your DAFNI username", required=True)
parser.add_argument("--password", help="Your DAFNI password", required=True)
parser.add_argument(
    "--version-message",
    help="A message to help others understand what you changed in this version",
    required=True,
)
parser.add_argument(
    "--parent-model", help="The ID for the parent Model to tie your Model to"
)

args = parser.parse_args()

print("Logging in to DAFNI")
jwt = login(args.username, args.password)
print(jwt)

print("Validate Model definition")
valid, errors = validate_model_definition(jwt, args.model_definition)
if not valid:
    print("Definition validation failed with the following errors:", errors)
    exit

print("Get Urls")
upload_id, urls = get_model_upload_urls(jwt)
definition_url = urls["definition"]
image_url = urls["image"]

print("Upload Model definition")
upload_file_to_minio(jwt, definition_url, args.model_definition)
print("Upload image")
upload_file_to_minio(jwt, image_url, args.image)

print("Start Model ingest")
if args.parent_model == None:
    start_model_ingest(jwt, upload_id, args.version_message)
else:
    start_model_version_ingest(jwt, args.parent_model, upload_id, args.version_message)
