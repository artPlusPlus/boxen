class ObjectCache(object):
    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        while self._order > self._capacity:
            del self._objects[self._order.pop(0)]

    def __init__(self, capacity):
        self._capacity = capacity
        self._objects = {}
        self._order = []

    def __len__(self):
        return len(self._order)

    def __getitem__(self, key):
        return self._objects[key]

    def __setitem__(self, key, value):
        try:
            self._order.remove(key)
        except ValueError:
            self._objects[key] = value
        self._order.append(key)

        while self._order > self._capacity:
            del self._objects[self._order.pop(0)]

    def __delitem__(self, key):
        try:
            self._order.remove(key)
        except ValueError:
            pass

        try:
            del self._objects[key]
        except KeyError:
            pass

    def __iter__(self):
        for key in reversed(self._order):
            yield self._objects[key]

    def __reversed__(self):
        return [self._objects[k] for k in self._order]

    def __contains__(self, key):
        return key in self._objects