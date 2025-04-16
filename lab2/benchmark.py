import time
from algorithms.algorithms import force_closest_pair, run_algoritm
from algorithms.rand_gen import rand_gen
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_benchmark_results(results):
    """
    绘制 benchmark 结果图，使用 log10 横轴。
    :param results: 一个字典，包含点数对应的运行时间数据。
    """
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    plt.figure(figsize=(10, 6))
    plt.title("运行时间对比（点数 vs 时间）", fontsize=16)
    plt.xlabel("点数（log10）", fontsize=14)
    plt.ylabel("平均运行时间（秒）", fontsize=14)
    plt.xscale("log", base=10)
    plt.yscale("log")

    for algo, data in results.items():
        x = np.array(sorted(data.keys()))
        y = np.array([data[n] for n in x])
        plt.plot(x, y, marker='o', label=algo.replace("_", " ").title())

        if algo == "divide_and_conquer_optimized" and len(x) >= 3:
            idx = 2  
            c_theory = y[idx] / (x[idx] * np.log2(x[idx]))
            theory_y = c_theory * (x * np.log2(x))
            theory_y = np.where(theory_y <= 120, theory_y, np.nan)  
            mask = theory_y <= 120
            plt.plot(x, theory_y[mask], '--', label="理论时间 O(n log n)")

            
    ref_algo = "brute_force"
    if ref_algo in results and len(results[ref_algo]) >= 3:
        x_ref = np.array(sorted(results[ref_algo].keys()))
        y_ref = np.array([results[ref_algo][n] for n in x_ref])
        idx = 2  # 第三个数据点
        c_brute = y_ref[idx] / (x_ref[idx] ** 2)
        y_theory_brute = c_brute * (x_ref ** 2)
        y_theory_brute = np.where(y_theory_brute <= 120, y_theory_brute, np.nan)
        mask = (y_theory_brute <= 120) & (x_ref <= 40000)
        plt.plot(x_ref[mask], y_theory_brute[mask], linestyle='--', color='gray', label='理论时间 O(n²)')


    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./lab2/logs/benchmark_plot.png", dpi=300)
    plt.show()


def benchmark(algorithm_name: str, points: list, repeat: int = 3):
    """
    对指定算法进行多次运行测试，返回平均耗时与最短距离结果。
    """
    algo_map = {
        "brute_force": "brute",
        "divide_and_conquer": "divide",
        "divide_and_conquer_optimized": "divide_optimized"
    }

    if algorithm_name not in algo_map:
        raise ValueError(f"未知算法: {algorithm_name}")

    total_time = 0
    result = [-1, None]  # 初始化结果为无效值
    timeout = 120
    for _ in range(repeat):
        start = time.perf_counter()
        try:
            result = run_algoritm(points, algo_map[algorithm_name])
        except TimeoutError:
            return timeout, result
        end = time.perf_counter()
        elapsed_time = end - start
        total_time += elapsed_time

        if total_time > timeout:
            return timeout, result

    avg_time = total_time / repeat
    return avg_time, result


def run(point_sizes: list = [10, 100, 500, 1000, 5000, 10000], repeat: int = 5):
    """
    主测试流程，包括绘图。
    """
    print(f"{'点数':<6}{'算法':<18}{'多次平均时间（秒）':<11}{'最近距离':<15}")
    print("-" * 65)

    results = {
        "brute_force": {},
        "divide_and_conquer": {},
        "divide_and_conquer_optimized": {}
    }

    with open("./lab2/logs/benchmark_results.txt", "w") as f:
        f.write(f"{'点数':<6}{'算法':<18}{'多次平均时间（秒）':<11}{'最近距离':<15}\n")
        f.write("-" * 65 + "\n")
        for size in point_sizes:
            points = rand_gen(size, 0, 1000000)
            for algo in ["brute_force", "divide_and_conquer", "divide_and_conquer_optimized"]:
                if size > 10000 and algo == "brute_force" or size > 200000:
                    repeat = 1
                if algo == "brute_force" and size > 40000:
                    results[algo][size] = 120.0000
                    continue

                avg_time, (dist, _) = benchmark(algo, points, repeat=repeat)
                print(f"{size:<8}{algo:<30}{avg_time:<20.6f}{dist:<15.4f}")
                results[algo][size] = avg_time
                f.write(f"{size:<8}{algo:<30}{avg_time:<20.6f}{dist:<15.4f}\n")

    # 绘制结果并保存时间数据到txt
    plot_benchmark_results(results)


if __name__ == "__main__":
    run()