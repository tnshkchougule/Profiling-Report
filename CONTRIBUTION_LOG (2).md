# Contribution Log

Log of work done on this repository — **BFS vs DFS Maze Path-Finding Profiling**
(SLE-2, 02AML204 – Introduction to Artificial Intelligence).

## Project Work

- Chose the algorithm pair to compare: BFS vs DFS
- Wrote `get_neighbors()`, `bfs()`, and `dfs()` — both return `(path, nodes_expanded)` for a fair comparison
- Built `generate_maze()` — a random, solvable maze generator with walls and open areas/cycles (not a perfect spanning-tree maze), so BFS and DFS can return genuinely different path lengths
- Set up 3 test cases — 11×11 (best case), 21×21 (average case), 31×31 (worst case) — and ran each algorithm 5 times per case using `time.perf_counter()`
- Attempted `py-spy` for the flame graph; not installable in the offline sandbox used to draft the report, so substituted Python's built-in `cProfile` module instead, with the exact `py-spy` command documented for reproduction on a normal machine
- Generated `fig1_maze.png` (maze + BFS path), `fig2_bars.png` (time/nodes comparison), `fig3_flamechart.png` (cProfile flame chart)
- Reviewed all numbers in `results.json`, verified the figures matched the data, and wrote the Justification & Conclusion sections of the report
- Drafted the SLE-2 report following the required template — Algorithms, Profiling Method, Results, Justification, AI Contribution Note, Conclusion
- Filled in personal details (PRN, Name, Division) and removed the unused GitHub-link placeholder from the final report
- Wrote `README.md` documenting the project, results table, and how to run it
- Set up local project folder in VS Code, installed `matplotlib`, and ran `experiment.py` successfully, confirming output matched the report's numbers exactly
- Created the GitHub repository and pushed `README.md`
- Re-uploaded `experiment.py` to the repository after it was accidentally deleted in an earlier commit

## AI Contribution Summary

**AI tool used:** Claude (Anthropic)

**What AI helped with:**
- Writing the BFS/DFS implementation and the random maze generator
- Setting up the timing/profiling script and the cProfile-based flame chart (used as a substitute for `py-spy`, which could not be installed in the offline environment the report was drafted in)
- Generating the maze diagram and comparison charts
- Structuring and drafting the SLE-2 report and this repository's documentation
- Troubleshooting local setup issues (file extension errors, missing terminal folder context, matplotlib installation)

**What the student did:**
- Chose the algorithm pair and the three test-case maze sizes
- Reviewed and verified all generated results and figures
- Wrote the final Justification and Conclusion sections in her own words
- Ran the code locally, debugged setup issues on her own machine, and confirmed the output matched the report
- Set up and managed the GitHub repository
