# allows for decorating routes int the Controller class
def route(rule, **options):
    def wrap(fn):
        routes = getattr(fn, 'routes', [])      # routes = fn.routes default=[]
        routes.append((rule, options))
        setattr(fn, 'routes', routes)           # fn.routes = routes
        return fn
    return wrap

