import random
import os
from typing import Set, Tuple, List

def generate_graph(n: int, m: int, ensure_connected: bool = True, 
                  allow_self_loops: bool = False, allow_multiple_edges: bool = False) -> List[Tuple[int, int]]:
    """
    生成图的边列表
    
    Args:
        n: 节点数
        m: 边数
        ensure_connected: 是否确保图连通
        allow_self_loops: 是否允许自环
        allow_multiple_edges: 是否允许重复边
    
    Returns:
        边的列表 [(u, v), ...]
    """
    if not allow_multiple_edges and not allow_self_loops:
        max_edges = n * (n - 1) // 2  # 简单无向图的最大边数
        if m > max_edges:
            raise ValueError(f"对于{n}个节点的简单图，最多只能有{max_edges}条边，但要求{m}条边")
    
    edges = []
    used_edges: Set[Tuple[int, int]] = set()
    
    # 如果需要确保连通，首先生成一个生成树
    if ensure_connected and n > 1:
        # 随机生成一个生成树
        nodes = list(range(n))
        random.shuffle(nodes)
        
        for i in range(1, n):
            # 将当前节点连接到之前的某个节点
            parent = random.randint(0, i - 1)
            u, v = nodes[parent], nodes[i]
            
            # 确保边的顺序一致（小节点在前）
            if u > v:
                u, v = v, u
            
            edges.append((u, v))
            if not allow_multiple_edges:
                used_edges.add((u, v))
    
    # 添加剩余的边
    remaining_edges = m - len(edges)
    attempts = 0
    max_attempts = remaining_edges * 100  # 防止无限循环
    
    while len(edges) < m and attempts < max_attempts:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        # 检查自环
        if not allow_self_loops and u == v:
            attempts += 1
            continue
        
        # 确保边的顺序一致（小节点在前）
        if u > v:
            u, v = v, u
        
        # 检查重复边
        if not allow_multiple_edges and (u, v) in used_edges:
            attempts += 1
            continue
        
        edges.append((u, v))
        if not allow_multiple_edges:
            used_edges.add((u, v))
        
        attempts += 1
    
    if len(edges) < m:
        print(f"警告: 只能生成{len(edges)}条边，而不是要求的{m}条边")
    
    return edges

