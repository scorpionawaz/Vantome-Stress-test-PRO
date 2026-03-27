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

# Global state tracking
memory_leak_storage = []
active_stress_processes = []
stress_metrics = {
    "cpu_spike_count": 0,
    "memory_leak_count": 0,
    "crash_count": 0,
    "timeout_count": 0,
    "total_memory_mb": 0
}

# Configure logging with timestamps and immediate flushing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # Force internal loggers to use this config
)
logger = logging.getLogger(__name__)

# Ensure stdout is unbuffered if the env variable isn't set
import sys
if not hasattr(sys.stdout, 'reconfigure'): # Python < 3.7
    pass 
else:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def extreme_cpu_burn():
    """
    EXTREME CPU BURN - Maximum intensity calculations
    Uses multiple computation strategies simultaneously
    """
    try:
        while True:
            # Strategy 1: Heavy mathematical operations
            for i in range(5000):
                _ = math.factorial(20)
                _ = math.sqrt(i) * math.sin(i) * math.cos(i)
                _ = math.exp(0.5) * math.log(i + 2)
                _ = (i ** 2) % 9973
            
            # Strategy 2: List operations
            data = list(range(50000))
            _ = sorted(data, key=lambda x: x**2)
            _ = [x for x in data if x % 7 == 0]
            
            # Strategy 3: String operations
            _ = ''.join([str(i) * 10 for i in range(1000)])
            
            # Strategy 4: Recursive-like operations
            result = sum([i**2 for i in range(10000)])
            _ = result
            
    except KeyboardInterrupt:
        pass

def memory_allocator(size_mb, duration_seconds=60):
    """
    Allocates memory for a specified duration
    """
    try:
        # Create a large bytearray and keep it in memory
        chunk = bytearray(size_mb * 1024 * 1024)
        memory_leak_storage.append(chunk)
        
        # Keep it alive for the duration
        time.sleep(duration_seconds)
    except MemoryError:
        logger.error(f"❌ OUT OF MEMORY! Failed to allocate {size_mb}MB")

def log_stress_event(event_type, details):
    """Log stress events to metrics"""
    timestamp = datetime.now().isoformat()
    logger.warning(f"🚨 [{event_type}] {details} - {timestamp}")

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "CyberMedic Chaos Dashboard",
        "timestamp": datetime.now().isoformat(),
        "memory_leaks_active": len(memory_leak_storage),
        "active_processes": len(active_stress_processes)
    }), 200


@app.route('/ui')
def dashboard():
    """Serves the Chaos Dashboard UI"""
    return render_template('index.html')


# ========== CPU STRESS ==========

@app.route('/simulate/cpu-spike')
def burn_cpu():
    """
    🔥 EXTREME CPU SPIKE - Maximum intensity multi-core stress
    Duration: 45 seconds
    Expected: 100% CPU usage across all cores
    """
    num_workers = os.cpu_count()  # Use ALL cores
    
    logger.warning(f"🔥🔥 EXTREME CPU SPIKE INITIATED - {num_workers} workers for 45 seconds")
    
    def extreme_cpu_worker():
        """Extreme CPU burn worker"""
        end_time = time.time() + 45
        iterations = 0
        try:
            while time.time() < end_time:
                # EXTREME: Multiple heavy calculations
                for i in range(10000):
                    # Factorial is extremely expensive
                    _ = math.factorial(25)
                    # Combined trig functions
                    _ = (math.sqrt(i) * math.sin(i) * math.cos(i)) ** 2
                    # Exponential and logarithm
                    _ = math.exp(0.1) * math.log(i + 2)
                    # Modulo operations
                    _ = (i ** 3) % 9973
                    _ = (i ** 2) % 7919
                
                # Intensive list operations
                data = list(range(100000))
                _ = sorted(data, key=lambda x: (x**2) % 9973)
                _ = [x for x in data if x % 13 == 0]
                
                iterations += 1
        except Exception as e:
            logger.error(f"CPU worker error: {e}")
        
        return iterations
    
    # Spawn worker threads for ALL cores
    threads = []
    for i in range(num_workers):
        t = threading.Thread(target=extreme_cpu_worker, daemon=True)
        t.start()
        threads.append(t)
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
    """
    EXTREME EXTENDED CPU STRESS - 2 minute maximum intensity load
    For testing auto-scaling thresholds
    """
    num_workers = os.cpu_count()
    
    logger.warning(f"🔥🔥 EXTREME LONG CPU SPIKE - {num_workers} workers for 120 seconds")
    
    def sustained_extreme_cpu_load():
        end_time = time.time() + 120
        try:
            while time.time() < end_time:
                # EXTREME: Repeated heavy operations
                for i in range(15000):
                    _ = math.factorial(25)
                    _ = (math.sqrt(i) * math.sin(i) * math.cos(i)) ** 2
                    _ = math.exp(0.1) * math.log(i + 2)
                
                # Heavy sorting and filtering
                data = list(range(150000))
                _ = sorted(data, key=lambda x: (x**3) % 9973)
        except Exception as e:
            logger.error(f"CPU load error: {e}")
    
    threads = [threading.Thread(target=sustained_extreme_cpu_load, daemon=True) 
               for _ in range(num_workers)]
    
    for t in threads:
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


