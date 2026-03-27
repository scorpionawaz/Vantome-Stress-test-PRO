# 📊 CyberMedic Pro Dashboard - Visual Guide

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ⚡ CYBERMEDIC PRO                                 │
│    Advanced Chaos Engineering & Performance Analysis Dashboard       │
│                                                                      │
│     ● EXCELLENT        ● Uptime: 2m 45s                            │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 🔥 CPU STRESS TESTS                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────┐                          │
│ │ ⚡ EXTREME CPU   │  │ 🔥 EXTREME       │                          │
│ │ Spike (45s)      │  │ Extended Load    │                          │
│ │ Maximum intensity│  │ 2-minute stress  │                          │
│ │ [IGNITE]         │  │ [START EXTREME]  │                          │
│ └──────────────────┘  └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 💾 MEMORY STRESS TESTS                                              │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│ │ 💧 Memory Leak   │  │ 🔴 Aggressive    │  │ 🧹 Clear Memory  │   │
│ │ 100MB per call   │  │ 500MB spike      │  │ Free all         │   │
│ │ [LEAK 100MB]     │  │ [SPIKE 500MB]    │  │ [FREE ALL]       │   │
│ └──────────────────┘  └──────────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ⏱️ LATENCY & TIMEOUT TESTS                                          │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────┐                          │
│ │ 🕐 Timeout       │  │ 🌊 Cascading     │                          │
│ │ 15s hang         │  │ 20 concurrent    │                          │
│ │ [SIMULATE]       │  │ [CASCADE]        │                          │
│ └──────────────────┘  └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 📊 LIVE METRICS & PERFORMANCE ANALYSIS                              │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│ │ Memory       │  │ Active Leaks │  │ CPU Spikes   │  │ Crashes  │ │
│ │ 2.5 MB       │  │ 0 chunks     │  │ 1 event      │  │ 0        │ │
│ └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │
│                                                                      │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│ │ Avg Response │  │ Crash Recov  │  │ System Load  │  │ Stability│ │
│ │ 45 ms        │  │ 100 %        │  │ 5.2 %        │  │ 100 %    │ │
│ └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘ │
│                                                                      │
│ ┌─ Response Log ──────────────────────────────────────────────────┐ │
│ │ [14:32:45] ✓ /simulate/cpu-spike - Response: 200 in 2ms       │ │
│ │ [14:33:12] ✓ /metrics - Response: 200 in 45ms                 │ │
│ │ [14:34:01] ✓ /simulate/timeout - Response: 202 in 15023ms     │ │
│ │ [14:34:56] ✗ /simulate/crash - Error: 500 in 8ms              │ │
│ │ [14:35:10] ✓ /metrics - Response: 200 in 52ms                 │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Performance Rating Guide

### EXCELLENT (Green) ✓
```
Criteria:
  - Avg Latency: < 100ms
  - Crash Recovery: > 95%
  - System Load: < 30%
  - Stability: > 80%
  
What it means:
  ✓ System is healthy
  ✓ Responsive (fast latency)
  ✓ No crashes
  ✓ Good resource usage
  
Example:
  ● EXCELLENT
  Avg Response: 45ms
  Crash Recovery: 100%
  System Load: 5%
  Stability: 100%
```

### GOOD (Light Green) ✓
```
Criteria:
  - Avg Latency: 100-500ms
  - Crash Recovery: 80-95%
  - System Load: 30-60%
  - Stability: 60-80%
  
What it means:
  ✓ System is operational
  ~ Some latency visible
  ~ Minor crashes or resource issues
  
Example:
  ● GOOD
  Avg Response: 250ms
  Crash Recovery: 92%
  System Load: 45%
  Stability: 75%
```

### FAIR (Yellow) ≈
```
Criteria:
  - Avg Latency: 500-1000ms
  - Crash Recovery: 60-80%
  - System Load: 60-85%
  - Stability: 40-60%
  
What it means:
  ~ System is degraded
  ~ Noticeable latency
  ~ Frequent issues
  ~ Approaching limits
  
Example:
  ≈ FAIR
  Avg Response: 750ms
  Crash Recovery: 75%
  System Load: 72%
  Stability: 55%
```

### POOR (Orange) ✗
```
Criteria:
  - Avg Latency: 1000-5000ms
  - Crash Recovery: 40-60%
  - System Load: 85-95%
  - Stability: 20-40%
  
What it means:
  ✗ System is struggling
  ✗ Severe latency
  ✗ Multiple failures
  ✗ Critical issues building
  
Example:
  ✗ POOR
  Avg Response: 2500ms
  Crash Recovery: 50%
  System Load: 92%
  Stability: 35%
```

