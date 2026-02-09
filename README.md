# WinHtut16-ADA_assignment1_st126687
ADA Assignment 1: Interval Scheduling Empirical Runtime and Optimality Study
Overview
This repository contains the Python implementation and empirical analysis for the Interval Scheduling Problem as part of the Advanced Algorithms & Data Structures course Assignment 1. The project addresses both theoretical concepts (e.g., greedy choice property, optimality proofs via contradiction, Big-O complexity validation) and practical coding (e.g., modular scripts for algorithms and experiments).

Problem Statement
Given a set of n intervals I = {(s_i, f_i)} where s_i < f_i, the goal is to select the maximum-size subset of pairwise non-overlapping intervals. Two intervals are compatible if f_i ≤ s_j or f_j ≤ s_i.
Theoretical Insight: This is a classic optimization problem solvable optimally in polynomial time via greedy (EFT), but heuristics like EST/SD may fail (e.g., counterexample: short interval [4,7] blocking two longer compatible ones [1,5] and [6,10]).

Repository Structure
The code is modularized into separate Python scripts for clarity and reusability:
1) assignment1.py: Main script orchestrating the experiments, including Big-O validation, plot generation, and runtime measurements.
2) dataset_gen.py: Dataset generation functions (uniform random intervals with T = α · n · D for overlap regimes: α=0.1 high, α=1 medium, α=5 low).
3) greedy_algos.py: Implementations of greedy strategies (EFT: sort by f_i, EST: sort by s_i, SD: sort by (f_i - s_i)) – all O(n log n).
4) exhaustive_algo.py: Exhaustive subset enumeration (bitmask, O(n 2^n)) for optimality oracle on small n.
5) interval_scheduling.py: Core problem utilities (e.g., compatibility checks, selection logic).
6) exhaustive_plots_alpha_0.1.png, exhaustive_plots_alpha_1.png, exhaustive_plots_alpha_5.png: Runtime vs. n and normalized t(n)/(n 2^n) for exhaustive.
7) greedy_plots_alpha_0.1.png, greedy_plots_alpha_1.png, greedy_plots_alpha_5.png: Log-log runtime and normalized t(n)/(n log_2 n) for greedy.

README.md: This file.

Theoretical Highlights

Greedy Algorithms: Runtime O(n log n) dominated by sorting. EFT is optimal (proof: by contradiction, replacing intervals in an optimal schedule with earlier-finishing ones preserves size and compatibility). EST and SD are heuristics; they fail in high-overlap due to poor local choices.
Exhaustive Algorithm: Enumerates 2^n subsets, sorts and checks each (O(n log n) per subset), totaling O(n 2^n). Practical only for n ≤ 20.
Dataset Design: Scaling T with n ensures stable overlap density. High α reduces conflicts, making heuristics closer to optimal.
Big-O Validation: Plots confirm O(n log n) for greedy (log-log slope ≈1, normalization flattens); O(n 2^n) for exhaustive (exponential growth, normalization approaches constant). Pruning (e.g., branch-and-bound) reduces average runtime for small n but not worst-case, as adversarial inputs force full enumeration.
Expected Outcomes: EFT matches optimal; heuristics suboptimal in dense regimes. Runtimes align with theory, with overlap affecting constants.

How to Run
Requirements

Python 3.12+ with libraries: numpy, matplotlib, statistics, random, time (install via pip install numpy matplotlib if needed).

Steps

Clone the repo: git clone https://github.com/WinHtut16/WinHtut16-ADA_assignment1_st126687.
Run the main script: python assignment1.py – this executes experiments, generates plots, and saves them to the folder.
Adjust parameters in assignment1.py (e.g., num_trials=10, D=10, n ranges) for custom runs.
Example: For small n, compare greedy vs. exhaustive optimality; for large n, observe greedy scalability.

View plots: Open PNG files in plots/ for visual analysis (e.g., log-log for greedy confirms theoretical bounds).

Solution Quality: EFT always optimal; EST/SD gaps up to 20% in high overlap (α=0.1).
Runtime: Greedy handles n=1M in seconds; exhaustive explodes beyond n=20.
Plots Analysis: See PNGs—normalization flattens, validating asymptotics. Overlap regimes show denser inputs increase constants but not complexity.

For full report details (e.g., counterexamples, induction proofs for correctness), refer to the assignment documentation or integrated comments in code.
License
MIT License – free to use and modify.
For issues or questions, open a GitHub issue or contact st126687@ait.asia.
