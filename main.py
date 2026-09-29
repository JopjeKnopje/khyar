import csv
import os
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from bs4.dammit import EntitySubstitution
import httpx
from bs4 import BeautifulSoup
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
                    text = td.get_text().strip('\n')
                    lst.append(text)

                yield Entry.from_list(lst)

def parse_html(html_content: str) -> list[Entry]:
    soup = BeautifulSoup(html_content, "html.parser")

    entries: list[Entry] = []

    for entry in iterate_html_element(soup):
        if entry:
            entries.append(entry)

    return entries


@cli.command
def parse() -> None:

    entries: list[Entry] = []
    for i, file in enumerate(Path(r"html/").glob("*.html")):
        print(file)
        with open(file.absolute().__str__(), "r") as f:
            entry = parse_html(f.read())
            entries.extend(entry)
            break

    for e in entries:
        print(e)

    write_csv("output.csv", entries)


@cli.command
def download(
    page_count: int,
    html_path: str = "html"
    ) -> None:

    os.makedirs(html_path, exist_ok=True)

    for i in range(page_count):
        content = make_request(f"https://www.chaiandconversation.com/persian-dictionary?page={i}#dictionary-results")
        path = f"{html_path}/page_{i}.html"
        with open(path, "w") as f:
            _ = f.write(content)





if __name__ == "__main__":
    cli()
