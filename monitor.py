# Filename: monitor.py
import psutil
import time
from prometheus_client import start_http_server, Gauge

# Define Prometheus metrics
cpu_gauge = Gauge('container_cpu_usage_percent', 'CPU usage in percentage')
memory_percent_gauge = Gauge('container_memory_usage_percent', 'Memory usage in percentage')
memory_used_gauge = Gauge('container_memory_used_mb', 'Memory used in MB')
memory_total_gauge = Gauge('container_memory_total_mb', 'Total memory in MB')

def get_cpu_memory_usage():
    # Get CPU usage in percentage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Get memory usage details
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    memory_used = memory_info.used / (1024 * 1024)  # Convert bytes to MB
    memory_total = memory_info.total / (1024 * 1024)  # Convert bytes to MB

    return cpu_percent, memory_percent, memory_used, memory_total

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    
    # Continuously update metrics
    while True:
        cpu, mem_percent, mem_used, mem_total = get_cpu_memory_usage()

        # Update Prometheus metrics
        cpu_gauge.set(cpu)
        memory_percent_gauge.set(mem_percent)
        memory_used_gauge.set(mem_used)
        memory_total_gauge.set(mem_total)

        time.sleep(5)
