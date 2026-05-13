---
layout: page
title: project introduction
permalink: /project-introduction/
description: Sound bite, summary, and project motivation.
nav: true
nav_order: 3
---

## Sound Bite

We built an FPGA-accelerated Bayesian-network structure-learning system that uses software preprocessing and hardware-parallel MCMC scoring to explore probabilistic graph structures faster than a software-only approach.

## Summary

Bayesian networks are interpretable probabilistic models that represent variables and their conditional dependencies with a directed acyclic graph. Learning the best graph structure from data is computationally difficult because the number of possible structures grows super-exponentially with the number of variables. Practical algorithms therefore rely on heuristic search or sampling methods, both of which repeatedly score proposed graph structures or node orderings.

This project targets that scoring bottleneck on the DE1-SoC platform. The ARM Cortex-A9 hard processor system handles dataset preprocessing, candidate parent-set generation, and local-score calculation. The Cyclone V FPGA handles the repeated MCMC proposal and scoring loop, where many node-level compatibility checks and score accumulations can be performed in parallel.

## Why This Matters

Unlike black-box models, Bayesian networks expose dependency structure directly. This makes them useful in settings where uncertainty, causal reasoning, and interpretability are important. Accelerating structure learning makes these models more practical for larger datasets and faster design-space exploration.

TODO: Add one paragraph describing the final demo from the user's point of view.
