import pytest

import uuid

from boxen import _container


_TEST_OBJECT = {'id': 0,
                'name': 'TEST_125'}
_TEST_DATA = {'id': str(uuid.uuid4()),
              'object_keys': ['foo_key'],
              'object_data': [_TEST_OBJECT]}


@pytest.fixture(scope='module')
def _container_file(request):
    import os
    import tempfile
    import ujson

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        result = tmp_file.name
        tmp_file.write(ujson.dumps(_TEST_DATA))

    def fin():
        os.remove(result)
    request.addfinalizer(fin)

    return result


def test_get(_container_file):
    container = _container.Container()
    container._read(_container_file)

    response = container.get('foo_key')
    assert response['id'] == _TEST_OBJECT['id']
    assert response['name'] == _TEST_OBJECT['name']


def test_put(_container_file):
    container = _container.Container()
    container._read(_container_file)

    put_data = {'id': 0,
                'name': 'TEST_PUT'}

    key = container.put('foo_key', put_data)
    assert key == 'foo_key'

    response = container.get(key)
    assert response['id'] == put_data['id']
    assert response['name'] == put_data['name']


def test_post(_container_file):
    container = _container.Container()
    container._read(_container_file)

    post_data = {'id': 1,
                 'name': 'TEST_POST'}
    key = container.post(post_data)

    response = container.get(key)
    assert response['id'] == post_data['id']
    assert response['name'] == post_data['name']


def test_delete(_container_file):
    container = _container.Container()
    container._read(_container_file)

    container.delete('foo_key')

    response = container.get('foo_key')
    assert response is None