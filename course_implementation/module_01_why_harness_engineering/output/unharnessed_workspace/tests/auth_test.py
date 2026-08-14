from auth import validate

def test_validate():
    assert validate('token') == {'ok': True}
