"""Tests for utility methods"""

from pathlib import Path

import pytest
from guiproject.utils import splitted_line, get_index, find_whitespaces, \
    split_line

PATH = Path(__file__).parent


@pytest.fixture
def example_text():
    """Fixture for sample text file"""
    with open(PATH / "text.txt") as file:
        yield file.read()


def test_no_whitespace():
    """Test if no white space is throws error"""
    line = "A"

    iterable = find_whitespaces(line)

    assert list(iterable) == []

    with pytest.raises(StopIteration):
        next(iterable)


@pytest.mark.parametrize("sequence,width,result",
                         [
                             ([8, 10, 12, 15, 18], 14, 12),
                             ([8, 10, 12, 15, 18], 7, 8),
                             ([], 14, None),
                             ([8, 10, 12], 18, 12),
                             ([8], 6, 8),
                             ([8], 9, 8)
                         ])
def test_get_index(sequence, width, result):
    """Get the index of the first white before width or if there is non the
    next one"""
    indices = get_index(sequence, width)

    assert indices == result

    indices = get_index(
        (y for y in sequence), width)

    assert indices == result

    indices = get_index(
        iter(sequence), width)

    assert indices == result


@pytest.mark.parametrize("line, comparison_line",
                         [
                             ("abcdefg is", "abcdefg\nis"),
                         ])
def test_split_line(line, comparison_line):
    """Test if splitting of lines works"""

    processed_line = split_line(line, 6)

    assert processed_line == comparison_line


@pytest.mark.parametrize("width", [60, 80, 120])
def test_splitting_lines(example_text, width):
    """Test if line are really split"""
    formatted_text = splitted_line(example_text, width)

    for text in formatted_text.splitlines():
        assert len(text) < width
