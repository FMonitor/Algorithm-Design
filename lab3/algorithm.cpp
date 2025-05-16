#include "algorithm.h"
#include <chrono>
#include <vector>
#include <unordered_set>
#include <algorithm>
#include <unordered_map>

using namespace std;
using namespace std::chrono;

// 判断当前颜色是否合法
bool isSafe(const vector<vector<int>>& graph, const vector<int>& colors, int node, int color) {
    for (int neighbor : graph[node]) {
        if (colors[neighbor] == color) return false;
    }
    return true;
}




// 普通回溯函数
bool backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    int node,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    // 检查是否超时
    auto now = high_resolution_clock::now();
    if (duration_cast<milliseconds>(now - start_time).count() > time_limit_ms)
        return false;

    // 所有节点都被成功着色
    if (node == graph.size())
        return true;

    for (int c = 1; c <= m; ++c) {
        if (isSafe(graph, colors, node, c)) {
            colors[node] = c;

            if (backtrack(graph, m, colors, node + 1, start_time, time_limit_ms))
                return true;

            // 回溯
            colors[node] = 0;
        }
    }

    return false;
}

// 外部接口：simple_backtrack
bool simple_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    auto start_time = high_resolution_clock::now();
    return backtrack(graph, m, colors, 0, start_time, time_limit_ms);
}

// 计算某颜色在某节点上的冲突数
int countConflicts(const vector<vector<int>>& graph, const vector<int>& colors, int node, int color) {
    int conflicts = 0;
    for (int neighbor : graph[node]) {
        if (colors[neighbor] == color)
            conflicts++;
    }
    return conflicts;
}





// 回溯 + 优先选择冲突最少颜色
bool backtrackMinConflict(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    int node,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    // 检查是否超时
    auto now = high_resolution_clock::now();
    if (duration_cast<milliseconds>(now - start_time).count() > time_limit_ms)
        return false;

    if (node == graph.size())
        return true;

    // 准备颜色列表
    vector<int> color_order(m);
    for (int i = 0; i < m; ++i) color_order[i] = i + 1;

    // 对颜色排序：按冲突数从小到大排序
    sort(color_order.begin(), color_order.end(), [&](int a, int b) {
        return countConflicts(graph, colors, node, a) < countConflicts(graph, colors, node, b);
    });

    // 尝试颜色
    for (int c : color_order) {
        if (isSafe(graph, colors, node, c)) {
            colors[node] = c;

            if (backtrackMinConflict(graph, m, colors, node + 1, start_time, time_limit_ms))
                return true;

            colors[node] = 0; // 回溯
        }
    }

    return false;
}

// 外部接口
bool min_conflict_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    auto start_time = high_resolution_clock::now();
    return backtrackMinConflict(graph, m, colors, 0, start_time, time_limit_ms);
}





// 回溯 + 前向检查
bool backtrackForwardChecking(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    int node,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    // 超时检测
    auto now = high_resolution_clock::now();
    if (duration_cast<milliseconds>(now - start_time).count() > time_limit_ms)
        return false;

    if (node == graph.size())
        return true;

    for (int c : domains[node]) {
        if (isSafe(graph, colors, node, c)) {
            colors[node] = c;

            // 记录前向检查前的邻居可选颜色
            vector<pair<int, int>> removed; // (邻居编号, 被移除颜色)
            bool valid = true;

            for (int neighbor : graph[node]) {
                if (colors[neighbor] == 0 && domains[neighbor].count(c)) {
                    domains[neighbor].erase(c);
                    removed.emplace_back(neighbor, c);

                    if (domains[neighbor].empty()) {
                        valid = false;
                        break;
                    }
                }
            }

            if (valid && backtrackForwardChecking(graph, m, colors, node + 1, domains, start_time, time_limit_ms))
                return true;

            // 回溯：恢复 domains 和颜色
            for (auto& [neighbor, color] : removed)
                domains[neighbor].insert(color);

            colors[node] = 0;
        }
    }

    return false;
}

// 外部接口
bool forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackForwardChecking(graph, m, colors, 0, domains, start_time, time_limit_ms);
}





