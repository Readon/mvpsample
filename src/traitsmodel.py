
from traits.api import HasTraits
from mvp import Model


class TraitsModel(HasTraits, Model):
    def __init__(self):
        super(TraitsModel, self).__init__()
        return