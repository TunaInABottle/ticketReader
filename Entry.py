import re
from typing import List


class Entry:
    def __init__(self, entry_text: str):
        splitted_entry = entry_text.split(' ')
        self.product = self.extract_product(splitted_entry)
        self.price = self.extract_price(splitted_entry)

    def __str__(self) -> str:
        return(self.product.ljust(25) + str(format(self.price, '.2f')).rjust(5, " "))


    def extract_price(self, split_entry: List[str]) -> str:
        # Assumption: price is always the last element in an entry
        price = split_entry[-1]
        # if first character is not a number, guess it negative
        price = re.sub(  r"^[^0-9]", '-', price)
        
        return float( price.replace(",", ".") )


    def extract_product(self, split_entry: List[str]) -> str:
        iva_col_regex = re.compile(r"\S?[Vv][Ii]")
        # Assumption: product is everything but the last element of an entry
        product = " ".join(split_entry[0:len(split_entry)-1]) 
        product = re.sub(  r"[ ]+$", '', product) #remove trailing space
        product = re.sub( iva_col_regex , '', product) #remove column related to IVA
        return product


    def IVA_entry(self) -> bool:
        return re.search('cui IVA', self.product, re.IGNORECASE)