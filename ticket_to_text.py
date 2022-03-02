from PIL import Image
import pytesseract
import cv2


def ticket_to_text(img_path):
    img = Image.open( img_path )

    #pyt_opt = "-c tessedit_char_whitelist= ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz --psm 6"
    pyt_opt = "--psm 6"

    '''test = pytesseract.image_to_string(img, lang = "ita", config = pyt_opt)


    with open('my_data.txt', 'w') as file:
        df = file.write(test)
    '''


    ######


    image = cv2.imread( img_path )
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 

    cv2.imwrite('gray.png',out_gray)

    test = pytesseract.image_to_string( Image.open( "gray.png" ) , lang = "ita", config = pyt_opt)


    with open('my_data_binary.txt', 'w') as file:
        df = file.write(test)

    #cv2.imshow('gray', out_gray)  
    #cv2.imwrite('gray.png',out_gray)


    #cv2.imshow('binary', out_binary)  
    #cv2.imwrite('binary.png',out_binary)