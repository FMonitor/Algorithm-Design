import numpy as np
import os
import time
import subprocess
import sys
import matplotlib.pyplot as plt

os.chdir(sys.path[0])

def On2(n, n_base, T_base):
    # 缩放因子使用相对规模的平方比例
    scale = (n / n_base) ** 2
    # 计算理论时间：T_base * (n / n_base)^2
    return T_base * scale 

def Onlogn(n, n_base, T_base):
    # 缩放因子使用相对规模的 n log n 比例
    scale = (n * np.log2(n)) / (n_base * np.log2(n_base))
    # 计算理论时间：T_base * (n * log(n)) / (n_base * log(n_base))
    return T_base * scale 


cpp_program = "./Algorithms.exe"

algorithms_n2 = ["selection", "bubble", "insertion"]
algorithms_nln = ["merge", "quick"]

sizes_n2 = [10000,20000,30000,40000,50000,60000,70000,80000]
sizes_nln = [1000000,2000000,3000000,4000000,5000000,6000000,7000000,8000000,9000000,10000000]

time_limit = 120
def run_benchmark(algorithm, size):
    try:
        start_time = time.time()
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

# 运行 benchmark
results_n2 = {alg: [] for alg in algorithms_n2}
for size in sizes_n2:
    for alg in algorithms_n2:
        time_taken = run_benchmark(alg, size)
        results_n2[alg].append(time_taken)

results_nln = {alg: [] for alg in algorithms_nln}
for size in sizes_nln:
    for alg in algorithms_nln:
        time_taken = run_benchmark(alg, size)
        results_nln[alg].append(time_taken)

for alg in algorithms_n2:
    pivot = 2
    n_base_n2 = sizes_n2[pivot]  
    T_base_n2 = results_n2[alg][pivot]  # 基准点的实际时间
    # 计算每个数据点的理论时间
    theoretical_values_n2 = [On2(n, n_base_n2, T_base_n2) for n in sizes_n2]
    
    plt.figure(figsize=(10, 6))
    plt.title(f"{alg.capitalize()} Sort: Theoretical vs. Actual", fontsize=20)
    plt.plot(sizes_n2, theoretical_values_n2, label="Theoretical", color="red", linestyle="--")
    plt.plot(sizes_n2, results_n2[alg], label="Actual", color="blue")
    plt.xlabel("Input Size", fontsize=16)
    plt.ylabel("Time (s)", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(f"theoretical_vs_actual_{alg}.png")
    plt.show()

# 画 O(n log n) 复杂度的算法
for alg in algorithms_nln:
    pivot_nln = 2
    n_base_nln = sizes_nln[pivot_nln]
    mid_idx_nln = sizes_nln.index(n_base_nln)  # 找到基准点的位置
    T_base_nln = results_nln[alg][mid_idx_nln]  # 基准点的实际时间
    # 计算每个数据点的理论时间
    theoretical_values_nln = [Onlogn(n, n_base_nln, T_base_nln) for n in sizes_nln]
    
    plt.figure(figsize=(10, 6))
    plt.title(f"{alg.capitalize()} Sort: Theoretical vs. Actual", fontsize=20)
    plt.plot(sizes_nln, theoretical_values_nln, label="Theoretical", color="red", linestyle="--")
    plt.plot(sizes_nln, results_nln[alg], label="Actual", color="blue")
    plt.xlabel("Input Size", fontsize=16)
    plt.ylabel("Time (s)", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(f"theoretical_vs_actual_{alg}.png")
    plt.show()