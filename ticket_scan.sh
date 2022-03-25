#!/bin/bash


echo "Executing OCR on" $1
python ticket_img_ocr.py $1

echo "converting text to a data format"
python main.py $1