### CRITICAL (Red) ✗
```
Criteria:
  - Avg Latency: > 5000ms
  - Crash Recovery: < 40%
  - System Load: > 95%
  - Stability: < 20%
  
What it means:
  ✗ System is failing
  ✗ Extreme latency
  ✗ Majority of requests fail
  ✗ Immediate intervention needed
  
Example:
  ✗ CRITICAL
  Avg Response: 8500ms
  Crash Recovery: 25%
  System Load: 98%
  Stability: 15%
```

---

## 📈 Metric Explanations

### 1. Memory Allocated
```
What: Total RAM used by stress testing
Range: 0 MB → 4000 MB (4GB)
Increases when:
  - Click "LEAK 100MB" (adds 100MB)
  - Click "SPIKE 500MB" (adds 500MB)
Decreases when:
  - Click "FREE ALL"
Affects: Stability, System Load
```

### 2. Active Leaks
```
What: Number of memory chunks retained
Range: 0 → ∞ (until OOM)
One chunk = 100MB (or 500MB for spike)
When = 10: 1000MB allocated
When = 20: 2000MB allocated
Indicates: How many memory leak events have occurred
```

### 3. CPU Spikes
```
What: Total CPU stress events triggered
Range: 0 → ∞
Increases when:
  - Click "IGNITE CPU SPIKE"
  - Click "START EXTREME LOAD"
  - Click "LAUNCH CHAOS"
Does NOT directly affect score
Informational: Shows stress test history
```

### 4. Crash Events
```
What: Total HTTP 500 errors
Range: 0 → ∞
Increases when:
  - Click "FORCE CRASH"
  - Click "TRIGGER CRASHES"
  - Memory runs out
  - System becomes unstable
Major impact: Reduces crash recovery rate & stability
```

### 5. Avg Response Time (ms)
```
Calculation: Average of last 50 response times
Range: 0 → 10000+ ms
Good: < 100ms (EXCELLENT)
Fair: 100-500ms (GOOD)
Poor: 500-1000ms (FAIR)
Critical: > 1000ms (POOR/CRITICAL)

Example timeline:
  Normal: 45ms (no stress)
  + CPU spike: 50ms (minimal impact)
  + Memory leak: 150ms (noticeable)
  + Timeout test: 5000ms (when timeout active)
  + Multiple tests: 1000ms+ (combined impact)
```

### 6. Crash Recovery Rate (%)
```
Calculation: (Successful requests / Total requests) × 100%
Range: 0-100%
Excellent: > 95%
Good: 80-95%
Fair: 60-80%
Poor: 40-60%
Critical: < 40%

Example:
  Total requests: 20
  Successful: 20
  Crashes: 0
  Recovery rate: 20/20 = 100%
  
Then force crash:
  Total requests: 21
  Successful: 20
  Crashes: 1
  Recovery rate: 20/21 = 95.2%
```

### 7. System Load Index (%)
```
Calculation: (Memory/4096 × 50) + (Latency/100 × 30) + (Crashes × 5)
Range: 0-100%
Capped at 100%

Example calculation:
  Memory: 2GB of 4GB = 50% × 50 = 25 points
  Latency: 500ms / 100 × 30 = 150 points (capped at 100)
  Crashes: 3 × 5 = 15 points
  Total: min(100, 190) = 100 = CRITICAL

Breaking it down:
  Memory stress: 50% weight
  Latency stress: 30% weight
  Crash stress: 20% weight
```

### 8. Stability Score (%)
```
Calculation:
  Start with 100
  - 10 if avg latency > 50ms
  - 20 if memory > 500MB
  - 30 if any crashes
  
Range: 0-100%
Safe: > 80%
Acceptable: 60-80%
Degraded: 40-60%
Critical: < 40%

Example breakdown:
  Healthy: 100% (no penalties)
  + Small latency: 90% (-10)
  + High memory: 70% (-20)
  + One crash: 40% (-30)
```

---

## 🧪 Real-World Scenarios

### Scenario 1: Initial State
```
Performance: ● EXCELLENT
Memory: 0 MB
CPU Spikes: 0
Crashes: 0
Avg Latency: ~50ms (network only)
Crash Recovery: 100%
System Load: 2%
Stability: 100%
```

### Scenario 2: After CPU Spike (45s)
```
[During test]
- Avg latency: ~60ms (slightly higher)
- System load: 95% (CPU at max)
- Stability: 95% (minor impact)

[After 45 seconds]
- System recovers
- Performance returns to EXCELLENT
- Shows resilience
```

