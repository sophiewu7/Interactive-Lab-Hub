import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
import subprocess
import pygame
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

'''
Reference: https://github.com/ysthehurricane/Virtual-Drawing
'''

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

rotation = 90
width=135
height=240

################################
wCam, hCam = 1920, 1080
wScreen, hScreen = 1600, 1200
################################
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
 
detector = htm.handDetector(detectionCon=int(0.5))

########## Colors ##################
colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255), "Eraser"]
colors_board = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 175, 0), (255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), "Eraser"]
music = ['black.mp3', 'white.mp3', 'blue.mp3', 'green.mp3', 'red.mp3', 'yellow.mp3', 'cyan.mp3', 'pink.mp3', 'eraser.mp3']
color_radius = 40
color_gap = 30
selected_color = (0, 0, 0)
canvas = np.zeros((hCam, wCam, 3), np.uint8)
brushthickness = 15
eraserthickness = 50
eraser_mode = False
####################################

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)


def draw_start():
    image = Image.new("RGB", (height, width), (0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((60, 50), "Virtual Painter", font=font, fill="#FFFFFF")
    disp.image(image, rotation)
    
    
def fill_screen_with_color(color):
    image = Image.new("RGB", (height, width), color)
    disp.image(image, rotation)

def draw_color_palette(img):
    y_start = 120

    for i, item in enumerate(colors):
        center = (color_radius + 40, y_start + i * (color_radius * 2 + color_gap))
        if item != "Eraser":
            cv2.circle(img, center, color_radius, item, cv2.FILLED)
        else:
            cv2.putText(img, "Eraser", (center[0] - 30, center[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


def calculate_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def fingersUp(lmList):
    if len(lmList) > 20:
        thumb_up = lmList[4][2] < lmList[3][2]
        index_up = lmList[8][2] < lmList[7][2]
        middle_up = lmList[12][2] < lmList[11][2]
        ring_up = lmList[16][2] < lmList[15][2]
        pinky_up = lmList[20][2] < lmList[19][2]
        return [thumb_up, index_up, middle_up, ring_up, pinky_up]
    else:
        return [False, False, False, False, False]
    
    
def isFist(lmList):
    return all(lmList[i][2] > lmList[i - 2][2] for i in range(8, 21, 4))


def find_selected_color(img, indexX, indexY):
    global selected_color, eraser_mode
    y_start = 120
    for i, item in enumerate(colors):
        center = (color_radius + 40, y_start + i * (color_radius * 2 + color_gap))
        distance_to_circle = math.hypot(indexX - center[0], indexY - center[1])
        threshold = 10
        if distance_to_circle - threshold < color_radius:
            if item == "Eraser":
                eraser_mode = True
            else:
                selected_color = item
                eraser_mode = False
                fill_screen_with_color(colors_board[i])
            cv2.circle(img, center, color_radius + 10, (255, 255, 255), 5)
            play_music(music[i])
            
def play_music(mp3_file):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()


draw_start()

xp, yp = 0, 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    draw_color_palette(img)
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2] 
        x2, y2 = lmList[12][1], lmList[12][2]
        
        if isFist(lmList):
            eraser_mode = True
        else:
            fingers = fingersUp(lmList)
            index_finger_up = fingers[1]
            middle_finger_up = fingers[2]
            
            if calculate_distance(x1, y1, x2, y2) < 100:
                fingers_together = True
            else:
                fingers_together = False

            if fingers_together:
                find_selected_color(img, x1, y1)
                xp, yp = 0, 0 

            elif index_finger_up and not middle_finger_up:
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if eraser_mode:
                    cv2.line(canvas, (xp, yp), (x1, y1), (0, 0, 0), eraserthickness)
                else:
                    cv2.line(canvas, (xp, yp), (x1, y1), selected_color, brushthickness)
                xp, yp = x1, y1
            else:
                xp, yp = 0, 0
        
    # Overlay the canvas on the image
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)
    
    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display the image window
    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
