class VariableTypes:
    def __init__(self, _value="", _id="", name="", _type="", scope=""):
        self.value = _value
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

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self.type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def scope(self):
        return self.scope

    @scope.setter
    def scope(self, value):
        self._scope = value
