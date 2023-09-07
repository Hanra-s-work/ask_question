# tests/test_ask_question.py
import unittest.mock
from ask_question import AskQuestion


def test_is_empty() -> None:
    """ Test if the input string is empty """
    aqi = AskQuestion()
    assert aqi.is_empty("") is True
    assert aqi.is_empty("\t") is False
    assert aqi.is_empty("   ") is False
    assert aqi.is_empty("Hello") is False


def test_is_version() -> None:
    """ Test if the version tester is working """
    aqi = AskQuestion()
    assert aqi.is_version("1.0.0") is True
    assert aqi.is_version("1.a.0") is False


def test_contains_illegal_characters() -> None:
    """ Test if the illegal characters tester is working """
    aqi = AskQuestion()
    illegal_chars = "#@$"
    assert aqi.contains_illegal_characters("Hello", illegal_chars) is False
    assert aqi.contains_illegal_characters("H#llo", illegal_chars) is True


def test_remove_char_overflow() -> None:
    """ Test if the character overflow remover is working """
    aqi = AskQuestion()
    assert aqi.remove_char_overflow("Hello", "l", 1, False) == "Helo"
    assert aqi.remove_char_overflow("Hello", "l", 2, False) == "Hello"


def test_clean_number() -> None:
    """ Test if the number cleaner is working """
    aqi = AskQuestion()
    assert aqi.clean_number("1,000.99") == "1.00099"
    assert aqi.clean_number("1.234.567,89") == "1.23456789"


@unittest.mock.patch('builtins.input', side_effect=["1.23"])
# Simulate user input for "1.23" when asked for a float
def test_ask_question_valid_input() -> None:
    """Test asking question with valid inputs."""
    aqi = AskQuestion()
    assert aqi.ask_question("Enter a float: ", "float") == 1.23


def test_ask_question_invalid_input() -> None:
    """Test asking question with invalid inputs."""
    aqi = AskQuestion()
    assert aqi.test_input("abc ", "int") is False
    assert aqi.usr_answer == ""


@unittest.mock.patch('builtins.input', side_effect=["y"])
# Simulate user input for "y" when asked for a bool
def test_ask_question_bool_input():
    """Test asking boolean questions and answering them correctly."""
    aqi = AskQuestion()
    assert aqi.ask_question("Yes or No? ", "bool") is True


@unittest.mock.patch('builtins.input', side_effect=["1.0.0"])
# Simulate user input for "1.0.0" when asked for a version
def test_ask_question_version_input():
    """Test asking version questions and answering them correctly."""
    aqi = AskQuestion()
    assert aqi.ask_question("Enter a version: ", "version") == "1.0.0"


def test_ask_question_empty_input():
    """Test asking empty string as input to ask_question function."""
    aqi = AskQuestion()
    assert aqi.test_input("", "str") is False
    assert aqi.usr_answer == ""


def test_ask_question_space_input():
    """Test asking empty string as input to ask_question function."""
    aqi = AskQuestion()
    assert aqi.test_input(" ", "str") is False
    assert aqi.usr_answer == ""


def test_ask_question_tab_input():
    """Test asking empty string as input to ask_question function."""
    aqi = AskQuestion()
    assert aqi.test_input("\t", "str") is False
    assert aqi.usr_answer == ""


def test_ask_question_tab_and_space_input():
    """Test asking empty string as input to ask_question function."""
    aqi = AskQuestion()
    assert aqi.test_input("\t ", "str") is False
    assert aqi.usr_answer == ""


def test_ask_question_tab_and_space_mix_input():
    """Test asking empty string as input to ask_question function."""
    aqi = AskQuestion()
    assert aqi.test_input(
        "\t  \t\t\t  \t\t   \t\t  \t\t   \t\t \t\t",
        "str"
    ) is False
    assert aqi.usr_answer == ""


def test_ask_question_whitespace_input():
    """Test asking whitespace as input to ask_question function."""
    aqi = AskQuestion()
    # Simulate user input for whitespace
    assert aqi.test_input("            ", "str") is False
    assert aqi.usr_answer == ""


def test_ask_question_tabs_input():
    """Test asking whitespace as input to ask_question function."""
    aqi = AskQuestion()
    # Simulate user input for tabs
    assert aqi.test_input("\t\t\t\t\t\t\t\t\t\t\t\t", "str") is False
    assert aqi.usr_answer == ""


def test_ask_question_invalid_characters():
    """Test asking invalid characters as input to ask_question function."""
    aqi = AskQuestion()
    # Simulate user input for "!@#" when asked for alphanumeric
    assert aqi.test_input("!@#", "alnum") is False
    assert aqi.usr_answer == ""


@unittest.mock.patch('builtins.input', side_effect=["42"])
# Simulate user input for "42" when asked for a uint
def test_ask_question_valid_uint():
    """ Test asking valid uints (positive integers) in the range [0, 2^32-1]. """
    aqi = AskQuestion()
    assert aqi.ask_question("Enter a uint: ", "uint") == 42


def test_ask_question_invalid_uint():
    """Test asking invalid uints (negative integers) in the range [0, 2^32-1]."""
    aqi = AskQuestion()
    # Simulate user input for "-42" when asked for a uint
    assert aqi.test_input("-42", "uint") is False
    assert aqi.usr_answer == ""


@unittest.mock.patch('builtins.input', side_effect=["3.14"])
# Simulate user input for "3.14" when asked for a ufloat
def test_ask_question_valid_ufloat():
    """Test asking valid ufloats (positive floats) in the range [0, 2^32-1]."""
    aqi = AskQuestion()
    assert aqi.ask_question("Enter a ufloat: ", "ufloat") == 3.14


def test_ask_question_invalid_ufloat():
    """Test asking invalid ufloats (negative floats) in the range [0, 2^32-1]."""
    aqi = AskQuestion()
    # Simulate user input for "-3.14" when asked for a ufloat
    assert aqi.test_input("-3.14", "ufloat") is False
    assert aqi.usr_answer == ""
