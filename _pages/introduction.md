---
layout: about
title: "ECE 5760: Bayesian-network structure learning on FPGA"
permalink: /
subtitle: By Irwin Wang and Joseph Wan

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false
  more_info: >
    <p>ECE 5760</p>
    <p>Final project notes</p>

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

For our final project in ECE 5760, we focused on accelerating the learning of Bayesian network structures using an FPGA (DE1-SoC platform). Bayesian networks are a foundational (OG) machine learning method that model probabilistic relationships between variables using directed graphs. Despite the rise of modern deep learning approaches, Bayesian networks remain highly relevant due to their interpretability and ability to capture explicit dependencies between real-world variables.

Unlike CNNs or DNNs, which often act as black boxes, Bayesian networks provide a structured and explainable representation of data through conditional relationships. This makes them particularly useful in domains where understanding the underlying system is as important as prediction accuracy. However, learning the optimal graph structure is computationally expensive, making it a strong candidate for hardware acceleration.

In this project, we developed a combined software and hardware pipeline that offloads key computations onto the FPGA. Our system precomputes probabilistic scores and evaluates candidate graph structures efficiently in hardware, enabling faster exploration of the solution space. Users can provide their own datasets, and the system learns a probabilistic graph structure that can be used for inference and analysis.

## Demo

Here is a demonstration of our FPGA-accelerated Bayesian network learning system:

{% include video.liquid path="https://www.youtube.com/embed/dQw4w9WgXcQ" class="img-fluid rounded z-depth-1" %}
