---
layout: page
title: results
permalink: /results/
description: Test data, performance, accuracy, safety, and usability.
nav: true
nav_order: 4
---

## Test Data and Waveforms

TODO: Add all relevant test data, simulation output, scope traces, waveforms, screenshots, and plots.

Suggested evidence:

- software reference score versus FPGA score
- proposal acceptance trace
- MCMC convergence behavior
- fixed-point error measurements
- resource utilization summary
- timing report summary

## Speed of Execution

TODO: Add measured runtime and throughput.

Report:

- software-only baseline runtime
- FPGA-accelerated runtime
- speedup
- clock frequency
- cycles per proposal or proposals per second
- any observed hesitation, flicker, concurrency, or interactivity concerns

## Accuracy

TODO: Add numeric accuracy results.

Report:

- fixed-point versus floating-point score error
- final graph/order agreement versus software reference
- acceptance-rate differences
- sensitivity to LUT width, LUT range, and fixed-point format

## Safety

The design does not directly actuate external hardware and does not create a physical safety hazard beyond normal DE1-SoC usage. Safety enforcement is mainly through bounded memory access, fixed table sizes, deterministic reset behavior, and validation against software reference outputs.

TODO: Add any project-specific safety constraints, input validation, or failure handling.

## Usability

TODO: Describe how users run the preprocessing, load the FPGA tables, start the sampler, and interpret the output.

Include:

- required input dataset format
- setup steps
- expected outputs
- known limitations
- what another user found easy or confusing
