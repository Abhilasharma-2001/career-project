import os
from datetime import datetime

log_file = "system_log.txt"

with open(log_file, "a") as f:
    f.write(f"\n===== {datetime.now()} =====\n")

    cpu_output = os.popen("top -b -n1 | head -5").read()
    f.write("\nCPU Usage:\n")
    f.write(cpu_output)

    # 🚨 ALERT LOGIC
    cpu_line = cpu_output.split("\n")[2]
    cpu_usage = float(cpu_line.split(",")[0].split()[1])

    if cpu_usage > 80:
        f.write("\n🚨 ALERT: High CPU Usage!\n")

    f.write("\nMemory Usage:\n")
    f.write(os.popen("free -h").read())

    f.write("\nDisk Usage:\n")
    f.write(os.popen("df -h").read())