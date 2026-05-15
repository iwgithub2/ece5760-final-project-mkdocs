---
layout: page
title: high-level design
permalink: /high-level-design/
description: Architecture, math, rationale, and hardware/software partitioning.
nav: true
nav_order: 2
---

## Rationale and Sources

The project idea came from the observation that Bayesian-network structure learning has a natural split between complex setup work and repetitive scoring work. Software is well suited for parsing datasets, generating candidate parent sets, and producing reproducible score tables. Hardware is better suited for repeatedly evaluating proposed orders using parallel, fixed-function logic.

The acceleration target is the inner scoring loop of an MCMC sampler over topological orderings. Instead of directly exploring individual graph structures, the sampler explores node orders. For each proposed order, the system scores the parent sets that are compatible with that order and then applies the Metropolis-Hastings acceptance rule.

TODO: Add exact sources for the project idea, papers, lecture notes, codebases, and prior designs.

## Background Math

Bayesian-network structure learning seeks a directed acyclic graph that explains observed data. For a node ordering, the posterior score can be viewed as a sum over all graph structures consistent with that order. The sampler uses this score to decide whether to accept or reject proposed order changes.

The scoring path works in log space to avoid underflow from very small probabilities and to replace multiplication with addition. A key accumulation operation is:

```text
node_score = node_score + log(1 + exp(local_score - node_score))
```

In hardware, the non-linear `log(1 + exp(x))` term can be approximated with a small lookup table and piecewise behavior. Large negative inputs contribute approximately zero, and large positive inputs approximate the identity function.

TODO: Add the final posterior-order formula and define each term.

## Role of Arm and FPGA

The design of the Bayesian Network Learner uses a hardware/software co-design approach, leveraging the DE1-SoC platform to partition tasks between the Hard Processor System (HPS), which features a ARM Cortex-A9 processor, and the FPGA. This partitioning strategy means that we can distribute sequential, memory-heavy, and user-interactive tasks to the CPU while using the FPGA to accelerate highly parallelizable, compute-bound  tasks.

### Software Profiling

To determine the most effective system partitioning, an initial implementation of the MCMC algorithm using exclusively software was profiled on the HPS. Using `gprof`, the execution time of a standard run (100,000 iterations on the 8 node [Asia](https://www.bnlearn.com/bnrepository/discrete-small.html#asia) graph) was analyzed to identify bottlenecks.

The profiling results revealed that the majority of CPU cycles were consumed by the core MCMC evaluation loop:

* **`check_compatibility` (41.72%):** Validates if a candidate parent set is compatible with the proposed topological order.
* **`score_order` (23.75%):** Iterates through candidate parent sets for each node to calculate the total log-likelihood of the proposed ordering.
* **`log_add` (15.31%):** Performing logarithmic addition of likelihoods to accumulate a node's score.

Together, these three functions accounted for **over 80%** of the total execution time of 10.6 seconds. Because MCMC structure learning requires at least hundreds of thousands iterations, and sometimes magnitudes higher, running this sequentially on an ARM processor limits practical performance. However, scoring individual nodes within a proposed order is an inherently independent operation, making it an ideal candidate for parallelism on an FPGA.

In addition to `gprof`, we also used the `perf` Linux profiler to analyze a longer, 30-million iteration run on a local machine. The flame graph shows that the `score_order_backend` dominates the call stack. Specifically, the mathematical operations inside the `log_add` function (such as `log1p` and `exp`) and the iterative bitwise masking inside `check_compatibility` create a massive bottleneck.

![alt text](images/flame%20graph.png)

### Hardware/Software Partitioning Strategy
![alt text](<images/Top level.png>)

Based on the profiling data, the architecture was divided to maximize throughput while also keeping hardware simple. As illustrated in the top-level block diagram above, the system is split into two distinct domains communicating via AXI bridges on the DE1-Soc Avalon bus.

**1. HPS Software Responsibilities:**
The ARM processor manages the setup, orchestration, and user interface.

* **Precompute Scores (Software):** Calculating the BDeu scores for all valid parent sets requires parsing the dataset and performing complex Gamma function calculations (`calculate_bde_score`, which took ~18% of the CPU time). This happens once per dataset, and is kept in software then communicated to the FPGA.
* **Initialize and Start FPGA:** The HPS transfers the precomputed score database to the FPGA's M10K BRAMs through the AXI Bridge. Configuration parameters such as the RNG seed, number of iterations, and active nodes are passed through a Lightweight AXI Bridge using Memory-Mapped PIO outputs.
* **Graph Extraction and Display:** Once the FPGA completes its runs, the HPS reads back the best topological order via PIO inputs. It then extracts the final DAG, runs the interactive probability inference program through the terminal, and renders the graph visually using the VGA Subsystem.

**2. FPGA Hardware Responsibilities:**
The FPGA logic is dedicated towards the computationally expensive MCMC loop.

* **Parallel Evaluation:** It utilizes multiple node scorers and dedicated dual-ported M10K BRAMs to evaluate the compatibility and scores of all nodes in parallel.
* **Hardware Math & Randomization:** The intensive `log1p` and `exp` functions identified in the flame graph are replaced by a fast, pipelined Log-Add LUT. Pseudo-random numbers generated by a linear-feedback shift register (LFSR) are used for proposal generation, allowing the hardware to evaluate and accept/reject states quickly.
