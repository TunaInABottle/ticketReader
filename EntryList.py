
from typing import List 
import Entry

#############

import logging, logging.config, yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("sampleLogger")
work_log = logging.getLogger("debugLogger")

#############

class EntryList:
    def __init__(self, entries_list=None):
        self.entries_list = []

        if entries_list is not None:
            for el in entries_list:
                self.__add_entry(el)    

        self.max = max([item.price for item in self.entries_list])

        self.__add_skewness()

    def __add_entry(self, entry_string: str) -> None:
        entry = Entry.Entry(entry_string)
        if entry.is_relevant():
            self.entries_list.append( entry )

    def get_entries_dict(self) -> dict:
        return {
            "name": [item.product for item in self.entries_list],
            "price": [item.price for item in self.entries_list]
            }

    def __add_skewness(self) -> None:
        # As the content of the ticket comes from OCR, there might be some errors
        # in the reading, this function puts this error into data
        skewness = sum([item.price for item in self.entries_list]) - 2 * self.max
        if not skewness == 0:
            logger.info("the following ticket has some problems with the read numbers, adding skewness entry")
            self.entries_list.append( Entry.Entry(f"PRICE SKEWNESS {round(skewness, 2)}") )


    def __str__(self) -> str:
        whole = "Entry list:\n"
        for el in self.entries_list:
            whole += str(el) + "\n"
        return whole