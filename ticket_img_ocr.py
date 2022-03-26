import sys
from PIL import Image
import pytesseract
import cv2

textPath = './ticketTexts/'


# TODO get from command line the image name
def main():
    img_to_text("./processedInput/", sys.argv[1])


def img_to_text(folder_path, img_name):

    img_path = folder_path + img_name

    #img = Image.open( img_path )

    pyt_opt = r'--oem 3 --psm 6'


    ######
    image = cv2.imread( img_path )


    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #converting it to binary image by Thresholding
    #this step is require if you have colored image because if you skip this part
    #then tesseract won't able to detect text correctly and this will give incorrect result
    
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    cv2.imwrite('tmp/threshold.png',threshold_img)

    tesseract_out = pytesseract.image_to_string( threshold_img, lang = "ita", config = pyt_opt)



    with open(textPath + img_name + '.txt', 'w') as file:
        df = file.write(tesseract_out)
        print(f"ticket text written in {textPath}{img_name}.txt")







if __name__ == "__main__":
    main()