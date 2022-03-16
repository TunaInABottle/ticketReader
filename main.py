from ticket_img_orc import img_to_text
from ticket_text_processor import process_ticket_text, extract_ticket_place
import pandas as pd




#@TODO iterate in folder path, write output in new folder
def main():
    img_name = "20220118_poli.jpg"
    
    #img_to_text("./processedInput/", img_name)

    ##########################
    ticket_expenses = []
    with open('./textFromImage/' + img_name  + '.txt', 'r') as file:
        file_content = file.read()
        ticket_expenses = process_ticket_text( file_content )
        ticket_place = extract_ticket_place( file_content )

    ticket_expenses['place'] = ticket_place
    ticket_expenses['date'] = pd.to_datetime(img_name.split('_')[0])
    print(ticket_expenses)
        




if __name__ == "__main__":
    main()
