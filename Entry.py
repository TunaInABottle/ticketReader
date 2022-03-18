class Entry:
    def __init__(self, entry_text: str):
        self.product = self.extract_product(entry_text)
        self.price = self.extract_price(entry_text)


