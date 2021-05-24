import string
from pathlib import Path

import pytest
from guiproject.utils import splitted_line

PATH = Path(__file__).parent


@pytest.fixture
def example_text():
    with open(PATH / "text.txt") as file:
        yield file.read()



def test_splitting_simple_lines():

    text = """toooooooooookjkoooolong jhgj jkjh"""

    formatted_text = splitted_line(text, 14)

    print(formatted_text)



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
