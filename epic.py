import os
import time
from collections import Counter

LOG_PATH = "/var/log/nginx/access.log"
LIMIT = 100
INTERVAL = 60

def monitor_traffic():
    while True:
        try:
            with open(LOG_PATH, "r") as f:
                lines = f.readlines()
                
            ips = [line.split()[0] for line in lines]
            ip_counts = Counter(ips)

            for ip, count in ip_counts.items():
                if count > LIMIT:
                    print(f"IP {ip} terdeteksi DDoS ({count} request). Memblokir...")
                    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
            
            open(LOG_PATH, "w").close()
            
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor_traffic()
