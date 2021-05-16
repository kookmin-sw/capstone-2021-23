#gstreamer UDP CLI
gst-launch-1.0 v4l2src device="/dev/video0" ! "video/x-raw, framerate=30/1, height=480, width=640" ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=192.168.0.46 port=9000 sync=false

# videorate 기능 -> 비디오 화질과 관5
# gst-launch-1.0 v4l2src device="/dev/video0" ! video/x-raw, width=640,height=480 ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency byte-stream=true bitrate=500 ! h264parse config-interval=1 ! rtph264pay ! udpsink host=192.168.0.46 port=9000



# gst-launch-1.0 v4l2src device="/dev/video0" ! "video/x-raw, framerate=30/1, height=480, width=640" ! videoconvert ! x264enc tune=zerolatency byte-stream=true bitrate=500 threads=2 ! rtph264pay config-interval=1 ! udpsink host=192.168.0.46 port=9000 sync=false


# 원래 버전
# gst-launch-1.0 v4l2src device="/dev/video0" ! "video/x-raw, framerate=20/1, height=480, width=640" ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=192.168.0.46 port=9000 sync=false
