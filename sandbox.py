from Ticket import Ticket
import re

'''
img_name = "20220118_poli.jpg"

with open('./textFromImage/' + img_name  + '.txt', 'r') as file:
    file_content = file.read()
    ticket = Ticket( file_content )

print(ticket)
'''


#Regex matching
price_regex = re.compile(r"[\S]?[0-9]+[, .]?[0-9]+$")
print( price_regex.findall("""Sconto Articolo -0,24
ACETO B. DI ALCOOL xVI 0,69
YOG.BIANCO MILA xVI 1,15
FILI RISO SUZI WAN xVI 2,79
UVA SULTANINA PRIMIA *VI 0,99
ACETO B. DI ALCOOL *VI 0,69
YOG.BIANCO MILA *VI 1,19
INF .MELA POMPADOUR *VI 2,39
CAROTE VASSOIO *VI 0,99
SENSATIONAL BURGER G *VI 4,99
Scanto % Bollone -2,50
RISO PRIMIA VIALONE *VI 2,59
Sconto Articolo -0,84
CECI V/VERDE BIO xVI 0,99
sconto Articolo -0,24
CECI V/VERDE BIO xVI 099
Sconto Articolo -0 24
CECI V/VERDE BIO «VI 0.99""") )


print("p99"[-3])