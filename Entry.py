import re
from typing import List

class Entry:
    __iva_col_regex = re.compile(r"\S?[Vv][Ii]|\d+[,.]\d{2}%$")
    __price_regex = re.compile(r"[\S]?[0-9]+[, .]?[0-9]+$") #ASSUMPTION an entry ends with the price

    def __init__(self, entry_text: str):
        splitted_entry = entry_text.split(' ')
        self.product = self.extract_product(splitted_entry)
        self.price = self.extract_price(entry_text)

    def __str__(self) -> str:
        return(self.product.ljust(25) + str(format(self.price, '.2f')).rjust(5, " "))


    # TODO Make regex search for numbers, extract result, merge if space in between
    def extract_price(self, entry_text: str) -> str:
        price = self.__price_regex.findall(entry_text)[-1]

        # if first character is not a number, guess it negative
        price = re.sub(  r"^[^0-9]", '-', price)
        
        price = price.replace(" ", ".")
        price = price.replace(",", ".")

        # insert dot if the string has no character in between
        if price[-3] != ".":
            price = price[:-2] + "." + price[-2:]

        return float( price )


    def extract_product(self, split_entry: List[str]) -> str:
        # Assumption: product is everything but the last element of an entry
        product = " ".join(split_entry[0:len(split_entry)-1]) 
        product = re.sub( self.__iva_col_regex , '', product) #remove column related to IVA
        product = re.sub( r"[ ]+$", '', product) #remove trailing space
        return product


    def is_relevant(self) -> bool:
        if self.product == "":
            return False
        return not re.search('cui IVA|pagamento contante|Resto|Documento n| pagato|PARTITA IVA|PART.IVA|Pagamento elet', self.product, re.IGNORECASE)