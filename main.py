from email.utils import parsedate_to_datetime
from numpy import datetime64
from ticket_img_ocr import img_to_text
from ticket_text_processor import process_ticket_text, extract_ticket_place, new_ticket_id
import pandas as pd

tickets_data_path = "data/tickets.csv"

img_name = "20220118_poli.jpg"


#@TODO iterate in folder path, write output in new folder
#@TODO make some checks on files already processed
#Assumption: Filename has as prefix the date written as YYYYMMDD
def main():
    
    #img_to_text("./processedInput/", img_name)


    with open('./textFromImage/' + img_name  + '.txt', 'r') as file:
        file_content = file.read()
        new_ticket = process_ticket_text( file_content )
        ticket_place = extract_ticket_place( file_content )

    tickets_data = pd.read_csv(tickets_data_path)


    tickets_data["date"] = pd.to_datetime(tickets_data["date"], format='%Y-%m-%d')

    next_id = new_ticket_id(tickets_data)

    new_ticket['id'] = next_id
    new_ticket['place'] = ticket_place
    new_ticket['date'] = pd.to_datetime(img_name.split('_')[0])

    new_tickets_data = pd.concat([tickets_data, new_ticket])    
    
    new_tickets_data.to_csv(tickets_data_path, index = False)




if __name__ == "__main__":
    main()
