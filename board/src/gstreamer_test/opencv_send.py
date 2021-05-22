import cv2

# 카메라 열기 -그냥 보내는 거
cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, framerate=30/1, width=640, height=480 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

# videoconvert 로 포맷 변경해서 보내는거.
# cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1, width=640, height=480 ! videoconvert ! video/x-raw, format=BGR ! appsink drop=1', cv2.CAP_GSTREAMER)

# 비디오 객체 생성
# gst_out = "appsrc ! video/x-raw ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=127.0.0.1 port=10000"

# 비
gst_out2 = "appsrc ! video/x-raw ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=192.168.0.46 port=9000"


# 흑백은 마지막에 False로 컬러는 True
# writer1 = cv2.VideoWriter(gst_out,cv2.CAP_GSTREAMER,0,float(20),(640,480),True)
writer2 = cv2.VideoWriter(gst_out2,cv2.CAP_GSTREAMER,0,float(20),(640,480),True)


while True:

    _, frame = cap.read()

    cv2.imshow('receive', frame)

    # canny 적용.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny= cv2.Canny(gray,100,255)

    # writer1.write(frame)

    # 그냥 프레임
    writer2.write(frame)

    if cv2.waitKey(1)&0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
