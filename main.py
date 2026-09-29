from base64 import encode
import csv
from errno import ENOTDIR
import os
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import httpx
import msgspec
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
from cyclopts.core import App

cli = App()


@dataclass
class Entry:
    phonetic: str
    english: str
    script: str
    appears_in: str

    @staticmethod
    def from_list(data: list[str]) -> Entry:
        return Entry(*data)


@dataclass
class FarsiDict:
    entries: list[Entry]


def make_request(url: str) -> str:
    print(f"making request @ {url}")
    return httpx.get(url, follow_redirects=True, timeout=15.0).text


def write_csv(path: str, entries: list[Entry]) -> None:
    fields = [name for name in Entry.__annotations__]
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(fields)
        for e in entries:
            writer.writerow([getattr(e, atr) for atr in fields])


def iterate_html_element(soup: BeautifulSoup) -> Generator[Entry]:
    # for loops nested, call me momma bird
    for table in soup.find_all("table", {"class": "table vocab-list"}):
        lst: list[str] = []
        for tbody in table.find_all("tbody"):
            for tr in tbody.find_all("tr"):
                lst.clear()

                for td in tr.find_all("td"):
                    text = td.get_text().strip("\n")
                    lst.append(text)

                yield Entry.from_list(lst)


def parse_html_page_entries(html_content: str) -> list[Entry]:
    soup = BeautifulSoup(html_content, "html.parser")
    page_entries: list[Entry] = []

    for entry in iterate_html_element(soup):
        if entry:
            page_entries.append(entry)
    return page_entries


def convert_to_unit_and_prefix(size: float) -> str:
    units = ["bytes", "KiB", "MiB"]
    count = 0
    while size > 1024.0:
        size /= 1024.0
        count += 1
    return f"{size:.2f}{units[count]}"


@cli.command
def parse(html_dir: str = "html", output_file: str = "data.json") -> None:

    output_path = Path(output_file).as_posix()

    entry_count = 0

    files = Path(f"{html_dir}/").glob("*.html")
    with open(output_path, "wb+") as output:
        for file in files:
            print(f"parsing file {file}")
            with open(file.absolute().__str__(), "r") as input:
                page_entries = parse_html_page_entries(input.read())
                entry_count += len(page_entries)
                json = msgspec.json.encode(page_entries)
                _ = output.write(json)

    file_size = os.path.getsize(output_path)
    size_str = convert_to_unit_and_prefix(file_size)
    print(f"file: {output_file}, size {size_str} @ {entry_count} dictionary entries, ")


@cli.command
def download(page_count: int, html_path: str = "html") -> None:

    os.makedirs(html_path, exist_ok=True)

    for i in range(page_count):
        content = make_request(
            f"https://www.chaiandconversation.com/persian-dictionary?page={i}#dictionary-results"
        )
        path = f"{html_path}/page_{i}.html"
        with open(path, "w") as f:
            _ = f.write(content)


if __name__ == "__main__":
    cli()
