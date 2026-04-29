---
layout: page
title: implementation
permalink: /implementation/
description: Preprocessing outputs and hardware boundary.
nav: true
nav_order: 2
---

## Preprocessing

The preprocessing step builds parent-set and local-score tables for FPGA-side sampling.

```sh
uv run python preprocess_bn.py \
  --data cleaned-datasets/asia_samples.csv \
  --output-dir out_bn_tables \
  --target-type discrete \
  --max-parent-size 4 \
  --max-candidates-per-node 10 \
  --bootstrap-iters 20 \
  --min-stability-frequency 0.3 \
  --score bdeu \
  --equivalent-sample-size 1.0 \
  --fixed-point q16.16 \
  --emit-hex
```

## Outputs

| Output | Description |
| --- | --- |
| `parent_sets.bin` | Packed parent-set masks. |
| `local_scores.bin` | Signed fixed-point local scores. |
| `node_offsets.json` | Node offsets, counts, names, and score scaling. |
| `config_used.json` | Reproducibility config. |
| `readable_debug.csv` | Human-readable table dump. |
| `parent_sets.hex` | Optional FPGA memory-init text. |
| `local_scores.hex` | Optional FPGA memory-init text. |

## Boundary

The preprocessing path emits tables for the FPGA sampler.
It does not itself implement the FPGA MCMC/order sampler.