### Scenario 3: Memory Leak (10× calls)
```
Memory: 100MB × 10 = 1000MB (1GB)
Active Leaks: 10
Avg Latency: 150-200ms (memory pressure)
System Load: 30% (memory × 50 / 4096)
Stability: 80-85%
Performance: GOOD → FAIR (as it grows)
```

### Scenario 4: Timeout Cascade
```
During cascade (20 requests hanging):
- Avg latency: 20000+ms (timeout is 15-20s)
- Multiple timeouts increase latency massively
- System load: Increases due to latency
- Stability: Decreases
- Performance drops from EXCELLENT → GOOD

After cascade ends:
- Latency normalizes (moving average)
- Performance recovers
- Shows system can recover from timeouts
```

### Scenario 5: Force Crash
```
Single crash:
- Crashes: 1
- Crash recovery rate: 95-98%
- Stability: -30 = ~70%
- Performance: EXCELLENT → GOOD

Multiple crashes:
- Each crash: -30 stability
- 3 crashes: Stability ~10%
- Recovery rate: 70-80%
- Performance: CRITICAL
```

### Scenario 6: Full Chaos Mode
```
Simultaneous stress (CPU + Memory + Latency):
- Memory: 300MB
- Latency: 5000+ms
- Crashes: Multiple
- CPU: 100%

Result:
- Stability: < 20%
- System load: 99%
- Avg latency: 1000-3000ms
- Crash recovery: 50-70%
- Performance: CRITICAL

Shows complete system failure
```

---

## 🎨 Color Coding

| Metric | Color | Meaning |
|--------|-------|---------|
| **Green** (#00ff41) | Excellent | System is healthy |
| **Light Green** (#00ff88) | Good | Acceptable performance |
| **Yellow** (#ffaa00) | Fair | Degraded but operational |
| **Orange** (#ff6600) | Poor | Severe issues |
| **Red** (#ff0055) | Critical | System failing |
| **Cyan** (#00d9ff) | Primary | Active/highlighted |

---

## 📊 How to Interpret the Log

Each log entry shows:
```
[HH:MM:SS] [ICON] MESSAGE

Icons:
  ✓ = Success (green)
  ✗ = Error (red)
  ● = Info (yellow)

Example:
  [14:32:45] ✓ /simulate/cpu-spike - Response: 200 in 2ms
    ├─ Time: 14:32:45 (2:32:45 PM)
    ├─ Status: ✓ Success
    ├─ Endpoint: /simulate/cpu-spike
    ├─ HTTP Code: 200 (OK)
    └─ Duration: 2ms (very fast)

  [14:34:56] ✗ /simulate/crash - Error: 500 in 8ms
    ├─ Time: 14:34:56
    ├─ Status: ✗ Error
    ├─ Endpoint: /simulate/crash
    ├─ HTTP Code: 500 (Server Error)
    └─ Duration: 8ms (intentional crash, still fast)
```

---

## 🎯 Performance Rating Thresholds

```
Score Calculation:
  base_score = 100
  
  if (avgLatency > 0ms):
    score -= min(50, (avgLatency / 100) * 10)
  
  if (memory > 1000MB):
    score -= min(30, (memory / 1000) * 15)
  
  if (crashes > 0):
    score -= crashes * 15
  
  final_score = max(0, min(100, score))

Rating thresholds:
  85+ = EXCELLENT
  70-84 = GOOD
  50-69 = FAIR
  25-49 = POOR
  0-24 = CRITICAL
```

---

## 💡 Tips for Interpreting Results

1. **Check Baseline First**
   - Open dashboard fresh
   - Note the EXCELLENT rating
   - This is your "healthy" reference point

2. **Run Tests One at a Time**
   - Trigger CPU spike
   - Wait for it to complete
   - Check metrics
   - Clear memory if needed
   - Repeat with different test

3. **Watch the Trend**
   - Don't focus on single value
   - Watch how metrics change
   - See if system recovers

4. **Compare Performance**
   - Before vs during stress
   - During vs after stress
   - Shows recovery capability

5. **Identify Weak Points**
   - Which stress causes biggest impact?
   - How long does recovery take?
   - Does system eventually stabilize?

---

## 🚀 Dashboard Auto-Updates

The dashboard **automatically refreshes**:
- Metrics: Every 3 seconds
- Uptime: Every 1 second
- Performance rating: Real-time (when metrics change)
- Log entries: Immediately when action triggered

**No manual refresh needed!**

---

Happy Chaos Testing! ⚡🔥💥
