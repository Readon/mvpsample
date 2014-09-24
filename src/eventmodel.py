
from eventize import on_change, Attribute
from eventize import Attribute as String
from eventize import Attribute as Int
from eventize import Attribute as Float
from eventize.attribute import OnChangeHandler
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
            item = getattr(type(self), entry)
            handle_type = item.__class__
            connection = on_change(self, entry, handle_type)
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
    on_change = OnChangeHandler()
    def __init__(self, min_, max_, default=None):
        super(Range, self).__init__(default or min_)

        self._min = min_
        self._max = max_
        self.on_change += self._validate

    def _validate(self, event):
        if event.value > self._max or event.value < self._min:
            setattr(event.subject, event.name, event.old_value)
            raise Exception('Value %d out of Range (%d, %d)' % (event.value, self._min, self._max))


if __name__ == '__main__':
    class MyModel(Model):
        weight = Range(1, 90)
        text = Attribute("oo")

    model = MyModel()
    model1 = MyModel()
    func = None

    def foo(event):
        print func(event)

    if model.is_bindable("weight"):
        func = model.connect("weight", foo)
    setattr(model, "text", "123")
    setattr(model, "weight", 80)

    if model1.is_bindable("weight"):
        func = model1.connect("weight", foo)
    setattr(model1, "text", "456")
    setattr(model1, "weight", 81)

    try:
        setattr(model1, "weight", 100)
        print "check failed."
    except:
        print "check succeed."
    print model1.text