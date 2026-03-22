import requests
from bs4 import BeautifulSoup

URL = "https://radsport-seite.de/termine-resultate-2026.html"

def fetch_raw_html():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()
    return response.text

def extract_rows(html):
    soup = BeautifulSoup(html, "html.parser")
    pre = soup.find("pre")
    lines = pre.text.split("\n")
    return lines

if __name__ == "__main__":
    html = fetch_raw_html()
    lines = extract_rows(html)
    for l in lines[:20]:
        print(l)
