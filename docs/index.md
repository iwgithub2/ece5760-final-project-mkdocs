# ECE 5760 Final Project

Static project website for Bayesian-network structure learning on FPGA.

## Project Focus

This site tracks the final project notes, implementation status, and reproducible build/update steps.
Edit the Markdown files in this repository to update the website.

## Current Tracks

- Hill-climber baseline for comparison.
- MCMC/order-sampler variant for FPGA-oriented search.
- Deterministic preprocessing for parent-set and local-score tables.
- Fixed-point scoring experiments for hardware-friendly log-add behavior.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `docs/` | Markdown source pages. |
| `mkdocs.yml` | Site config, theme, navigation. |
| `.github/workflows/run-mkdocs.yml` | GitHub Pages build/deploy workflow. |
| `site/` | Local build output, ignored by git. |

## Fast Local Preview

```sh
uv run --with mkdocs==1.6.1 mkdocs serve
```
