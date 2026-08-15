# Test-Driven Agent (TDA) Feedback Loop

1. **Subprocess Isolation**: Never trust model self-evaluations; execute real `pytest` exit codes.
2. **Traceback Extraction**: Feed only the concise failure traceback into the next iteration prompt.
3. **Anti-Regression Lock**: Append every discovered bug test permanently to `tests/test_regression.py`.
