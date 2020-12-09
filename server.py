from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = self.path

        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        print("Request headers:", self.headers)
        print("<----- Request End -----\n")

        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()

    def do_POST(self):
        request_path = self.path

        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)

        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        #body = self.body

        print("Content Length:", length)
        print("Request headers:", request_headers)
        print("Request payload:", self.rfile.read(28))
        print("Body:", self)
        print("<----- Request End -----\n")

        self.send_response(200)
        self.end_headers()

    do_PUT = do_POST
    do_DELETE = do_GET

def main():
    port = 8889
    print('Listening on localhost:%s' % port)
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.set_ciphers('ALL:@SECLEVEL=0')
    ctx.load_verify_locations('ac14k_m.pem')
    server = HTTPServer(('', port), RequestHandler)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    server.serve_forever()

if __name__ == "__main__":
    main()
