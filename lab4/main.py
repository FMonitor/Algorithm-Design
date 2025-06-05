import time
import concurrent.futures
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
import seaborn as sns
from algorithms import (
    egg_drop_brute_force,
    egg_drop_naive,
    egg_drop_binary,
    egg_drop_optimized
)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体

# ==== 参数设置 ====
# eggs_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # 针对Brute Force, Naive DP, Binary DP
# eggs_list = [1, 3, 5, 10, 15, 20, 25, 50, 75,
#              100, 150, 200, 250, 300, 500]  # 针对Optimized DP

eggs_list = [5] # 单个鸡蛋数量纵向对比

# floors_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]  # 针对Brute Force
# floors_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]  # 针对Naive DP
# floors_list = [100, 500, 1000, 2000, 3000, 4000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000]  # 针对Binary DP
# floors_list = [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 300000, 500000, 1000000, 1200000, 1500000, 1800000, 2000000]  # 针对Optimized DP

# 针对所有算法的通用楼层数量列表
floors_list = [   1,2,3,4,5,6,7,8,9,10,12,15,18, 20, 30, 40, 50, 75, 100, 125, 150, 200, 250, 300, 500, 750, 1000,
               1500, 2000, 2500, 3000, 5000, 10000, 15000, 20000, 25000, 30000, 50000,
               75000, 100000, 150000, 200000, 250000, 300000, 500000, 750000, 1000000,
               1250000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000,7500000,10000000] 

RUNS_PER_ALGO = 3              # 每个组合运行次数
MAX_RUNTIME = 5                # 单次运行最大秒数

# ==== 算法映射 ====
algorithms = {
    "Brute Force": egg_drop_brute_force,
    "Naive DP": egg_drop_naive,
    "Binary DP": egg_drop_binary,
    "Optimized DP": egg_drop_optimized
}


def run_single_test(algo_name, algo_func, e, f):
    avg_time = benchmark_algorithm(algo_func, e, f)
    return (algo_name, e, f, avg_time)


def target(queue, func, args):
    try:
        start = time.time()
        func(*args)
        end = time.time()
        queue.put(end - start)
    except Exception as e:
        queue.put(None)

# ==== 单次运行封装 ====


def run_with_timeout(func, args, timeout):
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=target, args=(queue, func, args))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return None

    return queue.get() if not queue.empty() else None

# ==== 批量测试 ====


def benchmark_algorithm(func, e, f):
    times = []
    for _ in range(RUNS_PER_ALGO):
        t = run_with_timeout(func, (e, f), MAX_RUNTIME)
        if t is not None:
            times.append(t)
        else:
            print(f"超时: {func.__name__}({e}, {f})")
    return np.mean(times) if times else np.nan

# ==== 新增：绘制特定鸡蛋数量下的算法耗时曲线 ====


def plot_algorithm_comparison(results, target_eggs=10):
    """绘制特定鸡蛋数量下四种算法的耗时曲线"""
    if target_eggs not in eggs_list:
        print(f"警告: 鸡蛋数量 {target_eggs} 不在测试列表中")
        return

    plt.figure(figsize=(12, 8))

    colors = ['red', 'blue', 'green', 'orange']
    markers = ['o', 's', '^', 'D']
    linestyles = ['-', '--', '-.', ':']

    algo_data = {}

    # 从结果中提取特定鸡蛋数量的数据
    for algo_name, e, f, avg_time in results:
        if e == target_eggs:
            if algo_name not in algo_data:
                algo_data[algo_name] = {'floors': [], 'times': []}

            # 将 nan 值替换为 MAX_RUNTIME
            time_value = MAX_RUNTIME if np.isnan(avg_time) else avg_time

            algo_data[algo_name]['floors'].append(f)
            algo_data[algo_name]['times'].append(time_value)

    # 对每个算法的数据按楼层数排序
    for algo_name in algo_data:
        floors_times = list(
            zip(algo_data[algo_name]['floors'], algo_data[algo_name]['times']))
        floors_times.sort(key=lambda x: x[0])  # 按楼层数排序

        floors, times = zip(*floors_times)
        algo_data[algo_name]['floors'] = list(floors)
        algo_data[algo_name]['times'] = list(times)

    # 绘制曲线
    for i, (algo_name, data) in enumerate(algo_data.items()):
        if data['floors'] and data['times']:
            plt.plot(data['floors'], data['times'],
                     color=colors[i % len(colors)],
                     marker=markers[i % len(markers)],
                     linestyle=linestyles[i % len(linestyles)],
                     linewidth=2,
                     markersize=6,
                     label=algo_name,
                     alpha=0.8)

    plt.xlabel('楼层数 (floors)', fontsize=12)
    plt.ylabel('执行时间 (秒)', fontsize=12)
    plt.title(f'扔鸡蛋问题算法性能对比 (鸡蛋数: {target_eggs})', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')  # 使用对数坐标轴，因为楼层数变化范围很大

    # 设置坐标轴格式
    from matplotlib.ticker import FuncFormatter

    def format_func(x, p):
        return f'{x:.0f}'

    plt.gca().xaxis.set_major_formatter(FuncFormatter(format_func))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x:.3f}'))

    plt.tight_layout()
    plt.savefig(
        f'algorithm_comparison_{target_eggs}eggs.png', dpi=300, bbox_inches='tight')
    plt.show()

# ==== 主程序 ====


def main():
    tasks = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for algo_name, algo_func in algorithms.items():
            for e in eggs_list:
                for f in floors_list:
                    tasks.append(executor.submit(
                        run_single_test, algo_name, algo_func, e, f))

        # 收集结果
        results = [t.result() for t in concurrent.futures.as_completed(tasks)]

    # 整理结果为：每个算法对应一个 heatmap_data
    algo_heatmaps = {name: np.full(
        (len(eggs_list), len(floors_list)), np.nan) for name in algorithms}

    for algo_name, e, f, avg_time in results:
        i = eggs_list.index(e)
        j = floors_list.index(f)
        algo_heatmaps[algo_name][i, j] = avg_time
        print(f"{algo_name} → {e} eggs, {f} floors: {avg_time:.4f} sec")

    # 可视化热力图
    for algo_name, heatmap_data in algo_heatmaps.items():
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            heatmap_data,
            xticklabels=floors_list,
            yticklabels=eggs_list,
            cmap="YlOrRd",
            annot=True,
            fmt=".2f"
        )
        plt.title(f"运行时间热力图：{algo_name}")
        plt.xlabel("楼层数 (floors)")
        plt.ylabel("鸡蛋数 (eggs)")
        plt.tight_layout()
        plt.savefig(f"heatmap_{algo_name.replace(' ', '_')}.png")
        plt.show()

    # ==== 新增：绘制特定鸡蛋数量下的算法对比图 ====
    plot_algorithm_comparison(results, target_eggs=5)


if __name__ == "__main__":
    main()