def save_graph_to_file(filename: str, n: int, edges: List[Tuple[int, int]]):
    """将图保存到文件"""
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        f.write(f"{len(edges)}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

def generate_graph_series(n: int, edge_counts: List[int], output_dir: str = "graphs", 
                         base_filename: str = "graph", **kwargs):
    """
    生成一系列不同边数的图
    
    Args:
        n: 节点数
        edge_counts: 边数列表
        output_dir: 输出目录
        base_filename: 基础文件名
        **kwargs: 传递给generate_graph的其他参数
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    for i, m in enumerate(edge_counts):
        print(f"正在生成第{i+1}/{len(edge_counts)}个图: {n}节点, {m}边...")
        
        # 生成图
        edges = generate_graph(n, m, **kwargs)
        
        # 生成文件名
        filename = f"{base_filename}_n{n}_m{m}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # 保存到文件
        save_graph_to_file(filepath, n, edges)
        
        print(f"已保存到: {filepath}")

def generate_predefined_patterns():
    """生成一些预定义的图模式"""
    
    # 1. 小规模测试图
    print("=== 生成小规模测试图 ===")
    small_n = 20
    small_edges = [10, 15, 20, 25, 30, 40, 50]
    generate_graph_series(small_n, small_edges, "small_graphs", "small_graph")
    
    # 2. 中等规模图
    print("\n=== 生成中等规模图 ===")
    medium_n = 100
    medium_edges = [99, 150, 200, 300, 500, 800, 1000, 1500, 2000]
    generate_graph_series(medium_n, medium_edges, "medium_graphs", "medium_graph")
    
    # 3. 大规模图
    print("\n=== 生成大规模图 ===")
    large_n = 9000
    large_edges = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
    generate_graph_series(large_n, large_edges, "large_graphs", "large_graph")
    
    # 4. 特殊图类型
    print("\n=== 生成特殊图类型 ===")
    
    # 稀疏图
    sparse_n = 500
    sparse_edges = [499, 600, 750, 1000]  # 接近树的稀疏图
    generate_graph_series(sparse_n, sparse_edges, "special_graphs", "sparse_graph")
    
    # 稠密图
    dense_n = 200
    max_edges = dense_n * (dense_n - 1) // 2
    dense_ratios = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
    dense_edges = [int(max_edges * ratio) for ratio in dense_ratios]
    generate_graph_series(dense_n, dense_edges, "special_graphs", "dense_graph")

def interactive_generator():
    """交互式图生成器"""
    print("=== 交互式图生成器 ===")
    
    # 获取基本参数
    n = int(input("请输入节点数: "))
    
    print("\n选择边数设置方式:")
    print("1. 手动输入边数列表")
    print("2. 等差数列")
    print("3. 等比数列")
    print("4. 基于连接密度")
    
    choice = input("请选择 (1-4): ")
    
    edge_counts = []
    
    if choice == "1":
        edge_str = input("请输入边数列表，用逗号分隔 (例: 10,20,30,50): ")
        edge_counts = [int(x.strip()) for x in edge_str.split(',')]
    
    elif choice == "2":
        start = int(input("起始边数: "))
        end = int(input("结束边数: "))
        step = int(input("步长: "))
        edge_counts = list(range(start, end + 1, step))
    
    elif choice == "3":
        start = int(input("起始边数: "))
        ratio = float(input("倍数 (例: 1.5): "))
        count = int(input("生成几个图: "))
        
        current = start
        for _ in range(count):
            edge_counts.append(int(current))
            current *= ratio
    
    elif choice == "4":
        max_edges = n * (n - 1) // 2
        print(f"最大可能边数: {max_edges}")
        
        densities_str = input("请输入密度列表 (0-1之间，用逗号分隔，例: 0.1,0.2,0.5): ")
        densities = [float(x.strip()) for x in densities_str.split(',')]
        edge_counts = [max(n-1, int(max_edges * d)) for d in densities]
    
    # 获取其他选项
    print("\n图的类型选项:")
    ensure_connected = input("确保图连通? (y/n, 默认y): ").lower() != 'n'
    allow_self_loops = input("允许自环? (y/n, 默认n): ").lower() == 'y'
    allow_multiple_edges = input("允许重复边? (y/n, 默认n): ").lower() == 'y'
    
    output_dir = input("输出目录名 (默认: custom_graphs): ").strip()
    if not output_dir:
        output_dir = "custom_graphs"
    
    base_filename = input("基础文件名 (默认: graph): ").strip()
    if not base_filename:
        base_filename = "graph"
    
    print(f"\n将生成以下图:")
    print(f"节点数: {n}")
    print(f"边数列表: {edge_counts}")
    print(f"确保连通: {ensure_connected}")
    print(f"允许自环: {allow_self_loops}")
    print(f"允许重复边: {allow_multiple_edges}")
    
    confirm = input("\n确认生成? (y/n): ").lower()
    if confirm == 'y':
        generate_graph_series(n, edge_counts, output_dir, base_filename,
                            ensure_connected=ensure_connected,
                            allow_self_loops=allow_self_loops,
                            allow_multiple_edges=allow_multiple_edges)
        print("生成完成!")
    else:
        print("已取消生成。")

def main():
    """主函数"""
    print("图生成器")
    print("=========")
    
    while True:
        print("\n请选择:")
        print("1. 生成预定义的图集合")
        print("2. 交互式生成图")
        print("3. 退出")
        
        choice = input("请选择 (1-3): ")
        
        if choice == "1":
            # 设置随机种子以确保可重现性
            random.seed(42)
            generate_predefined_patterns()
            
        elif choice == "2":
            interactive_generator()
            
        elif choice == "3":
            print("再见!")
            break
            
        else:
            print("无效选择，请重新输入。")

if __name__ == "__main__":
    main()