#!/usr/bin/env python3
"""
Simple HTTP server for testing the CS2 Esports Tracker
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import threading
import time

# Configuration
PORT = 8080
TEST_PAGE = "standalone-test.html"

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Default to index.html for root requests
        if self.path == '/':
            self.path = f'/{TEST_PAGE}'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1)
    url = f"http://localhost:{PORT}"
    print(f"Opening test page in browser: {url}")
    webbrowser.open(url)

def main():
    # Change to the app directory
    os.chdir('/app')
    
    # Start the server
    handler = TestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    
    print(f"Starting test server on port {PORT}...")
    print(f"Test page: http://localhost:{PORT}/{TEST_PAGE}")
    print("Press Ctrl+C to stop the server")
    
    # Open browser in a new thread
    threading.Thread(target=open_browser).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    main()