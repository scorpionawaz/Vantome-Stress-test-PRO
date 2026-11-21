from flask import Flask, jsonify, render_template
import time
import math
import logging
import threading
import multiprocessing
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

memory_leak_storage = []
active_stress_processes = []
stress_metrics = {
    "cpu_spike_count": 0,
    "memory_leak_count": 0,
    "crash_count": 0,
    "timeout_count": 0,
    "total_memory_mb": 0
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

def log_stress_event(event_type, details):
    timestamp = datetime.now().isoformat()
    logger.warning(f"🚨 [{event_type}] {details} - {timestamp}")

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "CyberMedic Chaos Dashboard",
        "timestamp": datetime.now().isoformat(),
        "memory_leaks_active": len(memory_leak_storage),
        "active_processes": len(active_stress_processes)
    }), 200

@app.route('/')
@app.route('/ui')
def dashboard():
    return render_template('index.html')

@app.route('/simulate/cpu-spike')
def burn_cpu():
    num_workers = os.cpu_count() or 2
    logger.warning(f"🔥🔥 EXTREME CPU SPIKE INITIATED - {num_workers} workers for 45 seconds")
    
    def extreme_cpu_worker():
        end_time = time.time() + 45
        iterations = 0
        try:
            while time.time() < end_time:
                for i in range(10000):
                    _ = math.factorial(25)
                    _ = (math.sqrt(i) * math.sin(i) * math.cos(i)) ** 2
                    _ = math.exp(0.1) * math.log(i + 2)
                    _ = (i ** 3) % 9973
                    _ = (i ** 2) % 7919
                data = list(range(100000))
                _ = sorted(data, key=lambda x: (x**2) % 9973)
                iterations += 1
        except Exception as e:
            logger.error(f"CPU worker error: {e}")
        return iterations
    
    for i in range(num_workers):
        t = threading.Thread(target=extreme_cpu_worker, daemon=True)
        t.start()
        active_stress_processes.append(t)
    
    stress_metrics["cpu_spike_count"] += 1
    log_stress_event("CPU_SPIKE", f"Spawned {num_workers} EXTREME CPU burners")
    
    return jsonify({
        "status": "cpu_stressed",
        "message": f"EXTREME CPU stress started with {num_workers} workers",
        "duration_seconds": 45,
        "expected_cpu": "~100% (ALL CORES)",
        "intensity": "EXTREME",
        "workers": num_workers,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/simulate/cpu-spike-long')
def burn_cpu_long():
    num_workers = os.cpu_count() or 2
    logger.warning(f"🔥🔥 EXTREME LONG CPU SPIKE - {num_workers} workers for 120 seconds")
    
    def sustained_extreme_cpu_load():
        end_time = time.time() + 120
        try:
            while time.time() < end_time:
                for i in range(15000):
                    _ = math.factorial(25)
                    _ = (math.sqrt(i) * math.sin(i) * math.cos(i)) ** 2
                data = list(range(150000))
                _ = sorted(data, key=lambda x: (x**3) % 9973)
        except Exception as e:
            logger.error(f"CPU load error: {e}")
    
    for _ in range(num_workers):
        t = threading.Thread(target=sustained_extreme_cpu_load, daemon=True)
        t.start()
        active_stress_processes.append(t)
    
    return jsonify({
        "status": "sustained_extreme_cpu_stress",
        "workers": num_workers,
        "duration_seconds": 120,
        "intensity": "EXTREME",
        "expected_cpu": "~100% sustained",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/simulate/memory-leak')
def leak_memory():
    logger.warning("💾 MEMORY LEAK INITIATED - allocating 100MB...")
    
    def allocate_memory():
        try:
            chunk = bytearray(100 * 1024 * 1024)
            memory_leak_storage.append(chunk)
            current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
            logger.warning(f"📈 Memory consumed: {current_total:.1f}MB across {len(memory_leak_storage)} chunks")
        except MemoryError:
            logger.error("💥 OUT OF MEMORY ERROR - Container will crash!")
    
    thread = threading.Thread(target=allocate_memory, daemon=True)
    thread.start()
    stress_metrics["memory_leak_count"] += 1
    current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
    
    return jsonify({
        "status": "memory_leaking",
        "message": "100MB allocated and retained",
        "total_memory_mb": round(current_total, 2),
        "leak_count": len(memory_leak_storage),
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/simulate/memory-spike')
def memory_spike():
    logger.warning("🔴 AGGRESSIVE MEMORY SPIKE - 500MB allocation")
    try:
        chunk = bytearray(500 * 1024 * 1024)
        memory_leak_storage.append(chunk)
        current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
        return jsonify({
            "status": "memory_spike",
            "allocated_mb": 500,
            "total_memory_mb": round(current_total, 2),
            "timestamp": datetime.now().isoformat()
        }), 200
    except MemoryError:
        logger.error("💥 OUT OF MEMORY - Container will crash soon!")
        return jsonify({
            "status": "oom_error",
            "message": "Failed to allocate 500MB - system out of memory"
        }), 500

@app.route('/simulate/memory-leak/clear')
def clear_memory():
    global memory_leak_storage
    old_size = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
    memory_leak_storage.clear()
    logger.info(f"🧹 Memory cleared ({old_size:.1f}MB freed)")
    return jsonify({
        "status": "memory_cleared",
        "freed_mb": round(old_size, 2),
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/simulate/timeout')
def choke_latency():
    logger.warning("⏱️ LATENCY SPIKE - 15 second hang")
    def slow_operation():
        time.sleep(15)
        logger.warning("✓ Latency test completed")
    thread = threading.Thread(target=slow_operation, daemon=True)
    thread.start()
    stress_metrics["timeout_count"] += 1
    return jsonify({
        "status": "hanging",
        "message": "Request will hang for 15 seconds",
        "expected_latency_ms": 15000,
        "timestamp": datetime.now().isoformat()
    }), 202

@app.route('/simulate/timeout-cascade')
def timeout_cascade():
    logger.warning("🌊 CASCADING TIMEOUTS - spawning 20 hanging requests")
    def cascade_delay():
        time.sleep(20)
    for _ in range(20):
        thread = threading.Thread(target=cascade_delay, daemon=True)
        thread.start()
    return jsonify({
        "status": "cascading_timeouts",
        "hanging_requests": 20,
        "duration_seconds": 20,
        "message": "20 requests will hang for 20 seconds",
        "timestamp": datetime.now().isoformat()
    }), 202

@app.route('/simulate/crash')
def force_500_error():
    logger.error("💥 FATAL ERROR - Triggering ZeroDivisionError")
    stress_metrics["crash_count"] += 1
    log_stress_event("CRASH", "Simulating runtime exception")
    return str(1 / 0)

@app.route('/simulate/crash-series')
def crash_series():
    logger.error("🔁 CRASH SERIES - will fail soon")
    log_stress_event("CRASH_SERIES", "Initiating sequential crashes")
    stress_metrics["crash_count"] += 1
    def delayed_crash():
        time.sleep(2)
        _ = 1 / 0
    for _ in range(3):
        t = threading.Thread(target=delayed_crash, daemon=True)
        t.start()
        active_stress_processes.append(t)
    return jsonify({
        "status": "crash_series_initiated",
        "message": "Sequential crashes triggered",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/simulate/full-chaos')
def full_chaos():
    logger.warning("☣️ FULL CHAOS MODE INITIATED")
    num_workers = os.cpu_count() or 2
    
    def chaos_worker():
        end_time = time.time() + 60
        try:
            while time.time() < end_time:
                _ = math.factorial(25)
                _ = bytearray(50 * 1024 * 1024)
        except Exception:
            pass
            
    for _ in range(min(num_workers, 4)):
        t = threading.Thread(target=chaos_worker, daemon=True)
        t.start()
        active_stress_processes.append(t)
        
    stress_metrics["cpu_spike_count"] += 1
    stress_metrics["timeout_count"] += 1
    
    return jsonify({
        "status": "full_chaos_active",
        "message": "Full system stress initiated across CPU, Memory, and Latency",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/metrics')
def get_metrics():
    current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "memory": {
            "total_allocated_mb": round(current_total, 2),
            "leak_chunks": len(memory_leak_storage),
            "max_per_chunk_mb": 100
        },
        "events": stress_metrics,
        "active_processes": len(active_stress_processes)
    }), 200

@app.route('/status')
def get_status():
    return jsonify({
        "status": "operational",
        "endpoints": [
            "/", "/ui", "/health", "/metrics", "/status",
            "/simulate/cpu-spike", "/simulate/cpu-spike-long",
            "/simulate/memory-leak", "/simulate/memory-spike", "/simulate/memory-leak/clear",
            "/simulate/timeout", "/simulate/timeout-cascade",
            "/simulate/crash", "/simulate/crash-series", "/simulate/full-chaos"
        ]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
