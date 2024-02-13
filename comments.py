import pandas as pd


def add_comments_number_to_vtubers_list(path):
    df = pd.read_csv(path)

    pd.option_context('display.max_rows', None, 'display.max_columns', None)
