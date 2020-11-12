
import cv2
from ChessLocalization import localization

def main():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("view")
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        quit
    cv2.imshow("view", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        exit
    cam.release()
    cv2.destroyAllWindows()

    localization(frame)

if __name__ == "__main__":
    main()