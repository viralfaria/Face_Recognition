import cv2
import time
import os
# Directory
name = input("Enter the name: ")
directory = name

# Parent Directory path
parent_dir = "C:/Users/viral/PycharmProjects/Face_Recognition/Images"

# Path
path = os.path.join(parent_dir, directory)

# Create the directory
try:
    os.mkdir(path)
except OSError as error:
    print(error)

start_time = time.time()
cam = cv2.VideoCapture(0)

cv2.namedWindow("Capture Image")
img_counter = 1
while True:

    ret, frame = cam.read()
    # cv2.imshow("Capture Image",frame)
    if not ret:
        break
    # k=cv2.waitKey(1)
    # if k%256 ==27:
    #     print ("Escape pressed ..")
    #     break

    curr_time = int(time.time())
    time_elapsed = curr_time-int(start_time)
    if time_elapsed == 20:
        break

    img_name = "{}_{}.jpeg".format(name,img_counter)
    cv2.imwrite(os.path.join(path, img_name), frame)
    print("{} written!".format(img_name))
    img_counter += 1
    time.sleep(0.005)
cam.release()

cv2.destroyAllWindows()