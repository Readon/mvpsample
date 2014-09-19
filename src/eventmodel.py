
from eventize import on_change, Attribute
from eventize.attribute import Subject, OnChangeHandler
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


class Range(Attribute):
    def __init__(self, min_, max_, default=None):
        if default is not None:
            super(Range, self).__init__(default)
        else:
            super(Range, self).__init__(min_)

        self._min = min_
        self._max = max_
        self.on_change = OnChangeHandler(self._validate)

    def _validate(self, event):
        print event.value, self._max, self._min
        if event.value > self._max or event.value < self._min:
            raise Exception('Value out of Range (%d, %d)' % (self._min, self._max))


if __name__ == '__main__':
    class MyModel(Model):
        weight = Range(1, 90)
        text = "oo"

    model = MyModel()
    model1 = MyModel()
    func = None

    def foo(event):
        print "trigger"
        print func(event)
        setattr(model, "text", func(event))

    if model.is_bindable("weight"):
        func = model.connect("weight", foo)
    setattr(model, "text", "123")
    setattr(model, "weight", 80)
    setattr(model1, "weight", 81)
    print model.text