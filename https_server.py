from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from urllib.parse import parse_qs

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            try:
                with open("index.html", "rb") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()

        print("RAW POST:", data)

        params = parse_qs(data)
        print("PARSED:", params)

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Login received</h1>")

httpd = HTTPServer(("0.0.0.0", 8443), MyHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("HTTPS server running on https://0.0.0.0:8443")
httpd.serve_forever()