# ========== MEMORY STRESS ==========

@app.route('/simulate/memory-leak')
def leak_memory():
    """
    💾 MEMORY LEAK - Allocates 100MB and keeps it
    Call multiple times to accumulate (up to OOM)
    """
    logger.warning("💾 MEMORY LEAK INITIATED - allocating 100MB...")
    
    def allocate_memory():
        try:
            # Allocate 100MB of actual data
            chunk = bytearray(100 * 1024 * 1024)
            memory_leak_storage.append(chunk)
            
            current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
            logger.warning(f"📈 Memory consumed: {current_total:.1f}MB across {len(memory_leak_storage)} chunks")
        except MemoryError:
            logger.error("💥 OUT OF MEMORY ERROR - Container will crash!")
    
    # Run in background thread
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
    """
    🔴 AGGRESSIVE MEMORY SPIKE - 500MB instant allocation
    For testing OOM scenarios quickly
    """
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
    """Clear memory leak storage"""
    global memory_leak_storage
    old_size = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
    memory_leak_storage.clear()
    logger.info(f"🧹 Memory cleared ({old_size:.1f}MB freed)")
    
    return jsonify({
        "status": "memory_cleared",
        "freed_mb": round(old_size, 2),
        "timestamp": datetime.now().isoformat()
    }), 200


# ========== LATENCY STRESS ==========

@app.route('/simulate/timeout')
def choke_latency():
    """
    ⏱️ LATENCY SPIKE - 15 second hang (simulates DB deadlock)
    """
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
    """
    🌊 CASCADING TIMEOUTS - Multiple hanging requests
    Simulates connection pool exhaustion
    """
    logger.warning("🌊 CASCADING TIMEOUTS - spawning 20 hanging requests")
    
    def cascade_delay():
        time.sleep(20)
    
    for i in range(20):
        thread = threading.Thread(target=cascade_delay, daemon=True)
        thread.start()
    
    return jsonify({
        "status": "cascading_timeouts",
        "hanging_requests": 20,
        "duration_seconds": 20,
        "message": "20 requests will hang for 20 seconds",
        "timestamp": datetime.now().isoformat()
    }), 202


# ========== CRASH SCENARIOS ==========

@app.route('/simulate/crash')
def force_500_error():
    """
    💥 RUNTIME CRASH - Forces ZeroDivisionError
    Returns HTTP 500 with full traceback
    """
    logger.error("💥 FATAL ERROR - Triggering ZeroDivisionError")
    
    stress_metrics["crash_count"] += 1
    log_stress_event("CRASH", "Simulating runtime exception")
    
    # This will crash the request
    result = 1 / 0
    return "This will never execute"


