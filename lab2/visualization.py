import matplotlib.pyplot as plt
import matplotlib.animation as animation
from algorithms.rand_gen import rand_gen
import numpy as np
import matplotlib
import math

def update_force(frame):
    """ 更新蛮力搜索的动画帧 """
    global best_dist, best_pair
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("Force Closest Pair")
    
    # 重新绘制所有点
    for x, y in points:
        ax.scatter(x, y, color='black')
    
    i, j = frame
    p1, p2 = points[i], points[j]
    ax.scatter(*p1, color='blue')
    ax.scatter(*p2, color='blue')
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')
    
    # 添加图例
    red_patch = plt.Line2D([0], [0], color='red', marker='o', markersize=5, label='当前最近点对', linestyle='None')
    red_line = plt.Line2D([0], [0], color='red', label='当前最短距离')
    blue_patch = plt.Line2D([0], [0], color='blue', marker='o', markersize=5, label='正在比较的点对', linestyle='None')
    blue_line = plt.Line2D([0], [0], color='blue', label='正在比较的距离')
    ax.legend(handles=[red_patch, red_line, blue_patch, blue_line], loc='upper right')

    dist = np.linalg.norm(np.array(p1) - np.array(p2))
    if dist < best_dist:
        best_dist = dist
        best_pair = (p1, p2)
    
    # 绘制当前的最短路径（红色）
    if best_pair:
        p1, p2 = best_pair
        ax.scatter(*p1, color='red')
        ax.scatter(*p2, color='red')
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-')

    print(f"Frame: {frame}, Current Closest Pair: {best_pair}, Distance: {best_dist}")


def prepare_divide_frames(Px, Py, depth=0):
    """
    准备分治法可视化所需的帧
    """
    n = len(Px)
    
    # 基础情况: 若点数较少，使用暴力法
    if n <= 3:
        # 添加蛮力法比较的帧
        for i in range(len(Px)):
            for j in range(i + 1, len(Px)):
                frames_divide.append({
                    'type': 'brute',
                    'points': Px,
                    'pair': (Px[i], Px[j]),
                    'depth': depth
                })
        return
    
    # 按 x 坐标划分左右子集
    mid = n // 2
    mid_x = Px[mid][0]
    
    # 添加分割线
    frames_divide.append({
        'type': 'divide',
        'points': Px,
        'mid_x': mid_x,
        'depth': depth
    })
    
    Lx, Rx = Px[:mid], Px[mid:]
    Ly, Ry = [], []
    
    for p in Py:
        if p[0] <= mid_x:
            Ly.append(p)
        else:
            Ry.append(p)
    
    # 递归左右子集
    prepare_divide_frames(Lx, Ly, depth + 1)
    prepare_divide_frames(Rx, Ry, depth + 1)
    
    # 添加合并帧（删除分割线）
    frames_divide.append({
        'type': 'merge_start',
        'points': Px,
        'mid_x': mid_x,
        'depth': depth
    })
    
    # 当前左右子集的最近点对距离
    dl = min_dist_between_points(Lx)
    dr = min_dist_between_points(Rx)
    d = min(dl, dr)
    
    # 添加带状区域处理
    strip = [p for p in Py if abs(p[0] - mid_x) < d]
    
    # 添加带状区域帧
    frames_divide.append({
        'type': 'strip',
        'points': Px,
        'strip': strip,
        'mid_x': mid_x,
        'd': d,
        'depth': depth
    })
    
    # 带状区域内点的比较
    for i in range(len(strip)):
        for j in range(i+1, min(i+7, len(strip))):
            frames_divide.append({
                'type': 'strip_compare',
                'points': Px,
                'strip': strip,
                'mid_x': mid_x,
                'd': d,
                'pair': (strip[i], strip[j]),
                'depth': depth
            })
            frames_divide.append({
                'type': 'strip_compare',
                'points': Px,
                'strip': strip,
                'mid_x': mid_x,
                'd': d,
                'pair': (strip[i], strip[j]),
                'depth': depth
            })
    
    # 结束合并
    frames_divide.append({
        'type': 'merge_end',
        'points': Px,
        'depth': depth
    })

def min_dist_between_points(points):
    """计算点集中的最小距离"""
    if len(points) <= 1:
        return float('inf')
    min_dist = float('inf')
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = math.dist(points[i], points[j])
            min_dist = min(min_dist, dist)
    return min_dist

