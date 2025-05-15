from utils import (
    init_nodes,
    select_unassigned_node_v1,
    select_unassigned_node_mrv_v2,
    select_unassigned_node_degree_v3,
    select_unassigned_node_mrv_degree_v4,
    select_color_c1,
    select_color_c2,
    no_prune_p1,
    forward_checking_p2,
    print_assignment,
    is_consistent
)
import copy

def coloring_v1_c1_p1(adjacency, colors):
    # 初始化节点和颜色域
    nodes = init_nodes(adjacency, colors)

    cnt = 0

    def backtrack(assignment):
        # nonlocal  cnt
        # cnt+=1
        # if cnt % 1000000 == 0:
        #     print(f"当前搜索次数：{cnt}")
        """递归回溯搜索函数"""
        # 如果所有节点都已赋值，说明找到了解
        if len(assignment) == len(nodes):
            return assignment.copy()

        # 点选择策略 v1：按顺序选择一个未赋值节点
        node = select_unassigned_node_v1(nodes.keys(), assignment)

        # 颜色选择策略 c1：按顺序尝试该节点的所有可能颜色
        for color in select_color_c1(node, nodes):
            # 检查一致性（相当于约束检查）
            if is_consistent(node, color, assignment, adjacency):
                # 尝试赋值
                assignment[node] = color

                # 剪枝策略 p1：不做任何剪枝，直接继续搜索
                result = backtrack(assignment)
                if result is not None:
                    return result

                # 回溯：撤销赋值
                del assignment[node]

        # 所有颜色都不行，返回失败
        return None
    

    
    return backtrack({})

def coloring_v1_c1_p2(adjacency, max_colors):
    nodes = init_nodes(adjacency, max_colors)
    cnt = 0
    new_nodes = copy.deepcopy(nodes)

    def backtrack(assignment):
        # nonlocal  cnt
        # cnt+=1
        # if cnt % 1000000 == 0:
        #     print(f"当前搜索次数：{cnt}")
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_v1(nodes.keys(), assignment)

        for color in select_color_c1(var, new_nodes):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color

                copied_new_nodes = copy.deepcopy(new_nodes)
                copied_new_nodes[var] = [color]

                if forward_checking_p2(adjacency, var, assignment, copied_new_nodes):
                    result = backtrack(assignment)
                    if result:
                        return result

                del assignment[var]
                new_nodes.update(copied_new_nodes)

        return None

    
    return backtrack({})

def coloring_v1_c2_p1(adjacency, max_colors):
    nodes = init_nodes(adjacency, max_colors)
    cnt = 0

    def backtrack(assignment):
        # nonlocal  cnt
        # cnt+=1
        # if cnt % 1000000 == 0:
        #     print(f"当前搜索次数：{cnt}")
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_v1(nodes.keys(), assignment)

        for color in select_color_c2(var, nodes, adjacency, assignment):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[var]

        return None

    
    return backtrack({})

def coloring_v1_c2_p2(adjacency, max_colors):
    """
    使用 v1-c2-p2 策略的地图填色算法：
    - v1: 按顺序选择变量（未赋值节点）
    - c2: 选择冲突最少的颜色
    - p2: 前向检查剪枝
    """

    nodes = init_nodes(adjacency, max_colors) 
    cnt = 0
    new_domains = copy.deepcopy(nodes)  # 每个节点当前可用的颜色域

    def backtrack(assignment):
        nonlocal  cnt
        cnt+=1
        # if cnt % 1000000 == 0:
        #     print(f"当前搜索次数：{cnt}")
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_v1(nodes.keys(), assignment)

        for color in select_color_c2(var, new_domains, adjacency, assignment):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color

                copied_domains = copy.deepcopy(new_domains)
                copied_domains[var] = [color]

                if forward_checking_p2(adjacency, var, assignment, copied_domains):
                    new_domains.update(copied_domains)
                    result = backtrack(assignment)
                    if result:
                        return result

                # 回溯撤销赋值和域更新
                del assignment[var]
                new_domains.update(copy.deepcopy(nodes))  # 恢复初始 domains

        return None

    return backtrack({})

