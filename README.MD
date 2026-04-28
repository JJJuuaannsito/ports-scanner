# 🔎 Port Scanner

A multithreaded TCP port scanner written in Python.

It detects open ports, guesses common services, performs basic banner grabbing, and displays the results in a clean terminal table using Rich.

---

## 🚀 Features

- TCP port scanning
- Scan single ports, multiple ports, or ranges
- Multithreaded scanning
- Basic service detection
- Basic banner grabbing
- HTTP/HTTPS status detection
- Redirect detection
- JSON output support
- Clean terminal UI with Rich

---

## 📦 Requirements

- Python 3.10+
- Rich

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/JJJuuaannsito/ports-scanner.git
cd port-scanner
```

---

## ▶️ Usage

```bash
python main.py <host> -p <ports>
```

### Examples

```bash
Scan common ports:

python main.py scanme.nmap.org -p 22,80,443

Scan a range:

python main.py scanme.nmap.org -p 1-1000

Use more threads:

python main.py scanme.nmap.org -p 1-1000 -t 100

Change timeout:

python main.py scanme.nmap.org -p 1-1000 --timeout 3

Save output as JSON:

python main.py scanme.nmap.org -p 1-1000 -o results.json
```

---

## 📄 Example Output

```
╭──── Simple Port Scanner ────╮
│ Target: scanme.nmap.org     │
│ Ports: 1000                 │
│ Threads: 50                 │
│ Timeout: 2.0s               │
╰─────────────────────────────╯

              Open Ports
┏━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Port ┃ Proto ┃ Service ┃ Info                 ┃
┡━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│   22 │ tcp   │ ssh     │ SSH-2.0-OpenSSH...   │
│   80 │ tcp   │ http    │ HTTP/1.1 200 OK ...  │
└──────┴───────┴─────────┴──────────────────────┘

Scan finished in 2.31s — 2 open port(s) found.
```

---

## ⚠️ Disclaimer

This tool is for educational purposes only.
Do not scan systems without permission.

---

## 📁 Project Structure

```
port_scanner/
├── main.py
├── sc/
│   ├── core.py
│   ├── config.py
│   ├── utils.py
│   └── __init__.py
```

---

Install dependencies:

```bash
pip install -r requirements.txt

---

## 📜 License

MIT License

```
