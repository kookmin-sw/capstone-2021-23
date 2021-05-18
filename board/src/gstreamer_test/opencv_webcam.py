import cv2

# 카메라 열기 -그냥 보
cap = cv2.VideoCapture(0)


while True:

    _, frame = cap.read()

    cv2.imshow('receive', frame)


    if cv2.waitKey(1)&0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
