import time
import random
import cProfile
import pstats
import io
import json
from collections import deque
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

random.seed(42)

# ---------------------------------------------------------------
# Maze generator: random walls (with cycles/open areas, unlike a
# perfect spanning-tree maze) so BFS and DFS can genuinely find
# different-length paths. Regenerates until start->goal is solvable.
# ---------------------------------------------------------------
def generate_maze(size, wall_density=0.32):
    while True:
        grid = [[1 if (r, c) not in [(0, 0), (size - 1, size - 1)] and random.random() < wall_density
                 else 0 for c in range(size)] for r in range(size)]
        start = (0, 0)
        goal = (size - 1, size - 1)
        grid[start[0]][start[1]] = 0
        grid[goal[0]][goal[1]] = 0
        # solvability check (plain BFS reachability)
        seen = {start}
        q = deque([start])
        while q:
            r, c = q.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        if goal in seen:
            return grid, start, goal


def get_neighbors(maze, pos, rows, cols):
    r, c = pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
            yield (nr, nc)


def bfs(maze, start, goal, rows, cols):
    frontier = deque([start])
    visited = {start}
    parent = {start: None}
    nodes_expanded = 0
    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], nodes_expanded
        for n in get_neighbors(maze, node, rows, cols):
            if n not in visited:
                visited.add(n)
                parent[n] = node
                frontier.append(n)
    return None, nodes_expanded


def dfs(maze, start, goal, rows, cols):
    frontier = [start]
    visited = {start}
    parent = {start: None}
    nodes_expanded = 0
    while frontier:
        node = frontier.pop()
        nodes_expanded += 1
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], nodes_expanded
        for n in get_neighbors(maze, node, rows, cols):
            if n not in visited:
                visited.add(n)
                parent[n] = node
                frontier.append(n)
    return None, nodes_expanded


def run_trials(fn, maze, start, goal, rows, cols, runs=5):
    times = []
    nodes = None
    path = None
    for _ in range(runs):
        t0 = time.perf_counter()
        p, n = fn(maze, start, goal, rows, cols)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
        nodes, path = n, p
    return sum(times) / len(times), nodes, path, times


# ---------------------------------------------------------------
# Three test cases: best (small maze), average (medium), worst (large)
# ---------------------------------------------------------------
test_cases = [
    ("Best case (11x11 maze)", 11),
    ("Average case (21x21 maze)", 21),
    ("Worst case (31x31 maze)", 31),
]

all_results = {}
mazes = {}
for label, size in test_cases:
    maze, start, goal = generate_maze(size)
    rows, cols = len(maze), len(maze[0])
    mazes[label] = (maze, start, goal, rows, cols)

    bfs_avg, bfs_nodes, bfs_path, bfs_times = run_trials(bfs, maze, start, goal, rows, cols)
    dfs_avg, dfs_nodes, dfs_path, dfs_times = run_trials(dfs, maze, start, goal, rows, cols)

    all_results[label] = {
        "size": f"{rows}x{cols}",
        "BFS": {"avg_time_ms": bfs_avg, "nodes_expanded": bfs_nodes,
                "path_length": len(bfs_path), "runs_ms": bfs_times},
        "DFS": {"avg_time_ms": dfs_avg, "nodes_expanded": dfs_nodes,
                "path_length": len(dfs_path), "runs_ms": dfs_times},
    }

