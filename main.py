from ticket_img_ocr import img_to_text
from ticket_text_processor import process_ticket_text, extract_ticket_place, new_ticket_id
import pandas as pd




#@TODO iterate in folder path, write output in new folder
#@TODO make some checks on files already processed
#@TODO read JSON, write ticket id, write JSON
#Assumption: Filename has as prefix the date written as YYYYMMDD
def main():
    img_name = "20220118_poli.jpg"
    
    #img_to_text("./processedInput/", img_name)


    with open('./textFromImage/' + img_name  + '.txt', 'r') as file:
        file_content = file.read()
        ticket_expenses = process_ticket_text( file_content )
        ticket_place = extract_ticket_place( file_content )

    ticket_expenses['id'] = new_ticket_id(ticket_expenses) #@TODO
    ticket_expenses['place'] = ticket_place
    ticket_expenses['date'] = pd.to_datetime(img_name.split('_')[0])
    print(ticket_expenses)
    
    
    ticket_expenses.to_csv("data/tickets.csv", index = False)
    #ticket_expenses.to_json("data/tickets.json", orient="records", date_format="iso", indent=2)




if __name__ == "__main__":
    main()
