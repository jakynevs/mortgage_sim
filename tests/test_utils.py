import pytest
from app import valid_dni, valid_name, valid_email, valid_requested_capital

def test_valid_dni():
    # Test valid DNI
    assert valid_dni("12244896H") == True  
    # Test valid forigners DNI
    assert valid_dni("X2244896G") == True  

    # Test invalid DNI (wrong length, wrong format, etc.)
    assert valid_dni("1234") == False
    assert valid_dni("12345678") == False
    assert valid_dni("ABCDEFGHI") == False
    assert valid_dni(234526791) == False

def test_valid_name():
    # Test valid name
    assert valid_name("Jack") == True

    # Test invalid name 
    assert valid_name(1224) == False
    assert valid_name("asdfgklzxcvbnm1234567890asdfghjkl;xcvbn1224qwertyuiopasdfghjklzxcvbnm;lkjhgfdqwertyuiopasdfghjkl,mnbvcxz") == False

def test_valid_email():
    # Test valid email
    assert valid_email("jack@roams.es") == True

    # Test invalid email
    assert valid_email(1224) == False
    assert valid_email("jackroams.es") == False

def test_valid_requested_capital():
    # Test valid requested_capital
    assert valid_requested_capital(1000000) == True

    # Test invalid requested_capital (wrong format, length)
    assert valid_requested_capital(0000) == False
    assert valid_requested_capital("jack@roams.es") == False
