import cv2
import numpy as np

file_mask = "samples/background2.jpg"
file_foreground = "samples/frameori2.jpg"
file_mog = "samples/test_mog.jpg"

img_back = cv2.imread(file_mask)
img_fore = cv2.imread(file_foreground)
img_mog = cv2.imread(file_mog)
img_back = cv2.resize(img_back, (960,540))
img_fore = cv2.resize(img_fore, (960,540))

kernel = np.ones((5,5),np.float32)/25
hsv_background = cv2.cvtColor(img_back, cv2.COLOR_RGB2HSV)
hsv_foreground = cv2.cvtColor(img_fore, cv2.COLOR_RGB2HSV)
gray_background = cv2.cvtColor(img_back, cv2.COLOR_RGB2GRAY)
gray_foreground = cv2.cvtColor(img_fore, cv2.COLOR_RGB2GRAY)


hue, saturation, value = cv2.split(hsv_foreground)
hueBack, satBack, valBack = cv2.split(hsv_background)
#cv2.imwrite("samples/grayforeground.jpg", gray_foreground)

#gray_foreground = cv2.blur(gray_foreground, (5,5))
#gray_background = cv2.blur(gray_background,(5,5))
# Background subtraction
abssub = (gray_background*2)-(gray_foreground*2)
subtracRGB = cv2.absdiff(gray_foreground,gray_background)
subtraction = cv2.absdiff(value,valBack)

# Threshold
_,threshold = cv2.threshold(subtracRGB, 100,255,cv2.THRESH_OTSU)

im_floodfill = threshold.copy()
h, w = subtraction.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Shadow Removal


# Filing hole
# Inverse Binary
cv2.floodFill(threshold,mask, (0,0),255)
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
temp_floodfill = im_floodfill
# Build RoI
img_zero = np.zeros((540, 960), np.uint8)
pts = np.array([[385,220],[50,465],[1040,465],[705,220]])

#cv2.polylines(temp_floodfill,[pts],True,(255,255,0),thickness=1)
cv2.fillPoly(img_zero,[pts],(255,255,0))
# Morphology
kernel = np.ones((3,3),np.uint8)
kernel1 = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]], dtype=np.uint8)
kernel2 = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]], dtype=np.uint8)

morp_erosi1 = cv2.erode(im_floodfill,kernel1,iterations=1)
morp_erosi1 = cv2.erode(morp_erosi1,kernel2,iterations=1)
morp_dilasi1 = cv2.dilate(morp_erosi1, kernel, iterations=1)
morp_erosi2 = cv2.erode(morp_dilasi1,kernel,iterations=1)
morp_dilasi2 = cv2.dilate(morp_erosi2, kernel, iterations=1)
morp_dilasi3 = cv2.dilate(morp_dilasi2, kernel, iterations=1)
morp_dilasi4 = cv2.dilate(morp_dilasi3, kernel, iterations=1)

combine = cv2.bitwise_and(img_zero,im_floodfill)
bit_and = cv2.bitwise_not(combine,gray_foreground)


com_edge_bin = cv2.bitwise_and(bit_and,subtraction)
chanel3bin = cv2.cvtColor(im_floodfill,cv2.COLOR_GRAY2RGB)
mask = cv2.bitwise_and(img_fore,chanel3bin)
edge_canny = cv2.Canny(mask, 240,255)

im2, contours, hierarchy = cv2.findContours(morp_dilasi4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#draw = cv2.drawContours(img_fore, contours, -1, (0,255,0), 3)

cnt = contours[0]
M = cv2.moments(cnt)

print M
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

print cx
print cy

#areas = [cv2.contourArea(c) for c in contours]
#max_index = np.argmax(areas)
#cnt=contours[max_index]

x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img_fore,(x,y),(x+w,y+h),(255,255,0),2)
print x
print y
print x+w
print y+h
#crop = img_fore[y:y+h, x:x+w]


#print M
#x,y,w,h = cv2.boundingRect(contours)
#cv2.rectangle(img_fore,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("edge", subtraction)
cv2.imshow("binary", im_floodfill)
cv2.waitKey(0)
cv2.destroyAllWindows()
