# Loop Detection Algorithm Guide

When an agent encounters recurring failures, it often attempts the identical command repeatedly:

1. **Sliding Window**: Maintain `command_history = deque(maxlen=N)` where $N = \text{max\_retries}$ (default: 2 or 3).
2. **Homogeneity Check**: If $\text{len}(\text{set}(\text{recent})) == 1$, trigger circuit breaker.
3. **Recovery**: Force LLM to switch tools (e.g. read source code or test traceback) instead of retrying shell execution.
