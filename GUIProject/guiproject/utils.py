import string
from collections import deque
from typing import Generator, Iterable


def find_whitespaces(line: str) -> Generator[int, None, None]:
    for index, character in enumerate(line):

        if character in string.whitespace:
            yield index


def get_index(indices: Iterable[int], width):
    min_list = deque(maxlen=1)

    last_item = None

    for item in indices:

        if item < width:
            min_list.append(item)
        else:
            last_item = item
            break

    if min_list:
        return min_list.pop()

    return last_item


def split_line(line: str, width: int) -> str:
    # convert line to list in order to make it mutable

    mutable_line = list(line)

    indices = find_whitespaces(line.rstrip())

    if indices:
        replace_index = get_index(indices, width)

        while replace_index:
            mutable_line[replace_index] = '\n'

            start_index = width + replace_index + 1

            replace_index = get_index(indices, start_index)

    return ''.join(mutable_line)


def splitted_line(text: str, width: int) -> str:
    final_lines = []

    for line in text.splitlines():
        final_lines.append(split_line(line, width))

    return '\n'.join(final_lines)
