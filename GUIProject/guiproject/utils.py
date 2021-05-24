import string
from typing import Iterable


def find_whitespaces(line: str) -> Iterable[int]:
    for index, character in enumerate(line):

        if character in string.whitespace:
            yield index


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

                while ws_list:

                    ws = max(ws_list)
                    splitted_line[ws] = '\n'

                    starting_value = ws + width + 1

                    if starting_value > line_length:
                        break

                    ws_list = list(
                        filter(lambda x: x < starting_value, indices))

        final_lines.append(''.join(splitted_line))

    return '\n'.join(final_lines)
