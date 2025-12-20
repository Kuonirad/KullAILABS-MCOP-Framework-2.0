# Bolt's Journal - Critical Learnings

This journal tracks critical performance learnings, bottlenecks, and optimizations.

## 2024-05-22 - [Logging Overhead in Critical Paths]
**Learning:** Expensive computations for debug logs (like JSON.stringify and hashing large arrays) execute even when the log level is higher (e.g., INFO), causing unnecessary CPU waste.
**Action:** Always wrap expensive log payload generation in `if (logger.isLevelEnabled('debug'))` or similar checks.
