import http.server
import os

class NotFoundException(Exception):
    pass

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = os.getcwd() + self.path

            if not os.path.exists(path) and not os.path.isfile(path):
                raise NotFoundException(f'{self.path} not found')
            elif os.path.exists(path):
                # path is a directory
                # want to see if there is an index.html or index.htm file inside
                if os.path.isfile(os.path.join(path, 'index.html')):
                    path = os.path.join(path, 'index.html')
                elif os.path.isfile(os.path.join(path, 'index.htm')):
                    path = os.path.join(path, 'index.htm')
                else:
                    pass
                    #send a list of files in the directory

            with open(path, 'rb') as file:
                self.send(file.read())
        except NotFoundException as e:
            self.error_handler(e)
        except IOError as e:
            self.error_handler('server read error')

    def error_handler(self, err):
        error_page = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Web-Server Python</title>
                </head>
                <body>
                    <p>Error code: 404</p>
                </body>
            </html>
        """
        print(err)
        self.send(bytes(error_page, 'utf-8'), status=404)

    def send(self, content, status=200): #contents in bytes
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == '__main__':
    with http.server.HTTPServer(('', 8080), HTTPRequestHandler) as httpd:
        httpd.serve_forever()