// 回溯 + 前向检查 + 冲突最少优先
bool backtrackMinConflictFC(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    int node,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    // 超时检测
    auto now = high_resolution_clock::now();
    if (duration_cast<milliseconds>(now - start_time).count() > time_limit_ms)
        return false;

    if (node == graph.size())
        return true;

    // 将当前 domain 中颜色按冲突数从小到大排序
    vector<int> color_order(domains[node].begin(), domains[node].end());
    sort(color_order.begin(), color_order.end(), [&](int a, int b) {
        return countConflicts(graph, colors, node, a) < countConflicts(graph, colors, node, b);
    });

    for (int c : color_order) {
        if (isSafe(graph, colors, node, c)) {
            colors[node] = c;

            // 执行前向检查
            vector<pair<int, int>> removed;
            bool valid = true;

            for (int neighbor : graph[node]) {
                if (colors[neighbor] == 0 && domains[neighbor].count(c)) {
                    domains[neighbor].erase(c);
                    removed.emplace_back(neighbor, c);
                    if (domains[neighbor].empty()) {
                        valid = false;
                        break;
                    }
                }
            }

            if (valid && backtrackMinConflictFC(graph, m, colors, node + 1, domains, start_time, time_limit_ms))
                return true;

            // 回溯
            for (auto& [neighbor, color] : removed)
                domains[neighbor].insert(color);

            colors[node] = 0;
        }
    }

    return false;
}

// 外部接口函数
bool min_conflict_forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackMinConflictFC(graph, m, colors, 0, domains, start_time, time_limit_ms);
}





// 选择剩余颜色数最少（MRV）的变量
int selectMRVNode(const vector<int>& colors, const vector<unordered_set<int>>& domains) {
    int min_domain_size = INT_MAX;
    int selected_node = -1;

    for (int i = 0; i < colors.size(); ++i) {
        if (colors[i] == 0) {
            int domain_size = domains[i].size();
            if (domain_size < min_domain_size) {
                min_domain_size = domain_size;
                selected_node = i;
            }
        }
    }

    return selected_node;
}

