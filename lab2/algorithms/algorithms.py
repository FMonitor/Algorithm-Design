import math

closest_pair = None
min_dist = float("inf")


def force_closest_pair(points):
    """
    使用蛮力法求解最近点对问题。

    :param points: 一个包含 (x, y) 坐标的点列表
    :return: (最小距离, 最近点对)
    """
    min_dist = float("inf")
    closest_pair = None
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            dist = math.dist(points[i], points[j])  # 计算欧几里得距离
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])

    return min_dist, closest_pair


def closest_strip(strip, d,mid_x, optimized = False):
    """
    检查 y 轴排序后下方最多 6 个点,或执行优化算法：
    在跨区域的条带中寻找最小距离点对。
    只比较不同侧的最多 4 个点（d × d 区域内）。
    """
    if(optimized):
        min_d = d
        closest_pair = None
        n = len(strip)
        for i in range(n):
            p = strip[i]
            count = 0  
            for j in range(i + 1, n):
                q = strip[j]
                if (q[1] - p[1]) >= d:
                    break

                # 只比较处于 mid_x 另一侧的点
                if (p[0] < mid_x and q[0] >= mid_x) or (p[0] >= mid_x and q[0] < mid_x):
                    dist = math.dist(p, q)
                    if dist < min_d:
                        min_d = dist
                        closest_pair = (p, q)
                    count += 1
                    if count >= 4:  # 最多比较 4 个点
                        break

        return min_d, closest_pair
    else:
        min_d = d
        closest_pair = None
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                dist = math.dist(strip[i], strip[j])
                if dist < min_d:
                    min_d = dist
                    closest_pair = (strip[i], strip[j])
        return min_d, closest_pair

def divide_closest_pair(Px, Py, optimized = False):
    """
    递归求解最近点对。
    """
    n = len(Px)

    if n <= 3:
        return force_closest_pair(Px)

    mid = n // 2
    Lx, Rx = Px[:mid], Px[mid:]
    Ly, Ry = [], []
    mid_x = Px[mid][0]

    for p in Py:
        if p[0] <= mid_x:
            Ly.append(p)
        else:
            Ry.append(p)

    dl, pair_l = divide_closest_pair(Lx, Ly)
    dr, pair_r = divide_closest_pair(Rx, Ry)

    if dl < dr:
        d, closest_pair = dl, pair_l
    else:
        d, closest_pair = dr, pair_r

    strip = [p for p in Py if abs(p[0] - mid_x) < d]
    ds, pair_s = closest_strip(strip, d, mid_x, optimized)

    if ds < d:
        return ds, pair_s
    else:
        return d, closest_pair


def run_algoritm(points, algorithm="divide"):
    """
    运行算法，返回最近点对的距离和点对。

    :param points: 点列表
    :param algorithm: 使用的算法类型，默认为 "divide"。
    :return: (最小距离, 最近点对)
    """
    if not points:
        return 0, None
    if algorithm == "brute":
        return force_closest_pair(points)
    elif algorithm == "divide":
        Px = sorted(points, key=lambda p: p[0])  # 按 x 坐标排序
        Py = sorted(points, key=lambda p: p[1])  # 按 y 坐标排序
        return divide_closest_pair(Px, Py, False)
    elif algorithm == "divide_optimized":
        Px = sorted(points, key=lambda p: p[0])  # 按 x 坐标排序
        Py = sorted(points, key=lambda p: p[1])  # 按 y 坐标排序
        return divide_closest_pair(Px, Py, True)
    else:
        raise ValueError("Unsupported algorithm. Use 'brute' or 'divide'.")


if __name__ == "__main__":
    # 测试代码
    test_points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    dist, pair = run_algoritm(test_points)
    print("最近点对距离:", dist, "最近点对:", pair)
