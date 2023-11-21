# Test out Tensorflow GPU calcs vrs CPU
# Adapted from test example in :-
# https://stackoverflow.com/questions/55749899/training-a-simple-model-in-tensorflow-gpu-slower-than-cpu

import os
import time
import tensorflow as tf
from tensorflow.python.client import device_lib
import matplotlib.pyplot as plt

gPATHI = ""
gPATHO = ""
# Pre-amble to setup folders
isDAFNI = os.environ.get("ISDAFNI")
print("ISDAFNI Environment variable = ", isDAFNI, type(isDAFNI))
if isDAFNI == "True":
    if os.name == "nt":
        pren = os.environ.get("HOMEDRIVE")
    else:
        pren = "/"
    gPATHI = os.path.join(pren, "data", "inputs")
    gPATHO = os.path.join(pren, "data", "outputs")
    print("Running within DAFNI: ", gPATHO)
else:
    print("Not running within DAFNI, using run directory")

tf.compat.v1.disable_eager_execution()

local_dev_ps = device_lib.list_local_devices()
for dv in local_dev_ps: print(dv.name)

# Set matrix sizes eg. 50x50, 100x100 etc
sizes = [50, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

cpu_times = []
for size in sizes:
    tf.compat.v1.reset_default_graph()
    with tf.device('cpu:0'):
        start = time.time()
        v1 = tf.Variable(tf.random.normal((size, size)))
        v2 = tf.Variable(tf.random.normal((size, size)))
        op = tf.matmul(v1, v2)
        det = tf.linalg.det(op)
        op2 = tf.linalg.inv(op)
    with tf.compat.v1.Session() as sess: # config=config) as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        sess.run(op)
        sess.run(det)
        sess.run(op2)
    cpu_times.append(time.time() - start)
    print('cpu time took: {0:.4f}'.format(time.time() - start))

try:
    gpu_times = []
    for size in sizes:
        tf.compat.v1.reset_default_graph()
        with tf.device('gpu:0'):
            start = time.time()
            v1 = tf.Variable(tf.random.normal((size, size)))
            v2 = tf.Variable(tf.random.normal((size, size)))
            op = tf.matmul(v1, v2)
            det = tf.linalg.det(op)
            op2 = tf.linalg.inv(op)
        with tf.compat.v1.Session() as sess: #config=config) as sess:
            sess.run(tf.compat.v1.global_variables_initializer())
            sess.run(op)
            sess.run(det)
            sess.run(op2)
        gpu_times.append(time.time() - start)
        print('gpu time took: {0:.4f}'.format(time.time() - start))
except Exception as err:
    # Handle case with no appropriate GPU (or Cuda not installed)
    print("Issue running using GPU(CUDA) :", type(err).__name__, err)
    gpu_times = [0.0] * len(sizes)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(sizes, gpu_times, label='GPU')
ax.plot(sizes, cpu_times, label='CPU')
plt.xlabel('Matrix Size')
plt.ylabel('Calc. Time (sec)')
plt.legend()
plt.savefig(os.path.join(gPATHO, 'times.png'))