// 回溯 + MRV 策略
bool backtrackMRV(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    // 超时检测
    auto now = high_resolution_clock::now();
    if (duration_cast<milliseconds>(now - start_time).count() > time_limit_ms)
        return false;

    // 所有变量已着色
    bool complete = true;
    for (int c : colors) {
        if (c == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    // 使用 MRV 策略选择变量
    int node = selectMRVNode(colors, domains);
    if (node == -1) return false; // 没有合法变量了

    for (int c = 1; c <= m; ++c) {
        if (isSafe(graph, colors, node, c)) {
            colors[node] = c;

            if (backtrackMRV(graph, m, colors, domains, start_time, time_limit_ms))
                return true;

            // 回溯
            colors[node] = 0;
        }
    }

    return false;
}

// 外部接口函数
bool mrv_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackMRV(graph, m, colors, domains, start_time, time_limit_ms);
}





// 获取合法颜色并按冲突数排序（最少冲突优先）
vector<int> getSortedColorsByConflict(
    const vector<vector<int>>& graph,
    const vector<int>& colors,
    int node,
    int m
) {
    // 预计算冲突数
    vector<int> conflicts(m + 1, 0);
    for (int neighbor : graph[node]) {
        if (colors[neighbor] > 0) {
            conflicts[colors[neighbor]]++;
        }
    }
    
    // 创建颜色列表
    vector<int> color_list;
    for (int c = 1; c <= m; ++c) {
        color_list.push_back(c);
    }
    
    // 按冲突数排序
    sort(color_list.begin(), color_list.end(), 
         [&conflicts](int a, int b) {
             return conflicts[a] < conflicts[b];
         });
    
    return color_list;
}

// MRV + 最小冲突排序 回溯
bool backtrackMRVMinConflict(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int c : colors) {
        if (c == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectMRVNode(colors, domains);
    if (node == -1) return false;

    vector<int> sorted_colors = getSortedColorsByConflict(graph, colors, node, m);

    for (int c : sorted_colors) {
        if (isSafe(graph, colors, node, c)) {
            colors[node] = c;

            if (backtrackMRVMinConflict(graph, m, colors, domains, start_time, time_limit_ms))
                return true;

            colors[node] = 0;
        }
    }

    return false;
}

// 外部接口
bool mrv_min_conflict_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVMinConflict(graph, m, colors, domains, start_time, time_limit_ms);
}





// MRV + 前向检查
bool backtrackMRVForwardChecking(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int c : colors) {
        if (c == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectMRVNode(colors, domains);
    if (node == -1) return false;

    // 复制当前域，用于回溯恢复
    vector<unordered_set<int>> original_domains = domains;

    for (int color : domains[node]) {
        if (isSafe(graph, colors, node, color)) {
            colors[node] = color;

            // 更新邻居的可选颜色（前向检查）
            bool forward_ok = true;
            for (int neighbor : graph[node]) {
                if (colors[neighbor] == 0) {
                    domains[neighbor].erase(color);
                    if (domains[neighbor].empty()) {
                        forward_ok = false;
                        break;
                    }
                }
            }

            if (forward_ok) {
                if (backtrackMRVForwardChecking(graph, m, colors, domains, start_time, time_limit_ms))
                    return true;
            }

            // 回溯恢复
            domains = original_domains;
            colors[node] = 0;
        }
    }

    return false;
}

bool mrv_forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVForwardChecking(graph, m, colors, domains, start_time, time_limit_ms);
}






int selectMRVMinConFCNode(
    const vector<int>& colors,
    const vector<unordered_set<int>>& domains
) {
    int min_domain_size = INT_MAX;
    int selected_node = -1;

    for (int i = 0; i < colors.size(); ++i) {
        if (colors[i] == 0 && domains[i].size() < min_domain_size) {
            min_domain_size = domains[i].size();
            selected_node = i;
        }
    }

    return selected_node;
}

bool backtrackMRVMinConflictFC(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int c : colors) {
        if (c == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectMRVMinConFCNode(colors, domains);
    if (node == -1) return false;

    // 生成按冲突数量排序的颜色列表（从少到多）
    vector<pair<int, int>> color_conflicts;  // (conflict_count, color)
    for (int color : domains[node]) {
        int conflicts = 0;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == color)
                conflicts++;
        }
        color_conflicts.emplace_back(conflicts, color);
    }

    sort(color_conflicts.begin(), color_conflicts.end());

    vector<unordered_set<int>> original_domains = domains;

    for (auto [_, color] : color_conflicts) {
        if (isSafe(graph, colors, node, color)) {
            colors[node] = color;

            // Forward checking
            bool forward_ok = true;
            for (int neighbor : graph[node]) {
                if (colors[neighbor] == 0) {
                    domains[neighbor].erase(color);
                    if (domains[neighbor].empty()) {
                        forward_ok = false;
                        break;
                    }
                }
            }

            if (forward_ok) {
                if (backtrackMRVMinConflictFC(graph, m, colors, domains, start_time, time_limit_ms))
                    return true;
            }

            // 回溯
            colors[node] = 0;
            domains = original_domains;
        }
    }

    return false;
}

bool mrv_min_conflict_forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVMinConflictFC(graph, m, colors, domains, start_time, time_limit_ms);
}





