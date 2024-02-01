import pytest
from app import valid_dni 

def test_valid_dni():
    # Test valid DNI
    assert valid_dni("12244896H") == True  
    # Test valid forigners DNI
    assert valid_dni("X2244896H") == True  

    # Test invalid DNI (wrong length, wrong format, etc.)
    assert valid_dni("1234") == False
    assert valid_dni("12345678") == False
    assert valid_dni("ABCDEFGHI") == False
    assert valid_dni(234526791) == False
