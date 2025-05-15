import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation

# Adjacency list and positions as provided
adjacency = {
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

positions = {
    1: (0, 0),
    2: (-1, -1),
    3: (1.5, -0.5),
    4: (0.5, -1),
    5: (0.5, -2),
    6: (2, -2),
    7: (1, -3),
    8: (3, -1),
    9: (3, -3)
}

color_map = ['red', 'green', 'blue', 'yellow']
colors = 4
frames = []  # Store intermediate frames for animation


def backtrack_coloring_animated(adjacency, colors):
    n = len(adjacency)
    nodes = list(adjacency.keys())
    color_assignment = {node: -1 for node in nodes}
    snapshots = []

    def snapshot():
        # Take a deep copy for snapshot
        snapshots.append(color_assignment.copy())

    def is_safe(node, color):
        for neighbor in adjacency[node]:
            if color_assignment[neighbor] == color:
                return False
        return True

    def backtrack(index):
        if index == n:
            snapshot()
            return True
        node = nodes[index]
        for color in range(colors):
            if is_safe(node, color):
                color_assignment[node] = color
                snapshot()
                if backtrack(index + 1):
                    return True
                color_assignment[node] = -1
                snapshot()
        return False

    backtrack(0)
    return snapshots


snapshots = backtrack_coloring_animated(adjacency, colors)

# Create animation frames
fig, ax = plt.subplots(figsize=(8, 6))
def update(frame_index):
    ax.clear()
    frame = snapshots[frame_index]
    # Redraw everything for this frame
    for node, neighbors in adjacency.items():
        for neighbor in neighbors:
            if node < neighbor:
                x1, y1 = positions[node]
                x2, y2 = positions[neighbor]
                ax.plot([x1, x2], [y1, y2], color='black', linewidth=1)
    for node, (x, y) in positions.items():
        color_idx = frame[node]
        facecolor = color_map[color_idx] if color_idx != -1 else 'lightgray'
        circle = mpatches.Circle((x, y), radius=0.3, facecolor=facecolor,
                                 edgecolor='black', linewidth=1.5, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(node), ha='center', va='center',
                fontsize=12, fontweight='bold', zorder=3)
    ax.set_xlim(-2, 4)
    ax.set_ylim(-4, 2)
    ax.set_aspect('equal')
    ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=len(snapshots), interval=500, repeat=False)
ani.save('/mnt/data/map_coloring_backtrack.gif', writer='pillow', fps=2)
plt.close(fig)
