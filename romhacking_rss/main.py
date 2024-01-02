""" Entry point for web app """
from datetime import datetime
import hashlib

from bs4 import BeautifulSoup
from flask import Flask, Response, request
from rfeed import Feed, Guid, Item
import requests

BASE_URL = "https://www.romhacking.net"


app = Flask(__name__)


@app.route("/")
def home():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5412.99 Safari/537.36"
    }
    rh_response = requests.get(BASE_URL, params=request.args, headers=headers)
    if not rh_response.ok:
        raise Exception("Response failed", rh_response.reason)
    return Response(generate_response(rh_response.text), mimetype="application/rss+xml")


def generate_response(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.title:
        feed_title = soup.title.string
    else:
        feed_title = "Romhacking feed"
    description = "Result as of {date}".format(date=datetime.now())
    table_body = soup.find("tbody")
    if not table_body:
        raise Exception("Failed to find items for search criteria")
    items = []
    for row in table_body.find_all("tr"):
        title_soup = row.find(class_="Title")
        title = title_soup.string
        url = BASE_URL + title_soup.a["href"]
        author = row.find(class_="col_2").string
        date_string = row.find(class_="col_9").string
        date = datetime.strptime(date_string, "%d %b %Y")
        items.append(
            Item(
                title=title,
                link=url,
                description="",
                author=author,
                guid=Guid(id_from_romhack(title, date)),
                pubDate=date,
            )
        )
    return Feed(title=feed_title, link="/", items=items, description=description).rss()


def id_from_romhack(title, date):
    # romhacking only stores date to day precision. we need
    # to make up a uniqueness constraint that is consistent
    # across the search query to not flag duplicates as new
    # romhacks are created and others fall in search list.
    # to this end, we make most significant digits the date,
    # and the least significant a chopped hash of the game name.
    title_prefix = int(date.strftime("%Y%m%d"))
    title_sha1 = hashlib.sha1(title.encode("utf-8")).hexdigest()
    title_suffix = int(title_sha1, 16) % (10**8)
    return str(title_prefix) + str(title_suffix)
