import os
import uuid

try:
    import ujson as json_lib
except ImportError:
    try:
        import simplejson as json_lib
    except ImportError:
        import json as json_lib


class Container(object):
    """
    Manages file i/o for a set of objects.
    """
    def __init__(self):
        self._path = None
        self._id = None,
        self._object_map = {}
        self._object_order = []

    def get(self, key):
        try:
            return self._object_map[key]
        except KeyError:
            return None

    def put(self, key, object_data):
        self._object_map[key] = object_data
        if key not in self._object_order:
            self._object_order.append(key)

        self._write()

        return key

    def post(self, object_data):
        key = str(uuid.uuid4())
        self._object_map[key] = object_data
        self._object_order.append(key)

        self._write()

        return key

    def delete(self, key):
        try:
            del self._object_map[key]
        except KeyError:
            pass

        try:
            self._object_order.remove(key)
        except ValueError:
            pass

    def _write(self):
        data = {}
        data['id'] = self._id
        data['object_keys'] = self._object_order
        data['object_data'] = [self._object_map[k] for k in self._object_order]
        with open(self._path, mode='w') as cf:
            cf.write(json_lib.dumps(data))

    def _read(self, path):
        if not os.path.isfile(path):
            msg = 'boxen container file not found: {0}'.format(path)
            raise IOError(msg)

        with open(path, mode='r') as cf:
            data = json_lib.loads(cf.read())

        self._path = path
        self._id = data['id']
        for key, data in zip(data['object_keys'], data['object_data']):
            self._object_order.append(key)
            self._object_map[key] = data

    def __len__(self):
        return len(self._object_map)

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self._object_order[key]
        return self._object_map[key]

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if isinstance(key, int):
            key = self._object_order[key]
        self.delete(key)

    def __iter__(self):
        for key in self._object_order:
            yield self._object_map[key]

    def __reversed__(self):
        return [self._object_map[k] for k in reversed(self._object_map)]

    def __contains__(self, key):
        return key in self._object_map
