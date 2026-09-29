import csv
import os
from collections.abc import Generator
from pathlib import Path
import sys

import httpx
from bs4 import BeautifulSoup

from entry import Entry


def make_request(url: str) -> str:
    print(f"making request @ {url}")
    return httpx.get(url, follow_redirects=True, timeout=15.0).text


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        _ = f.write(content)


def write_csv(path: str, entries: list[Entry]) -> None:
    fields = [name for name in Entry.__annotations__]
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(fields)
        for e in entries:
            writer.writerow([getattr(e, atr) for atr in fields])


def parse(html_content: str) -> Generator[Entry]:
    soup = BeautifulSoup(html_content, "html.parser")

    content: str
    title: str

    for art in soup.find_all("article"):
        for header in art.find_all("header"):
            title = header.a.contents[0]

        for div in art.find_all("div"):
            if div.p:
                content = div.p.contents[0]

        yield Entry(content=content, title=title)


def app() -> None:

    dir_path = "html"
    os.makedirs(dir_path, exist_ok=True)

    for i in range(215):
        content = make_request(f"https://www.chaiandconversation.com/persian-dictionary?page={i}#dictionary-results")
        write_file(f"{dir_path}/page_{i}.txt", content)


    sys.exit(0)

    entries: list[Entry] = []
    for file in Path(r"html/").glob("*.txt"):
        entry = parse(html_content=read_file(file.absolute().__str__()))
        entries.extend(entry)

    for e in entries:
        print(e)

    write_csv("output.csv", entries)


if __name__ == "__main__":
    app()
