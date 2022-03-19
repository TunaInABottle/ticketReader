from Ticket import Ticket

img_name = "20220118_poli.jpg"

with open('./textFromImage/' + img_name  + '.txt', 'r') as file:
    file_content = file.read()
    ticket = Ticket( file_content )

print(ticket)