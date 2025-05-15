#ifndef ALGORITHM_H
#define ALGORITHM_H

#include <vector>

// 所有算法接口统一格式：
// 返回值：是否找到合法解
// 参数：图、颜色数、输出颜色数组、时间限制（毫秒）

bool simple_backtrack(
    const std::vector<std::vector<int>>& graph,
    int m,
    std::vector<int>& colors,
    long long time_limit_ms
);

bool min_conflict_backtrack(
    const std::vector<std::vector<int>>& graph,
    int m,
    std::vector<int>& colors,
    long long time_limit_ms
);

bool forward_checking_backtrack(
    const std::vector<std::vector<int>>& graph,
    int m,
    std::vector<int>& colors,
    long long time_limit_ms
);

bool min_conflict_forward_checking_backtrack(
    const std::vector<std::vector<int>>& graph,
    int m,
    std::vector<int>& colors,
    long long time_limit_ms
);

#endif 