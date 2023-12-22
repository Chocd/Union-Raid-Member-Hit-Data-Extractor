#### Uses CV2 AND TESSERACT OR EASYOCR TO READ MEMBER DATA WITH OCR AND OUTPUT A CSV FILE

#### EASYOCR IS 10 TIMES BETTER USE THAT

## Usage instructions

1- Get all requirements installed (cv2 and tesseract)  
pip3 install opencv-python   
pip3 install pytesseract   
https://tesseract-ocr.github.io/tessdoc/Installation.html   

2- Put all images into folders seperated by day   
3- run main.py   

Outer folder must be named IMAGES. So an image file for day 2 should be in ..IMAGES/DAY2/imagename.jpg

image files must show 6 members from the top, with previous members completely hidden at the top. example images are added but censored.

last image (so first members to hit for the day) must be named extraN.xxx, where N is the number of members left to get.

#### CURRENTLY ONLY WORKS WITH 1440P SCREENS BECAUSE I WAS TO LAZY TO ADD UPSCALER/DOWNSCALER AND CHECK. CHANGE COORDINATES IN CODE IF YOU WANT TO USE ANOTHER RESOLUTION
