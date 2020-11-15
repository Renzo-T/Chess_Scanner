
import cv2
from ChessLocalization import localization
from ChessLocalization import dice
from GPCam import gpcam
import os

def main():
    # scriptDir = os.path.dirname(__file__)
    # img_path = os.path.join(scriptDir, 'images/frame.png')
    # frame = cv2.imread(img_path)
    
    frame = gpcam()
    # frame_path = os.path.join(scriptDir, 'images/frame.png')
    # cv2.imwrite(frame_path, frame)

    board = localization(frame)
    img = dice(board)

if __name__ == "__main__":
    main()