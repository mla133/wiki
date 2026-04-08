# Retry With Exponential Backoff

tags: [python, networking, reliability]
status: evergreen

## Problem

Retry flaky operations (network calls, IO) without
hammering the service.

## Solution

```python
import time
import random

def retry(fn, retries=5, base_delay=0.5, max_delay=30):
    for attempt in range(retries):
        try:
            return fn()
        except Exception:
            if attempt == retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            delay = min(delay, max_delay)
            delay *= random.uniform(0.8, 1.2)
            time.sleep(delay)
```
