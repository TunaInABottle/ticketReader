import re
import pandas as pd
import logging
import logging.config
import yaml
from typing import List, Tuple

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("sampleLogger")
debug_log = logging.getLogger("debugLogger")

###########################################



def process_ticket_text(ticket_string: str) -> pd.DataFrame: 

    raw_entries = extract_ticket_entries(ticket_string)

    # Make ticket entries from text
    ticket_entries = []
    for idx, entry_text in enumerate(raw_entries):
        ticket_entries.append(format_ticket_entry(entry_text))

    pd_ticket = pd.DataFrame(ticket_entries)

    # Checking skewness of the numbers, eventually adding a skew entry to the data
    price_skew = price_skewness(pd_ticket)
    if price_skew != 0:
        logger.info("The scanned ticket has an error of %s. an entry will be added to report this", price_skew)
        skew_entry = pd.DataFrame([['PRICE SKEWNESS', price_skew]],
                   columns=['name', 'price'])

        pd_ticket = pd.concat([pd_ticket, skew_entry], ignore_index=True)

    return pd_ticket



def extract_ticket_entries(ticket_string):
    # Assumption: a ticket entry ends with a price written as float
    
    # Identify string at the end of the line that have decimals numbers
    ticket_entry_regex = re.compile(r"[\W\S]?\d+[.,]\d{2}$")

    # Extract only strings that are receipt entries
    text_list = ticket_string.splitlines()
    filtered_text_list = list(filter(ticket_entry_regex.search, text_list))
    return filtered_text_list



def price_skewness(pd_ticket: pd.DataFrame) -> int:
    return round(pd_ticket["price"].sum() - 2 * pd_ticket["price"].max(), 2)


def format_ticket_entry(entry_string: str) -> dict:
    clean_entry = ticket_entry_tidying(entry_string)

    entry_dict = ticket_entry_features(clean_entry)

    # skip entries related to IVA
    if is_IVA_entry(entry_dict["name"]):
        return {"name": None, "price": None}

    return entry_dict

def ticket_entry_tidying(entry_string: str) -> str:
    # remove IVA columns
    iva_regex = re.compile(r"\S?[Vv][Ii]")
    clean_entry = re.sub( iva_regex , '', entry_string)
    return clean_entry

def is_IVA_entry(entry_name: str) -> bool:
    return re.search('cui IVA', entry_name, re.IGNORECASE)



def ticket_entry_features(entry_str: str) -> dict:
    splitted_entry = entry_str.split(' ')

    price = extract_entry_price(splitted_entry)

    product = extract_entry_product(splitted_entry)
    return {"name": product, "price": price}



def extract_entry_product(split_entry: List[str]) -> str:
    # Assumption: product is everything but the last element of an entry
    product = " ".join(split_entry[0:len(split_entry)-1]) 
    product = re.sub(  r"[ ]+$", '', product) #remove trailing space
    return product



def extract_entry_price(split_entry: List[str]) -> str:
    # Assumption: price is always the last element in an entry
    price = split_entry[-1]

    # if first character is not a number, guess it negative
    price = re.sub(  r"^[^0-9]", '-', price)

    # convert price to float
    price = float( price.replace(",", ".") )
    return price


#############################


def extract_ticket_place(ticket_str: str) -> str:
    street_regex = re.compile(r"Via |Piazza ")

    # Look for the entry with the street name
    text_list = ticket_str.splitlines()
    filtered_text_list = list(filter(street_regex.search, text_list))

    if len(filtered_text_list) > 1:
        logger.warning("detected more than one street, only the first entry will be taken. filtered_text_list content: " + ' --- '.join(filtered_text_list))

    # remove 'n' if present
    street = re.sub(  r" n[.,;:]?", '', filtered_text_list[0])

    places_df = pd.read_csv('data/place_list.csv', encoding='utf-8')

    place_id = place_id_from_street(street, places_df)


    return place_id



def place_id_from_street(street: str, places_df: pd.DataFrame) -> str:
    searched_place_id = ""
    try:
        searched_place_id = places_df.loc[places_df["street"] == street, "id"].values[0]
    except:
        logger.info("The place does not exist in the dataset, it will now be created")
        searched_place_id = "pl999"
    return searched_place_id

