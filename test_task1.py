import pytest
from task1 import get_primes

def test_get_primes_no_primes_below_2():
    assert get_primes(1) == []

def test_get_primes_2_is_prime():
    assert get_primes(2) == [2]

def test_get_primes_up_to_10():
    assert get_primes(10) == [2, 3, 5, 7]

def test_get_primes_up_to_20():
    assert get_primes(20) == [2, 3, 5, 7, 11, 13, 17, 19]

def test_get_primes_up_to_50():
    assert get_primes(50) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def test_get_primes_large_input():
    assert get_primes(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def test_get_primes_up_to_1():
    assert get_primes(0) == []

def test_get_primes_negative_input():
    assert get_primes(-10) == []

def test_get_primes_large_prime():
    assert get_primes(29) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_get_primes_edge_case():
    assert get_primes(3) == [2, 3]
