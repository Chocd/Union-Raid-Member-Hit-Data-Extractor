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

        thresh1 = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU )[1]
        thresh2 =  cv2.blur(thresh1,(3,3))

        
        blur = cv2.GaussianBlur(thresh1, (3, 3), 0)
        thresh = 255 - cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU )[1]
        thresh = 255 - cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU )[1]



        if str(currimage).startswith('extra'):

            withoutExt = str(currimage).split('.')
            num = withoutExt[0][withoutExt[0].__len__() - 1]
            for i in range(int(num)):

                ##############################################
                # MEMBER NAMES
                ##############################################

                x,y,w,h = 1075, 1075-(i*125), 138, 51  
                ROI1 = thresh[y:y+h,x:x+w]
                data = pytesseract.image_to_string(ROI1, lang='eng',config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')

                ##############################################
                # DAMAGE NUMBERS
                ##############################################
                
                x,y,w,h = 1370, 1068-(i*125), 153, 61  
                ROI2 = thresh2[y:y+h,x:x+w]
                data2 = pytesseract.image_to_string(ROI2, lang='eng',config='--psm 6 -c tessedit_char_whitelist=0123456789,.')
                


                ##############################################
                # BOSS NAMES
                ##############################################

                x,y,w,h = 1102, 1119-(i*125), 155, 50  
                ROI3 = thresh[y:y+h,x:x+w]
                data3 = pytesseract.image_to_string(ROI3, lang='eng',config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')

                ##############################################

                playerName = str(data).replace("\n","")
                hitAmount = str(data2).replace("\n","")
                bossName = str(data3).replace("\n","")
                hitAmount = str(hitAmount).replace(".","")
                hitAmount = str(hitAmount).replace(",","")

                if playerName in playerDict.keys():
                    playerDict[playerName].append(bossName)
                    playerDict[playerName].append(hitAmount)
                else:
                    playerDict[playerName] = [bossName]
                    playerDict[playerName].append(hitAmount)
        else:
            for i in range(6):

                ##############################################
                # MEMBER NAMES
                ##############################################
                
                x,y,w,h = 1075, 393+(i*125), 138, 51  
                ROI1 = thresh[y:y+h,x:x+w]
                data = pytesseract.image_to_string(ROI1, lang='eng',config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')

                ##############################################
                # DAMAGE NUMBERS
                ##############################################
                
                x,y,w,h = 1380, 397+(i*125), 140, 44  
                ROI2 = thresh2[y:y+h,x:x+w]
                data2 = pytesseract.image_to_string(ROI2, lang='eng',config='--psm 7 -c tessedit_char_whitelist=0123456789,.')
                

                ##############################################
                # BOSS NAMES
                ##############################################

                x,y,w,h = 1102, 438+(i*125), 152, 50  
                ROI3 = thresh[y:y+h,x:x+w]
                data3 = pytesseract.image_to_string(ROI3, lang='eng',config='--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789')


                ##############################################

                
                playerName = str(data).replace("\n","")
                hitAmount = str(data2).replace("\n","")
                bossName = str(data3).replace("\n","")
                hitAmount = str(hitAmount).replace(".","")
                hitAmount = str(hitAmount).replace(",","")

                if playerName in playerDict.keys():
                    playerDict[playerName].append(bossName)
                    playerDict[playerName].append(hitAmount)
                else:
                    playerDict[playerName] = [bossName]
                    playerDict[playerName].append(hitAmount)
        
    dayDict[foldername] = playerDict
    playerDict = dict()
            
            


playerTotalDamageDict = dict()
for keyofday, day in dayDict.items():
    for key,player in day.items():
        if key in playerTotalDamageDict:
            for damage in player:
                if str(damage).isdigit():
                    playerTotalDamageDict[key] = playerTotalDamageDict[key] + int(damage)
        else:
            playerTotalDamageDict[key] = 0
            for damage in player:
                if str(damage).isdigit():
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
            if hitCount < 6:
                for i in range(6-hitCount):
                    f.write(",-")
        
        f.write("\n")
            


