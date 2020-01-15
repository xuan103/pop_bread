#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import easygui
from yoloOpencv import opencvYOLO
import cv2
import imutils
import time
from libPOS import desktop
#import RPi.GPIO as GPIO 
#GPIO.setmode(GPIO.BCM)

#------------------------------------------------------------------------
labels_tw = { "b01":["單片土司", 8], "b02":["雙片土司", 16], \
           "b03":["牛角麵包", 30], "b04":["奶油牛奶條", 55], "b05":["紅豆麵包", 35], \
           "b06":["炸甜甜圈", 30], "b07":["牛肉漢堡", 85], "b08":["瑞士捲", 35]}

labels_en = { "b01":["Toast", 0.4], "b02":["Toasts", 0.8], \
           "b03":["Croissant", 2.6], "b04":["Baguette", 1.8], "b05":["Red-bean bun", 0.6], \
           "b06":["Donut", 2.2],"b07":["Hamburger", 5.2],"b08":["Swiss Roll", 1.8] }

idle_checkout = (8, 10)
video_out = "output.avi"
dt = desktop("images/bg.jpg", "images/bgClick.jpg")
flipFrame = (True,True) #(H, V)
lang = "EN"  #TW, EN
#-------------------------------------------------------------------------
f = open("detection_type.txt", "r")
detection = f.readline()
f.close()

if(detection == "USD"):   #BREAD or USD
    yolo = opencvYOLO(modeltype="yolov3-tiny", \
        objnames="cfg.usd_dollars_square.tiny/obj.names", \
        weights="cfg.usd_dollars_square.tiny/weights/yolov3-tiny_260000.weights",\
        cfg="cfg.usd_dollars_square.tiny/yolov3-tiny.cfg")
    #yolo = opencvYOLO(modeltype="yolov3-tiny", \
    #    objnames="cfg.usd_dollars.tiny/obj.names", \
    #    weights="cfg.usd_dollars.tiny/weights/yolov3-tiny_80000.weights",\
    #    cfg="cfg.usd_dollars.tiny/yolov3-tiny.cfg")

    labels_tw = { "1ca":["1 cent", 0.01], "1cb":["1 cent", 0.01],
                 "5ca":["5 cent", 0.05], "5cb":["5 cent", 0.05],
                 "1a":["1 dollar", 1.00], "1b":["1 dollar", 1.00],
                 "5a":["5 dollars", 5.00], "5b":["5 dollar", 5.00],
                 "10a":["10 dollars", 10.00], "10b":["10 dollar", 10.00],
                 "20a":["20 dollars", 20.00], "20b":["20 dollar", 20.00],
                 "100a":["100 dollars", 100.00], "100b":["100 dollars", 100.00],
                 "25da":["2.5 dollars", 2.50], "25db":["2.5 dollars", 2.50] }

    labels_en = { "1ca":["1 cent", 0.01], "1cb":["1 cent", 0.01],
                 "5ca":["5 cent", 0.05], "5cb":["5 cent", 0.05],
                 "1a":["1 dollar", 1.00], "1b":["1 dollar", 1.00],
                 "5a":["5 dollars", 5.00], "5b":["5 dollar", 5.00],
                 "10a":["10 dollars", 10.00], "10b":["10 dollar", 10.00],
                 "20a":["20 dollars", 20.00], "20b":["20 dollar", 20.00],
                 "100a":["100 dollars", 100.00], "100b":["100 dollars", 100.00],
                 "25da":["2.5 dollars", 2.50], "25db":["2.5 dollars", 2.50] }

else:
    yolo = opencvYOLO(modeltype="yolov3-tiny", \
        objnames="cfg.breads_fake.tiny/obj.names", \
        weights="cfg.breads_fake.tiny/weights/yolov3-tiny_100000.weights",\
        cfg="cfg.breads_fake.tiny/yolov3-tiny.cfg")

    labels_tw = { "b01":["單片土司", 8], "b02":["雙片土司", 16], \
           "b03":["牛角麵包", 30], "b04":["奶油牛奶條", 55], "b05":["紅豆麵包", 35], \
           "b06":["炸甜甜圈", 30], "b07":["牛肉漢堡", 85], "b08":["瑞士捲", 35]}

labels_en = { "b01":["Toast", 0.4], "b02":["Toasts", 0.8], \
           "b03":["Croissant", 2.6], "b04":["Baguette", 1.8], "b05":["Red-bean bun", 0.6], \
           "b06":["Donut", 2.2],"b07":["Hamburger", 5.2],"b08":["Swiss Roll", 1.8] }

pinBTN = 5
#GPIO.setup(pinBTN, GPIO.IN)

