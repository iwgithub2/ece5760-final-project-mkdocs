---
layout: page
title: program and hardware design
permalink: /program-hardware-design/
description: Software and FPGA design.
nav: true
nav_order: 3
---

## Software Design

The software running on the HPS is responsible for managing the MCMC structure learning process. It bridges the gap between the raw dataset, the parallel FPGA compute, and the end user. The software flow can be broken down into four primary stages: offline precomputation, initialization of FPGA memory, graph extraction, and then an interactive demonstration.

### 1. Precomputation of BDeu Scores

Calculating the Bayesian Dirichlet equivalent uniform (BDeu) score for a given parent set requires iterating over the entire dataset and computing expensive log-gamma functions. Implementing this in hardware would be complicated and resource-intensive, which is why we choose to handle this step in software before the MCMC algorithm runs.

To ensure the hardware recieves relevant scores without exceeding memory limits:

* **Stratified Candidate Selection:** A PC-side precomputation engine (`precompute.c`) calculates scores for candidate parent sets up to $k$ maximum parents. Because the FPGA RAM depth per node is limited, the software uses a stratified sorting strategy to retain only the best candidates (up to a maximum of 255 per node).
* **Hardware Formatting:** The resulting database is saved as a binary file. When the main HPS application (`mcmc_fixed.c`) loads this file, it converts the floating-point local scores into a Q16.16 fixed-point format.
* **Data Transfer:** These fixed-point scores and their corresponding one-hot encoded parent bitmasks are written directly to the FPGA's M10K BRAMs via the Heavyweight AXI Bridge. To make the number of candidates configurable in software, a mask of `0xFFFFFFFF` is appended to the end of each node's list to tell the hardware scorer when to stop fetching candidates.

### 2. PIO Communication and Memory Mapping

To interact with the FPGA, the ARM processor maps the physical hardware addresses into its virtual memory space. The Lightweight AXI Bridge is utilized for control and status registers using Parallel I/O (PIO) interfaces:

* **Outputs to FPGA:** The HPS configures the MCMC run by writing to PIO registers, passing the random number generator `seed`, total `iterations`, `active_nodes`, and a `node_mask`. Once configured, the software toggles a `reset` line and sends the `start` signal.
* **Inputs from FPGA:** The software polls a `done` signal to wait for the hardware to finish. Upon completion, it reads back the `best_score`, the `clk_count` to calculate execution time, and the optimized topological order, which is packed into 32-bit words to save memory bandwidth.

### 3. Graph Extraction from the Best Ordering

Because the MCMC search space relies on topological orderings rather than explicit graphs, the FPGA returns an optimized node ordering, not the physical edges of the DAG. Once the HPS retrieves this optimal order, it must extract the final graph. The software performs a single pass over the precomputed candidate database for each node:

1. It looks at the node's position in the returned order.
2. It filters out any candidate parent sets that contain nodes appearing after the current node in the topological order (checking for compatibility).
3. It selects the compatible parent set with the highest local score.

By combining these optimal parent sets across all nodes, the software reconstructs the final Directed Acyclic Graph (DAG) and evaluates its precision, recall, and overall score against the known edge list.

### 4. Interactive Graph Display and Inference Demo

To make the system verifiable and interactive, the software features a demonstration using a VGA subsystem on the FPGA and the command-line interface for user input.

* **VGA Graph Rendering:** Using the AXI bridge mapped to the SDRAM and FPGA On-Chip Memory, the software writes to pixel and character buffers to draw the learned Bayesian Network on a connected VGA monitor. It dynamically spaces the nodes into layers based on their topological depth, rendering them as labeled circles with directed lines indicating causal relationships.
* **Interactive Probability Inference:** Through the terminal, the software builds empirical Conditional Probability Tables (CPTs) by scanning the dataset using the newly learned graph structure. Users can input specific evidence (e.g., `Age=2, Accident=1`) and query target nodes. The HPS utilizes a multi-threaded likelihood weighting algorithm to estimate the conditional probabilities based on the user's queries.


## Hardware Details

The FPGA design stores precomputed parent-set masks and local scores in BRAM. It proposes new node orders, checks which parent sets are valid under the proposed order, accumulates scores for each node, and applies the MCMC acceptance rule.

Core hardware blocks:

| Block | Purpose |
| --- | --- |
| LFSR/random source | Generates random proposal choices and acceptance thresholds. |
| Order representation | Stores the current and proposed topological order. |
| Parent-set memory | Stores candidate parent masks generated by software. |
| Score memory | Stores fixed-point local scores. |
| Compatibility logic | Checks whether a parent set is valid for the proposed order. |
| Per-node score accumulators | Accumulate valid local scores in parallel. |
| Log-add LUT | Approximates `log(1 + exp(x))`. |
| MCMC controller | Accepts or rejects proposed orders. |

TODO: Add enough detail that another group could rebuild the design: module names, interfaces, clocking, reset behavior, memory map, and HPS/FPGA communication.

## External Design and Code References

TODO: List every external codebase, hardware design, paper implementation, dataset, or course module reused or adapted.

For each item, include source name, URL/citation, license or usage permission, what was reused, and what was modified.

## Things Tried That Did Not Work

TODO: Add failed or abandoned approaches.

Candidates:

- Direct graph-space sampling versus order-space sampling.
- Floating-point hardware scoring versus fixed-point scoring.
- Different LUT ranges or fixed-point widths.
- Designs that exceeded timing, memory, or FPGA resource limits.
