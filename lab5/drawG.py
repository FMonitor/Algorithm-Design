import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import defaultdict

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体

def read_graph_from_file(filename):
    """从文件读取图数据"""
    edges = []
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        m = int(f.readline().strip())
        
        for line in f:
            line = line.strip()
            if line:
                u, v = map(int, line.split())
                edges.append((u, v))
    
    return n, m, edges

def find_bridges_tarjan(n, edges):
    """使用Tarjan算法找桥（用于验证）"""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    bridges = []
    time = [0]  # 使用列表来模拟引用传递
    
    def bridge_util(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph[u]:
            if not visited[v]:
                parent[v] = u
                bridge_util(v)
                
                low[u] = min(low[u], low[v])
                
                # 如果low[v] > disc[u]，则(u,v)是桥
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
    
    # 处理所有连通分量
    for i in range(n):
        if not visited[i]:
            bridge_util(i)
    
    return bridges

def find_spanning_tree_and_cycles(n, edges):
    """找到生成树边和非树边（环边）"""
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    tree_edges = []
    cycle_edges = []
    
    for u, v in edges:
        if union(u, v):
            tree_edges.append((u, v))
        else:
            cycle_edges.append((u, v))
    
    return tree_edges, cycle_edges

def visualize_graph(n, edges, bridges=None, title="Graph Visualization"):
    """可视化图"""
    plt.figure(figsize=(16, 12))
    
    # 创建NetworkX图
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    # 统计重复边
    edge_count = defaultdict(int)
    for u, v in edges:
        # 标准化边的表示（小节点在前）
        edge = (min(u, v), max(u, v))
        edge_count[edge] += 1
    
    # 添加边到图中
    for (u, v), count in edge_count.items():
        G.add_edge(u, v, weight=count)
    
    # 使用spring布局，增加节点间距
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # 绘制所有边（灰色）
    edge_list = list(edge_count.keys())
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, 
                          edge_color='lightgray', width=1, alpha=0.6)
    
    # 绘制桥（红色，粗线）
    if bridges:
        bridge_edges = [(min(u, v), max(u, v)) for u, v in bridges]
        bridge_edges = [e for e in bridge_edges if e in edge_count]
        if bridge_edges:
            nx.draw_networkx_edges(G, pos, edgelist=bridge_edges,
                                 edge_color='red', width=3, alpha=0.8)
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=300, alpha=0.8)
    
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    # 添加边权重标签（显示重复边的数量）
    edge_labels = {}
    for (u, v), count in edge_count.items():
        if count > 1:
            edge_labels[(u, v)] = str(count)
    
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)
    
    plt.title(f"{title}\n节点数: {n}, 边数: {len(edges)}, 桥数: {len(bridges) if bridges else 'Unknown'}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def create_detailed_analysis():
    """创建详细的图分析报告"""
    filename = "./lab5/mediumDG.txt"
    n, m, edges = read_graph_from_file(filename)
    
    print("=== 图的基本信息 ===")
    print(f"节点数: {n}")
    print(f"边数: {m}")
    print(f"实际读取边数: {len(edges)}")
    
    # 统计重复边
    edge_count = defaultdict(int)
    for u, v in edges:
        edge = (min(u, v), max(u, v))
        edge_count[edge] += 1
    
    print(f"唯一边数: {len(edge_count)}")
    
    # 显示重复边
    duplicate_edges = [(edge, count) for edge, count in edge_count.items() if count > 1]
    if duplicate_edges:
        print(f"重复边数: {len(duplicate_edges)}")
        print("重复边列表:")
        for (u, v), count in duplicate_edges[:10]:  # 只显示前10个
            print(f"  ({u}, {v}): {count}次")
        if len(duplicate_edges) > 10:
            print(f"  ... 还有{len(duplicate_edges) - 10}个重复边")
    
    # 自环检查
    self_loops = [(u, v) for u, v in edges if u == v]
    if self_loops:
        print(f"自环数: {len(self_loops)}")
        print("自环列表:", self_loops[:10])
    
    # 找到生成树和环边
    tree_edges, cycle_edges = find_spanning_tree_and_cycles(n, list(edge_count.keys()))
    print(f"\n=== 生成树信息 ===")
    print(f"生成树边数: {len(tree_edges)}")
    print(f"非树边数（环边）: {len(cycle_edges)}")
    
    # 使用Tarjan算法找桥
    bridges = find_bridges_tarjan(n, list(edge_count.keys()))
    print(f"\n=== 桥的信息 ===")
    print(f"桥的数量: {len(bridges)}")
    if bridges:
        print("桥的列表:")
        for u, v in bridges:
            print(f"  ({u}, {v})")
    
    # 连通性分析
    G = nx.Graph()
    G.add_edges_from(edge_count.keys())
    connected_components = list(nx.connected_components(G))
    print(f"\n=== 连通性分析 ===")
    print(f"连通分量数: {len(connected_components)}")
    for i, component in enumerate(connected_components):
        print(f"分量 {i+1}: {len(component)} 个节点")
        if len(component) <= 10:
            print(f"  节点: {sorted(component)}")
    
    return n, edges, bridges, tree_edges, cycle_edges

def main():
    """主函数"""
    # 分析图
    n, edges, bridges, tree_edges, cycle_edges = create_detailed_analysis()
    
    # 可视化
    print("\n正在生成可视化图表...")
    
    # 1. 完整图（包含桥的标记）
    visualize_graph(n, edges, bridges, "完整图（红色边为桥）")
    
    # 2. 只显示生成树
    plt.figure(figsize=(14, 10))
    G_tree = nx.Graph()
    G_tree.add_edges_from(tree_edges)
    pos = nx.spring_layout(G_tree, k=3, iterations=50, seed=42)
    
    nx.draw_networkx_edges(G_tree, pos, edge_color='blue', width=2)
    nx.draw_networkx_nodes(G_tree, pos, node_color='lightgreen', node_size=300)
    nx.draw_networkx_labels(G_tree, pos, font_size=8, font_weight='bold')
    
    # 标记桥
    if bridges:
        bridge_edges_in_tree = [(u, v) for u, v in bridges if (u, v) in tree_edges or (v, u) in tree_edges]
        if bridge_edges_in_tree:
            nx.draw_networkx_edges(G_tree, pos, edgelist=bridge_edges_in_tree,
                                 edge_color='red', width=4, alpha=0.8)
    
    plt.title(f"生成树（红色边为桥）\n树边数: {len(tree_edges)}, 桥数: {len(bridges)}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    # 3. 度数分析
    plt.figure(figsize=(12, 6))
    
    # 计算度数
    degree_count = defaultdict(int)
    for u, v in edges:
        degree_count[u] += 1
        degree_count[v] += 1
    
    degrees = [degree_count[i] for i in range(n)]
    
    plt.subplot(1, 2, 1)
    plt.hist(degrees, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    plt.xlabel('度数')
    plt.ylabel('节点数量')
    plt.title('节点度数分布')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.bar(range(n), degrees, color='lightcoral', alpha=0.7)
    plt.xlabel('节点ID')
    plt.ylabel('度数')
    plt.title('各节点度数')
    plt.xticks(range(0, n, 5))
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()