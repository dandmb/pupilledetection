import numpy as np
import cv2
import math
import os

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
cwd = os.getcwd()
cap = cv2.VideoCapture('video.mp4')
path = os.path.join(cwd,'myframes')
pathgray = os.path.join(cwd,'grayframes')
paththres = os.path.join(cwd,'thresholded')
pathContours = os.path.join(cwd,'contourFrames')
pathDepart = os.path.join(cwd,'frameDepart')

count=0

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:


        #frame de depart
        cv2.imwrite(os.path.join(pathDepart , "frame%d.jpg" % count), frame)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #conversion black and white
        cv2.imwrite(os.path.join(pathgray , "frame%d.jpg" % count), gray)
       



        retval, thresholded = cv2.threshold(gray, 30, 255, 0)

        #Application du seuil
        cv2.imwrite(os.path.join(paththres , "frame%d.jpg" % count), thresholded)
        #count=count+1

        closed = cv2.erode(cv2.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        


        drawing = np.copy(frame)
        cv2.drawContours(drawing, contours, -1, (255, 0, 0), 2)

        #Recuperation avec contour
        cv2.imwrite(os.path.join(pathContours , "frame%d.jpg" % count), drawing)



        for contour in contours:
        
            contour = cv2.convexHull(contour)
            area = cv2.contourArea(contour)
            #print(area)
            
            circumference = cv2.arcLength(contour,True)
            
            if area!=0:
                circularity = circumference ** 2 / (4*math.pi*area)
                print(circularity)

            bounding_box = cv2.boundingRect(contour)

            if area < 150:
                continue
            if circularity >1.1:
                continue

            extend = area / (bounding_box[2] * bounding_box[3])

                # reject the contours with big extend
            if extend > 0.8:
                continue

                # calculate countour center and draw a dot there
            m = cv2.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv2.circle(drawing, center, 3, (0, 255, 0), -1)

                # fit an ellipse around the contour and draw it into the image
            try:
                ellipse = cv2.fitEllipse(contour)
                cv2.ellipse(drawing, box=ellipse, color=(0, 0, 255),thickness=5)
                cv2.imwrite(os.path.join(path , "frame%d.jpg" % count), drawing)
                count=count+1
            except:
                pass

        
    # Display the resulting frame
            imS = cv2.resize(drawing, (700, 500))
            cv2.imshow("Drawing", imS)

    # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    # Break the loop

    else:
        break
	# When everything done, release the video capture object
cap.release()
	# Closes all the frames
cv2.destroyAllWindows()

