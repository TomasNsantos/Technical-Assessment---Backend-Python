import pytest
from app.utils.validators import is_valid_cpf

@pytest.mark.parametrize(
    "cpf",
    [
        "52998224725",
        "16899535009",
        "98765432100",
    ],
)

def test_validar_cpf(cpf):
    assert is_valid_cpf(cpf) is True

@pytest.mark.parametrize(
    "cpf",
    [
        "12345678900",
        "11111111111",
        "22222222222",
        "abc",
        "",
    ]
)
def test_invalidar_cpf(cpf):
    assert is_valid_cpf(cpf) is False