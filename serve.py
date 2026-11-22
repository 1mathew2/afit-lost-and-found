"""One-command launcher for the AFIT Lost & Found Portal.

Usage:
    python serve.py            # LAN sharing + public tunnel (if cloudflared.exe is present)
    python serve.py --lan      # LAN sharing only (no internet needed)

Prints the URLs and writes scan_me_qr.png — scan it with the phone camera.
"""
import os
import re
import socket
import subprocess
import sys
import threading
import time

PORT = 8000
ROOT = os.path.dirname(os.path.abspath(__file__))
TUNNEL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")


def lan_ip():
    """Best-effort local LAN IP (the address the phone would reach)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))          # no traffic is sent; just picks a route
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def make_qr(url, path):
    try:
        import qrcode
        qrcode.make(url).save(path)
        return True
    except ImportError:
        return False


def start_tunnel():
    """Starts a cloudflared quick tunnel; returns (process, url_or_None)."""
    exe = os.path.join(ROOT, "cloudflared.exe")
    if not os.path.exists(exe):
        return None, None
    try:
        proc = subprocess.Popen(
            [exe, "tunnel", "--url", f"http://localhost:{PORT}", "--no-autoupdate"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", cwd=ROOT,
        )
    except OSError:
        return None, None
    deadline = time.time() + 20
    while time.time() < deadline:
        line = proc.stdout.readline() if proc.stdout else ""
        m = TUNNEL_RE.search(line)
        if m:
            return proc, m.group(0)
        if proc.poll() is not None:
            return proc, None
    return proc, None


def main():
    lan_only = "--lan" in sys.argv
    ip = lan_ip()
    lan_url = f"http://{ip}:{PORT}"

    tunnel = None
    public_url = None
    if not lan_only:
        print("Starting public tunnel (cloudflared)...")
        tunnel, public_url = start_tunnel()

    share_url = public_url or lan_url
    qr_path = os.path.join(ROOT, "scan_me_qr.png")
    have_qr = make_qr(share_url, qr_path)

    print("=" * 60)
    print("  AFIT Lost & Found Portal — sharing mode")
    print("=" * 60)
    print(f"  On this PC :  http://localhost:{PORT}")
    print(f"  Same Wi-Fi :  {lan_url}")
    if public_url:
        print(f"  ANYWHERE   :  {public_url}")
    else:
        print("  Public link:  unavailable (no internet or cloudflared missing) — LAN still works")
    if have_qr:
        print(f"  QR code    :  {qr_path}  (points at the {'public' if public_url else 'LAN'} link)")
    else:
        print("  QR code    :  run  pip install qrcode  and restart to get one")
    print()
    print("  Phone setup: scan the QR, or open the URL, then use the browser")
    print("  menu -> 'Add to Home screen / Install' to get the app icon.")
    if public_url:
        print("  Note: the public link is temporary and expires when this")
        print("  window is closed or the PC sleeps.")
    print("=" * 60)

    try:
        subprocess.call([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0", "--port", str(PORT),
        ], cwd=ROOT)
    except KeyboardInterrupt:
        pass
    finally:
        if tunnel and tunnel.poll() is None:
            tunnel.terminate()


if __name__ == "__main__":
    main()