def coloring_v2_c1_p1(adjacency, max_colors):

    nodes = init_nodes(adjacency, max_colors)
    cnt = 0

    def backtrack(assignment):
        # nonlocal  cnt
        # cnt+=1
        # if cnt % 1000000 == 0:
        #     print(f"当前搜索次数：{cnt}")
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_mrv_v2(nodes, assignment)

        for color in select_color_c1(var, nodes):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[var]

        return None

    return backtrack({})

import copy

def coloring_v2_c1_p2(adjacency, max_colors):

    nodes = init_nodes(adjacency, max_colors) 
    cnt = 0
    new_domains = copy.deepcopy(nodes)  # 每个节点当前可用的颜色域

    def backtrack(assignment):
        # nonlocal  cnt
        # cnt+=1
        # if cnt % 1000000 == 0:
        #     print(f"当前搜索次数：{cnt}")
        if len(assignment) == len(nodes):
            return assignment.copy()  # 找到解
        
        var = select_unassigned_node_mrv_v2(new_domains, assignment)
        if var is None:
            return None  # 如果没有未赋值节点且未满足终止条件，则失败

        for color in new_domains[var]:
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color

                copied_domains = copy.deepcopy(new_domains)
                copied_domains[var] = [color]

                # p2: 前向检查剪枝
                if forward_checking_p2(adjacency, var, assignment, copied_domains):
                    new_domains.update(copied_domains)

                    result = backtrack(assignment)
                    if result:
                        return result

                # 回溯撤销赋值和域更新
                del assignment[var]
                new_domains.clear()
                new_domains.update(copy.deepcopy(nodes))

        return None

    return backtrack({})

def coloring_v2_c2_p1(adjacency, max_colors):
    nodes = init_nodes(adjacency, max_colors)

    def backtrack(assignment):
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_mrv_v2(nodes, assignment)
        if var is None:
            return None

        for color in select_color_c2(var, nodes, adjacency, assignment):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[var]

        return None

    return backtrack({})


def coloring_v2_c2_p2(adjacency, max_colors):
    import copy

    nodes = init_nodes(adjacency, max_colors)
    new_domains = copy.deepcopy(nodes)

    def backtrack(assignment):
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_mrv_v2(new_domains, assignment)
        if var is None:
            return None

        for color in select_color_c2(var, new_domains, adjacency, assignment):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color

                copied_domains = copy.deepcopy(new_domains)
                copied_domains[var] = [color]

                if forward_checking_p2(adjacency, var, assignment, copied_domains):
                    new_domains.update(copied_domains)
                    result = backtrack(assignment)
                    if result:
                        return result

                del assignment[var]
                new_domains.clear()
                new_domains.update(copy.deepcopy(nodes))

        return None

    return backtrack({})

def coloring_v3_c1_p1(adjacency, max_colors):
    """
    使用 v3-c1-p1 策略的地图填色算法：
    - v3: 最大度数启发式选择变量
    - c1: 按顺序选择颜色
    - p1: 不剪枝
    """
    from utils import init_nodes, is_consistent, select_color_c1

    nodes = init_nodes(adjacency, max_colors)

    def backtrack(assignment):
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_degree_v3(adjacency, assignment)

        if var is None:
            return None

        for color in select_color_c1(var, nodes):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[var]  # 回溯

        return None

    return backtrack({})

def coloring_v3_c1_p2(adjacency, max_colors):
    from utils import init_nodes, is_consistent, forward_checking_p2, select_color_c1
    import copy

    nodes = init_nodes(adjacency, max_colors)
    new_domains = copy.deepcopy(nodes)

    def backtrack(assignment):
        if len(assignment) == len(nodes):
            return assignment.copy()

        var = select_unassigned_node_degree_v3(adjacency, assignment)
        if var is None:
            return None

        for color in select_color_c1(var, new_domains):
            if is_consistent(var, color, assignment, adjacency):
                assignment[var] = color

                copied_domains = copy.deepcopy(new_domains)
                copied_domains[var] = [color]

                if forward_checking_p2(adjacency, var, assignment, copied_domains):
                    new_domains.update(copied_domains)
                    result = backtrack(assignment)
                    if result:
                        return result

                del assignment[var]
                new_domains.clear()
                new_domains.update(copy.deepcopy(nodes))

        return None

    return backtrack({})