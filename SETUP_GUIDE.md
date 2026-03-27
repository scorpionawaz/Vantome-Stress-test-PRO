# 🚀 CyberMedic Chaos Dashboard - Setup & Testing Guide

## 📋 Prerequisites

```bash
pip install flask
# Optional but recommended for production:
pip install gunicorn
```

## 📁 File Structure

```
project/
├── stress_app.py          # Main Flask application
└── templates/
    └── index.html         # Web UI dashboard
```

## 🏃 Running the Application

### Option 1: Development Server (Single-threaded - Limited stress)
```bash
python stress_app.py
```
Visit: `http://localhost:8080/ui`

### Option 2: Production Server (Multi-worker - RECOMMENDED for real stress)
```bash
gunicorn --workers 4 --threads 4 --worker-class gthread -b 0.0.0.0:8080 stress_app:app
```

### Option 3: Docker (for isolated testing)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY stress_app.py .
COPY templates/ templates/
CMD ["gunicorn", "--workers", "4", "--threads", "4", "--worker-class", "gthread", "-b", "0.0.0.0:8080", "stress_app:app"]
```

```bash
docker build -t cybermedic .
docker run -p 8080:8080 --memory=4g cybermedic
```

---

## 🎯 Testing Each Stress Vector

### **1️⃣ CPU STRESS**

#### Test CPU Spike (45 seconds)
```bash
# Via UI: Click "Trigger CPU Spike"
# Via CLI:
curl http://localhost:8080/simulate/cpu-spike

# Monitor in real-time (Linux/Mac):
watch -n 1 "top -b -n 1 | head -20"

# Or use the metrics endpoint:
watch -n 1 "curl -s http://localhost:8080/metrics | python -m json.tool"
```

**Expected Results:**
- ✅ CPU usage jumps to 100%
- ✅ All cores show activity
- ✅ Returns immediately (async)
- ⏱️ Duration: 45 seconds

#### Test Extended CPU Load (120 seconds)
```bash
curl http://localhost:8080/simulate/cpu-spike-long
```

---

### **2️⃣ MEMORY STRESS**

#### Test Memory Leak (100MB per call)
```bash
# Single call
curl http://localhost:8080/simulate/memory-leak

# Multiple calls to accumulate
for i in {1..10}; do
  curl http://localhost:8080/simulate/memory-leak
  echo "Call $i: allocated $((i * 100))MB"
  sleep 1
done

# Monitor memory usage:
watch -n 1 "free -h"

# Check metrics:
curl http://localhost:8080/metrics | python -m json.tool
```

**Expected Results:**
- ✅ Memory increases by ~100MB per call
- ✅ Memory is retained (not released)
- ✅ Eventually triggers OOM if repeated enough

#### Test Aggressive Memory Spike (500MB)
```bash
curl http://localhost:8080/simulate/memory-spike
```

#### Clear Memory Between Tests
```bash
curl http://localhost:8080/simulate/memory-leak/clear
```

---

### **3️⃣ LATENCY STRESS**

#### Test Single Timeout (15 seconds)
```bash
curl http://localhost:8080/simulate/timeout
# This will hang for 15 seconds before returning

# In another terminal, measure response time:
time curl http://localhost:8080/simulate/timeout
```

#### Test Cascading Timeouts (20 concurrent hangs)
```bash
# Spawns 20 requests that all hang for 20 seconds
curl http://localhost:8080/simulate/timeout-cascade

# Try to hit other endpoints while cascade is running:
for i in {1..5}; do
  curl http://localhost:8080/ &
done
# Notice other requests will queue up
```

**Expected Results:**
- ✅ High average latency
- ✅ Response times 15-20+ seconds
- ✅ Connection pool exhaustion
- ✅ Cascading failures if repeated

---

### **4️⃣ ERROR & CRASH TESTS**

#### Test Runtime Crash (HTTP 500)
```bash
curl http://localhost:8080/simulate/crash
# Returns: HTTP 500 with ZeroDivisionError traceback

# Check logs for error:
# You should see: ZeroDivisionError: division by zero
```

#### Test Crash Series (3 sequential crashes)
```bash
curl http://localhost:8080/simulate/crash-series
# Queues 3 crashes over 10 seconds

# Monitor logs to see them happen
tail -f app.log
```

---

### **5️⃣ FULL CHAOS MODE**

#### Launch Complete System Stress
```bash
curl http://localhost:8080/simulate/full-chaos

# This simultaneously triggers:
# - 60 second CPU stress
# - 300MB memory allocation
# - Multiple timeouts

