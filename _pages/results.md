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

For the Insurance dataset, both the FPGA/HPS path and the software baseline scale roughly linearly with iteration count on the log-log runtime plot. The FPGA/HPS path remains consistently faster over the measured range. The score convergence plot shows that more iterations improve the FPGA/HPS path substantially at low iteration counts, and the result approaches the software baseline once the number of samples is large enough. The remaining disconnect is likely caused by finite-sample MCMC behavior rather than a fundamentally different scoring objective. The hardware path uses fixed-point arithmetic, a reduced-fidelity lookup table for nonlinear log-space terms, and its own random proposal stream, while the software baseline uses higher-precision arithmetic and a different execution path. At low iteration counts, those small numerical and proposal-order differences can move the sampler through different regions of order space. As the number of samples increases, both paths have more chances to explore high-scoring orders, so the scores move closer together.

{% include figure.liquid path="assets/img/results/parallel_versions_score_convergence.png" class="img-fluid rounded z-depth-1" alt="Parallel versions score convergence" %}

The parallel-version experiment shows the expected behavior for sampling. With small iteration counts, more parallel versions improve the average score because the sampler explores more candidate orders early. At larger iteration counts, the curves converge, meaning the single-chain and multi-chain versions eventually reach similar quality once given enough time. This is useful because it suggests parallelism is most valuable when latency matters or when the sampler cannot run for very long.

## Accuracy

{% include figure.liquid path="assets/img/results/insurance_score_components_4way.png" class="img-fluid rounded z-depth-1" alt="Insurance score components for four-way parallel run" %}

The score-component plot separates recall, precision, and average score for the four-way parallel Insurance run. Recall is the percent of correct edges recovered from the reference graph. Precision is the percent of predicted edges that were actually correct. The average score tracks between recall and precision across the iteration sweep. All three improve sharply from 100 to 5,000 iterations, then flatten, which suggests diminishing returns after the sampler has reached a strong region of the order space.

{% include figure.liquid path="assets/img/results/ml_vs_fixed_software.png" class="img-fluid rounded z-depth-1" alt="ML-pruned candidates versus fixed candidate baseline" %}

The ML-pruned candidate experiment compares the fixed candidate strategy against the best non-fixed strategy in the software measurements. On Asia, ML pruning slightly improved F1 while reducing MCMC runtime. On Insurance, the fixed full-candidate run still had the best F1, but ML pruning greatly reduced runtime and table size. This is a tradeoff rather than a strict win: learned candidate pruning can make scoring much cheaper, but aggressive pruning can remove useful parent sets on larger graphs.

{% include figure.liquid path="assets/img/results/ml_pruning_accuracy_tradeoff.png" class="img-fluid rounded z-depth-1" alt="Accuracy runtime and table size tradeoffs for ML pruning" %}

The broader tradeoff plot shows the same pattern. Smaller ML-pruned tables run faster and use less memory, but their accuracy depends on whether the retained parent sets contain the useful edges. For a small graph like Asia, pruning can preserve or improve accuracy. For the larger Insurance graph, the best accuracy came from a much larger candidate table.

## Safety

The design does not directly actuate external hardware and does not create a physical safety hazard beyond normal DE1-SoC usage. Safety enforcement is mainly through bounded memory access, fixed table sizes, deterministic reset behavior, and validation against software reference outputs.

The main safety constraints are correctness and bounded operation. The HPS limits the number of active nodes and candidate parent sets before writing tables to FPGA memory. The FPGA uses fixed-size BRAM tables and sentinel masks to terminate candidate lists, which avoids unbounded traversal. Reset and start signals are controlled explicitly through memory-mapped registers.

## Usability

The user workflow is split into preprocessing, hardware execution, and result interpretation. The HPS loads the precomputed score table, configures the FPGA with parameters such as seed and iteration count, starts the sampler, and then reads back the best score and topological order. The final order is converted back into a graph in software and displayed through the VGA demo.

Loading a dataset from bnlearn is fairly straightforward because the preprocessing flow can convert a known Bayesian-network dataset into the local parent-set and score tables needed by the hardware. The harder part is getting both high accuracy and low latency. MCMC is a limiting technique by itself because it depends on enough random proposals to explore the order space well. If the iteration budget is small, the sampler may return quickly but miss better network structures; if the iteration budget is large, accuracy improves but latency rises. In practice, usability depends on tuning the candidate-parent limit, score-table size, lookup-table fidelity, and number of parallel chains for the dataset being tested.

