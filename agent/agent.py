# agent/agent.py
# NetID Guardian - Simple Agent for network scanning and posting events to backend.
# WARNING: Use only on networks you own or in lab environments.
import time
import requests
import nmap
import json
import os

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000/api/events')
SCAN_NET = os.environ.get('SCAN_NET', '192.168.1.0/24')

def arp_scan(network):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=network, arguments='-sn')
    except Exception as e:
        print('nmap scan failed:', e)
        return []
    hosts = []
    for host in nm.all_hosts():
        host_data = nm[host]
        addr = host_data.get('addresses', {})
        ip = addr.get('ipv4','')
        mac = addr.get('mac','')
        hosts.append({'ip': ip, 'mac': mac})
    return hosts

def port_scan(ip):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=ip, arguments='-sS -Pn -p 1-1024 --open --min-rate 500')
    except Exception as e:
        return []
    open_ports = []
    try:
        for proto in nm[ip].all_protocols():
            ports = nm[ip][proto].keys()
            for p in ports:
                open_ports.append(int(p))
    except Exception:
        pass
    return open_ports

def send_event(event):
    try:
        r = requests.post(BACKEND_URL, json=event, timeout=5)
        print('Sent event, status', r.status_code)
    except Exception as e:
        print('Failed to send event:', e)

def main_loop():
    while True:
        print('Starting ARP scan on', SCAN_NET)
        hosts = arp_scan(SCAN_NET)
        for h in hosts:
            ip = h.get('ip')
            mac = h.get('mac')
            if not ip:
                continue
            ports = port_scan(ip)
            event = {
                'type': 'device_scan',
                'ip': ip,
                'mac': mac,
                'open_ports': ports,
                'timestamp': int(time.time())
            }
            send_event(event)
        print('Scan complete. Sleeping 300s.')
        time.sleep(300)

if __name__ == '__main__':
    main_loop()
