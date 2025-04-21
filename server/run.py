from http.server import HTTPServer
from .server import CustomHandler
from .urls import urlpatterns

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Custom HTTP Server with API endpoint.")
    parser.add_argument("port", type=int, nargs="?", default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("directory", type=str, nargs="?", default=None, help="Directory to serve (default: current directory)")
    args = parser.parse_args()

    extra = {
        "urlpatterns": urlpatterns
    }
    if args.directory:
        extra['directory'] = args.directory
    
    handler_class = lambda *handler_args, **handler_kwargs: \
        CustomHandler(*handler_args, **handler_kwargs, **extra)
    
    server_address = ("", args.port)
    httpd = HTTPServer(server_address, handler_class)
    print(f"Serving on port http://0.0.0.0:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
