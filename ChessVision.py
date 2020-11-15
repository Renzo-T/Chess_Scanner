
import cv2
from ChessLocalization import localization
from ChessLocalization import dice
from GPCam import gpcam
import os

def main():
    scriptDir = os.path.dirname(__file__)

    img_path = os.path.join(scriptDir, 'images/full.png')
    frame = cv2.imread(img_path)

    # frame = gpcam()
    board = localization(frame)
    # frame_path = os.path.join(scriptDir, 'images/full.png')
    # cv2.imwrite(frame_path, frame)
    while(1):
        cv2.imshow('frame',board)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            cv2.destroyAllWindows()
            quit()
        elif k == ord('r'):
            frame = gpcam()
            board = localization(frame)
        elif k == ord('c'):
            break

    img = dice(board)

if __name__ == "__main__":
    main()