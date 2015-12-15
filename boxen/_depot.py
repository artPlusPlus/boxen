import os

try:
    import ujson as jlib
except ImportError:
    try:
        import simplejson as jlib
    except ImportError:
        import json as jlib

from ._object_cache import ObjectCache
from ._container import Container


class Depot(object):
    """
    A Depot manages Containers.


    """
    @property
    def _current_container(self):
        if self._cur_container is None or len(self._cur_container) == self._container_object_limit:
            container = Container()
            container_name = '{0:06d}'.format(len(self._containers))
            container_name = '_'.join([self._container_prefix, container_name, self._container_suffix])
            container._path = os.path.join(self._location, container_name)
            self._containers.append(container)

            self._cur_container = container
        return self._cur_container

    def __init__(self, cache_capacity=1000):
        self._name = None
        self._location = None
        self._object_cache = _ObjectCache(cache_capacity)
        self._container_object_limit = 1000
        self._map__object_key__container_key = {}
        self._containers = {}
        self._next_available_container = None

        self._object_cache_size = 1000
        self._container_prefix = ''
        self._container_suffix = ''

    def get(self, object_key):
        try:
            result = self._object_cache[object_key]
        except KeyError:
            container_key = self._map__object_key__container_key[object_key]
            container = self._containers[container_key]
            result = container.get(object_key)
        self._object_cache[object_key] = result
        # TODO: Implemement cache resizing
        return result

    def post(self, object_data):
        self._next_available_container.post(object_data)

    def put(self, key, object_data):
        try:
            container = self._map__object_key__container[key]
        except KeyError:
            container = self._next_available_container
        container.put(key, object_data)

    def delete(self, key):
        container = self._map__object_key__container[key]
        container.delete(key)

    def _load(self, depot_path):
        if not os.path.isdir(depot_path):
            msg = 'boxen depot directory not found: {0}'.format(depot_path)
            raise IOError(msg)

        depot_config = os.path.join(depot_path, '.boxen')

        if not os.path.isfile(depot_config):
            msg = 'No boxen depot configuration found in path: {0}'.format(depot_path)
            raise IOError(msg)

        depot_data = jlib.loads(depot_config)
        self._container_object_limit = depot_data['container_object_limit']
        self._object_cache_size = depot_data['object_cache_size']

