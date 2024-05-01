from urllib.parse import unquote
from os import path, makedirs, cpu_count
import time
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from typing import Tuple
import sys


CPU_COUNT = cpu_count()
NUMBER_OF_WORKERS = CPU_COUNT if CPU_COUNT <= 2 else CPU_COUNT // 2


if sys.version_info[0:2] != (3, 12):
    print("It is preffered to run this script on Python 3.12")

"""
The url with cat images/videos looks like this:
url = 'https://joyreactor.cc/tag/котэ/7491'


That is how I parse image/video posts:

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
posts = soup.findAll('a', class_='prettyPhotoLink') for older posts class_='image'
videos = soup.findAll('video')


print(posts[0].find("img").get("src"))
-> https://img2.joyreactor.cc/pics/post/котэ-999.jpeg

print(videos[0].find("source").get("src"))
-> https://img2.joyreactor.cc/pics/post/webm/гифки-живность-котэ-gif-8417001.webm


Now let's create :

vid_links = [tag.find("source").get("src") for tag in videos]
img_links = [tag.find("img").get("src") for tag in posts]
"""


class BaseScraper:
    """
    Base scraper class
    """

    # receives tagged url and pagination range in form of start and end variables
    def __init__(self, base_url: str, start: int, end: int):
        self.base_url = base_url
        self.tag = unquote(self.base_url).split("/")[-1]
        self.page_range = range(start, end)
        self.session = requests.session()
        if not path.exists(f"images"):  # creates dir to store subdirectory
            makedirs(f"images")
        if (  # creates subdirectory by the name of ThreadScrape to store images
            not type(self) is BaseScraper and
            not path.exists(f"images/{self}")
        ):
            makedirs(f"images/{self}")

    def extract_img_urls(self, page: int):
        with self.session.get(self.base_url + "/" + f"{page}", timeout=8) as req:
            if req.status_code == 200:
                soup_obj = BeautifulSoup(req.text, 'html.parser')
                # old posts store images in the 'image' class, not the 'prettyPhotoLink'
                if not (posts := soup_obj.findAll("a", class_="prettyPhotoLink")):
                    posts = soup_obj.findAll("div", class_="image")
                img_links = [post.find("img").get("src") for post in posts]
                if img_links:
                    print("Images extracted")
                    return img_links
                else:
                    print("Did not find anything")
                    return []
            else:
                print(f"Strangely, page {page} was not available, perhaps you got banned")
                return []

    def save_img(self, img: bytes):
        i = 0
        while path.exists(f"images/{self}/scraped_{self.tag}_{i}.jpeg"):
            i += 1
        try:
            with open(f"images/{self}/scraped_{self.tag}_{i}.jpeg", "wb") as f:
                # all of the pictures are jpegs, so they are saved accordingly
                f.write(img)
                print(f"Image saved as images/{self}/scraped_{self.tag}_{i}.jpeg")
        except IOError as e:
            print(f"An error occurred: {e}")

    def run(self):  # starts scraping, provides runtime
        start = time.time()
        self._calculate()
        end = time.time()
        print(f"Executed {self}, took {end - start} seconds")

    def fetch(self, link):
        print(f"Fetching {link}...")

    def parse(self, num):
        print(f"Parsing {num}...")


class ThreadScrape(BaseScraper):
    def __str__(self):
        return "ThreadScrape"

    def _thread_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            super().fetch(link)
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    def _thread_parse(self, num):
        img_links = self.extract_img_urls(num)
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
            for link in img_links:
                super().parse(num)
                executor.submit(self._thread_save, link)
                time.sleep(1.5)  # slows work, stay humble, do not commit DDoS

    def _calculate(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
            for i in self.page_range:
                executor.submit(self._thread_parse, i)
                time.sleep(5)  # slows work, stay humble, do not commit DDoS


def validate_input(cmd, url: str, start: str, end: str):
    if start.isdigit() and end.isdigit():
        start = int(start)
        end = int(end)
    else:
        raise TypeError("Can not convert str to int")
    if start > end and (start < 0 or end < 0):
        raise ValueError("Invalid page range")
    if url[-1] == "/":
        url = url[:-2]
        print("Trimmed the trailing '/' in the url")
    return url, start, end

import os
if __name__ == "__main__":
    if len(sys.argv) == 4 and (refined_args := validate_input(*sys.argv)):
        # refined_args = ("https://joyreactor.cc/tag/%D0%BA%D0%BE%D1%82%D1%8D", 298, 300)
        print(f"Base url is {refined_args[0]}, be aware that '%' symbol could be ignored by cmd")
        c = ThreadScrape(*refined_args)
        c.run()
    else:
        print("Not enough parameters")
