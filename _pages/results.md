---
layout: page
title: results and conclusions
permalink: /results/
description: Test data, performance, accuracy, safety, usability, and conclusions.
nav: true
nav_order: 3
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

## Conclusions

### Expectations Versus Results

TODO: Analyze how well the final design met expectations.

Discuss:

- whether FPGA acceleration improved the bottleneck
- whether fixed-point scoring was accurate enough
- whether the system scaled as expected
- what you would do differently next time

### Standards

TODO: State applicable standards or conventions.

Possible items:

- Verilog/SystemVerilog coding conventions
- Avalon/MM or HPS/FPGA interface conventions, if used
- fixed-point numeric format conventions
- dataset/file-format conventions

### Intellectual Property Considerations

TODO: Complete final IP analysis.

Questions to answer:

- Did the project reuse code or another design?
- Did it use Intel/Altera IP?
- Did it use public-domain or open-source code?
- Was anything reverse engineered?
- Were any patent or trademark issues relevant?
- Was any nondisclosure agreement required?
- Are there patent opportunities?
