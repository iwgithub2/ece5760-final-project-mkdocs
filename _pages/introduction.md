---
layout: introduction
title: "introduction"
permalink: /
subtitle: By Irwin Wang and Joseph Wan

selected_papers: false
social: false

announcements:
  enabled: false
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
  scrollable: true
  limit: 3
---

We built an FPGA-accelerated Bayesian-network structure-learning system that uses software preprocessing and hardware-parallel MCMC scoring to explore probabilistic graph structures faster than a software-only approach.

For our final project in ECE 5760, we focused on accelerating the learning of Bayesian network structures using an FPGA (DE1-SoC platform). Bayesian networks are a foundational (OG) machine learning method that model probabilistic relationships between variables using directed graphs. Despite the rise of modern deep learning approaches, Bayesian networks remain highly relevant due to their interpretability and ability to capture explicit dependencies between real-world variables.

Unlike CNNs or DNNs, which often act as black boxes, Bayesian networks provide a structured and explainable representation of data through conditional relationships. This makes them particularly useful in domains where understanding the underlying system is as important as prediction accuracy. However, learning the optimal graph structure is computationally expensive, making it a strong candidate for hardware acceleration.

In this project, we developed a combined software and hardware pipeline that offloads key computations onto the FPGA. Our system precomputes probabilistic scores and evaluates candidate graph structures efficiently in hardware, enabling faster exploration of the solution space. Users can provide their own datasets, and the system learns a probabilistic graph structure that can be used for inference and analysis.

The ARM Cortex-A9 hard processor system handles dataset preprocessing, candidate parent-set generation, and local-score calculation. The Cyclone V FPGA handles the repeated MCMC proposal and scoring loop, where many node-level compatibility checks and score accumulations can be performed in parallel.

## Demo

Here is a demonstration of our FPGA-accelerated Bayesian network learning system:

<style>
  .intro-video {
    width: 100%;
    aspect-ratio: 16 / 9;
    margin-top: 1.25rem;
    background: #000;
  }

  .intro-video iframe {
    display: block;
    width: 100%;
    height: 100%;
    border: 0;
  }
</style>

<div class="intro-video">
  <iframe
    src="https://www.youtube.com/embed/SyGYvctclgU"
    title="FPGA-accelerated Bayesian network learning demo"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>
