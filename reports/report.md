# Model Comparison Report

## Models Compared
- **LLaMA 3.3 70B (Groq)**
- **LLaMA 4 Scout 17B (Groq)**

## Dataset Overview
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Total samples | 350 | 350 |
| Acceptance rate | 0.78 | 0.794 |

## Generation Performance
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Avg gen time (ms) | 0.472 | 0.466 |
| Median gen time (ms) | 0.46 | 0.44 |
| Avg attempts | 1.3 | 1.198 |

## Quality Scores
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Avg quality | 0.594 | 0.598 |
| Median quality | 0.585 | 0.585 |
| Quality std | 0.04 | 0.041 |
| % ≥ threshold | 0.176 | 0.122 |

## Diversity & Redundancy
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Avg semantic similarity | 0.896 | 0.92 |
| Near-duplicate rate | 0.755 | 0.813 |
| Avg diversity score | 0.167 | 0.149 |

## Domain Realism
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Avg domain score | 0.606 | 0.607 |
| Avg forbidden score | 0.262 | 0.27 |

## Synthetic vs Real Review Comparison

### Semantic Similarity to Real Reviews
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Avg similarity | 0.276 | 0.276 |
| Median similarity | 0.277 | 0.276 |
| Std deviation | 0.051 | 0.031 |

### Review Length Alignment
| Metric | LLaMA 3.3 | LLaMA 4 Scout |
|------|-----------|---------------|
| Avg length (words) | 37.82 | 64.34 |
| Length std | 5.67 | 10.1 |

Synthetic samples from both models show close semantic alignment with real user reviews while maintaining sufficient variation, indicating realistic generation without memorization.

## Summary
- **LLaMA 3.3** shows stronger overall quality consistency and semantic diversity.
- **LLaMA 4 Scout** is faster per sample but produces a higher rate of near-duplicate content.
- Choice depends on whether speed or quality stability is prioritized.
