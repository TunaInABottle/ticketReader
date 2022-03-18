from datetime import datetime
import re
from typing import List
import pandas as pd
import logging
import logging.config
from pyparsing import Regex
import yaml
from ticket_text_processor import ticket_entry_tidying, ticket_entry_features
from dateutil import parser
from Entry import Entry

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("sampleLogger")
work_log = logging.getLogger("debugLogger")


##########################################

class Ticket:
    def __init__(self, ticket_text: str):
        self.entries = None
        self.date = None
        #self.debug = None
        self.process_text(ticket_text)



    # MODIFY internal structure
    def process_text(self, text: str) -> List:
        # Assumption: a ticket entry ends with a price written as float
        # Identify string at the end of the line that have decimals numbers
        entry_regex = re.compile(r"[\W\S]?\d+[.,]\d{2}$")
        # Assumption: dates written in YYYY-MM-DD or DD-MM-YYYY format
        date_regex = re.compile(r"\d{2,4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}")

        text_list = text.splitlines()
        entry_list = self.clean_price_entries(entry_regex, text_list)
        date_list = self.clean_date(date_regex, text_list)

        #self.debug = list(map(Entry, entry_list))

        self.entries = entry_list
        self.date = date_list

    

    def clean_date(self, regex: Regex, text_list: List) -> str:
        result = list(filter(regex.search, text_list))

        keep_date_only_regex = re.compile(r".*(?=\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})|(?<=\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}).*")

        # Verify list anomalies
        if len(result) == 0:
            raise ValueError("Unable to detect a date! The ticket may not have it, the ticket might have been misread or the RegEx might be incomplete")
        elif len(result) > 1:
            logger.warning("Two or more entries have been detected to have a valid date format, only the last will be taken")

        raw_date = result[-1]
        date = re.sub( keep_date_only_regex, '', raw_date )

        return parser.parse(date).strftime('%Y-%m-%d')



    def clean_price_entries(self, regex: Regex, text_list: List) -> pd.DataFrame:

        entry_list = list(filter(regex.search, text_list))
        # Make ticket entries from text
        ticket_entries = []
        for idx, entry_text in enumerate(entry_list):
            ticket_entries.append(self.format_ticket_entry(entry_text))

        pd_ticket = pd.DataFrame(ticket_entries)

        # Checking skewness of the numbers, eventually adding a "PRICE SKEWNESS" entry to the data
        pd_ticket = self.append_price_skewness(pd_ticket)

        return pd_ticket.dropna()



    def format_ticket_entry(self, entry_string: str) -> dict:
        clean_entry = ticket_entry_tidying(entry_string)

        entry_dict = ticket_entry_features(clean_entry)

        # skip entries related to IVA
        if self.related_to_IVA(entry_dict["name"]):
            return {"name": None, "price": None}

        return entry_dict


    def append_price_skewness(self, pd_ticket: pd.DataFrame) -> pd.DataFrame:
        price_skew = round(pd_ticket["price"].sum() - 2 * pd_ticket["price"].max(), 2)
        if price_skew != 0:
            logger.info("The scanned ticket has an error of %s. an entry will be added to report this", price_skew)
            skew_entry = pd.DataFrame([['PRICE SKEWNESS', price_skew]],
                    columns=['name', 'price'])

            pd_ticket = pd.concat([pd_ticket, skew_entry], ignore_index=True)
        return pd_ticket




    def related_to_IVA(self, entry_name: str) -> bool:
        return re.search('cui IVA', entry_name, re.IGNORECASE)





    def print(self) -> None:
        print(f"Date: {self.date}\nContent of the ticket:\n{self.entries}")

    def print_debug(self) -> None:
        #print(self.debug1)
        print(self.debug2)