int selectDHNode(const vector<vector<int>>& graph, const vector<int>& colors) {
    int max_unassigned_neighbors = -1;
    int selected_node = -1;

    for (int i = 0; i < graph.size(); ++i) {
        if (colors[i] != 0) continue;

        int unassigned_neighbors = 0;
        for (int neighbor : graph[i]) {
            if (colors[neighbor] == 0) {
                ++unassigned_neighbors;
            }
        }

        if (unassigned_neighbors > max_unassigned_neighbors) {
            max_unassigned_neighbors = unassigned_neighbors;
            selected_node = i;
        }
    }

    return selected_node;
}
bool backtrackDH(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    // 检查是否完成
    bool complete = true;
    for (int color : colors) {
        if (color == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectDHNode(graph, colors);
    if (node == -1) return false;

    for (int color = 1; color <= m; ++color) {
        if (isSafe(graph, colors, node, color)) {
            colors[node] = color;

            if (backtrackDH(graph, m, colors, start_time, time_limit_ms))
                return true;

            colors[node] = 0;  // 回溯
        }
    }

    return false;
}
bool dh_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    auto start_time = high_resolution_clock::now();
    return backtrackDH(graph, m, colors, start_time, time_limit_ms);
}





int selectMRVDHFCNode(
    const vector<int>& colors,
    const vector<unordered_set<int>>& domains,
    const vector<vector<int>>& graph
) {
    int min_domain_size = INT_MAX;
    vector<int> candidate_nodes;

    for (int i = 0; i < colors.size(); ++i) {
        if (colors[i] == 0) {
            int domain_size = domains[i].size();
            if (domain_size < min_domain_size) {
                min_domain_size = domain_size;
                candidate_nodes.clear();
                candidate_nodes.push_back(i);
            } else if (domain_size == min_domain_size) {
                candidate_nodes.push_back(i);
            }
        }
    }

    if (candidate_nodes.empty()) return -1;

    // Degree Heuristic: among candidates, pick the one with most uncolored neighbors
    int selected_node = candidate_nodes[0];
    int max_degree = -1;
    for (int node : candidate_nodes) {
        int degree = 0;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == 0) {
                degree++;
            }
        }
        if (degree > max_degree) {
            max_degree = degree;
            selected_node = node;
        }
    }

    return selected_node;
}

bool backtrackMRVDHForwardChecking(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int c : colors) {
        if (c == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectMRVDHFCNode(colors, domains, graph);
    if (node == -1) return false;

    vector<unordered_set<int>> original_domains = domains;

    for (int color : domains[node]) {
        if (isSafe(graph, colors, node, color)) {
            colors[node] = color;

            // 前向检查
            bool forward_ok = true;
            for (int neighbor : graph[node]) {
                if (colors[neighbor] == 0) {
                    domains[neighbor].erase(color);
                    if (domains[neighbor].empty()) {
                        forward_ok = false;
                        break;
                    }
                }
            }

            if (forward_ok) {
                if (backtrackMRVDHForwardChecking(graph, m, colors, domains, start_time, time_limit_ms))
                    return true;
            }

            // 回溯
            domains = original_domains;
            colors[node] = 0;
        }
    }

    return false;
}

bool mrv_dh_forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    vector<unordered_set<int>> domains(graph.size());
    for (int i = 0; i < graph.size(); ++i)
        for (int c = 1; c <= m; ++c)
            domains[i].insert(c);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVDHForwardChecking(graph, m, colors, domains, start_time, time_limit_ms);
}





