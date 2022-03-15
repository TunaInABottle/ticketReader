import re
import pandas as pd
import logging


def process_ticket_text(ticket_string: str) -> pd.DataFrame: 

    # Identify string at the end of the line that have decimals numbers
    ticket_entry_regex = re.compile(r"[\W\S]?\d+[.,]\d{2}$")

    # Extract only strings that are receipt entries
    text_vect = ticket_string.splitlines()
    newlist = list(filter(ticket_entry_regex.search, text_vect))

    #Make new ticket entries
    ticket_entries = []
    for idx, entry_string in enumerate(newlist):
        ticket_entries.append(format_ticket_entry(entry_string))


    pd_ticket = pd.DataFrame(ticket_entries)

    print(pd_ticket["price"].sum() - 2 * pd_ticket["price"].max() ) #@TODO throw warning if this is not 0

    print(pd_ticket)

    return pd_ticket


def format_ticket_entry(entry_string: str) -> dict:
    iva_regex = re.compile(r"\S?[Vv][Ii]")
    clean_entry = re.sub( iva_regex , '', entry_string)

    split_entry = clean_entry.split(' ')

    price = split_entry[-1]

    # if first character is not a number, guess it negative
    price = re.sub(  r"^[^0-9]", '-', price)
    # convert price to float
    price = float( price.replace(",", ".") )


    product = " ".join(split_entry[0:len(split_entry)-1])


    entry_dict = {"name": product, "price": price}

    return entry_dict
    # if sconto but not negative, put number as negative