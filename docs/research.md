# Research Notes

## Bayesian-Network Structure Learning

The project explores search methods for Bayesian-network structure learning with an FPGA target.
The software-side work produces deterministic inputs that are easier to validate in simulation and hardware.

## Search Paths

| Path | Role |
| --- | --- |
| Hill climber | Baseline quality and runtime reference. |
| MCMC/order sampler | Candidate hardware search path. |
| Fixed-point scoring | Hardware-oriented approximation study. |

## Fixed-Point Log-Add

The MCMC score accumulation uses a log-add form:

```text
node_score = node_score + log(1 + exp(local_score - node_score))
```

Current software experiments compare floating-point scoring with fixed-point LUT-backed variants.
The piecewise path is the useful hardware candidate: large negative inputs map near zero, while large positive inputs use the identity approximation.
