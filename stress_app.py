from flask import Flask, jsonify, render_template
import gc
import time
import math
import logging
import threading
import multiprocessing
import os
import sys
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

MAX_ACTIVE_STRESS_PROCESSES = 4

state_lock = threading.Lock()
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

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)


def _cpu_burn_worker(duration_seconds, inner_iters, list_size):
    try:
        os.nice(10)
    except (OSError, AttributeError):
        pass

    end_time = time.time() + duration_seconds
    try:
        while time.time() < end_time:
            for i in range(inner_iters):
                _ = math.factorial(25)
                _ = (math.sqrt(i) * math.sin(i) * math.cos(i)) ** 2
                _ = math.exp(0.1) * math.log(i + 2)
                _ = (i ** 3) % 9973
                _ = (i ** 2) % 7919
                if time.time() >= end_time:
                    break
            data = list(range(list_size))
            _ = sorted(data, key=lambda x: (x ** 2) % 9973)
    except Exception as e:
        logger.error(f"CPU worker error: {e}")


def _prune_active_processes():
    active_stress_processes[:] = [p for p in active_stress_processes if p.is_alive()]


def _spawn_cpu_stress(desired_workers, duration_seconds, inner_iters, list_size):
    mp_ctx = multiprocessing.get_context("spawn")
    spawned = 0
    with state_lock:
        _prune_active_processes()
        available_slots = max(0, MAX_ACTIVE_STRESS_PROCESSES - len(active_stress_processes))
        to_spawn = min(desired_workers, available_slots)
        for _ in range(to_spawn):
            p = mp_ctx.Process(
                target=_cpu_burn_worker,
                args=(duration_seconds, inner_iters, list_size),
                daemon=True
            )
            p.start()
            active_stress_processes.append(p)
            spawned += 1
    return spawned


def log_stress_event(event_type, details):
    timestamp = datetime.now().isoformat()
    logger.warning(f"🚨 [{event_type}] {details} - {timestamp}")


@app.route('/health')
def health_check():
    with state_lock:
        _prune_active_processes()
        leaks_active = len(memory_leak_storage)
        active_count = len(active_stress_processes)
    return jsonify({
        "status": "healthy",
        "service": "CyberMedic Chaos Dashboard",
        "timestamp": datetime.now().isoformat(),
        "memory_leaks_active": leaks_active,
        "active_processes": active_count
    }), 200


@app.route('/')
@app.route('/ui')
def dashboard():
    return render_template('index.html')


