import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle

def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList


def mark_attendance(name):
    now = datetime.now()
    date_ = now.strftime('%d-%B-%Y')
    try:
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = {}
            for line in myDataList:
                entry = line.split(',')
                entry[2] = entry[2].replace("\n", "")
                entry[2] = entry[2].replace(" ", "")
                nameList[entry[0]] = entry[2]

            if (name, date_) not in nameList.items() and name != "Unknown_Face":
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                f.writelines(f'{name}, {time}, {date}\n')
    except:
        with open('Attendance.csv', 'w+') as f:
            myDataList = f.readlines()
            nameList = {}
            for line in myDataList:
                entry = line.split(',')
                entry[2] = entry[2].replace("\n", "")
                entry[2] = entry[2].replace(" ", "")
                nameList[entry[0]] = entry[2]

            if (name, date_) not in nameList.items() and name != "Unknown_Face":
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                f.writelines(f'{name}, {time}, {date}\n')


path = "Images"
images = []
classNames = []
my_list = os.listdir(path)
for cl in my_list:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


encoded_face_train = find_encodings(images)

# take pictures from webcam
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            mark_attendance(name)

        else:
            name = "Unknown_Face"
        y1, x2, y2, x1 = faceloc
        # since we scaled down by 4 times
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

