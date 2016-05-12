import cv2

def resize(frame, width, height):
    frame = cv2.resize(frame, (width, height))
    return frame

def addText(frame, text, size, x, y):
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, "{0}".format(text), (x, y), font, size, (255, 255, 0), 1)

def cvtBGR2RGB(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def cvtRGB2GRAY(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return frame

def cvtRGB2HSV(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    return frame

def cvtGRAY2RGB(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    return frame

def initBackgrounSubtraction(real_time, start_time, init_time):
    if real_time < start_time + init_time:
        return False
    else:
        return True

def morphOpening(bin_frame, kernel, iteration):
    for iteration in range(0, iteration):
        bin_frame = cv2.erode(bin_frame, kernel)
        bin_frame = cv2.dilate(bin_frame, kernel)
    return bin_frame

def morphClosing(bin_frame, kernel, iteration):
    for iteration in range(1, iteration):
        bin_frame = cv2.dilate(bin_frame, kernel)
        bin_frame = cv2.erode(bin_frame, kernel)
    return bin_frame

def shadowRemoval(RGB_frame, Bin_frame):
    x = 5

def initCounting(registX1, registY1, registX2, registY2, centeroidX, centeroidY, clasification):
    if ((centeroidX >= registX1) & (centeroidX <= registX2)) & ((centeroidY >= registY1) & (centeroidY <= registY2)):
        return clasification

def backgroundSubtractionAverage(frame_ori, avg, alpha):
    accuWeight = cv2.accumulateWeighted(frame_ori, avg, alpha)
    cvtScaleAbs = cv2.convertScaleAbs(accuWeight)
    return cvtScaleAbs

def croppingImage(frame, x1, y1, x2, y2, filename):
    crop = frame[y1:y2, x1:x2]  #y1:y+h, x:x+w
    cv2.imwrite("{0}.jpg".format(filename), crop)

def backgroundSubtractionMoG(frame):
    initMOG2 = cv2.createBackgroundSubtractorMOG2()
    MOG2_frame = initMOG2.apply(frame)
    return MOG2_frame

