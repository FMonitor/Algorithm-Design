import argparse
import benchmark
import visualization


def main(mode: str = "visualize", num_points: list = [20]) -> None:
    """"
    主函数，解析命令行参数并根据模式运行相应的功能。"
    """
    if mode == "benchmark":
        benchmark.run(num_points)
    elif mode == "visualize":
        visualization.run(num_points)


if __name__ == "__main__":
    # mode = "benchmark"  # 默认模式为基准测试
    mode = "visualize"  # 可视化模式下长度设置无效
    num_points = [10, 100, 1000, 10000, 100000]
    main(mode, num_points)
