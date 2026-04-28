import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
from .config import TIMEOUT, MAX_THREADS


HTTP_PORTS = {80, 8080, 8000, 8888}
HTTPS_PORTS = {443, 8443}


def guess_service_by_port(port):
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def parse_http_info(banner):
    info = {
        "status": None,
        "server": None,
        "location": None,
    }

    if not banner:
        return info

    lines = banner.splitlines()

    if lines:
        info["status"] = lines[0].strip()

    for line in lines:
        lower = line.lower()

        if lower.startswith("server:"):
            info["server"] = line.split(":", 1)[1].strip()

        elif lower.startswith("location:"):
            info["location"] = line.split(":", 1)[1].strip()

    return info


def grab_http_banner(host, port):
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
            sock.settimeout(TIMEOUT)

            request = (
                f"HEAD / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: simple-port-scanner\r\n"
                f"Connection: close\r\n\r\n"
            ).encode()

            sock.sendall(request)
            return sock.recv(4096).decode(errors="ignore").strip()

    except Exception:
        return None


def grab_https_banner(host, port):
    try:
        context = ssl.create_default_context()

        with socket.create_connection((host, port), timeout=TIMEOUT) as raw_sock:
            raw_sock.settimeout(TIMEOUT)

            with context.wrap_socket(raw_sock, server_hostname=host) as tls_sock:
                request = (
                    f"HEAD / HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: simple-port-scanner\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode()

                tls_sock.sendall(request)
                return tls_sock.recv(4096).decode(errors="ignore").strip()

    except ssl.SSLError:
        return "TLS detected, but handshake failed"

    except Exception:
        return None


def grab_tcp_banner(host, port):
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
            sock.settimeout(TIMEOUT)
            sock.sendall(b"\r\n")
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner or None

    except Exception:
        return None


def scan_port(host, port, timeout=None):
    timeout = timeout or TIMEOUT

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

        if result != 0:
            return None

        service = guess_service_by_port(port)
        banner = None
        http_info = {}

        if port in HTTPS_PORTS:
            service = "https"
            banner = grab_https_banner(host, port)
            http_info = parse_http_info(banner)

        elif port in HTTP_PORTS:
            service = "http"
            banner = grab_http_banner(host, port)
            http_info = parse_http_info(banner)

        else:
            banner = grab_tcp_banner(host, port)

        return {
            "port": port,
            "protocol": "tcp",
            "service": service,
            "banner": banner,
            "http": http_info,
        }

    except Exception:
        return None


def scan_range(host, ports, threads=None, timeout=None):
    threads = threads or MAX_THREADS
    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda p: scan_port(host, p, timeout), ports)

    for result in results:
        if result:
            open_ports.append(result)

    return sorted(open_ports, key=lambda item: item["port"])