vector<int> getLeastConflictColors(
    const vector<vector<int>>& graph,
    const vector<int>& colors,
    int node,
    int m
) {
    vector<pair<int, int>> color_conflicts; // {conflict_count, color}
    for (int color = 1; color <= m; ++color) {
        int conflict = 0;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == color) {
                ++conflict;
            }
        }
        color_conflicts.emplace_back(conflict, color);
    }
    sort(color_conflicts.begin(), color_conflicts.end());
    
    vector<int> sorted_colors;
    for (const auto& [_, color] : color_conflicts)
        sorted_colors.push_back(color);
    
    return sorted_colors;
}
bool backtrackDHMinConflict(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    // 检查是否完成
    bool complete = true;
    for (int color : colors) {
        if (color == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    // 使用 DH 选择变量
    int node = selectDHNode(graph, colors);
    if (node == -1) return false;

    // 使用最小冲突顺序选择颜色
    vector<int> color_order = getLeastConflictColors(graph, colors, node, m);
    for (int color : color_order) {
        if (isSafe(graph, colors, node, color)) {
            colors[node] = color;

            if (backtrackDHMinConflict(graph, m, colors, start_time, time_limit_ms))
                return true;

            colors[node] = 0;  // 回溯
        }
    }

    return false;
}
bool dh_min_conflict_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    colors.assign(graph.size(), 0);
    auto start_time = high_resolution_clock::now();
    return backtrackDHMinConflict(graph, m, colors, start_time, time_limit_ms);
}






bool backtrackDHFC(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    // 是否所有节点已着色
    bool complete = true;
    for (int color : colors) {
        if (color == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectDHNode(graph, colors);
    if (node == -1) return false;

    // 使用 domain 中的颜色尝试
    for (int color : domains[node]) {
        if (!isSafe(graph, colors, node, color)) continue;

        colors[node] = color;
        vector<unordered_set<int>> old_domains = domains;

        // 前向检查：更新未赋值邻居的 domains
        bool valid = true;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == 0) {
                domains[neighbor].erase(color);
                if (domains[neighbor].empty()) {
                    valid = false;
                    break;
                }
            }
        }

        if (valid && backtrackDHFC(graph, m, colors, domains, start_time, time_limit_ms))
            return true;

        // 回溯
        colors[node] = 0;
        domains = old_domains;
    }

    return false;
}
bool dh_forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    int n = graph.size();
    colors.assign(n, 0);
    vector<unordered_set<int>> domains(n);
    for (int i = 0; i < n; ++i)
        for (int color = 1; color <= m; ++color)
            domains[i].insert(color);

    auto start_time = high_resolution_clock::now();
    return backtrackDHFC(graph, m, colors, domains, start_time, time_limit_ms);
}






bool backtrackDHMinConflictFC(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    // 判断是否完成
    bool complete = true;
    for (int color : colors) {
        if (color == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectDHNode(graph, colors);
    if (node == -1) return false;

    // 最小冲突颜色排序
    vector<int> color_order = getLeastConflictColors(graph, colors, node, m);

    for (int color : color_order) {
        if (domains[node].count(color) == 0) continue;
        if (!isSafe(graph, colors, node, color)) continue;

        colors[node] = color;
        vector<unordered_set<int>> old_domains = domains;

        // 前向检查：更新邻居的domains
        bool valid = true;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == 0) {
                domains[neighbor].erase(color);
                if (domains[neighbor].empty()) {
                    valid = false;
                    break;
                }
            }
        }

        if (valid && backtrackDHMinConflictFC(graph, m, colors, domains, start_time, time_limit_ms))
            return true;

        colors[node] = 0;
        domains = old_domains;
    }

    return false;
}

bool dh_min_conflict_forward_checking_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    int n = graph.size();
    colors.assign(n, 0);
    vector<unordered_set<int>> domains(n);
    for (int i = 0; i < n; ++i)
        for (int color = 1; color <= m; ++color)
            domains[i].insert(color);

    auto start_time = high_resolution_clock::now();
    return backtrackDHMinConflictFC(graph, m, colors, domains, start_time, time_limit_ms);
}





int selectMRVDHNode(
    const vector<vector<int>>& graph,
    const vector<int>& colors,
    const vector<unordered_set<int>>& domains
) {
    int n = graph.size();
    int min_domain_size = INT_MAX;
    int max_degree = -1;
    int selected = -1;

    for (int i = 0; i < n; ++i) {
        if (colors[i] != 0) continue; // 已着色跳过

        int domain_size = domains[i].size();
        int degree = 0;
        for (int neighbor : graph[i])
            if (colors[neighbor] == 0)
                ++degree;

        if (domain_size < min_domain_size || 
           (domain_size == min_domain_size && degree > max_degree)) {
            min_domain_size = domain_size;
            max_degree = degree;
            selected = i;
        }
    }
    return selected;
}

bool backtrackMRVDH(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int color : colors) {
        if (color == 0) {
            complete = false;
            break;
        }
    }
    if (complete) return true;

    int node = selectMRVDHNode(graph, colors, domains);
    if (node == -1) return false;

    for (int color : domains[node]) {
        if (!isSafe(graph, colors, node, color)) continue;

        colors[node] = color;
        if (backtrackMRVDH(graph, m, colors, domains, start_time, time_limit_ms))
            return true;
        colors[node] = 0;
    }

    return false;
}

