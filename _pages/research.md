---
layout: page
title: research
permalink: /research/
description: Structure-learning search paths and scoring notes.
nav: true
nav_order: 1
---

## Bayesian-Network Structure Learning

The project explores search methods for Bayesian-network structure learning with an FPGA target.
The software-side path produces deterministic inputs that are easier to validate in simulation and hardware.

## Search Paths

| Path | Role |
| --- | --- |
| Hill climber | Baseline quality and runtime reference. |
| MCMC/order sampler | Candidate hardware search path. |
| Fixed-point scoring | Hardware-oriented approximation study. |

## Fixed-Point Log-Add

The MCMC score accumulation uses:

```text
node_score = node_score + log(1 + exp(local_score - node_score))
```

The useful hardware candidate is piecewise: large negative inputs map near zero, while large positive inputs use the identity approximation.