with open("results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print(json.dumps(all_results, indent=2))

# Summary (averaged across the three cases)
bfs_avg_time = sum(all_results[l]["BFS"]["avg_time_ms"] for l, _ in test_cases) / 3
dfs_avg_time = sum(all_results[l]["DFS"]["avg_time_ms"] for l, _ in test_cases) / 3
bfs_avg_nodes = sum(all_results[l]["BFS"]["nodes_expanded"] for l, _ in test_cases) / 3
dfs_avg_nodes = sum(all_results[l]["DFS"]["nodes_expanded"] for l, _ in test_cases) / 3
print("\nAveraged across 3 cases:")
print(f"BFS: {bfs_avg_time:.4f} ms, {bfs_avg_nodes:.1f} nodes")
print(f"DFS: {dfs_avg_time:.4f} ms, {dfs_avg_nodes:.1f} nodes")

# ---------------------------------------------------------------
# Fig 1 -- best-case (11x11) maze diagram with BFS path highlighted
# ---------------------------------------------------------------
label0 = test_cases[0][0]
maze0, start0, goal0, rows0, cols0 = mazes[label0]
bfs_path0 = bfs(maze0, start0, goal0, rows0, cols0)[0]

fig, ax = plt.subplots(figsize=(5, 5))
for r in range(rows0):
    for c in range(cols0):
        color = "#2b2b2b" if maze0[r][c] == 1 else "#ffffff"
        ax.add_patch(patches.Rectangle((c, rows0 - 1 - r), 1, 1,
                                        facecolor=color, edgecolor="#999999", linewidth=0.3))

for (r, c) in bfs_path0:
    if (r, c) not in (start0, goal0):
        ax.add_patch(patches.Rectangle((c, rows0 - 1 - r), 1, 1,
                                        facecolor="#4C8BF5", edgecolor="#999999", linewidth=0.3, alpha=0.7))

sr, sc = start0
gr, gc = goal0
ax.add_patch(patches.Rectangle((sc, rows0 - 1 - sr), 1, 1, facecolor="#2ecc71", edgecolor="black"))
ax.add_patch(patches.Rectangle((gc, rows0 - 1 - gr), 1, 1, facecolor="#e74c3c", edgecolor="black"))
ax.text(sc + 0.5, rows0 - 1 - sr + 0.5, "S", ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(gc + 0.5, rows0 - 1 - gr + 0.5, "G", ha="center", va="center", fontsize=10, fontweight="bold")

ax.set_xlim(0, cols0)
ax.set_ylim(0, rows0)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.set_title(f"Best-case maze ({rows0}x{cols0}) — Start (S) to Goal (G)\nBFS shortest path shown in blue", fontsize=11)
plt.tight_layout()
plt.savefig("fig1_maze.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Fig 2 -- grouped bar chart: avg time & nodes expanded per test case
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
labels_short = ["Best\n(11x11)", "Average\n(21x21)", "Worst\n(31x31)"]
bfs_times_all = [all_results[l]["BFS"]["avg_time_ms"] for l, _ in test_cases]
dfs_times_all = [all_results[l]["DFS"]["avg_time_ms"] for l, _ in test_cases]
bfs_nodes_all = [all_results[l]["BFS"]["nodes_expanded"] for l, _ in test_cases]
dfs_nodes_all = [all_results[l]["DFS"]["nodes_expanded"] for l, _ in test_cases]

x = range(3)
w = 0.35
axes[0].bar([i - w/2 for i in x], bfs_times_all, width=w, label="BFS", color="#4C8BF5")
axes[0].bar([i + w/2 for i in x], dfs_times_all, width=w, label="DFS", color="#F5734C")
axes[0].set_xticks(list(x))
axes[0].set_xticklabels(labels_short, fontsize=8)
axes[0].set_title("Average Time (ms)")
axes[0].legend(fontsize=8)

axes[1].bar([i - w/2 for i in x], bfs_nodes_all, width=w, label="BFS", color="#4C8BF5")
axes[1].bar([i + w/2 for i in x], dfs_nodes_all, width=w, label="DFS", color="#F5734C")
axes[1].set_xticks(list(x))
axes[1].set_xticklabels(labels_short, fontsize=8)
axes[1].set_title("Nodes Expanded")
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.savefig("fig2_bars.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Flame chart -- profile a combined BFS+DFS workload across all 3 cases
# ---------------------------------------------------------------
def profiled_workload():
    for label, size in test_cases:
        maze, start, goal, rows, cols = mazes[label]
        for _ in range(20):
            bfs(maze, start, goal, rows, cols)
        for _ in range(20):
            dfs(maze, start, goal, rows, cols)

profiler = cProfile.Profile()
profiler.enable()
profiled_workload()
profiler.disable()

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
stats.print_stats(15)
with open("cprofile_report.txt", "w") as f:
    f.write(stream.getvalue())

stats_dict = stats.stats
rows_data = []
for (filename, lineno, funcname), (cc, nc, tt, ct, callers) in stats_dict.items():
    short_file = filename.split("/")[-1]
    label = f"{funcname} ({short_file}:{lineno})"
    rows_data.append((label, ct, tt))

rows_data.sort(key=lambda x: x[1], reverse=True)
rows_data = rows_data[:8]

fig, ax = plt.subplots(figsize=(9, 4.5))
labels = [r[0] for r in rows_data][::-1]
cum_times = [r[1] * 1000 for r in rows_data][::-1]

y_pos = range(len(labels))
bar_colors = plt.cm.autumn_r([min(1.0, t / max(cum_times)) for t in cum_times])
ax.barh(y_pos, cum_times, color=bar_colors, edgecolor="black", linewidth=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("Cumulative time (ms)")
ax.set_title("Flame-chart-style view — BFS+DFS across best/average/worst-case mazes\n"
             "(cProfile, used in place of py-spy; wider bar = more time, self + children)",
             fontsize=10)
for i, v in enumerate(cum_times):
    ax.text(v, i, f" {v:.2f} ms", va="center", fontsize=8)
ax.set_xlim(0, max(cum_times) * 1.18)
plt.tight_layout()
plt.savefig("fig3_flamechart.png", dpi=150)
plt.close()

print("\nTop functions by cumulative time (ms):")
for label, ct, tt in rows_data[::-1]:
    print(f"  {label}: {ct*1000:.3f} ms cumulative, {tt*1000:.3f} ms self")
