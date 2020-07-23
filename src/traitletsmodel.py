
from traitlets import HasTraits, Unicode as String, Int, Float
from mvp import Model as Base


class Range(Float):
    def __init__(self, min, max):
        super(Range, self).__init__(min=min, max=max)
        return


class Model(HasTraits, Base):
    def __init__(self):
        super(Model, self).__init__()
        return

    def is_bindable(self, entry):
        return entry in self.class_trait_names()

    def connect(self, entry, action):
        self.observe(action, names=entry)
        return self._conversion

    def disconnect(self, entry, action):
        self.unobserve(action, names=entry)
        return

    def _conversion(self, event):
        return event['new']


if __name__ == '__main__':
    class MyModel(Model):
        weight = Range(0.0, 90.0)
        text = String("")

    model = MyModel()
    model1 = MyModel()
    func = None

    def foo(event):
        print func(event)

    if model.is_bindable("text"):
        func = model.connect("text", foo)
    setattr(model, "text", "123")
    setattr(model, "weight", 80)

    if model1.is_bindable("text"):
        func = model1.connect("text", foo)
    setattr(model1, "text", "456")
    setattr(model1, "weight", 81)

    try:
        setattr(model1, "weight", 100)
        print "check failed"
    except:
        print "check succeed."