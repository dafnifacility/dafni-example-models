import os
import logging
import platform
import torch
import time
import numpy as np
import matplotlib.pyplot as plt

# Set up logging to /data/outputs/run.log
log_path = "/data/outputs/run.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


# Log system information
def log_system_info():
    logging.info(f"Platform: {platform.platform()}")
    logging.info(f"CPU count: {os.cpu_count()}")
    logging.info(f"PyTorch version: {torch.__version__}")
    logging.info(f"CUDA available: {torch.cuda.is_available()}")
    logging.info(f"CUDA version: {torch.version.cuda}")
    if torch.cuda.is_available():
        logging.info(f"CUDA device count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            logging.info(f"CUDA device {i} name: {torch.cuda.get_device_name(i)}")


log_system_info()

INPUT_PATH = ""
OUTPUT_PATH = ""

# Pre-amble to setup folders
isDAFNI = os.environ.get("ISDAFNI")
logging.info(f"ISDAFNI Environment variable = {isDAFNI} {type(isDAFNI)}")
if isDAFNI == "True":
    if os.name == "nt":
        pren = os.environ.get("HOMEDRIVE")
    else:
        pren = "/"
    INPUT_PATH = os.path.join(pren, "data", "inputs")
    OUTPUT_PATH = os.path.join(pren, "data", "outputs")
    logging.info(f"Running within DAFNI: {OUTPUT_PATH}")
else:
    logging.info("Not running within DAFNI, using run directory")
    OUTPUT_PATH = "/data/outputs"

# Ensure output directory exists
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
logging.info(f"Output directory: {OUTPUT_PATH}")

# Check PyTorch version and available devices
logging.info(f"PyTorch version: {torch.__version__}")
logging.info(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    logging.info(f"CUDA device count: {torch.cuda.device_count()}")
    logging.info(f"CUDA device name: {torch.cuda.get_device_name(0)}")

# Set matrix sizes
sizes = [50, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

# CPU benchmarks
cpu_times = []
for size in sizes:
    start = time.time()
    # Create random matrices
    a = torch.randn(size, size, device="cpu")
    b = torch.randn(size, size, device="cpu")

    # Matrix multiplication
    c = torch.matmul(a, b)

    # Matrix determinant
    det = torch.det(c)

    # Matrix inverse
    inv = torch.inverse(c)

    # Make sure operations are completed
    if torch.cuda.is_available():
        torch.cuda.synchronize()

    elapsed = time.time() - start
    cpu_times.append(elapsed)
    logging.info(f"CPU: Size={size}, Time={elapsed:.4f}s")

# GPU benchmarks (if available)
gpu_times = []
if torch.cuda.is_available():
    for size in sizes:
        start = time.time()
        a = torch.randn(size, size, device="cuda")
        b = torch.randn(size, size, device="cuda")
        c = torch.matmul(a, b)
        det = torch.det(c)
        inv = torch.inverse(c)
        torch.cuda.synchronize()
        elapsed = time.time() - start
        gpu_times.append(elapsed)
        logging.info(f"GPU: Size={size}, Time={elapsed:.4f}s")

# Plot results
plt.figure()
plt.plot(sizes, cpu_times, label="CPU")
if gpu_times:
    plt.plot(sizes, gpu_times, label="GPU")
plt.xlabel("Matrix Size")
plt.ylabel("Time (s)")
plt.title("Matrix Operations Benchmark")
plt.legend()
plt.savefig(os.path.join(OUTPUT_PATH, "benchmark.png"))
logging.info(f"Benchmark plot saved to {os.path.join(OUTPUT_PATH, 'benchmark.png')}")
