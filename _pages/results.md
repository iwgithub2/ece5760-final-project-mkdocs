---
layout: page
title: results and conclusions
permalink: /results/
description: Test data, performance, accuracy, safety, usability, and conclusions.
nav: true
nav_order: 3
---

## Test Data and Waveforms

The figures below summarize the timing, accuracy, and FPGA resource results from the final project measurements.

{% include figure.liquid path="assets/img/results/overall_sw_vs_fpga_speedup.png" class="img-fluid rounded z-depth-1" alt="Software versus FPGA execution time" %}

The end-to-end run measured in the timing sheet shows a large speedup from moving the repeated MCMC scoring loop to the FPGA path. The software baseline took 10.6 seconds, while the FPGA run took 0.28 seconds, corresponding to a 37.9x speedup. This supports the main design premise: the scoring loop is regular and parallel enough to benefit from hardware acceleration.

## Speed of Execution

{% include figure.liquid path="assets/img/results/insurance_runtime_score_convergence.png" class="img-fluid rounded z-depth-1" alt="Insurance runtime and score convergence" %}

For the Insurance dataset, both the FPGA/HPS path and the software baseline scale roughly linearly with iteration count on the log-log runtime plot. The FPGA/HPS path remains consistently faster over the measured range. The score convergence plot shows that more iterations improve the FPGA/HPS path substantially at low iteration counts, and the result approaches the software baseline once the number of samples is large enough.

{% include figure.liquid path="assets/img/results/parallel_versions_score_convergence.png" class="img-fluid rounded z-depth-1" alt="Parallel versions score convergence" %}

The parallel-version experiment shows the expected behavior for sampling. With small iteration counts, more parallel versions improve the average score because the sampler explores more candidate orders early. At larger iteration counts, the curves converge, meaning the single-chain and multi-chain versions eventually reach similar quality once given enough time. This is useful because it suggests parallelism is most valuable when latency matters or when the sampler cannot run for very long.

## Accuracy

{% include figure.liquid path="assets/img/results/insurance_score_components_4way.png" class="img-fluid rounded z-depth-1" alt="Insurance score components for four-way parallel run" %}

The score-component plot separates the three score columns from the spreadsheet for the four-way parallel Insurance run. Score 3 is treated as the average score because it tracks between score 1 and score 2 across the iteration sweep. All three scores improve sharply from 100 to 5,000 iterations, then flatten, which suggests diminishing returns after the sampler has reached a strong region of the order space.

{% include figure.liquid path="assets/img/results/ml_vs_fixed_software.png" class="img-fluid rounded z-depth-1" alt="ML-pruned candidates versus fixed candidate baseline" %}

The ML-pruned candidate experiment compares the fixed candidate strategy against the best non-fixed strategy in the software measurements. On Asia, ML pruning slightly improved F1 while reducing MCMC runtime. On Insurance, the fixed full-candidate run still had the best F1, but ML pruning greatly reduced runtime and table size. This is a tradeoff rather than a strict win: learned candidate pruning can make scoring much cheaper, but aggressive pruning can remove useful parent sets on larger graphs.

{% include figure.liquid path="assets/img/results/ml_pruning_accuracy_tradeoff.png" class="img-fluid rounded z-depth-1" alt="Accuracy runtime and table size tradeoffs for ML pruning" %}

The broader tradeoff plot shows the same pattern. Smaller ML-pruned tables run faster and use less memory, but their accuracy depends on whether the retained parent sets contain the useful edges. For a small graph like Asia, pruning can preserve or improve accuracy. For the larger Insurance graph, the best accuracy came from a much larger candidate table.

## Safety

The design does not directly actuate external hardware and does not create a physical safety hazard beyond normal DE1-SoC usage. Safety enforcement is mainly through bounded memory access, fixed table sizes, deterministic reset behavior, and validation against software reference outputs.

The main safety constraints are correctness and bounded operation. The HPS limits the number of active nodes and candidate parent sets before writing tables to FPGA memory. The FPGA uses fixed-size BRAM tables and sentinel masks to terminate candidate lists, which avoids unbounded traversal. Reset and start signals are controlled explicitly through memory-mapped registers.

## Usability

The user workflow is split into preprocessing, hardware execution, and result interpretation. The HPS loads the precomputed score table, configures the FPGA with parameters such as seed and iteration count, starts the sampler, and then reads back the best score and topological order. The final order is converted back into a graph in software and displayed through the VGA demo.

TODO: Add exact command-line usage and input dataset format.

## Resource Utilization

{% include figure.liquid path="assets/img/results/resource_utilization_parallel_configs.png" class="img-fluid rounded z-depth-1" alt="Resource utilization across parallel hardware configurations" %}

The area data shows the hardware cost of parallelism. The one-chain design uses 37% ALM utilization and 52% LAB utilization, while the four-chain design reaches 90% ALM utilization and 100% LAB utilization. This explains why the final design must balance parallelism against available FPGA fabric.

{% include figure.liquid path="assets/img/results/alm_component_breakdown.png" class="img-fluid rounded z-depth-1" alt="ALM component breakdown across hardware configurations" %}

The ALM breakdown shows that LUT logic is the dominant contributor, with registers and combined LUT/register usage also increasing as more chains are added. The result is consistent with the design: parallel scoring replicates compatibility logic, accumulators, and control state.

## Conclusions

### Expectations Versus Results

The results mostly matched the original expectation. The project was based on the idea that Bayesian-network structure learning has a software-friendly preprocessing stage and a hardware-friendly repeated scoring stage. The timing data supports that split: the FPGA path achieved a 37.9x speedup on the measured end-to-end timing comparison, and the runtime-scaling plots show that the accelerated path remains faster across iteration counts.

The main limitation is resource pressure. Parallelism improves early convergence and reduces latency, but it consumes FPGA fabric quickly. The four-chain design nearly fills the device, so future versions would need more careful sharing, pipelining, or memory layout improvements to scale beyond the tested configuration.

The ML-based pruning results were mixed but useful. Candidate pruning can reduce runtime and memory size dramatically, especially when using mutual information or ensemble rankers to keep only promising parent sets. However, the Insurance results show that pruning can also reduce final graph quality if important parent sets are removed. A future design could use adaptive pruning or dataset-specific candidate limits instead of one fixed policy.

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
