import random
import os

def generate_random_graph(n, m):
    """生成含 n 个节点、m 条边的无向图（邻接表表示），并输出到 map.col 文件"""
    if m > n * (n - 1) // 2:
        raise ValueError("边数超过了完全图的最大边数")
    
    edges = set()
    
    with open("rand_map.col", "w") as f:
        f.write(f"p edge {n} {m}\n") 
        
        while len(edges) < m:
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
                f.write(f"e {u} {v}\n")  # 按 col 格式写入边信息

if __name__ == "__main__":
    n = 120
    m = 3 * n
    generate_random_graph(n, m)
    print(f"生成的图包含 {n} 个节点")
    print(f"生成的图包含 {m} 条边")
