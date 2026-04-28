import argparse
import json
import socket
import time

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from sc.core import scan_range


console = Console()


def parse_ports(port_str):
    ports = set()

    for part in port_str.split(","):
        part = part.strip()

        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))

    return sorted(ports)


def build_info(item):
    http = item.get("http") or {}
    banner = item.get("banner")

    parts = []

    if http.get("status"):
        parts.append(http["status"])

    if http.get("server"):
        parts.append(f"Server: {http['server']}")

    if http.get("location"):
        parts.append(f"Redirect: {http['location']}")

    if not parts and banner:
        clean = banner.replace("\n", " | ").replace("\r", "")
        parts.append(clean[:120])

    return " | ".join(parts) if parts else "-"


def print_results(results):
    table = Table(title="Open Ports")

    table.add_column("Port", justify="right")
    table.add_column("Proto")
    table.add_column("Service")
    table.add_column("Info")

    for item in results:
        table.add_row(
            str(item["port"]),
            item["protocol"],
            item["service"],
            build_info(item),
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Port Scanner")

    parser.add_argument("host", help="Target host or IP")
    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help="Ports to scan. Example: 22,80,443 or 1-1000",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=50,
        help="Number of threads",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2,
        help="Socket timeout in seconds",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Save results as JSON file",
    )

    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.error:
        console.print("[red]Invalid host[/red]")
        return

    ports = parse_ports(args.ports)

    console.print(
        Panel.fit(
            f"[bold]Target:[/bold] {args.host} ({ip})\n"
            f"[bold]Ports:[/bold] {len(ports)}\n"
            f"[bold]Threads:[/bold] {args.threads}\n"
            f"[bold]Timeout:[/bold] {args.timeout}s",
            title="Port Scanner",
        )
    )

    start = time.time()
    results = scan_range(
        args.host,
        ports,
        threads=args.threads,
        timeout=args.timeout,
    )
    elapsed = time.time() - start

    if results:
        print_results(results)
    else:
        console.print("[yellow]No open ports found[/yellow]")

    console.print(
        f"\n[green]Scan finished[/green] "
        f"in {elapsed:.2f}s — "
        f"{len(results)} open port(s) found."
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2)

        console.print(f"[cyan]Results saved to:[/cyan] {args.output}")


if __name__ == "__main__":
    main()