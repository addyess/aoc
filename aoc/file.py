import inspect
import re
from pathlib import Path
from urllib.request import urlopen, Request


def _retrieve_input(f_path: str) -> Path:
    def int_part(word: str) -> int:
        return int(re.sub(r"[^0-9]", "", word))

    path_obj = Path(f_path)
    if not path_obj.exists():
        cookie_txt = Path("cookie").read_text()
        (
            year,
            day,
        ) = map(int_part, (path_obj.parent.stem, path_obj.stem))
        req = Request(
            f"https://adventofcode.com/{year}/day/{day}/input",
            headers=dict(cookie=cookie_txt),
        )
        resp = urlopen(req)
        path_obj.write_bytes(resp.read())
    return path_obj


def puzzle_input():
    """Read the contents of the input file.

    the input file is located at the caller's path
        replacing .py with .txt

    this method will pull the correct input for the puzzle
       based on a session cookie present in the "cookie" file
       if the file doesn't already exist
    """

    f_path = inspect.stack()[1].filename.replace(".py", ".txt")
    path_obj = _retrieve_input(f_path)

    for line in path_obj.read_text().splitlines():
        yield line.strip("\n")


def example(s_content: str):
    """Split a string into formatted lines."""
    for line in s_content.splitlines():
        yield line.strip("\n")
