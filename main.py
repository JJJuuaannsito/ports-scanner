import typer
import socket
import time
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from sc.core import scan_range

app = typer.Typer(help="Python Port Scanner")
console = Console()


def parse_ports(port_str: str):
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


# =========================
# COMMAND: scan
# =========================
@app.command()
def scan(
    host: str = typer.Argument(..., help="Target host or IP"),
    ports: str = typer.Option("1-1024", "-p", help="Ports to scan"),
    threads: int = typer.Option(50, "-t", help="Number of threads"),
    timeout: float = typer.Option(2, help="Timeout in seconds"),
    output: str = typer.Option(None, "-o", help="Save results to JSON"),
):
    """Scan a host for open ports."""

    try:
        ip = socket.gethostbyname(host)
    except socket.error:
        console.print("[red]Invalid host[/red]")
        raise typer.Exit()

    port_list = parse_ports(ports)

    console.print(
        Panel.fit(
            f"[bold]Target:[/bold] {host} ({ip})\n"
            f"[bold]Ports:[/bold] {len(port_list)}\n"
            f"[bold]Threads:[/bold] {threads}\n"
            f"[bold]Timeout:[/bold] {timeout}s",
            title="Port Scanner",
        )
    )

    start = time.time()

    results = scan_range(
        host,
        port_list,
        threads=threads,
        timeout=timeout,
    )

    elapsed = time.time() - start

    if results:
        print_results(results)
    else:
        console.print("[yellow]No open ports found[/yellow]")

    console.print(
        f"\n[green]Scan finished[/green] in {elapsed:.2f}s — {len(results)} open ports."
    )

    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        console.print(f"[cyan]Saved to {output}[/cyan]")


# =========================
# COMMAND: resolve
# =========================
@app.command()
def resolve(
    host: str = typer.Argument(..., help="Domain or IP to resolve"),
):
    """Resolve a domain to IP and reverse DNS."""

    try:
        ip = socket.gethostbyname(host)
        console.print(f"[green]IP:[/green] {ip}")
    except socket.error:
        console.print("[red]Could not resolve host[/red]")
        raise typer.Exit()

    try:
        reverse = socket.gethostbyaddr(ip)[0]
        console.print(f"[green]Reverse DNS:[/green] {reverse}")
    except socket.herror:
        console.print("[yellow]No reverse DNS found[/yellow]")


# =========================
# COMMAND: version
# =========================
@app.command()
def version():
    """Show tool version."""
    console.print("[bold cyan]Port Scanner v0.1[/bold cyan]")


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    app()