def update_divide(frame_idx):
    """更新分治法搜索的动画帧"""
    global final_best_dist, final_best_pair
    
    if frame_idx >= len(frames_divide):
        return
    
    frame = frames_divide[frame_idx]
    
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("Divide and Conquer Closest Pair")
    
    # 绘制所有点
    for x, y in points:
        ax.scatter(x, y, color='black', zorder=1)
    
    # 添加图例
    red_patch = plt.Line2D([0], [0], color='red', marker='o', markersize=5, label='当前最近点对', linestyle='None')
    red_line = plt.Line2D([0], [0], color='red', label='当前最短距离')
    blue_patch = plt.Line2D([0], [0], color='blue', marker='o', markersize=5, label='正在比较的点对', linestyle='None')
    blue_line = plt.Line2D([0], [0], color='blue', label='正在比较的距离')
    green_line = plt.Line2D([0], [0], color='green', label='分割线')
    purple_patch = plt.Line2D([0], [0], color='purple', marker='o', markersize=5, label='带状区域点', linestyle='None')
    ax.legend(handles=[red_patch, red_line, blue_patch, blue_line, green_line, purple_patch], loc='upper right', fontsize='small')
    
    # 修改: 查找并绘制所有当前活动的分割线
    active_divisions = []
    for i in range(frame_idx):
        prev_frame = frames_divide[i]
        if prev_frame['type'] == 'divide':
            active_divisions.append((prev_frame['mid_x'], prev_frame['depth']))
        elif prev_frame['type'] == 'merge_end' and prev_frame['depth'] in [d for _, d in active_divisions]:
            # 当遇到merge_end时，移除对应深度的分割线
            active_divisions = [(x, d) for x, d in active_divisions if d != prev_frame['depth']]
    
    # 绘制所有活动的分割线，深度越深颜色越浅
    for mid_x, depth in active_divisions:
        # 根据深度计算透明度，让不同层次的分割线可以区分
        alpha = max(0.3, 1.0 - depth * 0.2)
        ax.axvline(x=mid_x, color='green', linestyle='-', alpha=alpha, zorder=2)
    
    # 根据帧类型执行不同的绘制
    if frame['type'] == 'brute':
        # 蛮力法比较
        p1, p2 = frame['pair']
        ax.scatter(*p1, color='blue', zorder=3)
        ax.scatter(*p2, color='blue', zorder=3)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', zorder=3)
        
        dist = math.dist(p1, p2)
        if dist < final_best_dist:
            final_best_dist = dist
            final_best_pair = (p1, p2)
    
    elif frame['type'] == 'divide':
        # 当前帧的分割线用更明显的样式表示
        mid_x = frame['mid_x']
        ax.axvline(x=mid_x, color='green', linestyle='-', linewidth=2, zorder=3)
    
    elif frame['type'] == 'strip':
        # 绘制带状区域
        mid_x = frame['mid_x']
        d = frame['d']
        
        # 绘制带状区域边界
        ax.axvline(x=mid_x-d, color='green', linestyle='--', zorder=3)
        ax.axvline(x=mid_x+d, color='green', linestyle='--', zorder=3)
        
        # 高亮带状区域中的点
        for p in frame['strip']:
            ax.scatter(*p, color='purple', zorder=4)
    
    elif frame['type'] == 'strip_compare':
        # 带状区域点对比较
        mid_x = frame['mid_x']
        d = frame['d']
        
        # 绘制带状区域边界
        ax.axvline(x=mid_x-d, color='green', linestyle='--', zorder=3)
        ax.axvline(x=mid_x+d, color='green', linestyle='--', zorder=3)
        
        # 高亮带状区域中的点
        for p in frame['strip']:
            ax.scatter(*p, color='purple', zorder=2)
        
        # 绘制当前比较点对
        p1, p2 = frame['pair']
        ax.scatter(*p1, color='blue', zorder=4)
        ax.scatter(*p2, color='blue', zorder=4)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', zorder=4)
        
        dist = math.dist(p1, p2)
        if dist < final_best_dist:
            final_best_dist = dist
            final_best_pair = (p1, p2)
    
    # 绘制当前的最近点对（红色）
    if final_best_pair:
        p1, p2 = final_best_pair
        ax.scatter(*p1, color='red', zorder=5)
        ax.scatter(*p2, color='red', zorder=5)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', zorder=5)
    
    print(f"Divide Frame: {frame_idx}/{len(frames_divide)}, Type: {frame['type']}, Depth: {frame['depth']}")
    if final_best_pair:
        print(f"Current Best Distance: {final_best_dist}, Pair: {final_best_pair}")

def run():
    """
    主函数，运行蛮力法和分治法的可视化
    """
    global points, ax, frames_divide, final_best_dist, final_best_pair, best_dist, best_pair,frames_divide  
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    points = rand_gen(20, 0, 100)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("Closest Pair Visualization")

    for x, y in points:
        ax.scatter(x, y, color='black')

    frames = [] 
    best_dist = float('inf')
    best_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            frame = (i, j)
            frames.append(frame)

    # 生成蛮力法动画
    ani_force = animation.FuncAnimation(fig, update_force, frames=frames, repeat=False)
    ani_force.save("./lab2/logs/force.gif", writer="pillow")

    plt.show()

    # 为分治法准备可视化数据
    Px = sorted(points, key=lambda p: p[0])  # 按 x 坐标排序
    Py = sorted(points, key=lambda p: p[1])  # 按 y 坐标排序

    # 用于分治法的帧
    frames_divide = []

    # 调用函数准备分治法的帧
    prepare_divide_frames(Px, Py)

    # 存储最终结果
    final_best_dist = float('inf')
    final_best_pair = None


    # 生成分治法动画
    ani_divide = animation.FuncAnimation(fig, update_divide, frames=len(frames_divide), repeat=False)
    ani_divide.save("./lab2/logs/divide.gif", writer="pillow", fps=2)

    plt.show()

if __name__ == "__main__":
    run()   