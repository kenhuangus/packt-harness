# Module 1: Why Harness Engineering

## Overview
This module demonstrates why model capability alone does not equal production software reliability.
Formula: **Agent = Model + Harness**

## Key Concepts
1. **The Probabilistic Reasoner**: Models generate text via token probabilities, making them susceptible to hallucinations, context drift, and execution loops.
2. **The Deterministic Harness**: The system scaffolding surrounding the model that enforces path isolation, command sanitization, loop detection, and verification.
3. **The 98% Harness Rule**: Production reliability comes from system scaffolding rather than prompt engineering alone.

## Executable Demo
`harness_vs_model_demo.py` simulates both an un-harnessed model runner (showing failure modes) and a harnessed execution engine (showing deterministic protection).
