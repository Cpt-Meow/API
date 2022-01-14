import pytest


# start python -m pytest -s ex/ex10.py
def test_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f'Эта фраза короче 15 символов'
