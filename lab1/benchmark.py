import subprocess
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys

os.chdir(sys.path[0])

cpp_program = "./Algorithms"

algorithms = ["selection", "bubble", "insertion", "merge", "quick"]

sizes = [100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,5000000,6000000,7000000,8000000,9000000,10000000,15000000,20000000,25000000,30000000,35000000,40000000,45000000,50000000,55000000,60000000,65000000,70000000,75000000,80000000,85000000,90000000,95000000,100000000]

# 时间上限（秒）
time_limit = 120

def run_benchmark(algorithm, size):
    try:
        start_time = time.time()
        # 使用 subprocess.run 的 timeout 参数
        result = subprocess.run(
            [cpp_program, algorithm, str(size)],
            timeout=time_limit,
            check=True,
            capture_output=True,
            text=True
        )
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"{algorithm} sort with size {size}: {time_taken:.4f} seconds")
        return time_taken
    except subprocess.TimeoutExpired:
        print(f"{algorithm} sort with size {size}: Exceeded time limit of {time_limit} seconds")
        return time_limit

# 读取保存的数据，如果存在的话跳过已有的数据
read_txt = []
if os.path.exists("benchmarkResult.txt"):
    with open("benchmarkResult.txt", "r") as f:
        read_txt = f.readlines()



results = {alg: [] for alg in algorithms}
for size in sizes:
    for alg in algorithms:
        # 如果已有数据则跳过
        find = False
        for i in range(len(read_txt)):
            if f"{alg}:\n" in read_txt[i]:
                for j in range(len(sizes)):
                    if f"{size} " in read_txt[i + j + 1]:
                        results[alg].append(float(read_txt[i + j + 1].split()[1]))
                        find = True
                        break
        
        if find:
            continue
        time_taken = run_benchmark(alg, size)
        results[alg].append(time_taken)

# 保存数据
with open("benchmarkResult.txt", "w") as f:
    for alg in algorithms:
        f.write(f"{alg}:\n")
        for i in range(len(sizes)):
            f.write(f"{sizes[i]} {results[alg][i]}\n")
        f.write("\n")   

# 对数处理size
sizes = np.log(sizes)  

plt.figure(figsize=(10, 6))
for alg in algorithms:
    plt.plot(sizes, results[alg], label=alg)

plt.xlabel("Array Size(log n)", fontsize=16)
plt.ylabel("Time (seconds)", fontsize=16)
plt.title("Sorting Algorithm Performance", fontsize=20)
plt.legend(fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()


# 保存图像为png文件
plt.savefig("benchmarkResult.png")
plt.show()
