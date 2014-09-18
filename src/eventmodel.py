
from eventize import on_change
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
        try:
            connection = self._connections[entry]
        except:
            connection = on_change(self, entry)
            self._connections[entry] = connection
        connection += action
        return self._convertion

    def disconnect(self, entry, action):
        try:
            connection = self._connections[entry]
            connection -= action
        except:
            pass
        return

    def _convertion(self, event):
        return event.value

if __name__ == '__main__':
    class MyModel(Model):
        text = "oo"

    model = MyModel()
    func = None

    def foo(event):
        print "trigger"
        print func(event)
        setattr(model, "text", func(event))

    if model.is_bindable("text"):
        func = model.connect("text", foo)
    setattr(model, "text", "123")
    print model.text