bool mrv_dh_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    int n = graph.size();
    colors.assign(n, 0);
    vector<unordered_set<int>> domains(n);
    for (int i = 0; i < n; ++i)
        for (int color = 1; color <= m; ++color)
            domains[i].insert(color);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVDH(graph, m, colors, domains, start_time, time_limit_ms);
}





vector<int> getMinConflictColors(
    const vector<vector<int>>& graph,
    const vector<int>& colors,
    int node,
    const unordered_set<int>& domain
) {
    vector<pair<int, int>> color_conflicts; // {conflict_count, color}
    for (int color : domain) {
        int conflict = 0;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == color) {
                ++conflict;
            }
        }
        color_conflicts.emplace_back(conflict, color);
    }

    sort(color_conflicts.begin(), color_conflicts.end());
    vector<int> sorted_colors;
    for (const auto& p : color_conflicts) {
        sorted_colors.push_back(p.second);
    }
    return sorted_colors;
}

bool backtrackMRVDHMC(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int color : colors)
        if (color == 0) {
            complete = false;
            break;
        }
    if (complete) return true;

    int node = selectMRVDHNode(graph, colors, domains);
    if (node == -1) return false;

    vector<int> sorted_colors = getMinConflictColors(graph, colors, node, domains[node]);
    for (int color : sorted_colors) {
        if (!isSafe(graph, colors, node, color)) continue;

        colors[node] = color;
        if (backtrackMRVDHMC(graph, m, colors, domains, start_time, time_limit_ms))
            return true;
        colors[node] = 0;
    }

    return false;
}

bool mrv_dh_mc_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    int n = graph.size();
    colors.assign(n, 0);
    vector<unordered_set<int>> domains(n);
    for (int i = 0; i < n; ++i)
        for (int color = 1; color <= m; ++color)
            domains[i].insert(color);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVDHMC(graph, m, colors, domains, start_time, time_limit_ms);
}




bool backtrackMRVDHMCFC(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    vector<unordered_set<int>>& domains,
    time_point<high_resolution_clock> start_time,
    long long time_limit_ms
) {
    if (duration_cast<milliseconds>(high_resolution_clock::now() - start_time).count() > time_limit_ms)
        return false;

    bool complete = true;
    for (int color : colors)
        if (color == 0) {
            complete = false;
            break;
        }
    if (complete) return true;

    int node = selectMRVDHNode(graph, colors, domains);
    if (node == -1) return false;

    vector<int> sorted_colors = getMinConflictColors(graph, colors, node, domains[node]);
    for (int color : sorted_colors) {
        if (!isSafe(graph, colors, node, color)) continue;

        // 记录域变化以回溯
        unordered_map<int, int> removed;
        for (int neighbor : graph[node]) {
            if (colors[neighbor] == 0 && domains[neighbor].count(color)) {
                domains[neighbor].erase(color);
                removed[neighbor] = color;
                if (domains[neighbor].empty()) {
                    // 回溯
                    for (const auto& [v, c] : removed)
                        domains[v].insert(c);
                    goto try_next_color;
                }
            }
        }

        colors[node] = color;
        if (backtrackMRVDHMCFC(graph, m, colors, domains, start_time, time_limit_ms))
            return true;
        colors[node] = 0;

        // 回滚域
        for (const auto& [v, c] : removed)
            domains[v].insert(c);

    try_next_color:
        continue;
    }

    return false;
}

bool mrv_dh_mc_fc_backtrack(
    const vector<vector<int>>& graph,
    int m,
    vector<int>& colors,
    long long time_limit_ms
) {
    int n = graph.size();
    colors.assign(n, 0);
    vector<unordered_set<int>> domains(n);
    for (int i = 0; i < n; ++i)
        for (int color = 1; color <= m; ++color)
            domains[i].insert(color);

    auto start_time = high_resolution_clock::now();
    return backtrackMRVDHMCFC(graph, m, colors, domains, start_time, time_limit_ms);
}
