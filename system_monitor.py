import os
from datetime import datetime

log_file = "system_log.txt"
# Limit log file size (1 MB)
if os.path.exists(log_file) and os.path.getsize(log_file) > 1_000_000:
    os.remove(log_file)

def get_cpu_usage():
    cpu_line = os.popen("top -b -n1 | grep 'Cpu(s)'").read()
    parts = cpu_line.split()

    try:
        idle = float(parts[7])
        return 100 - idle
    except:
        return 0.0  # fallback safety

def get_disk_usage():
    try:
        disk_output = os.popen("df -h /").read()
        lines = disk_output.strip().split("\n")

        usage_percent = 0

        if len(lines) > 1:
            usage = lines[1].split()[4]
            usage_percent = int(usage.replace('%', ''))

        return disk_output, usage_percent

    except:
        return "Error fetching disk usage\n", 

def main():
    cpu_usage = get_cpu_usage()
    disk_output, disk_usage = get_disk_usage()

    with open(log_file, "a") as f:
        f.write(f"\n===== {datetime.now()} =====\n")

        # CPU
        f.write(f"\nCPU Usage: {cpu_usage:.2f}%\n")
        if cpu_usage > 80:
            f.write("⚠️ ALERT: High CPU Usage!\n")

        # Memory
        f.write("\nMemory Usage:\n")
        f.write(os.popen("free -h").read())

        # Disk
        f.write("\nDisk Usage:\n")
        f.write(disk_output)

        if disk_usage > 80:
            f.write("⚠️ ALERT: Disk usage above 80%!\n")

if __name__ == "__main__":
    main()