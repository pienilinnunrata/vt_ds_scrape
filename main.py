import logging

from comments import add_comments_number_to_vtubers_list
from names import save_vtubers

logging.basicConfig(level=logging.INFO)

save_vtubers()