cv2.namedWindow("Xuan", cv2.WND_PROP_FULLSCREEN)        # Create a named window
cv2.setWindowProperty("Xuan", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

start_time = time.time()
dt.emptyBG = None
last_movetime = time.time()  #objects > 0
YOLO = False  # YOLO detect in this loop?
txtStatus = ""

if(lang=="EN"):
    labels = labels_en
else:
    labels = labels_tw

def speak(wavfile):
    print("SPEAK:", wavfile)
    os.system('/usr/bin/aplay ' + wavfile)

def dollar_speak(num):
    strNum = str(num)

    if(lang=="TW"):
        if(num<=99):
            speak("wav.tw/number/" + str(num) + ".wav")
        elif(num<=999 and num>99):
            speak("wav.tw/number/" + strNum[-3] + "00.wav")
            speak("wav.tw/number/" + strNum[-2:] + ".wav")
        elif(num<=1999 and num>999):
            speak("wav.tw/number/1000.wav")
            speak("wav.tw/number/" + strNum[-3] + "00.wav")
            speak("wav.tw/number/" + strNum[-2:] + ".wav")

        speak("wav.tw/dollar_long.wav")

    elif(lang=="EN"):
        if('.' in strNum):
            str_num, float_num = strNum.split('.')
        else:
            int_num = num

        int_num = int(str_num)
        if(int_num<=20):
            speak("wav.en/number/" + str(int_num) + ".wav")
        elif(int_num>20 and int_num <100):
            speak("wav.en/number/" + str(int_num)[:1] + "0.wav")
            speak("wav.en/number/" + str(int_num)[1:2] + ".wav")
        elif(int_num>=100 and int_num <1000):
            speak("wav.en/number/" + str(int_num)[:1] + ".wav")
            speak("wav.en/number/hundred.wav")
            speak("wav.en/number/and.wav")
            speak("waven/number/" + str(int_num)[1:2] + "0.wav")
            speak("wav.en/number/" + str(int_num)[2:3] + ".wav")

        if('.' in strNum):
            speak("wav.en/number/point.wav")
            for f_num in float_num:
                speak("wav.en/number/" + f_num + ".wav")

        speak("wav.en/dollar_long.wav")


def speak_shoplist(itemList):
    totalPrice = 0.0
    for id, item in enumerate(itemList):
        itemID = item[0]
        itemName = item[1]
        itemNum = int(item[3])
        itemPrice = float(item[2])
        totalPrice += itemNum*itemPrice
        print("totalPrice:", totalPrice)

        if(lang=="TW"):
            if(itemID == "b01a"):
                if(itemNum==2):
                    unit = "2_slice.wav"
                else:
                    unit = "1_slice.wav"

            elif(itemID == "b01c"):
                unit = "1_pack.wav"

            else:
                if(itemNum==2):
                    unit = "2_item.wav"
                else:
                    unit = "1_item.wav"

            speak("wav.tw/menu/" + itemID + ".wav")
            #speak("wav/number/" + str(itemNum) + ".wav")
            speak("wav.tw/" + unit)
            speak("wav.tw/number/" + str(itemNum*itemPrice) + ".wav")
            speak("wav.tw/dollar.wav")

            speak("wav.tw/totalis.wav")
            dollar_speak(totalPrice)

        elif(lang=="EN"):
            if(itemNum==1):
                unit = "1_item.wav"
            else:
                unit = "2_item.wav"

            speak(unit)
            speak("wav.en/menu/" + itemID + ".wav")

            #speak("wav.en/totalis.wav")
            dollar_speak(itemNum*itemPrice)

    if(lang=="TW"):
        speak("wav.tw/totalis.wav")
    else:
        speak("wav.en/totalis.wav")

        dollar_speak(totalPrice)


def group(items):
    """
    groups a sorted list of integers into sublists based on the integer key
    """
    if len(items) == 0:
        return []

    items.sort()
    grouped_items = []
    prev_item, rest_items = items[0], items[1:]

    subgroup = [prev_item]
    for item in rest_items:
        if item != prev_item:
            grouped_items.append(subgroup)
            subgroup = []
        subgroup.append(item)
        prev_item = item

    grouped_items.append(subgroup)
    return grouped_items

if __name__ == "__main__":

    INPUT = cv2.VideoCapture(0)

    width = int(INPUT.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    height = int(INPUT.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float

    #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #out = cv2.VideoWriter(video_out,fourcc, 30.0, (int(width),int(height)))

    frameID = 0
    while True:
        #if(GPIO.input(pinBTN)==1):
        #if(detection == "USD"):
        #    yn = easygui.ynbox('目前為美金辨識，您要切換到麵包辨識嗎？（需要重開機）', '切換辨識', ('Yes', 'No'))
        #    target = "BREAD"
        #else:
        #    yn = easygui.ynbox('目前為麵包辨識，您要切換到美金辨識嗎？（需要重開機）', '切換辨識', ('Yes', 'No'))
        #    target = "USD"

        #if(yn is True):
        #    f = open("detection_type.txt", "w")
        #    f.write(target)
        #    f.close()
        #    #os.system('reboot')
        #    break

        hasFrame, frame = INPUT.read()
        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            print("--- %s seconds ---" % (time.time() - start_time))
            break


        '''
        yolo.getObject(frame, labelWant="", drawBox=True, bold=1, textsize=0.6, bcolor=(0,0,255), tcolor=(255,255,255))
        #print ("Object counts:", yolo.objCounts)
        #yolo.listLabels()
        #print("classIds:{}, confidences:{}, labelName:{}, bbox:{}".\
        #    format(len(yolo.classIds), len(yolo.scores), len(yolo.labelNames), len(yolo.bbox)) )
        #cv2.imshow("Frame", imutils.resize(frame, width=600))
        '''

        #objects = dt.getContours(frame, 1200)
        #print("Objects:", objects)
        if(flipFrame[0] is True):
            frame = cv2.flip(frame, 1 , dst=None)
        elif(flipFrame[1] is True):
            frame = cv2.flip(frame, 0 , dst=None)

        if(dt.emptyBG is None or time.time()-dt.emptyBG_time>=0.5):
            dt.emptyBG = frame.copy()
            dt.emptyBG_time = time.time()
            #print("Update BG")

        objects = dt.difference(dt.emptyBG, frame, 800)
        if(objects>0):
            last_movetime = time.time()
            timeout_move = str(round(time.time()-last_movetime, 0))
            txtStatus = "Idle:" + timeout_move
        else:
            waiting = time.time() - last_movetime
            timeout_move = str(round(time.time()-last_movetime, 0))
            txtStatus = "Idle:" + timeout_move

            if( (waiting > idle_checkout[0] and waiting<idle_checkout[1]) ):
                txtStatus = "Caculate"
                YOLO = True

        imgDisplay = dt.display(detection, frame.copy(), txtStatus)
        cv2.imshow("Xuan", imgDisplay)
        cv2.waitKey(1)

        if(YOLO is True):
            yoloStart = time.time()
            print("YOLO start...")
            cv2.imwrite("labeling/"+str(time.time())+".jpg", frame)

            if(lang=="TW"):
                speak("wav.tw/start_pos.wav")
            else:
                speak("wav.en/start_pos.wav")

            YOLO = False
            yolo.getObject(frame, labelWant="", drawBox=False, bold=1, textsize=0.6, bcolor=(0,0,255), tcolor=(255,255,255))


            for id, label in enumerate(yolo.labelNames):
                x = yolo.bbox[id][0]
                y = yolo.bbox[id][1]
                w = yolo.bbox[id][2]
                h = yolo.bbox[id][3]
                cx = int(x+w/3)
                cy = int(y+h/3)
                if(lang == "EN"):
                    frame = desktop.printText(desktop, txt=labels[label][0], bg=frame, color=(0,255,0,0), size=0.75, pos=(cx,cy), type="English")
                else:
                    frame = desktop.printText(desktop, txt=labels[label][0], bg=frame, color=(0,255,0,0), size=0.75, pos=(cx,cy), type="Chinese")

            #print("classIds:{}, confidences:{}, labelName:{}, bbox:{}".\
            #    format(len(yolo.classIds), len(yolo.scores), len(yolo.labelNames), len(yolo.bbox)) )
            if(len(yolo.labelNames)>0):
                types = group(yolo.labelNames)
                print("Labels:", types)
                shoplist = []
                for items in types:
                    shoplist.append([items[0], labels[items[0]][0], labels[items[0]][1], len(items)])
                    #desktop.printText(labels[items[0]][0], frame, color=(255,255,0,0), size=0.6, pos=(0,0), type="Chinese")

                txtStatus = "checkout"
                print(shoplist)

                imgDisplay = dt.display(detection, frame, txtStatus, shoplist)
                cv2.imshow("Xuan", imgDisplay)
                cv2.waitKey(1)
                if(len(shoplist)>0):
                    print("YOLO used:" + str(round(time.time()-yoloStart, 3)))
                    print("Shop list:", shoplist)
                    cv2.waitKey(1)
                    speak_shoplist(shoplist)

                    #time.sleep(10)

                #cv2.imshow("SunplusIT", imgDisplay)
                #cv2.waitKey(1)
                #time.sleep(0)

        #dt.emptyBG = frame.copy()
        #dt.emptyBG_time = time.time()
        #if(video_out!=""):
        #out.write(frame)
        
        #k = cv2.waitKey(1)
        #if k == 0xFF & ord("q"):
         #   out.release()
         #   break
	    
        while(1):
            ret, frame = INPUT.read() # get a frame
    	# cv2.imshow("capture", frame) # show a frame 生成攝像頭視窗

            k = cv2.waitKey(1) & 0xFF # 每幀數據延時 1ms，延時不能為 0，否則讀取的結果會是靜態幀
            if k == ord("s"): # 若檢測到按鍵 ‘s’，儲存路徑
                cv2.imwrite("/home/xuan/pos_bread/test.jpg", frame)

            elif k == ord("q"): # 若檢測到按鍵 ‘q’，退出
                break

#cap.release() # 釋放攝像頭
#cv2.destroyAllWindows() # 刪除建立的全部窗口
