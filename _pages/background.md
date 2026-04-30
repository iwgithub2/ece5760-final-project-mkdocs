---
layout: page
title: background
permalink: /background/
description: Bayesian-network structure learning and FPGA acceleration motivation.
nav: true
nav_order: 1
---

## Introduction

Bayesian networks are probabilistic graphical models that represent variables and their conditional dependencies with a directed acyclic graph (DAG). Each node represents a variable, and each directed edge encodes a dependency relationship. Unlike many modern black-box neural-network models, Bayesian networks expose their internal structure directly, making them useful when interpretability and causal reasoning matter as much as predictive performance.

This interpretability is especially valuable for real-world datasets that are noisy, incomplete, or uncertain. Bayesian networks model uncertainty natively through probability distributions, so they can represent partial evidence and reason about how uncertainty propagates through a system. They also support causal and counterfactual analysis: a user can ask how changing one variable affects the rest of the network and trace that effect through explicit graph structure.

These properties make Bayesian networks a strong fit for high-stakes domains such as medical diagnosis, genomic regulatory modeling, and risk assessment in autonomous systems. In these settings, it is often not enough for a model to produce a prediction. Users also need to understand why that prediction was made and how different assumptions would change the result.

## Structure-Learning Challenge

The main challenge is learning the structure of the Bayesian network from observational data. Finding the optimal DAG is NP-hard, and the number of possible graph structures grows super-exponentially as the number of nodes increases. Exhaustively evaluating every graph quickly becomes infeasible.

Practical systems therefore use heuristic methods. Greedy search methods such as hill climbing repeatedly modify a candidate graph to improve a scoring function. These methods are relatively fast, but they can become trapped in local optima. Sampling methods such as Markov Chain Monte Carlo (MCMC) instead perform a random walk through the search space, which can explore a broader range of possible structures and provide better uncertainty estimates.

Both approaches are bottlenecked by scoring. Each proposed graph or order must be evaluated to estimate how well it explains the observed data. Even when the raw dataset is preprocessed once in software, the search still requires a large number of repeated score lookups, compatibility checks, and accumulations.

## Search Versus Sampling

There are two common ways to approach Bayesian-network structure learning:

| Approach | Description | Tradeoff |
| --- | --- | --- |
| Greedy search | Iteratively improves a candidate graph using local changes. | Fast, but vulnerable to local optima. |
| Sampling | Randomly explores likely structures or node orderings. | Broader exploration, but more scoring work. |

This project focuses on an MCMC sampling approach over topological orderings rather than directly sampling individual graphs. Order space is smaller than graph space, so sampling can converge more efficiently. Once a high-quality order is found, it becomes easier to recover a likely Bayesian-network structure.

For a given order, the score is based on the posterior probability summed over all graphs consistent with that order. The algorithm proposes a new order, scores it, and then accepts or rejects the proposal. A better-scoring order is accepted automatically. A worse-scoring order may still be accepted with some probability, allowing the sampler to escape local optima and explore the posterior distribution more thoroughly.

## MCMC Scoring Bottleneck

The computational bottleneck is not repeatedly scanning the dataset. The software preprocessing stage handles the dataset once by computing local scores for possible parent sets. The bottleneck is the repeated scoring of proposed orders during sampling.

Scoring one order requires checking, for every node, which candidate parent sets are compatible with the proposed ordering and then accumulating the corresponding precomputed log probabilities. This work is highly repetitive and parallel across nodes, making it a good candidate for FPGA acceleration.

The score accumulation uses log-space arithmetic to avoid underflow from very small probabilities and to replace expensive multiplications with additions. One important operation is:

```text
node_score = node_score + log(1 + exp(local_score - node_score))
```

This non-linear log-add term can be approximated in hardware with a small lookup table (LUT) and simple piecewise behavior: large negative inputs contribute approximately zero, while large positive inputs approximate the identity function.

## Project Objective

The goal of this project is to accelerate Bayesian-network structure learning on the DE1-SoC platform by partitioning the workload between the ARM Cortex-A9 hard processor system (HPS) and the Cyclone V FPGA.

The HPS handles setup and preprocessing. It reads the dataset, computes valid candidate parent sets, calculates local scores, converts those scores into log space, and packages the resulting score tables for the FPGA.

The FPGA handles the high-volume sampling loop. It proposes order changes, evaluates proposed orders, and applies the MCMC acceptance rule. By scoring nodes in parallel and storing precomputed local scores in on-chip memory, the FPGA can reduce the repeated scoring cost that dominates the software-only sampler.

## Hardware Partitioning

| Component | Responsibility |
| --- | --- |
| HPS | Dataset preprocessing, local-score generation, log-space conversion, table loading. |
| FPGA BRAM | Storage for precomputed parent-set and local-score tables. |
| Proposal logic | Random order changes, driven by hardware random-number generation such as an LFSR. |
| Parallel scoring logic | Per-node compatibility checks and score accumulation. |
| Log-add LUT | Approximation for `log(1 + exp(x))` during score accumulation. |
| MCMC controller | Accepts better proposals and probabilistically accepts worse proposals. |

This partition keeps complex sequential setup in software while moving the repeated, parallel scoring work into custom hardware.
