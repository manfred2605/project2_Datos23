class VariableTypes:
    def __init__(self, value="", _id="", name="", _type="", scope=""):
        self.value = value
        self.id = _id
        self.name = name
        self.type = _type
        self.scope = scope

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self.value = value
