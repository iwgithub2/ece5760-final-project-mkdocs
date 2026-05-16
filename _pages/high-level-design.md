---
layout: page
title: high-level design
permalink: /high-level-design/
description: Architecture, math, rationale, and hardware/software partitioning.
nav: true
nav_order: 1
---

## Why Bayesian Networks Matter

Bayesian networks are useful because they represent uncertainty and dependency structure explicitly. Instead of only producing a prediction, a Bayesian network shows how variables are related through a directed acyclic graph. This makes the model more interpretable than many black-box machine learning systems and makes it easier to reason about why a prediction or inference result occurred.

This matters in domains where uncertainty is unavoidable and explanation is important. Examples include medical diagnosis, biological regulatory networks, and risk assessment systems. In those settings, the user often cares not only about the final result, but also about how evidence moves through the model and how changing one variable affects the rest of the system.

Bayesian networks also support conditional and causal-style reasoning. Once a graph and conditional probability tables are learned, a user can set evidence on some variables and query the probability of others. This makes the model useful for interactive "what-if" analysis, not just offline classification.

## Rationale and Sources

The project idea came from the observation that Bayesian-network structure learning has a natural split between complex setup work and repetitive scoring work. Software is well suited for parsing datasets, generating candidate parent sets, and producing reproducible score tables. Hardware is better suited for repeatedly evaluating proposed orders using parallel, fixed-function logic.

The acceleration target is the inner scoring loop of an MCMC sampler over topological orderings. Instead of directly exploring individual graph structures, the sampler explores node orders. For each proposed order, the system scores the parent sets that are compatible with that order and then applies the Metropolis-Hastings acceptance rule.

TODO: Add exact sources for the project idea, papers, lecture notes, codebases, and prior designs.

## Bayesian Networks

A Bayesian network is a probabilistic graphical model represented by a directed acyclic graph (DAG). Each node represents a random variable, and each directed edge represents a conditional dependence. The graph structure lets the joint probability distribution factor into smaller conditional probability terms:

```text
P(X_1, X_2, ..., X_n) = product_i P(X_i | Parents(X_i))
```

This factorization is the main reason Bayesian networks are practical. Instead of modeling one large joint distribution directly, the network decomposes the problem into local relationships between each node and its parents.

## Structure Learning

Bayesian-network structure learning seeks a directed acyclic graph that explains observed data. For a node ordering, the posterior score can be viewed as a sum over all graph structures consistent with that order. The sampler uses this score to decide whether to accept or reject proposed order changes.

In this project, the goal is not only to use a Bayesian network, but to learn its graph structure from data. The hard part is deciding which directed edges should exist. For `n` variables, the number of possible DAGs grows super-exponentially, so exhaustive search is not practical.

Structure-learning algorithms therefore score candidate structures and search for high-scoring ones. A score measures how well a proposed graph explains the observed data while usually penalizing unnecessary complexity. Our project uses precomputed local scores for candidate parent sets, then repeatedly combines those scores while exploring possible node orderings.

## Order Space and MCMC

Instead of sampling directly in graph space, the MCMC approach samples topological orders of the nodes. A topological order is an ordering of nodes where parents must appear before children. Once an order is fixed, only parent sets consistent with that order are legal.

This reduces the search problem. Rather than proposing arbitrary edge additions and removals, the sampler proposes changes to the order, then evaluates which parent sets remain valid under that order.

At each MCMC step:

1. Start with the current node order.
2. Propose a new order, such as by swapping two nodes.
3. Compute the score of the proposed order.
4. Accept the proposed order if it improves the score.
5. Sometimes accept a worse order to avoid getting stuck in a local optimum.

The acceptance rule is based on the Metropolis-Hastings algorithm. Better proposals are always accepted. Worse proposals are accepted with a probability based on the score difference and a random number.

## Log-Space Scoring

The scoring path works in log space to avoid underflow from very small probabilities and to replace multiplication with addition. A key accumulation operation is:

```text
node_score = node_score + log(1 + exp(local_score - node_score))
```

In hardware, the non-linear `log(1 + exp(x))` term can be approximated with a small lookup table and piecewise behavior. Large negative inputs contribute approximately zero, and large positive inputs approximate the identity function.

| Input range | Approximation |
| --- | --- |
| Large negative `x` | `log(1 + exp(x)) ~= 0` |
| Near zero `x` | lookup-table value |
| Large positive `x` | `log(1 + exp(x)) ~= x` |

TODO: Add the final posterior-order formula and define each term.

## Why the Math Maps to Hardware

The score of a proposed order decomposes by node. Each node can check its own compatible parent sets and accumulate its own score independently. This creates a natural source of parallelism: multiple node scores can be computed at the same time and then summed into a total order score.

The mathematical structure therefore matches the hardware structure. The software computes local scores once, and the FPGA repeatedly recombines those scores for many proposed orders.

## Software Profiling

To determine the most effective system partitioning, an initial implementation of the MCMC algorithm using exclusively software was profiled on the HPS. Using `gprof`, the execution time of a standard run (100,000 iterations on the 8-node [Asia](https://www.bnlearn.com/bnrepository/discrete-small.html#asia) graph) was analyzed to identify bottlenecks.

The profiling results revealed that the majority of CPU cycles were consumed by the core MCMC evaluation loop:

* **`check_compatibility` (41.72%):** Validates if a candidate parent set is compatible with the proposed topological order.
* **`score_order` (23.75%):** Iterates through candidate parent sets for each node to calculate the total log-likelihood of the proposed ordering.
* **`log_add` (15.31%):** Performing logarithmic addition of likelihoods to accumulate a node's score.

Together, these three functions accounted for **over 80%** of the total execution time of 10.6 seconds. Because MCMC structure learning requires at least hundreds of thousands of iterations, and sometimes magnitudes higher, running this sequentially on an ARM processor limits practical performance. However, scoring individual nodes within a proposed order is an inherently independent operation, making it an ideal candidate for parallelism on an FPGA.

In addition to `gprof`, we also used the `perf` Linux profiler to analyze a longer, 30-million iteration run on a local machine. The flame graph shows that the `score_order_backend` dominates the call stack. Specifically, the mathematical operations inside the `log_add` function (such as `log1p` and `exp`) and the iterative bitwise masking inside `check_compatibility` create a massive bottleneck.

{% include figure.liquid path="assets/img/flame_graph.png" class="img-fluid rounded z-depth-1" alt="alt text" title="Flame graph of MCMC run in software"%}
