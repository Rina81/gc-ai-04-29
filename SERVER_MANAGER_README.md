# MCP Server Manager

Simple CLI tool to manage MCP servers defined in `mcp.json`.

## Usage

### Interactive Mode (Default)
```bash
python server_manager.py
```
Or:
```bash
python server_manager.py interactive
```

### Command Line Mode

**Check server status (print to console):**
```bash
python server_manager.py status
```

**Check server status (save to file):**
```bash
python server_manager.py status <filename>
```
Example:
```bash
python server_manager.py status server_status.txt
```

**Start a server:**
```bash
python server_manager.py start <server_name>
```

**Stop a server:**
```bash
python server_manager.py stop <server_name>
```

**List all configured servers:**
```bash
python server_manager.py list
```

## Features

- ✓ View status of all configured servers
- ✓ Check HTTP server availability with automatic HTTP requests
- ✓ Start/stop local stdio servers
- ✓ Interactive menu for easy management
- ✓ Command-line interface for automation

## Requirements

- Python 3.7+
- `requests` library (for HTTP server status checks)

Install requests:
```bash
pip install requests
```

## Server Configuration

Servers are read from `mcp.json`. Supported types:
- `http`: Remote HTTP endpoints (monitored but not managed locally)
- `stdio`: Local processes that can be started/stopped