@app.route('/simulate/crash-series')
def crash_series():
    """
    🔁 CRASH SERIES - Triggers multiple 500 errors in sequence
    Tests error recovery and alerting
    """
    logger.error("🔁 CRASH SERIES - will fail soon")
    log_stress_event("CRASH_SERIES", "Initiating sequential crashes")
    
    def delayed_crash():
        time.sleep(5)
        _ = 1 / 0  # Will crash this thread
    
    for i in range(500):
        threading.Thread(target=delayed_crash, daemon=True).start()
    
    return jsonify({
        "status": "crash_series_initiated",
        "crashes_queued": 50,
        "message": "3 crashes will occur over next 10 seconds",
        "timestamp": datetime.now().isoformat()
    }), 202


# ========== COMBO SCENARIOS ==========

@app.route('/simulate/full-chaos')
def full_chaos():
    """
    ☣️ FULL CHAOS MODE - CPU + Memory + Latency simultaneously
    Tests comprehensive system stress
    """
    logger.warning("☣️ FULL CHAOS MODE ACTIVATED")
    log_stress_event("FULL_CHAOS", "Triggering CPU + Memory + Latency stress")
    
    # CPU stress
    def cpu_worker():
        end_time = time.time() + 60
        while time.time() < end_time:
            for i in range(5000):
                _ = math.sqrt(i)
    
    # Memory stress
    def mem_worker():
        try:
            for _ in range(3):
                chunk = bytearray(100 * 1024 * 1024)
                memory_leak_storage.append(chunk)
                time.sleep(5)
        except MemoryError:
            pass
    
    # Latency stress
    def latency_worker():
        for _ in range(5):
            time.sleep(10)
    
    # Spawn all stressors
    threading.Thread(target=cpu_worker, daemon=True).start()
    threading.Thread(target=mem_worker, daemon=True).start()
    threading.Thread(target=latency_worker, daemon=True).start()
    
    return jsonify({
        "status": "full_chaos",
        "cpu_stress": "60 seconds",
        "memory_stress": "300MB over 15 seconds",
        "latency_stress": "5x 10 second hangs",
        "message": "All stress vectors activated",
        "timestamp": datetime.now().isoformat()
    }), 200


# ========== METRICS & MONITORING ==========

@app.route('/metrics')
def metrics():
    """
    📊 Current stress metrics
    """
    current_memory = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "memory": {
            "total_allocated_mb": round(current_memory, 2),
            "leak_chunks": len(memory_leak_storage),
            "max_per_chunk_mb": 100
        },
        "events": {
            "cpu_spike_count": stress_metrics["cpu_spike_count"],
            "memory_leak_count": stress_metrics["memory_leak_count"],
            "crash_count": stress_metrics["crash_count"],
            "timeout_count": stress_metrics["timeout_count"]
        },
        "active_processes": len(active_stress_processes)
    }), 200


@app.route('/status')
def status():
    """
    🔍 Detailed system status
    """
    return jsonify({
        "service": "CyberMedic Chaos Dashboard",
        "status": "operational",
        "endpoints": {
            "cpu_spike": "/simulate/cpu-spike (45s)",
            "cpu_spike_long": "/simulate/cpu-spike-long (120s)",
            "memory_leak": "/simulate/memory-leak (+100MB)",
            "memory_spike": "/simulate/memory-spike (+500MB)",
            "timeout": "/simulate/timeout (15s hang)",
            "timeout_cascade": "/simulate/timeout-cascade (20x hangs)",
            "crash": "/simulate/crash (500 error)",
            "crash_series": "/simulate/crash-series (3 crashes)",
            "full_chaos": "/simulate/full-chaos (all stress)",
            "metrics": "/metrics (current stats)",
            "clear_memory": "/simulate/memory-leak/clear"
        },
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 CyberMedic Chaos Dashboard Starting...")
    logger.info("=" * 60)
    logger.info("Visit: http://localhost:8080/ui")
    logger.info("Metrics: http://localhost:8080/metrics")
    logger.info("Status: http://localhost:8080/status")
    logger.info("=" * 60)
    
    # For production, use Gunicorn:
    # gunicorn --workers 4 --threads 4 --worker-class gthread -b 0.0.0.0:8080 stress_app:app
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)