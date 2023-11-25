import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


directory = 'IMAGES'
dayDict = dict()
playerDict = dict()


for foldername in os.listdir(directory):
    for currimage in os.listdir(directory+'/'+foldername):
        print(foldername)
        image = cv2.imread(directory+'/'+foldername + '/'+currimage, 0)
        thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU )[1]


        if str(currimage).startswith('extra'):

            withoutExt = str(currimage).split('.')
            num = withoutExt[0][withoutExt[0].__len__() - 1]
            for i in range(int(num)):

                x,y,w,h = 1075, 1075-(i*125), 138, 51  
                ROI1 = thresh[y:y+h,x:x+w]
                data = pytesseract.image_to_string(ROI1, lang='eng',config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

                ##############################################
                # DAMAGE NUMBERS
                ##############################################
                
                x,y,w,h = 1370, 1068-(i*125), 153, 61  
                ROI2 = thresh[y:y+h,x:x+w]
                data2 = pytesseract.image_to_string(ROI2, lang='eng',config='--psm 6 -c tessedit_char_whitelist=0123456789,.')

                ##############################################
                # any other info?
                ##############################################

                playerName = str(data).replace("\n","")
                hitAmount = str(data2).replace("\n","")
                hitAmount = str(hitAmount).replace(".","")
                hitAmount = str(hitAmount).replace(",","")

                if playerName in playerDict.keys():
                    playerDict[playerName].append(hitAmount)
                else:
                    playerDict[playerName] = [hitAmount]
        else:
            for i in range(6):
                
                x,y,w,h = 1075, 393+(i*125), 138, 51  
                ROI1 = thresh[y:y+h,x:x+w]
                data = pytesseract.image_to_string(ROI1, lang='eng',config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

                ##############################################
                # DAMAGE NUMBERS
                ##############################################
                
                x,y,w,h = 1370, 383+(i*125), 153, 61  
                ROI2 = thresh[y:y+h,x:x+w]
                data2 = pytesseract.image_to_string(ROI2, lang='eng',config='--psm 6 -c tessedit_char_whitelist=0123456789,.')

                ##############################################
                # any other info?
                ##############################################

                
                playerName = str(data).replace("\n","")
                hitAmount = str(data2).replace("\n","")
                hitAmount = str(hitAmount).replace(".","")
                hitAmount = str(hitAmount).replace(",","")

                if playerName in playerDict.keys():
                    playerDict[playerName].append(hitAmount)
                else:
                    playerDict[playerName] = [hitAmount]
        
    dayDict[foldername] = playerDict
    playerDict = dict()
            
            


playerTotalDamageDict = dict()
for keyofday, day in dayDict.items():
    for key,player in day.items():
        if key in playerTotalDamageDict:
            for damage in player:
                playerTotalDamageDict[key] = playerTotalDamageDict[key] + int(damage)
        else:
            playerTotalDamageDict[key] = 0
            for damage in player:
                playerTotalDamageDict[key] = playerTotalDamageDict[key] + int(damage)


with open('output.csv', 'a') as f:
    for key, value in playerTotalDamageDict.items():
        f.write(str(key)+","+str(value))
        for day, dayval in dayDict.items():
            f.write(","+str(day))
            hitCount = 0
            if key in dayval:
                for damage in dayval[key]:
                    hitCount = hitCount + 1
                    f.write(","+ damage)
            if hitCount < 3:
                for i in range(3-hitCount):
                    f.write(",-")
        
        f.write("\n")
            


