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
    plt.title("运行时间对比（点数 vs 时间）",fontsize=16)
    plt.xlabel("点数（log10）", fontsize=14)
    plt.ylabel("平均运行时间（秒）", fontsize=14)
    plt.xscale("log", base=10)

    # 提取并绘图
    for algo, data in results.items():
        x = np.array(sorted(data.keys()))
        y = np.array([data[n] for n in x])
        plt.plot(x, y, marker='o', label=algo.replace("_", " ").title())

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
        "brute_force": force_closest_pair,
        "divide_and_conquer": run_algoritm
    }

    if algorithm_name not in algo_map:
        raise ValueError(f"未知算法: {algorithm_name}")

    total_time = 0
    result = None
    for _ in range(repeat):
        start = time.perf_counter()
        result = algo_map[algorithm_name](points)
        end = time.perf_counter()
        total_time += (end - start)

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
        "divide_and_conquer": {}
    }

    with open("./lab2/logs/benchmark_results.txt", "w") as f:
        f.write(f"{'点数':<6}{'算法':<18}{'多次平均时间（秒）':<11}{'最近距离':<15}\n")
        f.write("-" * 65 + "\n")
        for size in point_sizes:
            points = rand_gen(size, 0, 10000)
            for algo in ["brute_force", "divide_and_conquer"]:
                if size > 10000:
                    repeat = 1
                if algo == "brute_force" and size > 20000:
                    continue

                avg_time, (dist, _) = benchmark(algo, points, repeat=repeat)
                print(f"{size:<8}{algo:<20}{avg_time:<20.6f}{dist:<15.4f}")
                results[algo][size] = avg_time
                f.write(f"{size:<8}{algo:<20}{avg_time:<20.6f}{dist:<15.4f}\n")


    # 绘制结果并保存时间数据到txt
    plot_benchmark_results(results)

    


if __name__ == "__main__":
    run()
