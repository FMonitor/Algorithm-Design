#include "algorithm.h"
#include <chrono>
#include <vector>
#include <unordered_set>
#include <algorithm>

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
