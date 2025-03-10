import subprocess
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys

os.chdir(sys.path[0])

cpp_program = "./Algorithms.exe"

algorithms = ["selection", "bubble", "insertion", "merge", "quick"]

size = 10000000
test_times = 1

def run_benchmark(algorithm, size):
    start_time = time.time()
    subprocess.run([cpp_program, algorithm, str(size)], check=True)
    end_time = time.time()
    return end_time - start_time

results = []
for i in range(len(algorithms)):
    results.append(0)

for alg in algorithms:
    i = algorithms.index(alg)
    for j in range(test_times):
        print(f"running {alg} sort {j + 1} times")
        time_taken = run_benchmark(alg, size)
        results[i] += time_taken
        

for i in range(len(algorithms)):
    results[i] /= test_times
    print(f"{algorithms[i]} sort with size {size}: {results[i]:.4f} seconds")

with open("benchmarkResult20avg.txt", "w") as f:
    for i in range(len(algorithms)):
        f.write(f"{algorithms[i]}: {results[i]}\n")

# 获取log后的时间
results = np.log(results)

plt.figure(figsize=(10, 6))
plt.bar(algorithms, results)
plt.xlabel("Sorting Algorithm")
plt.ylabel("Time (seconds)")
plt.title("Sorting Algorithm Performance")
plt.grid()
plt.savefig("benchmarkResult20avg.png")
plt.show()
