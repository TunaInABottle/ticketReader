from ticket_img_orc import img_to_text
from ticket_text_processor import process_ticket_text

img_name = "20220118_poli.jpg"



#@TODO iterate in folder path, write output in new folder
def main():
    #img_to_text("./processedInput/", img_name)

    ##########################
    with open('./textFromImage/20220118_poli.jpg.txt', 'r') as file:
        process_ticket_text( file.read() )


        
if __name__ == "__main__":
    main()
