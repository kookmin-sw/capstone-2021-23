# Flask 웹서버 스트리밍

송신


'''
gst-launch-1.0 v4l2src device="/dev/video0" ! "video/x-raw, framerate=30/1" ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host={recevier ip 주소} port=10000 sync=false
'''


