# 🚨 CyberMedic Chaos Dashboard

A **production-grade chaos engineering and stress testing platform** built with Flask. Designed to test system resilience, auto-scaling, error recovery, and monitoring capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Features

### 🔥 **CPU Stress Testing**
- Spike CPU to 100% using multi-threaded calculations
- 45-second acute stress or 120-second sustained load
- Triggers auto-scaling, load balancing, and resource limits

### 💾 **Memory Stress Testing**
- 100MB memory leak (accumulates with repeated calls)
- 500MB aggressive memory spike
- Tests OOM handling, garbage collection, and container restarts

### ⏱️ **Latency & Timeout Testing**
- Single 15-second timeout (simulates DB deadlock)
- Cascading 20 concurrent timeouts (connection pool exhaustion)
- Tests request queueing and load shedding

### 💥 **Error & Crash Testing**
- Forces HTTP 500 errors (ZeroDivisionError)
- Sequential crash series (tests recovery loops)
- Validates error logging and alerting

### ☣️ **Full Chaos Mode**
- Simultaneous CPU + Memory + Latency stress
- Complete system failure scenario
- Tests comprehensive resilience

### 📊 **Live Metrics & Monitoring**
- Real-time stress event tracking
- Memory allocation monitoring
- Event counters (CPU spikes, crashes, timeouts)
- JSON API for integration

---

## 🚀 Quick Start

### Option 1: Local Python
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Flask (dev - limited stress)
python stress_app.py

# Or run with Gunicorn (production - real stress)
gunicorn --workers 4 --threads 4 --worker-class gthread -b 0.0.0.0:8080 stress_app:app
```

### Option 2: Shell Script
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Docker
```bash
docker build -t cybermedic .
docker run -p 8080:8080 --memory=4g cybermedic
```

### Option 4: Docker Compose (Recommended)
```bash
docker-compose up --build
```

---

## 📍 Access the Dashboard

Once running, open your browser:

```
http://localhost:8080/ui
```

You'll see the interactive dashboard with all stress test options.

---

## 🧪 API Endpoints

### Health & Metrics
- `GET /` - Health check
- `GET /metrics` - Current metrics (JSON)
- `GET /status` - Available endpoints
- `GET /ui` - Web dashboard

### CPU Stress
- `GET /simulate/cpu-spike` - 45s CPU burst
- `GET /simulate/cpu-spike-long` - 120s sustained CPU load

### Memory Stress
- `GET /simulate/memory-leak` - +100MB allocation
- `GET /simulate/memory-spike` - +500MB allocation
- `GET /simulate/memory-leak/clear` - Release all memory

### Latency Stress
- `GET /simulate/timeout` - 15s single hang
- `GET /simulate/timeout-cascade` - 20 concurrent hangs

### Error Testing
- `GET /simulate/crash` - HTTP 500 error
- `GET /simulate/crash-series` - 3 sequential crashes

### Full Chaos
- `GET /simulate/full-chaos` - All stress vectors

---

## 🧪 Testing Examples

### Via Browser
1. Open http://localhost:8080/ui
2. Click any button to trigger stress
3. Watch live metrics update in real-time

### Via Command Line

**CPU Spike:**
```bash
curl http://localhost:8080/simulate/cpu-spike
watch -n 1 "top -b -n 1 | head -20"  # Monitor CPU
```

**Memory Leak (repeat to trigger OOM):**
```bash
for i in {1..10}; do
  curl http://localhost:8080/simulate/memory-leak
  sleep 1
