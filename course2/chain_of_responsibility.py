EVENT_INT, EVENT_FLOAT, EVENT_STRING = "int", "float", "string"


class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, prop):
        self.kind = {int: EVENT_INT, float: EVENT_FLOAT, str: EVENT_STRING}[prop]
        self.prop = None


class EventSet:
    def __init__(self, prop):
        self.kind = {int: EVENT_INT, float: EVENT_FLOAT, str: EVENT_STRING}[type(prop)]
        self.prop = prop


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == EVENT_INT:
            if event.prop is None:
                return obj.integer_field
            else:
                obj.integer_field = event.prop
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == EVENT_FLOAT:
            if event.prop is None:
                return obj.float_field
            else:
                obj.float_field = event.prop
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == EVENT_STRING:
            if event.prop is None:
                return obj.string_field
            else:
                obj.string_field = event.prop
        else:
            return super().handle(obj, event)
