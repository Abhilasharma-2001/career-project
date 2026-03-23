import os
print("CPU Usage: ")
os.system("top -b -n1 | head -5")

print("\n Memory Usage: ")
os.system("free -h")

print("Disk Usage: ")
os.system("df -h")