done
curl http://localhost:8080/metrics
```

**Latency Spike:**
```bash
time curl http://localhost:8080/simulate/timeout
```

**Full Chaos:**
```bash
curl http://localhost:8080/simulate/full-chaos
watch -n 2 "curl -s http://localhost:8080/metrics | python -m json.tool"
```

---

## 📊 Example Metrics Response

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

---

## 🏗️ Architecture

### Multi-threaded Design
- Each stress test runs in a separate daemon thread
- Endpoints return immediately (async execution)
- Multiple stressors can run simultaneously
- Non-blocking for UI responsiveness

### Performance Characteristics
- **CPU Stress**: Uses multi-threaded calculations (bypasses GIL with threading)
- **Memory Stress**: Direct `bytearray` allocation (actual memory pressure)
- **Latency Stress**: `time.sleep()` to simulate real delays
- **Error Testing**: Native Python exceptions for accurate error simulation

### Scalability
- Designed for containerized environments (Kubernetes, Docker Swarm)
- Horizontal scaling: run multiple instances to stress multiple services
- Rate-limited to prevent system crash (optional adjustments available)

---

## 🔧 Configuration

### Stress Parameters (in `stress_app.py`)

**CPU Stress Duration:**
```python
# Line 104: CPU spike duration
end_time = time.time() + 45  # Change to desired seconds
```

**Memory Leak Size:**
```python
# Line 169: Leak size per call
chunk = bytearray(100 * 1024 * 1024)  # Change to desired MB
```

**Timeout Duration:**
```python
# Line 276: Timeout duration
time.sleep(15)  # Change to desired seconds
```

**Cascade Timeout Count:**
```python
# Line 299: Number of concurrent hangs
for i in range(20):  # Change to desired count
```

---

## 📈 Monitoring Integration

### Prometheus Metrics Format (Optional)
Extend the `/metrics` endpoint to output Prometheus format:

```python
@app.route('/metrics-prom')
def metrics_prometheus():
    mem = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
    return f"""
# HELP cybermedic_memory_mb Total memory allocated
# TYPE cybermedic_memory_mb gauge
cybermedic_memory_mb {mem}

# HELP cybermedic_cpu_spikes_total Total CPU spike events
# TYPE cybermedic_cpu_spikes_total counter
cybermedic_cpu_spikes_total {stress_metrics["cpu_spike_count"]}
"""
```

### Integration with Monitoring Tools
- **Datadog**: Import stress metrics as custom metrics
- **Prometheus**: Scrape `/metrics` endpoint
- **CloudWatch**: Set up custom metric alarms
- **New Relic**: Create custom dashboards from API responses

---

## 📋 Pre-requisites

- **Python 3.8+**
- **Flask 2.3+**
- **Optional**: Gunicorn for production
- **Optional**: Docker for containerization
- **Recommended**: 4GB+ RAM for memory stress tests

---

## ⚠️ Important Notes

### For Real Stress Testing
- **Use Gunicorn**, not Flask dev server
- Flask is single-threaded; stress will be limited
- Gunicorn with workers enables true multi-core stress

### Memory Leak Testing
- Allocations are **NOT released** (simulates real memory leaks)
- Use `/simulate/memory-leak/clear` to reset between tests
- Monitor actual system memory, not just the app

### Production Safety
- Run in isolated/sandboxed environment
- Set resource limits (CPU, memory) in containers
- Don't run against production systems
- Monitor system resources during testing

---

## 🧪 Test Scenarios

### Scenario 1: Auto-scaling Validation
1. Trigger `/simulate/cpu-spike`
2. Observe CPU metrics in your cloud provider
3. Verify auto-scaling policies trigger correctly
4. Confirm instances scale down after stress ends

### Scenario 2: Failover Testing
1. Run `/simulate/crash` multiple times
2. Monitor error logs and alerts
3. Verify failover mechanisms activate
4. Confirm service recovery

### Scenario 3: Load Balancer Testing
1. Trigger `/simulate/timeout-cascade`
2. Monitor connection distribution across instances
3. Verify load balancer handles timeouts gracefully
4. Check connection timeout settings

### Scenario 4: Memory Leak Detection
1. Repeatedly call `/simulate/memory-leak`
2. Monitor memory growth over time
3. Verify memory monitoring alerts trigger
4. Test container restart mechanisms

### Scenario 5: Complete System Stress
1. Run `/simulate/full-chaos`
2. Monitor CPU, memory, and latency simultaneously
3. Verify multi-metric alerting
4. Test recovery procedures

---

## 📚 Files Included

| File | Purpose |
|------|---------|
| `stress_app.py` | Main Flask application with all endpoints |
| `templates/index.html` | Interactive web dashboard |
| `requirements.txt` | Python dependencies |
| `run.sh` | Quick start shell script |
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `SETUP_GUIDE.md` | Detailed setup and testing guide |
| `README.md` | This file |

---

## 🐛 Troubleshooting

### "Port 8080 already in use"
```bash
lsof -i :8080
kill -9 <PID>
```

### "Memory allocation fails (OOM)"
```bash
# Increase system memory or adjust stress parameters
# For Docker: docker run --memory=8g
```

### "CPU stress not showing up"
```bash
# Use Gunicorn, not Flask dev server:
gunicorn --workers 4 --threads 4 --worker-class gthread -b 0.0.0.0:8080 stress_app:app
```

### "Metrics endpoint returns 0 values"
```bash
# Run a stress test first:
curl http://localhost:8080/simulate/cpu-spike
# Then check metrics:
curl http://localhost:8080/metrics
```

---

## 🤝 Contributing

Found a bug? Have a feature request?
1. Test your scenario thoroughly
2. Document the expected vs actual behavior
3. Share test results and logs

---

## 📄 License

MIT License - Feel free to use, modify, and distribute

---

## 🙏 Acknowledgments

Built for **chaos engineering**, **resilience testing**, and **stress validation**.

---

## 📞 Support & Resources

- **Local Testing**: `http://localhost:8080/ui`
- **API Docs**: `http://localhost:8080/status`
- **Health Check**: `http://localhost:8080/`
- **Metrics**: `http://localhost:8080/metrics`

---

## 🚀 Getting Started

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python stress_app.py` (or Gunicorn for real testing)
3. **Access**: `http://localhost:8080/ui`
4. **Test**: Click buttons or use curl commands
5. **Monitor**: Watch `/metrics` endpoint

---

**Happy Chaos Testing!** ☣️🧪
#   - V a n t o m e - S t r e s s - t e s t - P R O  
 