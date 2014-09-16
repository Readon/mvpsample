
from eventize import handle, Attribute
from mvp import Model as Base


class Model(Base):
    def __init__(self):
        super(Model, self).__init__()
        self._connections = {}
        return

    def is_bindable(self, entry):
        item = getattr(self, entry)
        return not callable(item)

    def connect(self, entry, action):
        if entry not in self._connections:
            connection = handle(self, entry)
            self._connections[entry] = connection
        else:
            connection = self._connections[entry]
        connection.on_change += action
        return self._convertion

    def disconnect(self, entry, action):
        if entry in self._connections:
            connection = self._connections[entry]
            connection.on_change -= action
        return

    def _convertion(self, event):
        return event.value

if __name__ == '__main__':
    class MyModel(Model):
        text = ""

    model = MyModel()
    func = None

    def foo(event):
        print func(event)

    if model.is_bindable("text"):
        func = model.connect("text", foo)
    setattr(model, "text", "123")
    print model.text