# Monitor all metrics:
watch -n 2 "curl -s http://localhost:8080/metrics | python -m json.tool"
```

---

## 📊 Monitoring & Metrics

### View Current Metrics
```bash
curl http://localhost:8080/metrics | python -m json.tool
```

### Example Output:
```json
{
  "timestamp": "2024-01-20T15:30:45.123456",
  "memory": {
    "total_allocated_mb": 300.5,
    "leak_chunks": 3,
    "max_per_chunk_mb": 100
  },
  "events": {
    "cpu_spike_count": 2,
    "memory_leak_count": 5,
    "crash_count": 1,
    "timeout_count": 3
  },
  "active_processes": 4
}
```

### View Service Status
```bash
curl http://localhost:8080/status | python -m json.tool
```

### Health Check
```bash
curl http://localhost:8080/
```

---

## 🔧 Advanced Testing

### Using Apache Bench for Load Testing
```bash
# Install: apt-get install apache2-utils

# Test CPU spike endpoints:
ab -n 10 -c 5 http://localhost:8080/simulate/cpu-spike

# Concurrent memory leak calls:
ab -n 20 -c 10 http://localhost:8080/simulate/memory-leak
```

### Using GNU Parallel for Concurrent Calls
```bash
# Install: apt-get install parallel

# Trigger 10 concurrent CPU spikes:
seq 1 10 | parallel "curl http://localhost:8080/simulate/cpu-spike"

# Cascade 20 timeout requests:
seq 1 20 | parallel "curl http://localhost:8080/simulate/timeout"
```

### Using Python for Stress Testing
```python
import requests
import concurrent.futures
import time

def stress_cpu():
    return requests.get('http://localhost:8080/simulate/cpu-spike')

def stress_memory():
    return requests.get('http://localhost:8080/simulate/memory-leak')

# Concurrent CPU stress
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for i in range(10):
        executor.submit(stress_cpu)

print("CPU stress initiated")
time.sleep(50)

# Check metrics
metrics = requests.get('http://localhost:8080/metrics').json()
print(f"Memory used: {metrics['memory']['total_allocated_mb']}MB")
```

---

## 🎯 Expected System Behavior

| Stress Type | Expected Metric | Tool Command |
|------------|-----------------|--------------|
| **CPU Spike** | 100% CPU | `top` or `htop` |
| **Memory Leak** | +100MB per call | `free -h` |
| **Timeout** | 15000ms latency | `curl` with `-w @time.txt` |
| **Crash** | HTTP 500 errors | Check logs or curl response |
| **Latency** | Connection queueing | Monitor connection count |

---

## 🧪 Test Sequence (Recommended Order)

1. **Start the app:**
   ```bash
   gunicorn --workers 4 --threads 4 --worker-class gthread -b 0.0.0.0:8080 stress_app:app
   ```

2. **Verify health:**
   ```bash
   curl http://localhost:8080/
   ```

3. **Test CPU:**
   ```bash
   curl http://localhost:8080/simulate/cpu-spike
   # Watch: top, htop, or metrics endpoint
   ```

4. **Test Memory:**
   ```bash
   curl http://localhost:8080/simulate/memory-leak
   # Repeat 5-10 times
   curl http://localhost:8080/metrics
   ```

5. **Test Latency:**
   ```bash
   curl http://localhost:8080/simulate/timeout
   ```

6. **Test Errors:**
   ```bash
   curl http://localhost:8080/simulate/crash
   ```

7. **Clear & Repeat:**
   ```bash
   curl http://localhost:8080/simulate/memory-leak/clear
   ```

---

## 📝 Logging & Debugging

### View Logs (if running with Gunicorn)
```bash
# Flask logs go to stdout
gunicorn ... 2>&1 | tee stress.log

# View in real-time:
tail -f stress.log | grep -E "CPU_SPIKE|MEMORY|CRASH"
```

### Enable Debug Logging
In `stress_app.py`, change:
```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```

---

## ⚠️ Troubleshooting

### "Port 8080 already in use"
```bash
# Find process using port 8080
lsof -i :8080

# Kill it
kill -9 <PID>

# Or use different port:
gunicorn -b 0.0.0.0:9000 stress_app:app
```

### Memory allocation fails
```bash
# Check available memory:
free -h

# If running in Docker, increase memory:
docker run -p 8080:8080 --memory=8g cybermedic
```

### CPU stress not visible
- Make sure you're using **Gunicorn with multiple workers**, not Flask dev server
- Flask dev server is single-threaded and won't show real CPU stress
- Use: `gunicorn --workers 4 --threads 4 ...`

### Timeouts not working
- Make sure you're hitting the endpoint and waiting
- Use `time curl http://localhost:8080/simulate/timeout` to measure latency

---

## 🎓 What This Teaches

✅ **System Resilience** - How does your app handle resource exhaustion?  
✅ **Auto-scaling** - Does your infrastructure scale up under load?  
✅ **Error Recovery** - Can the system recover from crashes?  
✅ **Monitoring** - Do your monitoring tools detect the issues?  
✅ **Alerting** - Do alerts trigger before catastrophic failure?  

---

## 📞 Support

For more info, check the endpoints:
- `GET /status` - List all available endpoints
- `GET /metrics` - Current metrics
- `GET /ui` - Web dashboard

Happy chaos testing! 🎉
