from ticket_img_ocr import img_to_text
import pandas as pd
from Ticket import Ticket
import sys
import getopt

#############

import logging, logging.config, yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger_ticket = logging.getLogger("ticketLogger")
logger = logging.getLogger("debugLogger")

#############

tickets_data_path = "data/tickets.csv"
#img_name = "20220118_poli.jpg"

#######################

#@TODO problem of inialization when folders/files are empty (especially data)


def main():
    img_name = sys.argv[1]
    
    # Make OCR on the shopping ticket
    #img_to_text("./processedInput/", img_name)

    with open('./ticketTexts/' + img_name  + '.txt', 'r') as file:
        new_ticket = Ticket( file.read() )

    tickets_data = pd.read_csv(tickets_data_path)

    if not new_ticket.is_in(tickets_data):
        new_tickets_data = pd.concat([tickets_data, new_ticket.dataframe()])    
        new_tickets_data.to_csv(tickets_data_path, index = False)
        logger_ticket.info(f"the ticket with name \"{img_name}\" has been appended to the dataset")
    else:
        logger_ticket.info(f"the ticket with name \"{img_name}\" has already been scanned in the past")


if __name__ == "__main__":
    main()
