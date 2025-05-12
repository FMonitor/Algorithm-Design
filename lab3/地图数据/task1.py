import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

adjacency_list = {
    1:[2,3,4,5],
    2:[1,4,5],
    3:[1,5,6,8],
    4:[1,2,5],
    5:[1,2,3,4,6,7],
    6:[3,5,7,8,9],
    7:[5,6,9],
    8:[3,6,9],
    9:[6,7,8]
}

G = nx.Graph()
for node, neighbors in adjacency_list.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

def is_valid(node, color, assignment, graph):
    for neighbor in graph[node]:
        if assignment.get(neighbor) == color:
            return False
    return True

def backtrack_coloring(graph, max_colors, assignment={}, node=1):
    if node == len(graph):
        return assignment
    
    for color in range(max_colors):
        if is_valid(node, color, assignment, graph):
            assignment[node] = color
            result = backtrack_coloring(graph, max_colors, assignment, node + 1)
            if result:
                return result
            del assignment[node]
    
    return None

# 执行回溯法着色（最多使用 4 种颜色）
backtrack_result = backtrack_coloring(adjacency_list, max_colors=4)
backtrack_colors = [backtrack_result[i] for i in range(len(adjacency_list))]
num_colors_backtrack = max(backtrack_colors) + 1

pos = nx.spring_layout(G, seed=42) 
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color=backtrack_colors, cmap=plt.cm.Set3, node_size=800, font_weight='bold')
plt.title(f"回溯法四色着色结果（使用颜色数：{num_colors_backtrack}）")
plt.tight_layout()
plt.show()

