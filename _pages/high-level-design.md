---
layout: page
title: high-level design
permalink: /high-level-design/
description: Architecture, math, rationale, and hardware/software partitioning.
nav: true
nav_order: 4
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

## Logical Structure

| Stage | Responsibility |
| --- | --- |
| Dataset preprocessing | Load data, identify variables, and prepare discrete values. |
| Parent-set generation | Enumerate or filter candidate parent sets for each node. |
| Local scoring | Compute local scores for node/parent-set combinations. |
| Table packing | Convert scores and parent masks into FPGA-readable memory tables. |
| Proposal generation | Generate candidate order changes in hardware. |
| Parallel scoring | Score each proposed order using per-node logic. |
| Acceptance control | Apply the MCMC acceptance rule and update the current order. |

## Hardware/Software Tradeoffs

Software handles the flexible, data-dependent setup steps that are easier to implement and debug on the HPS. This includes file parsing, parent-set enumeration, score calculation, and fixed-point conversion.

Hardware handles the repeated scoring operations that dominate runtime during sampling. The FPGA stores precomputed tables in BRAM, checks parent-set compatibility in parallel, accumulates log-space scores, and evaluates the MCMC accept/reject decision.

The tradeoff is flexibility versus throughput. Software is easier to modify and supports complex preprocessing, while hardware reduces the cost of repeated scoring once the tables have been generated.

## Relevant Patents, Copyrights, and Trademarks

TODO: Document relevant intellectual-property considerations.

Known items to review:

- DE1-SoC, Cyclone V, ARM Cortex-A9, and Intel/Altera naming and IP usage.
- Any Bayesian-network or MCMC code/designs reused from public repositories.
- Dataset licenses.
- Course-provided code or infrastructure.
