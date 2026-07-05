import glob
import logging
import os
import subprocess
import sys

# ------------------ Set input and output directory ------------------ #
pren = os.environ.get("HOMEDRIVE", "") if os.name == "nt" else "/"
inputs_path = os.path.join(pren, "data", "inputs")
outputs_path = os.path.join(pren, "data", "outputs")
os.makedirs(outputs_path, exist_ok=True)

# ------------------ Setup logging to output log file ------------------ # 
LOG_FILE = os.path.join(outputs_path, "download.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ------------------ Debugging info ------------------ #
logger.info("Running within DAFNI — output path: %s", outputs_path)
logger.info("Python version: %s", sys.version)
logger.info("Input  path : %s", inputs_path)
logger.info("Output path : %s", outputs_path)
logger.info("Log file    : %s", LOG_FILE)

# ------------------ Set input args file name ------------------ #
CONFIG_FILENAME = "download_args.json"
config_path = os.path.join(inputs_path, CONFIG_FILENAME)
if not os.path.isfile(config_path):
    logger.error("Config file not found: %s", config_path)
    sys.exit(0) # use exit 0 so the dafni model passes and produces output log, may not prduce log if set to 1
 
logger.info("Using config file: %s", config_path)

# Snapshot output directory before download to detect new files afterwards
files_before = set(glob.glob(os.path.join(outputs_path, "**", "*.nc"), recursive=True))

# ------------------ Run download command and handle any errors ------------------ #
cmd = [
    "dataset-download-tool",
    "--config",
    config_path,
    "--dest", # DO NOT CHANGE OUTPUT PATH WHEN RUNNING ON DAFNI, HERE OR IN CONFIG FILE
    outputs_path, 
    "--log-file",
    LOG_FILE,
]

logger.info("Starting download — command: %s", " ".join(cmd))
try:
    result = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    logger.info("Download completed successfully.")
    if result.stdout:
        logger.info("Tool stdout:\n%s", result.stdout.strip())
    if result.stderr:
        logger.warning("Tool stderr:\n%s", result.stderr.strip())

except FileNotFoundError:
    logger.error("dataset-download-tool not found. Make sure it is installed and on your PATH.")
    sys.exit(0)

except subprocess.CalledProcessError as exc:
    logger.error("dataset-download-tool exited with code %d.", exc.returncode)
    if exc.stdout:
        logger.error("stdout:\n%s", exc.stdout.strip())
    if exc.stderr:
        logger.error("stderr:\n%s", exc.stderr.strip())
    sys.exit(exc.returncode)

# ------------------ Prepare to run nc_reader_example.py ------------------ #
# Detect the newly downloaded .nc file
files_after = set(glob.glob(os.path.join(outputs_path, "**", "*.nc"), recursive=True))
new_files = sorted(files_after - files_before)

# ------------------ Downloaded file checks ------------------ #
if not new_files:
    logger.error("Download reported success but no new .nc file found in: %s", outputs_path)
    sys.exit(1)

if len(new_files) > 1:
    logger.warning("Multiple new .nc files found — using the first: %s", new_files)

nc_file = new_files[0]
logger.info("Detected downloaded file: %s", nc_file)

# ------------------ Locate nc_reader_example.py relative to this script ------------------ #
nc_reader = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nc_reader_example.py")

if not os.path.isfile(nc_reader):
    logger.error("nc_reader_example.py not found at: %s", nc_reader)
    sys.exit(1)

nc_cmd = [sys.executable, nc_reader, nc_file]
logger.info("Running nc_reader — command: %s", " ".join(nc_cmd))

# ------------------ Run script and handle any errors ------------------ #
try:
    nc_result = subprocess.run(
        nc_cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    if nc_result.stdout:
        logger.info("nc_reader output:\n%s", nc_result.stdout.strip())
    if nc_result.stderr:
        logger.warning("nc_reader stderr:\n%s", nc_result.stderr.strip())

except FileNotFoundError:
    logger.error("Python interpreter not found: %s", sys.executable)
    sys.exit(1)

except subprocess.CalledProcessError as exc:
    logger.error("nc_reader.py exited with code %d.", exc.returncode)
    if exc.stdout:
        logger.error("nc_reader stdout:\n%s", exc.stdout.strip())
    if exc.stderr:
        logger.error("nc_reader stderr:\n%s", exc.stderr.strip())
    sys.exit(exc.returncode)