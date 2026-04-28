# 🔎 Port Scanner

A multithreaded TCP port scanner written in Python with a modern CLI built using Typer.

It detects open ports, identifies common services, performs basic banner grabbing, and displays results in a clean terminal table using Rich.

---

## 🚀 Features

- TCP port scanning
- Multithreaded scanning
- Service detection (based on known ports)
- Banner grabbing
- HTTP/HTTPS status detection
- Redirect detection
- JSON output support
- Clean CLI interface with Typer
- Rich terminal output (tables, colors)

---

## 📦 Requirements

- Python 3.10+
- Typer
- Rich

Install dependencies:

```bash
pip install -r requirements.txt

```

---

## 🛠️ Installation

```bash
git clone https://github.com/JJJuuaannsito/ports-scanner.git
cd ports-scanner
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python main.py [COMMAND] [OPTIONS]
```

---

## Commands

```bash
python main.py scan <host> -p <ports>
```

Examples

```bash
python main.py scan scanme.nmap.org -p 22,80,443
python main.py scan scanme.nmap.org -p 1-1000
python main.py scan scanme.nmap.org -p 1-1000 -t 100
python main.py scan scanme.nmap.org -p 1-1000 --timeout 3
python main.py scan scanme.nmap.org -p 1-1000 -o results.json
```

---

## 🌐 Resolve host

```bash
python main.py resolve google.com
```

---

## 📦 Version

```bash
python main.py version
```

---

## 📖 Help

```bash
python main.py --help
```

---

## ⚠️ Disclaimer

This tool is for educational purposes only.

Only scan systems you own or have explicit permission to test.
