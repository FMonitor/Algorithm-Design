import time
import copy
import multiprocessing
from utils import print_assignment, generate_random_graph, read_col_file
from algorithms import (
    coloring_v1_c1_p1, coloring_v1_c1_p2,
    coloring_v1_c2_p1, coloring_v1_c2_p2,
    coloring_v2_c1_p1, coloring_v2_c1_p2,
    coloring_v2_c2_p1, coloring_v2_c2_p2,
    coloring_v3_c1_p1, coloring_v3_c1_p2
    # coloring_v3_c2_p1, coloring_v3_c2_p2,
    # coloring_v4_c1_p1, coloring_v4_c1_p2,
    # coloring_v4_c2_p1, coloring_v4_c2_p2
)

def draw_runtime_barplot(results):
    import matplotlib.pyplot as plt
    import os
    import seaborn as sns

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # 构造数据
    grouped = {}
    for res in results:
        key = os.path.basename(res['graph'])
        grouped.setdefault(key, []).append((res['algorithm'], res['time']))

    for idx, (graph_name, algos) in enumerate(grouped.items()):
        algos.sort()
        names, times = zip(*algos)
        plt.barh(
            [f"{name}" for name in names],
            times,
            label=graph_name
        )

    plt.xlabel("Time (seconds)")
    plt.title("Algorithm Runtime Comparison on le450_5a.col")
    plt.tight_layout()
    plt.savefig("runtime_barplot.png")
    plt.show()


def run_algorithm(queue, algorithm_func, adjacency, max_colors):
    """
    在子进程中运行算法并记录耗时
    """
    start_time = time.time()
    try:
        result = algorithm_func(adjacency, max_colors)
    except Exception as e:
        print(f" ! 算法执行出错: {e}")
        result = None
    elapsed = time.time() - start_time
    queue.put((result, elapsed))


def main():
    # 测试用图路径和对应颜色上限
    test_cases = [
        ('./lab3/map/le450_5a.col', 15)
        # ('./lab3/map/le450_15b.col', 15),
        # ('./lab3/map/le450_25c.col', 25)
    ]
    MAX_TIME = 600  # 单个算法最大运行时间（秒）

    algorithms = {
        # "V1_C1_P1": coloring_v1_c1_p1,
        # "V1_C1_P2": coloring_v1_c1_p2,
        # "V1_C2_P1": coloring_v1_c2_p1,
        # "V1_C2_P2": coloring_v1_c2_p2,
        "V2_C1_P1": coloring_v2_c1_p1,
        "V2_C1_P2": coloring_v2_c1_p2,
        "V2_C2_P1": coloring_v2_c2_p1,
        "V2_C2_P2": coloring_v2_c2_p2,
        "V3_C1_P1": coloring_v3_c1_p1,
        "V3_C1_P2": coloring_v3_c1_p2
        # "V3_C2_P1": coloring_v3_c2_p1,
        # "V3_C2_P2": coloring_v3_c2_p2,
        # "V4_C1_P1": coloring_v4_c1_p1,
        # "V4_C1_P2": coloring_v4_c1_p2,
        # "V4_C2_P1": coloring_v4_c2_p1,
        # "V4_C2_P2": coloring_v4_c2_p2
    }

    total_tasks = len(test_cases) * len(algorithms)
    completed = 0

    results = []

    print("🚀 开始地图填色问题测试 🚀\n")

    for file_path, max_colors in test_cases:
        print(f"\n正在处理图文件：{file_path}")
        print(f"最大可用颜色数：{max_colors}")

        try:
            original_adjacency = read_col_file(file_path)
            # n = 450
            # original_adjacency = generate_random_graph(n, 10*n)
            num_nodes = len(original_adjacency)
            print(f" 图中包含 {num_nodes} 个节点")
        except Exception as e:
            print(f"文件读取失败：{file_path}，错误：{e}")
            continue

        for name, algorithm in algorithms.items():
            completed += 1
            print(f"[{completed}/{total_tasks}] 正在运行算法：{name}")

            # 每次都复制一份干净的图
            copied_adjacency = copy.deepcopy(original_adjacency)
            # 小规模测试用图
            # copied_adjacency = {
            #     1: [2, 3, 4, 5],
            #     2: [1, 4, 5],
            #     3: [1, 5, 6, 8],
            #     4: [1, 2, 5],
            #     5: [1, 2, 3, 4, 6, 7],
            #     6: [3, 5, 7, 8, 9],
            #     7: [5, 6, 9],
            #     8: [3, 6, 9],
            #     9: [6, 7, 8]
            # }

            queue = multiprocessing.Queue()
            p = multiprocessing.Process(
                target=run_algorithm,
                args=(queue, algorithm, copied_adjacency, max_colors)
            )
            p.start()
            p.join(timeout=MAX_TIME)

            if p.is_alive():
                print(f"超时终止，超过 {MAX_TIME}s")
                p.terminate()
                p.join()
                result, elapsed = None, MAX_TIME
                success_str = "失败"
            else:
                try:
                    result, elapsed = queue.get_nowait()
                except Exception as e:
                    print(f"队列获取失败：{e}")
                    result, elapsed = None, MAX_TIME
                success_str = "成功" if result is not None else "失败"

            # 记录结果
            results.append({
                'graph': file_path,
                'algorithm': name,
                'success': success_str,
                'time': round(elapsed, 4)
            })

            print(f"耗时：{round(elapsed, 2)}s | 结果：{success_str}")

    # 输出汇总结果
    print("\n实验结果汇总：")
    print(f"{'图':<25} {'算法':<15} {'结果':<10} {'耗时(s)':<10}")
    print("-" * 60)
    for res in results:
        print(
            f"{res['graph']:<25} {res['algorithm']:<15} {res['success']:<10} {res['time']:<10}")

    # 绘图：运行时间对比
    draw_runtime_barplot(results)


if __name__ == '__main__':
    main()