@app.route('/simulate/cpu-spike')
def burn_cpu():
    desired_workers = min(os.cpu_count() or 2, MAX_ACTIVE_STRESS_PROCESSES)
    logger.warning(f"🔥🔥 EXTREME CPU SPIKE INITIATED - up to {desired_workers} workers for 45 seconds")
    spawned = _spawn_cpu_stress(desired_workers, 45, 5000, 50000)
    with state_lock:
        stress_metrics["cpu_spike_count"] += 1
    log_stress_event("CPU_SPIKE", f"Spawned {spawned} isolated CPU burners")
    return jsonify({
        "status": "cpu_stressed",
        "message": f"EXTREME CPU stress started with {spawned} workers",
        "duration_seconds": 45,
        "expected_cpu": "~100% (ALL CORES)",
        "intensity": "EXTREME",
        "workers": spawned,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/simulate/cpu-spike-long')
def burn_cpu_long():
    desired_workers = min(os.cpu_count() or 2, MAX_ACTIVE_STRESS_PROCESSES)
    logger.warning(f"🔥🔥 EXTREME LONG CPU SPIKE - up to {desired_workers} workers for 120 seconds")
    spawned = _spawn_cpu_stress(desired_workers, 120, 7500, 75000)
    with state_lock:
        stress_metrics["cpu_spike_count"] += 1
    log_stress_event("CPU_SPIKE_LONG", f"Spawned {spawned} isolated sustained CPU burners")
    return jsonify({
        "status": "sustained_extreme_cpu_stress",
        "workers": spawned,
        "duration_seconds": 120,
        "intensity": "EXTREME",
        "expected_cpu": "~100% sustained",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/simulate/memory-leak')
def leak_memory():
    logger.warning("💾 MEMORY LEAK INITIATED - allocating 100MB...")
    try:
        chunk = bytearray(100 * 1024 * 1024)
        with state_lock:
            memory_leak_storage.append(chunk)
            stress_metrics["memory_leak_count"] += 1
            current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
            stress_metrics["total_memory_mb"] = round(current_total, 2)
            leak_count = len(memory_leak_storage)
        logger.warning(f"📈 Memory consumed: {current_total:.1f}MB across {leak_count} chunks")
        return jsonify({
            "status": "memory_leaking",
            "message": "100MB allocated and retained",
            "total_memory_mb": round(current_total, 2),
            "leak_count": leak_count,
            "timestamp": datetime.now().isoformat()
        }), 200
    except MemoryError:
        logger.error("💥 OUT OF MEMORY ERROR - Failed to allocate 100MB")
        return jsonify({
            "status": "oom_error",
            "message": "Failed to allocate 100MB - system low on memory"
        }), 500


@app.route('/simulate/memory-spike')
def memory_spike():
    logger.warning("🔴 AGGRESSIVE MEMORY SPIKE - 500MB allocation")
    try:
        chunk = bytearray(500 * 1024 * 1024)
        with state_lock:
            memory_leak_storage.append(chunk)
            stress_metrics["memory_leak_count"] += 1
            current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
            stress_metrics["total_memory_mb"] = round(current_total, 2)
        return jsonify({
            "status": "memory_spike",
            "allocated_mb": 500,
            "total_memory_mb": round(current_total, 2),
            "timestamp": datetime.now().isoformat()
        }), 200
    except MemoryError:
        logger.error("💥 OUT OF MEMORY - Failed to allocate 500MB")
        return jsonify({
            "status": "oom_error",
            "message": "Failed to allocate 500MB - system out of memory"
        }), 500


@app.route('/simulate/memory-leak/clear')
def clear_memory():
    with state_lock:
        old_size = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
        memory_leak_storage.clear()
        stress_metrics["total_memory_mb"] = 0
    gc.collect()
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
    with state_lock:
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
    with state_lock:
        stress_metrics["timeout_count"] += 20
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
    with state_lock:
        stress_metrics["crash_count"] += 1
    log_stress_event("CRASH", "Simulating runtime exception")
    return str(1 / 0)


@app.route('/simulate/crash-series')
def crash_series():
    logger.error("🔁 CRASH SERIES - will fail soon")
    log_stress_event("CRASH_SERIES", "Initiating sequential crashes")
    with state_lock:
        stress_metrics["crash_count"] += 1

    def delayed_crash():
        time.sleep(2)
        _ = 1 / 0

    for _ in range(3):
        threading.Thread(target=delayed_crash, daemon=True).start()

    return jsonify({
        "status": "crash_series_initiated",
        "message": "Sequential crashes triggered",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/simulate/full-chaos')
def full_chaos():
    logger.warning("☣️ FULL CHAOS MODE INITIATED")
    desired_workers = min(os.cpu_count() or 2, MAX_ACTIVE_STRESS_PROCESSES)
    spawned = _spawn_cpu_stress(desired_workers, 60, 5000, 50000)

    try:
        chunk = bytearray(100 * 1024 * 1024)
        with state_lock:
            memory_leak_storage.append(chunk)
            stress_metrics["total_memory_mb"] = round(
                sum(len(c) for c in memory_leak_storage) / (1024 * 1024), 2
            )
    except MemoryError:
        logger.error("💥 FULL CHAOS - Out of memory during allocation")

    threading.Thread(target=lambda: time.sleep(15), daemon=True).start()

    with state_lock:
        stress_metrics["cpu_spike_count"] += 1
        stress_metrics["timeout_count"] += 1

    return jsonify({
        "status": "full_chaos_active",
        "workers": spawned,
        "message": "Full system stress initiated across CPU, Memory, and Latency",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/metrics')
def get_metrics():
    with state_lock:
        _prune_active_processes()
        current_total = sum(len(c) for c in memory_leak_storage) / (1024 * 1024)
        leak_chunks = len(memory_leak_storage)
        events_snapshot = dict(stress_metrics)
        events_snapshot["total_memory_mb"] = round(current_total, 2)
        active_count = len(active_stress_processes)
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "memory": {
            "total_allocated_mb": round(current_total, 2),
            "leak_chunks": leak_chunks,
            "max_per_chunk_mb": 100
        },
        "events": events_snapshot,
        "active_processes": active_count
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
