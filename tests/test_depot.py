import pytest

from boxen import _depot


@pytest.fixture(scope='module')
def _depot_directory(request):
    import os
    import tempfile
    import ujson

    depot_directory = tempfile.mkdtemp()

    def fin():
        import shutil
        shutil.rmtree(depot_directory)
    request.addfinalizer(fin)

    return depot_directory


def test_get(_depot_directory):
    depot = _depot.Depot()
    depot._location = _depot_directory

    response = depot.get('foo')
