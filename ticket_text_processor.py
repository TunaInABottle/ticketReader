import re


def process_ticket_text(ticket_string: str):
    regex = re.compile(r"\S?\d*[.,]\d{2}$")
    #regex = re.compile(r"-")


    text_vect = ticket_string.splitlines()
    #text_vect = ticket_string

    #print(text_vect)


    #for i in text_vect:
    #    if re.search(regex, i) is not None:
    #        print(i)
    newlist = list(filter(regex.search, text_vect))
    print(newlist)

    for idx, entry_string in enumerate(newlist):
        format_ticket_entry(entry_string)


    
def format_ticket_entry(entry_string: str):
    print(entry_string)
    # if sconto but not negative, put number as negative