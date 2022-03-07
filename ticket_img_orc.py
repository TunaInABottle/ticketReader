from PIL import Image
import pytesseract
import cv2


def img_to_text(folder_path, img_name):

    img_path = folder_path + img_name

    img = Image.open( img_path )

    #pyt_opt = "-c tessedit_char_whitelist= ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz --psm 6"
    pyt_opt = r'--oem 3 --psm 6'

    '''test = pytesseract.image_to_string(img, lang = "ita", config = pyt_opt)


    with open('my_data.txt', 'w') as file:
        df = file.write(test)
    '''


    ######
    image = cv2.imread( img_path )


    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #converting it to binary image by Thresholding
    #this step is require if you have colored image because if you skip this part
    #then tesseract won't able to detect text correctly and this will give incorrect result
    
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    cv2.imwrite('threshold.png',threshold_img)

    tesseract_out = pytesseract.image_to_string( threshold_img, lang = "ita", config = pyt_opt)



    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1] 

    cv2.imwrite('gray.png',out_gray)
    cv2.imwrite('binary.png',out_binary)

    tesseract_out = pytesseract.image_to_string( Image.open( "binary.png" ) , lang = "ita", config = pyt_opt)
    '''

    with open('./textFromImage/' + img_name + '.txt', 'w') as file:
        df = file.write(tesseract_out)

    #cv2.imshow('gray', out_gray)  
    #cv2.imwrite('gray.png',out_gray)


    #cv2.imshow('binary', out_binary)  
    #cv2.imwrite('binary.png',out_binary)