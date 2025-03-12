import subprocess
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys

os.chdir(sys.path[0])

cpp_program = "./Algorithms.exe"

algorithms = ["selection", "bubble", "insertion", "merge", "quick"]

size = 1000000
test_times = 20

def run_benchmark(algorithm, size):
    start_time = time.time()
    subprocess.run([cpp_program, algorithm, str(size)], check=True)
    end_time = time.time()
    return end_time - start_time

results = []
for i in range(len(algorithms)):
    results.append(0)

# 读取保存的数据，如果存在的话跳过已有的数据
read_txt = []
if os.path.exists("benchmarkResult20avg.txt"):
    with open("benchmarkResult20avg.txt", "r") as f:
        read_txt = f.readlines()

for alg in algorithms:
    i = algorithms.index(alg)
    for j in range(test_times):
        print(f"running {alg} sort {j + 1} times")
        # 如果已有数据则跳过
        find = False
        for k in range(len(read_txt)):
            if f"{alg}:" in read_txt[k]:
                results[i] += float(read_txt[k].split(" ")[1])
                find = True
        
        if find:
            continue
        time_taken = run_benchmark(alg, size)
        results[i] += time_taken
        

for i in range(len(algorithms)):
    results[i] /= test_times
    print(f"{algorithms[i]} sort with size {size}: {results[i]:.4f} seconds")

with open("benchmarkResult20avg.txt", "w") as f:
    for i in range(len(algorithms)):
        f.write(f"{algorithms[i]}: {results[i]}\n")

# 获取log后的时间
results = np.log10(results)

plt.figure(figsize=(10, 6))
plt.bar(algorithms, results)
plt.xlabel("Sorting Algorithm",fontsize=16)
plt.ylabel("Time (log10 sec)",fontsize=16)
plt.title("Sorting Algorithm Performance",fontsize=20)
plt.grid()
plt.xticks(fontsize=12) 
plt.yticks(fontsize=12)
plt.savefig("benchmarkResult20avg.png")
plt.show()
