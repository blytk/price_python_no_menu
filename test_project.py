import project
import pytest

# I use monkeypatch in order to simulate user input, as none of the functions accept any argument
def test_get_user_token(monkeypatch):
    user_input = "bitcoin"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert project.get_user_token() == "bitcoin"
    user_input = "ethereum"
    assert project.get_user_token() == "ethereum"


def test_get_user_date(monkeypatch):
    user_input = "01-01-2020"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert project.get_user_date() == "01-01-2020"
    user_input = "12-12-2019"
    assert project.get_user_date() == "12-12-2019"


def test_print_menu():
    assert project.print_menu() == 0
