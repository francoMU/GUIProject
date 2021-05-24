import string
from typing import List, Generator, Iterable


def find_whitespaces(line: str) -> Generator[int, None, None]:
    for index, character in enumerate(line):

        if character in string.whitespace:
            yield index


def get_index(indices: Iterable[int], width):
    ws_list = [item for item in indices if item < width]

    if ws_list:
        return max(ws_list)

    ws_list = [item for item in indices if item >= width]

    if ws_list:
        return min(ws_list)

    return


def split_line(line: str, width: int) -> str:
    # convert line to list in order to make it mutable

    mutable_line = list(line)

    indices = find_whitespaces(line.rstrip())

    print(indices)

    if indices:
        print("is not empty")
        replace_index = get_index(indices, width)

        if replace_index:
            mutable_line[replace_index] = '\n'
    else:
        print("is empty")

    return ''.join(mutable_line)


def splitted_line(text: str, width: int) -> str:
    final_lines = []

    for line in text.splitlines():

        splitted_line = list(line)

        line_length = len(line)

        indices = list(find_whitespaces(line))

        if indices:

            starting_value = width

            ws_list = list(filter(lambda x: x < starting_value, indices))

            if ws_list:
                ws = max(ws_list)
                splitted_line[ws] = '\n'

                starting_value = ws + width + 1

                ws_list = list(filter(lambda x: x < starting_value, indices))

                # while ws_list:

                #    ws = max(ws_list)
                #    splitted_line[ws] = '\n'

                #    starting_value = ws + width + 1

                #    if starting_value > line_length:
                #        break

                #   ws_list = list(
                #       filter(lambda x: x < starting_value, indices))

        final_lines.append(''.join(splitted_line))

    return '\n'.join(final_lines)
