import logging
import os
import uuid
from datetime import date


def get_new_vtuber_csv_name(vtuber_name):
    logging.debug("Getting new csv name")
    today = date.today()
    path_to_file = "scrapped_data/vtuber_pages/%s/%s_%d.%d.%d" % (
        vtuber_name, vtuber_name, today.year, today.month, today.day)
    create_directory(path_to_file)

    csv_name = path_to_file + "/{0}_".format(vtuber_name) + str(uuid.uuid1()) + ".csv"
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
