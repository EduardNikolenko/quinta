__all__ = ['Quinta']


class HTTPError(Exception):
    def __init__(self, status, message, *args, **kwargs):
        print(status, message)
        super().__init__(*args, **kwargs)


class Router(object):
    def __init__(self):
        self.builder = {}
        self.static = {}
    
    def match(self, environ):
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'
        if method in self.static and path in self.static[method]:
            target, getargs = self.static[method][path]
            return target, getargs(path) if getargs else {}
        raise HTTPError(404, "Not found: " + repr(path))
    
    def add(self, rule, method, target):
        self.static.setdefault(method, {})
        self.static[method][rule] = (target, None)


class Route(object):
    def __init__(self, app, rule, method, callback):
        self.app = app
        self.callback = callback
        self.method = method
        self.rule = rule
    
    def call(self):
        return self.callback()


class Quinta(object):
    def __init__(self):
        self.router = Router()
    
    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)
    
    def run(self, host='', port=8000):
        try:
            from wsgiref.simple_server import make_server
            httpd = make_server(host, port, self)
            print('Serving on port {0}'.format(port))
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Goodbye')
    
    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            route = Route(self, path, method, callback_func)
            self.router.add(route.rule, route.method, route)
            return callback_func
        
        return decorator(callback) if callback else decorator
    
    def _handle(self, environ):
        route, args = self.router.match(environ)
        return route.call()
    
    def wsgi(self, environ, start_response):
        out = self._handle(environ)
        if isinstance(out, str):
            out = out.encode('utf-8')
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [out]
