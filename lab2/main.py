import benchmark
import visualization


def main(mode: str = "visualize", num_points: list = [20], repeat: int = 5) -> None:
    """"
    主函数，解析命令行参数并根据模式运行相应的功能。"
    """
    if mode == "benchmark":
        benchmark.run(num_points, repeat)
    elif mode == "visualize":
        visualization.run()


# 参数设置
if __name__ == "__main__":
    mode = "benchmark"
    # mode = "visualize"
    repeat = 5
    num_points = [1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 12000, 14000, 16000, 18000, 20000, 30000, 40000, 50000, 60000, 75000, 100000, 150000,
                  200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1200000, 1400000, 1600000, 1800000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000]
    main(mode, num_points, repeat)
