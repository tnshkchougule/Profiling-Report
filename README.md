# Profiling-Report
# BFS vs DFS — Maze Path-Finding Profiling

SLE-2 profiling report 
Compares Breadth-First Search (BFS) and Depth-First Search (DFS) on randomly
generated grid mazes, measuring execution time, nodes expanded, and path
optimality across three maze sizes (best / average / worst case).

## What this does

- `get_neighbors()` — returns valid, in-bounds, non-wall neighbours of a cell
- `bfs()` — breadth-first search using a `deque` as the frontier (queue)
- `dfs()` — depth-first search using a `list` as the frontier (stack)
- `generate_maze()` — builds a random solvable maze with walls and open
  areas/cycles (not a perfect spanning-tree maze), so BFS and DFS can
  genuinely return different-length paths
- Both algorithms return `(path, nodes_expanded)` so they can be compared
  on equal footing

## Test setup

| Test case | Maze size |
|---|---|
| Best case | 11×11 |
| Average case | 21×21 |
| Worst case | 31×31 |

Each algorithm is run **5 times per maze** (15 runs total per algorithm) using
`time.perf_counter()` for precise timing. Nodes expanded = number of states
popped off the frontier before the goal is reached.

## Results

| Test Case | Algo | Avg Time (ms) | Nodes Expanded | Path Length |
|---|---|---|---|---|
| Best (11×11) | BFS | 0.0567 | 64 | 21 |
| Best (11×11) | DFS | 0.0440 | 52 | 23 |
| Average (21×21) | BFS | 0.1986 | 239 | 41 |
| Average (21×21) | DFS | 0.1269 | 148 | 75 |
| Worst (31×31) | BFS | 0.5444 | 655 | 61 |
| Worst (31×31) | DFS | 0.1197 | 130 | 109 |

**Key takeaway:** BFS always finds the true shortest path (guaranteed
optimal on an unweighted graph), but its time and node count grow fast as
the maze gets bigger. DFS is faster and touches fewer nodes, but its path
gets progressively less optimal — up to 1.8x longer than BFS's shortest
path on the worst-case maze.

## Profiling

- **Timing:** `time.perf_counter()` (5 runs per algorithm per test case)
- **Flame graph:** generated with `cProfile` in place of
  [`py-spy`](https://github.com/benfred/py-spy), since py-spy needs to
  attach to a running process and its binary wasn't installable in the
  offline sandbox this was drafted in. To capture the flame graph with
  actual py-spy on a normal machine:

  ```bash
  pip install py-spy
  py-spy record -o flamegraph.svg --rate 100 -- python experiment.py
  ```

## Files

| File | Description |
|---|---|
| `experiment.py` | Full source: maze generation, BFS, DFS, timing, cProfile flame-chart generation |
| `results.json` | Raw timing/node/path-length results per test case |
| `fig1_maze.png` | Best-case maze diagram with BFS shortest path highlighted |
| `fig2_bars.png` | Grouped bar chart: avg time & nodes expanded per test case |
| `fig3_flamechart.png` | cProfile-based flame chart across the combined workload |
| `SLE2_25UAM086_TanishkaChougule_Maze.docx` | Full written report (SLE-2 template) |

## Running it

```bash
pip install matplotlib
python experiment.py
```

This regenerates `results.json`, `fig1_maze.png`, `fig2_bars.png`, and
`fig3_flamechart.png`.

