# Press Space to click
# Press Esc to close the window
import cv2
name = input("Enter the name: ")
cam = cv2.VideoCapture(0)

cv2.namedWindow(name)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow(name, frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "{}_{}.png".format(name,img_counter)
        cv2.imwrite("Images/"+img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
