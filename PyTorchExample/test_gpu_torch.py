# Test out PyTorch GPU calculations vs CPU
# Adapted from the TensorFlow example and PyTorch best practices

import os
import time
import torch
import numpy as np
import matplotlib.pyplot as plt

INPUT_PATH = ""
OUTPUT_PATH = ""
# Pre-amble to setup folders
isDAFNI = os.environ.get("ISDAFNI")
print("ISDAFNI Environment variable = ", isDAFNI, type(isDAFNI))
if isDAFNI == "True":
    if os.name == "nt":
        pren = os.environ.get("HOMEDRIVE")
    else:
        pren = "/"
    INPUT_PATH = os.path.join(pren, "data", "inputs")
    OUTPUT_PATH = os.path.join(pren, "data", "outputs")
    print("Running within DAFNI: ", OUTPUT_PATH)
else:
    print("Not running within DAFNI, using run directory")
    OUTPUT_PATH = "/data/outputs"

# Ensure output directory exists
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
print(f"Output directory: {OUTPUT_PATH}")

# Check PyTorch version and available devices
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device count: {torch.cuda.device_count()}")
    print(f"CUDA device name: {torch.cuda.get_device_name(0)}")

# Set matrix sizes
sizes = [50, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

# CPU benchmarks
cpu_times = []
for size in sizes:
    start = time.time()
    # Create random matrices
    a = torch.randn(size, size, device='cpu')
    b = torch.randn(size, size, device='cpu')
    
    # Matrix multiplication
    c = torch.matmul(a, b)
    
    # Matrix determinant
    det = torch.linalg.det(c)
    
    # Matrix inverse
    inv = torch.linalg.inv(c)
    
    # Make sure operations are completed
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    
    cpu_times.append(time.time() - start)
    print(f'CPU time for size {size}: {cpu_times[-1]:.4f} seconds')

# GPU benchmarks
try:
    gpu_times = []
    if torch.cuda.is_available():
        for size in sizes:
            start = time.time()
            # Create random matrices on GPU
            a = torch.randn(size, size, device='cuda')
            b = torch.randn(size, size, device='cuda')
            
            # Matrix multiplication
            c = torch.matmul(a, b)
            
            # Matrix determinant
            det = torch.linalg.det(c)
            
            # Matrix inverse
            inv = torch.linalg.inv(c)
            
            # Make sure GPU operations are completed
            torch.cuda.synchronize()
            
            gpu_times.append(time.time() - start)
            print(f'GPU time for size {size}: {gpu_times[-1]:.4f} seconds')
    else:
        gpu_times = [0.0] * len(sizes)
        print("No GPU available for benchmarking")
except Exception as err:
    # Handle case with no appropriate GPU
    print(f"Issue running using GPU: {type(err).__name__}, {err}")
    gpu_times = [0.0] * len(sizes)

# Plot the results
fig, ax = plt.subplots(figsize=(8, 6))
# Convert to numpy arrays for plotting
sizes_np = np.array(sizes)
gpu_times_np = np.array(gpu_times)
cpu_times_np = np.array(cpu_times)
ax.plot(sizes_np, gpu_times_np, label='GPU')
ax.plot(sizes_np, cpu_times_np, label='CPU')
plt.xlabel('Matrix Size')
plt.ylabel('Calc. Time (sec)')
plt.legend()
plt.savefig(os.path.join(OUTPUT_PATH, 'times.png'))
