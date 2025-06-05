def egg_drop_brute_force(e, f):
    if f == 0:
        return 0
    if f == 1 or e == 1:
        return f

    min_attempts = float('inf')
    for x in range(2, f + 1):
        # 碎了的情况和没碎的情况
        # print(f"尝试在第 {x} 层楼扔鸡蛋")
        attempts = max(egg_drop_brute_force(e - 1, x - 1), egg_drop_brute_force(e, f - x)) + 1
        min_attempts = min(min_attempts, attempts)
    return min_attempts

def egg_drop_naive(e, f):
    # 初始化 dp 表
    dp = [[0] * (f + 1) for _ in range(e + 1)]

    # 初始状态
    for i in range(1, e + 1):
        dp[i][0] = 0  # 0 层楼，0 次
        dp[i][1] = 1  # 1 层楼，1 次
    for j in range(1, f + 1):
        dp[1][j] = j  # 1 个鸡蛋，线性搜索

    # 状态转移
    for i in range(2, e + 1):
        for j in range(2, f + 1):
            dp[i][j] = float('inf')
            for k in range(1, j + 1):
                cost = 1 + max(dp[i - 1][k - 1], dp[i][j - k])
                dp[i][j] = min(dp[i][j], cost)

    return dp[e][f]


def egg_drop_binary(e, f):
    dp = [[0] * (f + 1) for _ in range(e + 1)]

    for i in range(1, e + 1):
        dp[i][0] = 0
        dp[i][1] = 1
    for j in range(1, f + 1):
        dp[1][j] = j

    for i in range(2, e + 1):
        for j in range(2, f + 1):
            low, high = 1, j
            res = float('inf')
            while low <= high:
                mid = (low + high) // 2
                break_case = dp[i - 1][mid - 1]  # 碎了
                survive_case = dp[i][j - mid]    # 没碎
                cost = 1 + max(break_case, survive_case)
                if break_case > survive_case:
                    high = mid - 1
                else:
                    low = mid + 1
                res = min(res, cost)
            dp[i][j] = res

    return dp[e][f]


def egg_drop_optimized(e, f):
    # dp[k][e]: 最多允许 k 次尝试，e 个鸡蛋，最多能测试多少楼层
    dp = [[0] * (e + 1) for _ in range(f + 1)]

    for k in range(1, f + 1):
        for egg in range(1, e + 1):
            dp[k][egg] = dp[k - 1][egg - 1] + dp[k - 1][egg] + 1
            if dp[k][egg] >= f:
                return k
    return f 

def egg_drop_optimized_1d(e, f):
    """优化的动态规划算法，使用1维数组"""
    # dp[i] 表示当前试验次数下，i个鸡蛋最多能测试多少楼层
    dp = [0] * (e + 1)
    trial = 0
    
    # 继续增加试验次数，直到能够测试f层楼
    while dp[e] < f:
        trial += 1
        # 从右往左更新，避免覆盖还需要使用的值
        for i in range(e, 0, -1):
            dp[i] = dp[i - 1] + dp[i] + 1
    
    return trial  # 返回所需的试验次数


if __name__ == "__main__":
    # 测试代码
    eggs_list = [1, 2, 3, 4, 5]
    f = [5, 10, 15, 20, 25]
    print("鸡蛋数量,楼层数量,暴力算法,朴素 DP,二分 DP,优化 DP")
    
    for e in eggs_list:
        for floors in f:
            print(f"{e},{floors},{egg_drop_brute_force(e, floors)},{egg_drop_naive(e, floors)},{egg_drop_binary(e, floors)},{egg_drop_optimized(e, floors)}")