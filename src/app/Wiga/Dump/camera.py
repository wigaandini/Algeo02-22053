import http.server
import socketserver

# Specify the port you want to use
PORT = 8000

# Change to the directory where your HTML file is located
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()