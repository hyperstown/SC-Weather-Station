import json
import traceback
from urllib.parse import urlparse, parse_qs
from http.server import SimpleHTTPRequestHandler

from . import settings

class Request:
    def __init__(self, instance):
        url_parts = urlparse(instance.path)

        self.query_params = parse_qs(url_parts.query)
        self.url = url_parts.path
        self.headers = instance.headers
        self.data = None

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.urlpatterns = kwargs.pop('urlpatterns', [])
        return super().__init__(*args, **kwargs)

    def do_GET(self):
        request = Request(self)
        if request.url in self.urlpatterns:
            self.dispatch(request)
        else:
            super().do_GET()

    def dispatch(self, request):
        try:
            view = self.urlpatterns[request.url]
            data = view(request)
            self.send_response(200)
            if isinstance(data, (dict, list)):
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            self.wfile.write(data.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            error_template = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>{type(e).__name__} at {request.url}</title>
                </head>
                <body>
                    <h4>{type(e).__name__} at {request.url}</h4>
                    <div><pre>{traceback.format_exc()}</pre></div>
                </body>
                </html>
            """ if settings.DEBUG else f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                  <title>500 Internal Server Error</title>
                </head>
                <body>
                  <h1>Internal Server Error</h1>
                  <p>The server was unable to complete your request. Please try again later.</p>
                </body>
                </html>
            """
            traceback.print_exc()
            self.wfile.write(error_template.encode("utf-8"))

