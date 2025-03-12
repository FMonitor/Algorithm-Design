import numpy as np
import os
import time
import subprocess
import sys
import matplotlib.pyplot as plt

os.chdir(sys.path[0])

def On2(n):
    return n**2/1e9

def Onlogn(n):
    return n*np.log2(n)/1e9

cpp_program = "./Algorithms.exe"

algorithms_n2 = ["selection", "bubble", "insertion"]

algorithms_nln = ["merge", "quick"]

sizes_n2 = [10000,20000,30000,40000,50000,60000,70000,80000]

sizes_nln= [1000000,2000000,3000000,4000000,5000000,6000000,7000000,8000000,9000000,10000000]

# 调用Algorithms.exe中的算法，对比理论时间复杂度
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

# 理论时间复杂度
theoretical_n2 = {
    "Theoretical": [On2(n) for n in sizes_n2],
}

theoretical_nln = {
    "Theoretical": [Onlogn(n) for n in sizes_nln],
}

# 画图,虚线做理论值, 实线是实际
# p1
plt.figure(figsize=(10, 6))
plt.title("Theoretical Efficiency vs. Actual Efficiency",fontsize=20)

plt.plot(sizes_n2, theoretical_n2["Theoretical"], label="Theoretical", color="red", linestyle="--")
plt.plot(sizes_n2, results_n2["selection"],label = "Selection", color="red")
plt.plot(sizes_n2, results_n2["bubble"], label = "Bubble", color="blue")
plt.plot(sizes_n2, results_n2["insertion"], label = "Insert", color="green")
plt.xlabel("Input Size",fontsize=16)
plt.ylabel("Time (s)",fontsize=16)
plt.grid()

plt.legend(fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig("theoreticalEfficiency_n2.png")
plt.show()

# p2

plt.figure(figsize=(10, 6))
plt.title("Theoretical Efficiency vs. Actual Efficiency",fontsize=20)
plt.plot(sizes_nln, theoretical_nln["Theoretical"], label="Theoretical nlogn", color="red",linestyle="--")
plt.plot(sizes_nln, results_nln["merge"], label="Merge", color="green")
plt.plot(sizes_nln, results_nln["quick"], label="Quick", color="blue")

plt.xlabel("Input Size",fontsize=16)
plt.ylabel("Time (s)",fontsize=16)
plt.grid()

plt.legend(fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig("theoreticalEfficiency_nln.png")
plt.show()