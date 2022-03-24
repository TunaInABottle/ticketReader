import re
from typing import List

class Entry:
    __iva_col_regex = re.compile(r"\S?[Vv][Ii]")

    def __init__(self, entry_text: str):
        splitted_entry = entry_text.split(' ')
        self.product = self.extract_product(splitted_entry)
        self.price = self.extract_price(splitted_entry)

    def __str__(self) -> str:
        return(self.product.ljust(25) + str(format(self.price, '.2f')).rjust(5, " "))


    # TODO Make regex search for numbers, extract result, merge if space in between
    def extract_price(self, split_entry: List[str]) -> str:
        # Assumption: price is always the last element in an entry
        price = split_entry[-1]


        # if first character is not a number, guess it negative
        price = re.sub(  r"^[^0-9]", '-', price)
        
        return float( price.replace(",", ".") )


    def extract_product(self, split_entry: List[str]) -> str:
        # Assumption: product is everything but the last element of an entry
        product = " ".join(split_entry[0:len(split_entry)-1]) 
        product = re.sub(  r"[ ]+$", '', product) #remove trailing space
        product = re.sub( self.__iva_col_regex , '', product) #remove column related to IVA
        return product


    def is_relevant(self) -> bool:
        if self.product == "":
            return False
        return not re.search('cui IVA|pagamento contante', self.product, re.IGNORECASE)