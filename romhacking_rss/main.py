""" Entry point for web app """
from datetime import datetime
import hashlib

from bs4 import BeautifulSoup
from flask import Flask, request
from werkzeug.contrib.atom import AtomFeed
import requests

BASE_URL = "https://www.romhacking.net"


app = Flask(__name__)


@app.route("/")
def home():
    response = requests.get(BASE_URL, params=request.args)
    return generate_response(response.text)


def generate_response(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string
    subtitle = "Result as of {date}".format(date=datetime.now())
    feed = AtomFeed(title, feed_url="/", url="/", subtitle=subtitle)
    for row in soup.find("tbody").find_all("tr"):
        title_soup = row.find(class_="Title")
        title = title_soup.string
        url = BASE_URL + title_soup.a["href"]
        author = row.find(class_="col_2").string
        date_string = row.find(class_="col_9").string
        date = datetime.strptime(date_string, "%d %b %Y")
        feed.add(
            title,
            "",
            content_type="html",
            author=author,
            url=url,
            id=id_from_romhack(title, date),
            published=date,
            updated=date,
        )
    return feed.get_response()


def id_from_romhack(title, date):
    # romhacking only stores date to day precision. we need
    # to make up a uniqueness constraint that is consistent
    # across the search query to not flag duplicates as new
    # romhacks are created and others fall in search list.
    # to this end, we make most significant digits the date,
    # and the least significant a chopped hash of the game name.
    title_prefix = int(date.strftime("%Y%m%d"))
    title_sha1 = hashlib.sha1(title.encode("utf-8")).hexdigest()
    title_suffix = int(title_sha1, 16) % (10 ** 8)
    return str(title_prefix) + str(title_suffix)
