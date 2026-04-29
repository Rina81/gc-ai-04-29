#!/usr/bin/env python3
"""
MCP Server Manager - Start, stop, and monitor MCP servers
"""
import json
import subprocess
import sys
import os
import time
import requests
from pathlib import Path

class MCPServerManager:
    def __init__(self, config_file='mcp.json'):
        self.config_file = config_file
        self.servers = {}
        self.processes = {}
        self.load_config()
    
    def load_config(self):
        """Load servers from mcp.json"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.servers = config.get('servers', {})
        except FileNotFoundError:
            print(f"Error: {self.config_file} not found")
            sys.exit(1)
    
    def check_server_status(self, name, server_config):
        """Check if a server is running"""
        if server_config.get('type') == 'http':
            url = server_config.get('url')
            try:
                response = requests.get(url, timeout=2)
                return True, f"Running (Status: {response.status_code})"
            except:
                return False, "Not responding"
        return False, "Unknown type"
    
    def status(self, output_file=None):
        """Show status of all servers"""
        output = []
        output.append("\n" + "="*60)
        output.append("MCP SERVER STATUS")
        output.append("="*60)
        
        if not self.servers:
            output.append("No servers configured in mcp.json")
        else:
            for name, config in self.servers.items():
                is_running, status_msg = self.check_server_status(name, config)
                status_indicator = "✓" if is_running else "✗"
                server_type = config.get('type', 'unknown')
                url = config.get('url', config.get('command', 'N/A'))
                
                output.append(f"\n[{status_indicator}] {name}")
                output.append(f"    Type: {server_type}")
                output.append(f"    URL/Command: {url}")
                output.append(f"    Status: {status_msg}")
        
        output.append("\n" + "="*60 + "\n")
        
        result = "\n".join(output)
        
        # Print to console
        print(result)
        
        # Write to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"Status saved to {output_file}")
    
    def start_server(self, name):
        """Start a server"""
        if name not in self.servers:
            print(f"Error: Server '{name}' not found in config")
            return False
        
        server_config = self.servers[name]
        
        if server_config.get('type') == 'http':
            print(f"Note: Server '{name}' is a remote HTTP endpoint.")
            print(f"URL: {server_config.get('url')}")
            print("No local process to start.")
            return True
        
        if server_config.get('type') == 'stdio':
            try:
                cmd = [server_config.get('command')] + server_config.get('args', [])
                print(f"Starting {name}...")
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.processes[name] = proc
                print(f"✓ Server '{name}' started (PID: {proc.pid})")
                return True
            except Exception as e:
                print(f"✗ Failed to start {name}: {e}")
                return False
    
    def stop_server(self, name):
        """Stop a running server"""
        if name not in self.processes:
            print(f"Server '{name}' is not running")
            return False
        
        try:
            proc = self.processes[name]
            proc.terminate()
            proc.wait(timeout=5)
            del self.processes[name]
            print(f"✓ Server '{name}' stopped")
            return True
        except Exception as e:
            print(f"✗ Failed to stop {name}: {e}")
            return False
    
    def list_servers(self):
        """List all configured servers"""
        print("\nConfigured servers:")
        for name, config in self.servers.items():
            print(f"  - {name} ({config.get('type')})")
    
    def interactive_menu(self):
        """Interactive menu for server management"""
        while True:
            print("\n" + "="*60)
            print("MCP SERVER MANAGER")
            print("="*60)
            print("\nOptions:")
            print("  1. Show status (console)")
            print("  2. Show status (save to file)")
            print("  3. Start server")
            print("  4. Stop server")
            print("  5. List servers")
            print("  6. Exit")
            print("\n" + "-"*60)
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.status()
            elif choice == '2':
                filename = input("Enter filename (default: server_status.txt): ").strip()
                if not filename:
                    filename = "server_status.txt"
                self.status(filename)
            elif choice == '3':
                self.list_servers()
                name = input("\nEnter server name to start: ").strip()
                self.start_server(name)
            elif choice == '4':
                name = input("Enter server name to stop: ").strip()
                self.stop_server(name)
            elif choice == '5':
                self.list_servers()
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid option")

def main():
    manager = MCPServerManager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == 'status':
            output_file = sys.argv[2] if len(sys.argv) > 2 else None
            manager.status(output_file)
        elif cmd == 'start':
            if len(sys.argv) > 2:
                manager.start_server(sys.argv[2])
            else:
                print("Usage: python server_manager.py start <server_name>")
        elif cmd == 'stop':
            if len(sys.argv) > 2:
                manager.stop_server(sys.argv[2])
            else:
                print("Usage: python server_manager.py stop <server_name>")
        elif cmd == 'list':
            manager.list_servers()
        elif cmd == 'interactive':
            manager.interactive_menu()
        else:
            print("Unknown command")
    else:
        manager.interactive_menu()

if __name__ == '__main__':
    main()
