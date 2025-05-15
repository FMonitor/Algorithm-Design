import copy
import random

def generate_random_graph(n, m):
    """生成含 n 个节点、m 条边的无向图（邻接表表示）"""
    if m > n * (n - 1) // 2:
        raise ValueError("边数超过了完全图的最大边数")
    
    adjacency = {i: [] for i in range(1, n + 1)}
    edges = set()
    
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            adjacency[u].append(v)
            adjacency[v].append(u)
    
    print(f"生成的图包含 {n} 个节点")
    print(f"生成的图包含 {m} 条边")
    return adjacency

def read_col_file(path):
    """读取 .col 文件并返回邻接表"""
    adjacency = {}
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('e '):
                _, u, v = line.strip().split()
                u, v = int(u), int(v)
                if u not in adjacency:
                    adjacency[u] = []
                if v not in adjacency:
                    adjacency[v] = []
                adjacency[u].append(v)
                adjacency[v].append(u)
    return adjacency


def deep_copy_adjacency(adj):
    return copy.deepcopy(adj)

def get_node(colors):
    """返回所有节点初始的颜色域（颜色列表）"""
    return list(range(colors))

def init_nodes(adjacency, colors):
    """初始化每个节点的颜色域为全部颜色"""
    return {node: get_node(colors) for node in adjacency}

def is_consistent(node, color, assignment, adjacency):
    """检查当前颜色分配是否与已分配的颜色一致（即相邻节点是否有相同颜色）"""
    for neighbor in adjacency[node]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

# 点选择策略
# 1. 按照顺序选择未赋值的节点
def select_unassigned_node_v1(nodes, assignment):
    for node in nodes:
        if node not in assignment:
            return node
    return None

# 2. 最小剩余值（MRV）选择未赋值的节点
def select_unassigned_node_mrv_v2(nodes, assignment):
    unassigned = [node for node in nodes if node not in assignment]
    return min(unassigned, key=lambda node: len(nodes[node]), default=None)

# 3. 最大度数选择未赋值的节点
def select_unassigned_node_degree_v3(adjacency, assignment):
    unassigned = [node for node in adjacency if node not in assignment]
    return max(unassigned, key=lambda node: len(adjacency[node]), default=None)

# 4. 最小剩余值（MRV）+ 最大度数选择未赋值的节点
def select_unassigned_node_mrv_degree_v4(nodes, adjacency, assignment):
    unassigned = [node for node in nodes if node not in assignment]
    if not unassigned:
        return None
    min_remaining = min(len(nodes[node]) for node in unassigned)
    candidates = [n for n in unassigned if len(nodes[n]) == min_remaining]
    return max(candidates, key=lambda node: len(adjacency[node]))

# 颜色选择策略
# 1. 按照顺序选择颜色
def select_color_c1(node, nodes):
    return nodes[node]

# 2. 按照冲突数选择颜色
def select_color_c2(node, nodes, adjacency, assignment):
    def count_conflicts(value):
        return sum(value in nodes[neighbor] for neighbor in adjacency[node] if neighbor not in assignment)
    return sorted(nodes[node], key=count_conflicts)

# 剪枝策略
# 1. 不剪枝
def no_prune_p1(*args, **kwargs):
    return True

# 2. 前向检查剪枝
def forward_checking_p2(adjacency, var, assignment, new_nodes):
    removed = {}

    for neighbor in adjacency[var]:
        if neighbor not in assignment:
            color = assignment[var]
            if color in new_nodes[neighbor]:
                new_nodes[neighbor].remove(color)
                removed.setdefault(neighbor, []).append(color)

            if not new_nodes[neighbor]:  # 冲突剪枝
                for n, colors in removed.items():
                    new_nodes[n].extend(colors)
                return False
    return True


def print_assignment(assignment):
    for node in sorted(assignment.keys()):
        print(f"节点 {node} -> 颜色 {assignment[node]}")