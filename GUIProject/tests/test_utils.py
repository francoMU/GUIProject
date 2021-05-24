import string
from pathlib import Path

import pytest
from guiproject.utils import splitted_line, get_index, find_whitespaces, \
    split_line

PATH = Path(__file__).parent


@pytest.fixture
def example_text():
    with open(PATH / "text.txt") as file:
        yield file.read()


def test_get_index():
    """Get the index of the first white before width or if there is non the
    next one"""
    indices = get_index([8, 10, 12, 15, 18], 14)

    assert indices == 12

    indices = get_index([8, 10, 12, 15, 18], 7)

    assert indices == 8

    indices = get_index([], 7)

    assert indices is None


def test_get_index_of_generator():
    """Get index of whitespace"""
    indices = get_index(
        (y for y in [8, 10, 12, 15, 18]),
        14)

    assert indices == 12

    indices = get_index(
        (y for y in [8, 10, 12, 15, 18]), 7)

    #assert indices == 8

    indices = get_index([], 7)

    #assert indices is None


def test_no_whitespace():
    """Test if no white space is throws error"""
    line = "A"

    iterable = find_whitespaces(line)

    assert list(iterable) == []

    with pytest.raises(StopIteration):
        next(iterable)


def test_split_line():
    """Test if splitting of lines works"""

    line = "asdfsadfsdf is"

    comparison_line = line.replace(" ", "\n")

    processed_line = split_line(line, 6)

    assert processed_line == comparison_line


@pytest.mark.parametrize("width", [8])
def test_splitting_lines(example_text, width):
    formatted_text = splitted_line(example_text, width)

    print()
    print(formatted_text)

    for line in formatted_text.splitlines():

        if string.whitespace in line:
            pass
        else:
            assert len(line) <= width
