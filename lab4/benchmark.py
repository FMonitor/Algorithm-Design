import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from algorithms import (
    egg_drop_brute_force,
    egg_drop_naive,
    egg_drop_binary,
    egg_drop_optimized,
    egg_drop_optimized_1d
)
import multiprocessing
import math

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体

class TimeComplexityBenchmark:
    def __init__(self, eggs=5, max_runtime=5):
        self.eggs = eggs
        self.max_runtime = max_runtime
        
        # 测试用的楼层数列表（较少的数据点用于基准测试）
        # self.floors_list = [12,13, 14,15, 16,17, 18,19, 20,21, 22,23, 24, 26, 28, 30] # 针对Brute Force
        # self.floors_list =[200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000,3500, 4000, 4500, 5000, 5500, 6000] # 针对Naive DP
        # self.floors_list = [2000, 3000, 4000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 120000, 140000, 160000, 180000, 200000, 250000, 300000, 350000, 400000, 450000, 500000]  # 针对Binary DP
        self.floors_list = [ 100000, 200000, 300000, 500000, 1000000, 1200000, 1500000, 1800000, 2000000, 2200000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 20000000, 30000000]  # 针对Optimized DP
        # self.floors_list = [100000, 1000000, 10000000, 10000000, 100000000, 100000000, 1000000000, 2000000000, 3000000000, 4000000000, 5000000000]  # 针对Optimized DP 1D
        
        # 算法映射
        self.algorithms = {
            # "Brute Force": egg_drop_brute_force,
            # "Naive DP": egg_drop_naive,
            # "Binary DP": egg_drop_binary,
            "Optimized DP": egg_drop_optimized
            # "Optimized DP 1D": egg_drop_optimized_1d
        }
        
        # 理论时间复杂度函数
        self.theoretical_complexity = {
            # "Brute Force": self._brute_force_complexity,
            # "Naive DP": self._naive_dp_complexity,
            # "Binary DP": self._binary_dp_complexity,
            "Optimized DP": self._optimized_dp_complexity
            # "Optimized DP 1D": self._optimized_dp_complexity
        }
    
    def _brute_force_complexity(self, e, f):
        """暴力算法理论复杂度: O(2^f)"""
        return 2 ** min(f, 30)  # 限制指数增长避免数值过大
    
    def _naive_dp_complexity(self, e, f):
        """朴素DP理论复杂度: O(e * f^2)"""
        return e * f * f
    
    def _binary_dp_complexity(self, e, f):
        """二分DP理论复杂度: O(e * f * log(f))"""
        return e * f * math.log2(max(f, 1))
    
    def _optimized_dp_complexity(self, e, f):
        """优化DP理论复杂度: O(e * f)"""
        return e * max(f, 1)

    def target(self, queue, func, args):
        """多进程执行目标函数"""
        try:
            start = time.time()
            func(*args)
            end = time.time()
            queue.put(end - start)
        except Exception as e:
            queue.put(None)
    
    def run_with_timeout(self, func, args, timeout):
        """带超时的算法执行"""
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=self.target, args=(queue, func, args))
        p.start()
        p.join(timeout)

        if p.is_alive():
            p.terminate()
            p.join()
            return None

        return queue.get() if not queue.empty() else None
    
    def measure_actual_time(self, algorithm, floors, runs=3):
        """测量算法实际执行时间"""
        times = []
        for _ in range(runs):
            t = self.run_with_timeout(algorithm, (self.eggs, floors), self.max_runtime)
            if t is not None:
                times.append(t)
        
        return np.mean(times) if times else None
    
    def calibrate_theoretical_time(self, algorithm_name, actual_times):
        if len(actual_times) < 5 or actual_times[4] is None:
            return None
        
        calibration_index = 4
        calibration_floors = self.floors_list[calibration_index]
        actual_calibration_time = actual_times[calibration_index]
        
        # 计算理论复杂度
        theoretical_calibration = self.theoretical_complexity[algorithm_name](
            self.eggs, calibration_floors
        )
        
        # 计算校准系数
        calibration_factor = actual_calibration_time / theoretical_calibration
        
        return calibration_factor
    
    def run_benchmark(self):
        """运行完整的基准测试"""
        results = {}
        
        print(f"开始时间复杂度基准测试 (鸡蛋数: {self.eggs})")
        print("=" * 60)
        
        for algo_name, algo_func in self.algorithms.items():
            print(f"\n测试算法: {algo_name}")
            actual_times = []
            
            # 测量实际执行时间
            for floors in self.floors_list:
                print(f"  测试楼层数: {floors}...", end=" ")
                actual_time = self.measure_actual_time(algo_func, floors)
                actual_times.append(actual_time)
                
                if actual_time is not None:
                    print(f"完成 ({actual_time:.6f}秒)")
                else:
                    print("超时/失败")
            
            # 校准理论时间
            calibration_factor = self.calibrate_theoretical_time(algo_name, actual_times)
            
            # 计算理论时间
            theoretical_times = []
            for floors in self.floors_list:
                if calibration_factor is not None:
                    theoretical_complexity = self.theoretical_complexity[algo_name](
                        self.eggs, floors
                    )
                    theoretical_time = calibration_factor * theoretical_complexity
                    theoretical_times.append(theoretical_time)
                else:
                    theoretical_times.append(None)
            
            results[algo_name] = {
                'actual_times': actual_times,
                'theoretical_times': theoretical_times,
                'calibration_factor': calibration_factor
            }
        
        return results
    
    def create_comparison_table(self, results):
        """创建理论与实际时间对比表"""
        data = []
        
        for floors in self.floors_list:
            row = {'楼层数': floors}
            idx = self.floors_list.index(floors)
            
            for algo_name in self.algorithms.keys():
                actual_time = results[algo_name]['actual_times'][idx]
                theoretical_time = results[algo_name]['theoretical_times'][idx]
                
                if actual_time is not None:
                    row[f'{algo_name}_实际时间'] = f"{actual_time:.6f}"
                else:
                    row[f'{algo_name}_实际时间'] = "超时/失败"
                
                if theoretical_time is not None:
                    row[f'{algo_name}_理论时间'] = f"{theoretical_time:.6f}"
                else:
                    row[f'{algo_name}_理论时间'] = "N/A"
            
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def plot_comparison(self, results):
        """绘制理论与实际时间复杂度对比图"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        colors = {'actual': 'red', 'theoretical': 'blue'}
        
        for i, (algo_name, data) in enumerate(results.items()):
            ax = axes[i]
            
            actual_times = data['actual_times']
            theoretical_times = data['theoretical_times']
            
            # 过滤有效数据
            valid_floors = []
            valid_actual = []
            valid_theoretical = []
            
            for j, floors in enumerate(self.floors_list):
                if (actual_times[j] is not None and 
                    theoretical_times[j] is not None):
                    valid_floors.append(floors)
                    valid_actual.append(actual_times[j])
                    valid_theoretical.append(theoretical_times[j])
            
            if valid_floors:
                # 绘制实际时间
                ax.plot(valid_floors, valid_actual, 
                       color=colors['actual'], marker='o', linewidth=2,
                       label=f'{algo_name} - 实际时间', markersize=6)
                
                # 绘制理论时间
                ax.plot(valid_floors, valid_theoretical, 
                       color=colors['theoretical'], marker='s', linewidth=2,
                       linestyle='--', label=f'{algo_name} - 理论时间', markersize=6)
            
            ax.set_xlabel('楼层数', fontsize=10)
            ax.set_ylabel('执行时间 (秒)', fontsize=10)
            ax.set_title(f'{algo_name} 时间复杂度对比', fontsize=12)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
            # ax.set_xscale('log')
            # ax.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig(f'time_complexity_comparison_{self.eggs}eggs.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_unified_comparison(self, results):
        """绘制所有算法在同一张图上的对比"""
        plt.figure(figsize=(14, 10))
        
        # 定义颜色和标记
        colors = ['red', 'blue', 'green', 'orange']
        markers_actual = ['o', 's', '^', 'D']
        markers_theoretical = ['x', '+', '*', 'v']
        
        algo_names = list(results.keys())
        
        for i, (algo_name, data) in enumerate(results.items()):
            actual_times = data['actual_times']
            theoretical_times = data['theoretical_times']
            
            # 过滤有效数据
            valid_floors = []
            valid_actual = []
            valid_theoretical = []
            
            for j, floors in enumerate(self.floors_list):
                if (actual_times[j] is not None and 
                    theoretical_times[j] is not None):
                    valid_floors.append(floors)
                    valid_actual.append(actual_times[j])
                    valid_theoretical.append(theoretical_times[j])
            
            if valid_floors:
                # 绘制实际时间
                plt.plot(valid_floors, valid_actual, 
                        color=colors[i], marker=markers_actual[i], 
                        linewidth=2, markersize=6,
                        label=f'{algo_name} - 实际')
                
                # 绘制理论时间
                plt.plot(valid_floors, valid_theoretical, 
                        color=colors[i], marker=markers_theoretical[i], 
                        linewidth=2, linestyle='--', markersize=6,
                        label=f'{algo_name} - 理论')
        
        plt.xlabel('楼层数', fontsize=12)
        plt.ylabel('执行时间 (秒)', fontsize=12)
        plt.title(f'扔鸡蛋问题算法时间复杂度对比 (鸡蛋数: {self.eggs})', fontsize=14)
        plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.xscale('log')
        plt.yscale('log')
        
        plt.tight_layout()
        plt.savefig(f'unified_time_complexity_{self.eggs}eggs.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def print_calibration_info(self, results):
        """打印校准信息"""
        print("\n" + "=" * 60)
        print("算法校准信息:")
        print("=" * 60)
        
        for algo_name, data in results.items():
            calibration_factor = data['calibration_factor']
            if calibration_factor is not None:
                print(f"{algo_name}:")
                print(f"  校准系数: {calibration_factor:.2e}")
                print(f"  校准基准: 第3个数据点 (楼层数: {self.floors_list[2]})")
            else:
                print(f"{algo_name}: 校准失败 (数据不足)")

def main():
    # 创建基准测试实例
    benchmark = TimeComplexityBenchmark(eggs=5, max_runtime=10)
    
    # 运行基准测试
    results = benchmark.run_benchmark()
    
    # 打印校准信息
    benchmark.print_calibration_info(results)
    
    # 创建对比表
    comparison_table = benchmark.create_comparison_table(results)
    print("\n" + "=" * 60)
    print("理论与实际时间对比表:")
    print("=" * 60)
    print(comparison_table.to_string(index=False))
    
    # 保存表格到CSV
    comparison_table.to_csv(f'time_complexity_table_{benchmark.eggs}eggs.csv', 
                          index=False, encoding='utf-8-sig')
    print(f"\n对比表已保存到: time_complexity_table_{benchmark.eggs}eggs.csv")
    
    # 绘制对比图
    benchmark.plot_comparison(results)
    # benchmark.plot_unified_comparison(results)

if __name__ == "__main__":
    main()