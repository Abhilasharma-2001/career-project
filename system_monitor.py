import os
from datetime import datetime

log_file = "system_log.txt"

with open(log_file, "a") as f:
    f.write(f"\n===== {datetime.now()} =====\n")

    f.write("\nCPU Usage:\n")
    f.write(os.popen("top -b -n1 | head -5").read())

    f.write("\nMemory Usage:\n")
    f.write(os.popen("free -h").read())

    f.write("\nDisk Usage:\n")
    f.write(os.popen("df -h").read())