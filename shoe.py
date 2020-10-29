import cv2
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import tkinter.scrolledtext as tkst


#처음에는 파일이 없도록 GUI
#신발마다 색깔 지정(에어 조던: 빨강, 척: 파랑, 독일군:초록)

min_confidence = 0.5
width = 800
image_file = "./test_photos/Air jordan 1 high og dior 166.jpg"
title = "shoes recognition program"

def selectFile():
    file = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    read_image = cv2.imread(file)
    file_path['text'] = file_name
    detectAndDisplay(read_image)

def detectAndDisplay(image):
    net = cv2.dnn.readNet('./my_weight/my_yolo_2000.weights','./custom/my_yolo.cfg')
    classes = []
    output_layers = []
    with open('./custom/my_classes.names', "r") as f:
        for line in f.readlines():
            classes.append(line.strip())
    layer_names = net.getLayerNames()
    for i in net.getUnconnectedOutLayers():
        output_layers.append(layer_names[i[0] - 1])
    h, w = image.shape[:2]
    height = int(h * (width /w))
    img = cv2.resize(image,(width, height))
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB = True, crop = False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    box = []
    names = []
    confidence = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > min_confidence:
                centerX = int(detection[0] * width)
                centerY = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(centerX - w/2)
                y = int(centerY - h/2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                names.append(classes[class_id])

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = '{} {:,.2%}'.format(names[i], confidences[i])
            if names[i] == 'Air jordan 1 high og dior':
                color = (0,0,255)
            elif name[i] == 'Chuck 70 Classic Black 162058C':
                color = (255, 0, 0)
            elif name[i] == 'German Army Trainers':
                color = (0, 255, 0)
            cv2.rectangle(img,(x,y),(x + 2, y + h),color, 2)
            cv2.putText(img, label, (x, y -10), font, 1, color, 2)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=image)
    detection_image.config(image=imgtk)
    detection_image.image = imgtk

main = Tk()
main.title(title)
main.geometry()

read_image = cv2.imread(file_name)
image = cv2.cvtColor(read_image, cv2.COLOR_BGR2RGB)
image = Image.fromarray(image)
imgtk = ImageTk.PhotoImage(image=image)

label=Label(main, text=title)
label.config(font=("Courier", 18))
label.grid(row=0,column=0,columnspan=4)

file_title = Label(main, text='Image')
file_title.grid(row=4,column=0,columnspan=1)
file_path = Label(main, text=file_name)
file_path.grid(row=4,column=1,columnspan=2)
Button(main,text="Select", height=1,command=lambda:selectFile()).grid(row=4, column=3, columnspan=1, sticky=(N, S, W, E))

detection_image=Label(main)
detection_image.grid(row=5,column=0,columnspan=4)

detectAndDisplay(read_image)

main.mainloop()