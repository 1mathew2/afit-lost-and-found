"""One-command launcher: serves the portal to the LAN and generates a QR code for the phone.

Usage:  python serve.py
Then scan the QR (qr.png) with your phone camera, or type the printed URL.
"""
import io
import os
import socket
import subprocess
import sys

PORT = 8000
ROOT = os.path.dirname(os.path.abspath(__file__))


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
        img = qrcode.make(url)
        img.save(path)
        return True
    except ImportError:
        return False


def main():
    ip = lan_ip()
    url = f"http://{ip}:{PORT}"
    qr_path = os.path.join(ROOT, "scan_me_qr.png")
    have_qr = make_qr(url, qr_path)

    print("=" * 56)
    print("  AFIT Lost & Found Portal — sharing mode")
    print("=" * 56)
    print(f"  On this PC :  http://localhost:{PORT}")
    print(f"  On phones  :  {url}   (same Wi-Fi required)")
    if have_qr:
        print(f"  QR code    :  {qr_path}  — open it and scan with the phone camera")
    else:
        print("  QR code    :  run  pip install qrcode  and restart to get one")
    print()
    print("  If the phone cannot connect, allow Python through the")
    print("  Windows firewall prompt (private networks) and make sure")
    print("  both devices are on the SAME Wi-Fi (not a guest network).")
    print("=" * 56)

    try:
        subprocess.call([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0", "--port", str(PORT),
        ], cwd=ROOT)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
