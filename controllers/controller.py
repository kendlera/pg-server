from flask import Blueprint
import inspect


# controller abstract class
class Controller(Blueprint):
    def __init__(self, name, import_name, template_folder=None):
        Blueprint.__init__(self, name, import_name, template_folder=template_folder)

        # allows usage of route descriptor
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(method, "routes"):
                for rule, options in method.routes:
                    self.route(rule, **options)(method)