## Resource Utilization

{% include figure.liquid path="assets/img/results/resource_utilization_parallel_configs.png" class="img-fluid rounded z-depth-1" alt="Resource utilization across parallel hardware configurations" %}

The area data shows the hardware cost of parallelism. The one-chain design uses 37% ALM utilization and 52% LAB utilization, while the four-chain design reaches 90% ALM utilization and 100% LAB utilization. This explains why the final design must balance parallelism against available FPGA fabric.

M10K block usage was another hard limit. The one-chain, 32-bit by 1024-entry configuration used 204 of 397 M10K blocks, or 51% of the device. The two-chain version with the same 32-bit by 1024-entry lookup-table depth used 396 of 397 M10K blocks, effectively filling block memory. To reach three or four parallel chains, the design had to reduce lookup-table fidelity and memory footprint. The four-chain configuration used a 16-bit by 512-entry table and fit at 336 of 397 M10K blocks, or 85%. This means parallelization was constrained by memory as much as by logic: more chains required a smaller and lower-precision LUT, which helps fit the FPGA but also contributes to the accuracy gap between hardware and software.

{% include figure.liquid path="assets/img/results/alm_component_breakdown.png" class="img-fluid rounded z-depth-1" alt="ALM component breakdown across hardware configurations" %}

The ALM breakdown shows that LUT logic is the dominant contributor, with registers and combined LUT/register usage also increasing as more chains are added. The result is consistent with the design: parallel scoring replicates compatibility logic, accumulators, and control state.

## Conclusions

### Expectations Versus Results

The results mostly matched the original expectation. The project was based on the idea that Bayesian-network structure learning has a software-friendly preprocessing stage and a hardware-friendly repeated scoring stage. The timing data supports that split: the FPGA path achieved a 37.9x speedup on the measured end-to-end timing comparison, and the runtime-scaling plots show that the accelerated path remains faster across iteration counts.

The main limitation is resource pressure. Parallelism improves early convergence and reduces latency, but it consumes FPGA fabric quickly. The four-chain design nearly fills the device, so future versions would need more careful sharing, pipelining, or memory layout improvements to scale beyond the tested configuration.

The ML-based pruning results were mixed but useful. Candidate pruning can reduce runtime and memory size dramatically, especially when using mutual information or ensemble rankers to keep only promising parent sets. However, the Insurance results show that pruning can also reduce final graph quality if important parent sets are removed. A future design could use adaptive pruning or dataset-specific candidate limits instead of one fixed policy.

If we were doing the project again, we would think about scaling and modularity much earlier. Getting the full software-to-hardware path working was already difficult, and the original design had to be modified before parallelization could work cleanly. The final results also show that parallelization is not a complete solution: it helps most when the iteration count is small, but the benefit shrinks as the chains converge toward similar scores. A next version should focus on making the sampler easier to scale, improving the proposal strategy, and reducing memory pressure rather than only adding more replicated chains.

### Standards

The design follows the normal ECE 5760 DE1-SoC hardware/software conventions: memory-mapped HPS-to-FPGA communication, synchronous Verilog/SystemVerilog hardware, fixed reset behavior, and explicit register-level control from software. Numeric values are represented in fixed-point log space so that the FPGA can replace repeated probability multiplications with additions and lookup-table approximations. Dataset handling follows the bnlearn-style benchmark workflow: the software preprocessing step converts a named dataset into fixed-size score tables before hardware execution.

### Intellectual Property Considerations

We did not reuse outside code or another complete design for the Bayesian-network MCMC accelerator or preprocessing pipeline. The only borrowed course code was ECE 5760 VGA drawing/display support. The project used the standard Intel/Altera DE1-SoC toolchain and platform components available for the course board, but it did not rely on a confidential third-party design or sample part. No nondisclosure agreement was required.

The project is not reverse engineering an existing commercial design. Bayesian-network structure learning, MCMC sampling, fixed-point arithmetic, and FPGA acceleration are all established ideas in the literature, including prior work on reconfigurable computing for Bayesian networks. We are not aware of a specific patent opportunity from this course implementation. The main intellectual-property concern is citation and attribution, so the report references the background papers, bnlearn dataset source, vendor documentation, and ECE 5760 course material used for context or support code.
