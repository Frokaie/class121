import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img = np.flip(img, axis=1)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_red=np.array([0,120,50]) #hsv
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red)
    
    lower_red=np.array([170,120,70]) #hsv
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv,lower_red,upper_red)
    
    mask1=mask1+mask2
    #cv2.imshow("mask1",mask1)
    
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))  #removes noise from image
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))  #TO MAKE IT MORE PROMINENT 
    
    mask2=cv2.bitwise_not(mask1)  #select only the part that does not have mask1 and save into mask2
    #cv2.imshow('mask2',mask2)
    
    res_1=cv2.bitwise_and(img,img,mask=mask2)
    #cv2.imshow('segment out',res_1)
    
    res_2=cv2.bitwise_and(bg,bg,mask=mask1)
    #cv2.imshow('segment out',res_2)

    final_output=cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)
    
    
    
    #Generating the final output
    
    
    #Displaying the output to the user
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)


cap.release()
out.release()
cv2.destroyAllWindows()

