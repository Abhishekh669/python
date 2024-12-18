import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import io

PORT = 8080

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the request URL
        url = urllib.parse.urljoin('http://', self.path[1:])  # Exclude the leading '/'
        print(f"Intercepting GET request for: {url}")

        # Fetch the content from the actual server
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
                # Print out response details
                print(f"Status code: {response.status}")
                print(f"Response headers: {response.headers}")

                # Send the response headers to the client
                self.send_response(response.status)
                for header in response.headers:
                    self.send_header(header, response.headers[header])
                self.end_headers()

                # Send the response content to the client
                self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        # Handle POST requests similarly
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse the request URL
        url = urllib.parse.urljoin('http://', self.path[1:])  # Exclude the leading '/'
        print(f"Intercepting POST request for: {url}")

        try:
            req = urllib.request.Request(url, data=post_data, headers=dict(self.headers))
            with urllib.request.urlopen(req) as response:
                content = response.read()
                # Print out response details
                print(f"Status code: {response.status}")
                print(f"Response headers: {response.headers}")

                # Send the response headers to the client
                self.send_response(response.status)
                for header in response.headers:
                    self.send_header(header, response.headers[header])
                self.end_headers()

                # Send the response content to the client
                self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

Handler = Proxy

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
