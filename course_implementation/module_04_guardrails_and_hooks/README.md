# Module 4: Guardrails & Deterministic Hooks

## Overview
This module implements the 4-layer Defense-in-Depth security and control architecture for AI coding agents.

## 4-Layer Control Architecture
1. **Layer 1: Prompt System Rules** (Soft LLM guidelines)
2. **Layer 2: Tool Argument Schemas** (JSON Schema validation)
3. **Layer 3: Pre/Post Execution Hooks** (Hard process-level interceptors)
4. **Layer 4: OS Sandboxing** (Path traversal block & chroot isolation)
