# Module 6: Tests as the Reliability Layer

## Overview
This module demonstrates the Test-Driven Agent (TDA) execution loop and anti-regression safeguards.

## Core Concepts
1. **The TDA Loop**: Write/Identify failing tests -> Agent generates code -> Run test suite -> Feed traceback back -> Repair autonomously.
2. **Traceback Extraction**: Automatically capture stdout/stderr from test runners without manual copy-pasting.
3. **Anti-Regression Pipeline**: Every agent bug yields a permanent unit test added to the regression test suite.
