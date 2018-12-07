
class Facet(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Facet):
            return self.name == other.name and self.value == other.value
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
