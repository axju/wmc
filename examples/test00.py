import numpy as np
import cv2

# Create a black image
img = np.zeros((18,70,3), np.uint8)

# Write some Text

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (0,12)
fontScale              = 0.4
fontColor              = (255,255,255)
lineType               = 1

cv2.putText(img,'PASSWORD',
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)

#Display the image
cv2.imshow("img",img)

#Save image
cv2.imwrite("out.png", img)

cv2.waitKey(0)
