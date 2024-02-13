import errno
import logging

import requests
import csv
import os.path
import uuid
from googletrans import Translator
from datetime import date
from bs4 import BeautifulSoup

URL = "REDACTED"


# 1. get page number
# 2. get names and links from all pages
# 3. save names and links to txt/csv
#    page_name_jp | page_name_en | link

def save_vtubers():
    file_name = get_new_vtubers_csv_name()
    file = open(file_name, 'w', encoding='utf-8')
    logging.debug("Created file: {0}".format(file_name))
    for page_number in range(1, get_page_number()):
        logging.info("Getting vtubers from page #{0}".format(page_number))
        get_vtubers_from_page(page_number, file)


def get_vtubers_from_page(page_number, file):
    translator = Translator()
    writer = csv.writer(file)

    logging.debug("Getting page from URL: {0}".format(URL.format(page_number)))
    page = requests.get(URL.format(page_number))
    # logging.debug("body: {0}".format(page.json()))
    soup = BeautifulSoup(page.content, "html.parser")
    # with open("test_pages/test_vtubers_page.html", encoding='utf-8') as fp:
    #     soup = BeautifulSoup(fp, 'html.parser')

    vtubers_list = soup.findAll("ul", class_="p-postList -type-list")[0]
    vtuber_cards = vtubers_list.find_all("li", class_="p-postList__item")
    logging.debug("Saving vtuber information")
    for card_item in vtuber_cards:
        page_name_jp = card_item.find(class_="p-postList__title").text
        page_name_en = translator.translate(page_name_jp).text
        link = card_item.a["href"]
        comments_number = get_comments_number(link)

        data = [page_name_jp, page_name_en, link, comments_number]
        logging.info("Writing vtuber information: {0}".format(data))
        writer.writerow(data)


def get_comments_number(url) -> int:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    cc = soup.find("span", class_="wpdtc")
    return int(cc["title"])


def get_page_number() -> int:
    logging.debug("Getting number of pages with URL: {0}".format(URL.format("1")))
    page = requests.get(URL.format("1"))
    soup = BeautifulSoup(page.content, "html.parser")
    page_number = soup.find("a", class_="-to-last").text
    return int(page_number)


def get_new_vtubers_csv_name():
    logging.debug("Getting new csv name")
    today = date.today()
    path_to_file = "scrapped_data/vtubers_list/vtubers_%d.%d.%d" % (today.year, today.month, today.day)
    create_directory(path_to_file)

    csv_name = path_to_file + "/vtubers_list_" + str(uuid.uuid1()) + ".csv"
    logging.info("New csv file name: {0}", csv_name)
    return csv_name


def create_directory(path):
    logging.debug("Creating directory")
    try:
        os.makedirs(path)
    except OSError as e:
        logging.error(str(e))
        return
    logging.debug("New directory created")

# with open('test.txt', 'w') as f:
#     f.write('lol\n')
#     f.write('lol')
#
# names = []
#
# with open('test.txt', 'r') as f:
#     names.append(f.readline())
#     names.append(f.readline())
#
# print(names)
