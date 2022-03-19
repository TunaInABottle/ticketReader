import re
from typing import List, Pattern
import pandas as pd
from EntryList import EntryList
from Street import Street
from dateutil import parser
import id_generator

#############

import logging, logging.config, yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("sampleLogger")
work_log = logging.getLogger("debugLogger")

#############

class Ticket:
    def __init__(self, ticket_text: str):
        self.data_path = "data/tickets.csv"
        self.id = self.__calc_id()
        self.entry_list = None
        self.date = None
        self.street = None
        self.process_text(ticket_text)

    def process_text(self, text: str) -> List:
        text_list = text.splitlines()

        # Assumption: a ticket entry ends with a price written as float
        entry_regex = re.compile(r"[\W\S]?\d+[.,]\d{2}$")
        # Assumption: dates written in YYYY-MM-DD or DD-MM-YYYY format
        date_regex = re.compile(r"\d{2,4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}")
        street_regex = re.compile(r"Via |Piazza ")

        text_list = text.splitlines()

        self.date = self.extract_date(date_regex, text_list)
        self.street = Street(list(filter(street_regex.search, text_list)))
        self.entry_list = EntryList(list(filter(entry_regex.search, text_list)))

    def extract_date(self, regex: Pattern[str], text_list: List) -> str:
        result = list(filter(regex.search, text_list))

        keep_date_only_regex = re.compile(r".*(?=\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})|(?<=\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}).*")

        # Verify list anomalies
        if len(result) == 0:
            raise ValueError("Unable to detect a date! The ticket may not have it, it might have been misread or the RegEx might be incomplete")
        elif len(result) > 1:
            logger.warning("Two or more entries have been detected to have a valid date format, only the last will be taken")

        raw_date = result[-1]
        date = re.sub( keep_date_only_regex, '', raw_date )
        return parser.parse(date).strftime('%Y-%m-%d')

    def __calc_id(self) -> str:
        with open(self.data_path, 'r') as f:
            data = pd.read_csv(f, delimiter=',')
            return id_generator.next_id(data["id"].max())

    def dataframe(self) -> pd.DataFrame:
        entries_dict = self.entry_list.get_entries_dict()
        return pd.DataFrame({
            "id": self.id,
            "name": entries_dict["name"],
            "price": entries_dict["price"],
            "place": self.street.id,
            "date": self.date
            })

    # ASSUMPTION: The tickets are unique based on place, date and maximum price
    def is_in(self, df: pd.DataFrame) -> bool:
        return not df[(df["place"] == self.street.id) & (df["price"] == self.entry_list.max) & (df["date"] == self.date)].empty

    def __str__(self) -> str:
        return f"id: {self.id}\nDate: {self.date}\nStreet: {self.street}\n{self.entry_list}"