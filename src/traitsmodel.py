
from traits.api import HasTraits, TraitType
from mvp import Model as Base


class Model(HasTraits, Base):
    def __init__(self):
        super(Model, self).__init__()
        return

    def is_bindable(self, entry):
        return entry in self.class_trait_names()

    def connect(self, entry, action):
        self.on_trait_change(action, entry)
        return self._convertion

    def disconnect(self, entry, action):
        self.on_trait_change(action, entry, remove=True)
        return

    def _convertion(self, event):
        return event


from traits.api import String, Range
if __name__ == '__main__':
    class MyModel(Model):
        weight = Range(0, 90)
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