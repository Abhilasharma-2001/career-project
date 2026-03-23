import os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

log_file = "system_log.txt"
old_log_file = "system_log_old.txt"
last_alert_file = "last_alert.txt"

# Rotate log if > 1MB (keep old log)
if os.path.exists(log_file) and os.path.getsize(log_file) > 1_000_000:
    if os.path.exists(old_log_file):
        os.remove(old_log_file)
    os.rename(log_file, old_log_file)

# ---------------- CPU ----------------
def get_cpu_usage():
    cpu_line = os.popen("top -b -n1 | grep 'Cpu(s)'").read()
    parts = cpu_line.split()

    try:
        idle = float(parts[7])
        return 100 - idle
    except:
        return 0.0

# ---------------- DISK ----------------
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
        return "Error fetching disk usage\n", 0

# ---------------- EMAIL ----------------
def send_email_alert(message):
    sender = "ygamakasaaki@gmail.com"
    receiver = "ygamakasaaki@gmail.com"

    # Use environment variable (SECURE)
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(message)
    msg["Subject"] = "🚨 System Alert"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email failed:", e)

# ---------------- ALERT CONTROL ----------------
def can_send_alert():
    if not os.path.exists(last_alert_file):
        return True

    try:
        last_time = float(open(last_alert_file).read())
        return (time.time() - last_time) > 300  # 5 minutes gap
    except:
        return True

def update_alert_time():
    with open(last_alert_file, "w") as f:
        f.write(str(time.time()))

# ---------------- MAIN ----------------
def main():
    cpu_usage = get_cpu_usage()
    disk_output, disk_usage = get_disk_usage()

    with open(log_file, "a") as f:
        f.write(f"\n===== {datetime.now()} =====\n")

        # CPU
        f.write(f"\nCPU Usage: {cpu_usage:.2f}%\n")
        if cpu_usage > 80 and can_send_alert():
            alert_msg = f"High CPU Usage Alert: {cpu_usage:.2f}%"
            f.write("⚠️ ALERT: High CPU Usage!\n")
            send_email_alert(alert_msg)
            update_alert_time()

        # Memory
        f.write("\nMemory Usage:\n")
        f.write(os.popen("free -h").read())

        # Disk
        f.write("\nDisk Usage:\n")
        f.write(disk_output)

        if disk_usage > 80:
            f.write("⚠️ ALERT: Disk usage above 80%!\n")

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()