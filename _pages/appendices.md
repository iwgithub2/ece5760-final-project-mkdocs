---
layout: page
title: appendices
permalink: /appendices/
description: Code listings, schematics, team contributions, permissions, and references.
nav: true
nav_order: 4
---

## Appendix A: Permissions

#### Project on the Course Page

> The group approves this report for inclusion on the course website.

#### Project on the Course YouTube Channel

> The group approves the video for inclusion on the course youtube channel.

## Code and Hardware Listings

The project code and hardware design files are available in the project repository:

[iwgithub2/ece5760-final-project](https://github.com/iwgithub2/ece5760-final-project)

## External Schematics

No external hardware beyond the DE1-SoC board is currently documented.

TODO: If any external hardware was used, add schematics here.

## Team Contributions

| Team member | Contributions |
| --- | --- |
| Irwin Wang | Worked on software testing, initial baselining, and early experiments used for design decisions. This included evaluating fixed-point formats, LUT size, and the tradeoff between numeric fidelity and FPGA resource usage. He also collected much of the experimental data, wrote an initial draft of the parallelized solver, and wrote the C code used to display the output graph. |
| Joseph Wan | Worked on the overall system design, Quartus integration, and HPS/FPGA bring-up. He wrote much of the C code running on the HPS and spent significant time debugging Platform Designer to integrate the custom IP. He also worked on understanding the Bayesian-network math and tuning parameters to improve final accuracy. |

## References

1. ECE 5760 course materials and DE1-SoC documentation.
2. Intel/Altera Cyclone V and DE1-SoC documentation.
3. Asadi, N. B., Meng, T. H., and Wong, W. H. "Reconfigurable Computing for Learning Bayesian Networks." ACM/SIGDA International Symposium on Field Programmable Gate Arrays, 2008. [https://dl.acm.org/doi/pdf/10.1145/1344671.1344702](https://dl.acm.org/doi/pdf/10.1145/1344671.1344702)
4. bnlearn Bayesian-network datasets and benchmark networks. [https://www.bnlearn.com/](https://www.bnlearn.com/)
5. Background references on Bayesian-network structure learning, MCMC sampling, and Metropolis-Hastings acceptance.
6. ECE 5760 VGA drawing/display support code used for the project display.
